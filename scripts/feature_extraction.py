import cv2
import sys
import os
import pandas as pd
import numpy as np
import subprocess
import shutil
import multiprocessing
import gc
from pathlib import Path
from scipy.signal import find_peaks
from rembg import remove, new_session
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
LABELS_ROOT = DATA_ROOT / "labels"
ASSETS_ROOT = REPO_ROOT / "assets"
FEATURE_OUTPUT_ROOT = REPO_ROOT / "artifacts" / "feature_extraction"

# --- Windows CUDA DLL Fix ---
if os.name == 'nt':
    import site
    try:
        search_paths = set()
        try: search_paths.update(site.getsitepackages())
        except: pass
        search_paths.update(sys.path)
        
        for sp in search_paths:
            if not sp: continue
            nvidia_path = Path(sp) / "nvidia"
            if nvidia_path.exists() and nvidia_path.is_dir():
                for bin_dir in nvidia_path.glob("**/bin"):
                    if bin_dir.is_dir():
                        try:
                            os.add_dll_directory(str(bin_dir))
                            os.environ['PATH'] = str(bin_dir) + os.pathsep + os.environ['PATH']
                        except Exception:
                            pass
    except Exception:
        pass
# ----------------------------

# Legacy solutions API is broken on some Python 3.12 wheels, 
# so we rely entirely on the modern mediapipe.tasks API.


class VideoFeatureExtractor:
    def __init__(self, output_root, extraction_mode, 
                 num_changepoints, frame_skip, fast_rembg, mp_complexity, labels_df):
        """
        Configuration only. We DO NOT load AI models here to ensure 
        multiprocessing works without memory serialization/VRAM allocation errors.
        """
        self.output_root = Path(output_root)
        self.extraction_mode = extraction_mode
        self.num_changepoints = num_changepoints
        
        # Performance configurations
        self.frame_skip = frame_skip
        self.fast_rembg = fast_rembg
        self.mp_complexity = mp_complexity
        
        self.labels_df = labels_df
        self.upper_body_indices =[11, 12, 13, 14, 15, 16, 23, 24]

    def init_models(self):
        # Download MediaPipe PoseLandmarker model
        model_path_pose = str(ASSETS_ROOT / "pose_landmarker.task")
        if not Path(model_path_pose).exists():
            print("Downloading PoseLandmarker model...")
            urllib.request.urlretrieve(
                "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task",
                model_path_pose
            )
        base_options_pose = python.BaseOptions(model_asset_path=model_path_pose)
        options_pose = vision.PoseLandmarkerOptions(
            base_options=base_options_pose,
            output_segmentation_masks=False)
        self.pose_landmarker = vision.PoseLandmarker.create_from_options(options_pose)
        
        self.rembg_session = new_session(
            "u2net_human_seg", 
            providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
        )
        
        # Download MediaPipe FaceLandmarker model if needed
        model_path = str(ASSETS_ROOT / "face_landmarker.task")
        if not Path(model_path).exists():
            print("Downloading FaceLandmarker model...")
            urllib.request.urlretrieve(
                "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
                model_path
            )
            
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1)
        self.face_landmarker = vision.FaceLandmarker.create_from_options(options)

    def apply_rembg(self, frame_bgr):
        """Applies fast GPU background removal."""
        img_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        
        kwargs = {"session": self.rembg_session}
        if not self.fast_rembg:
            kwargs.update({
                "alpha_matting": True,
                "alpha_matting_foreground_threshold": 240,
                "alpha_matting_background_threshold": 10,
                "alpha_matting_erode_size": 10
            })
            
        res_rgba = np.array(remove(img_rgb, **kwargs))
        res_bgr = cv2.cvtColor(res_rgba[:, :, :3], cv2.COLOR_RGB2BGR)
        alpha = (res_rgba[:, :, 3] / 255.0)[:, :, np.newaxis]
        return (res_bgr * alpha).astype(np.uint8)

    def is_frame_valid(self, face_result, pose_result):
        if not face_result.face_landmarks:
            return False
        if not pose_result.pose_landmarks:
            return True 
            
        l_sh = pose_result.pose_landmarks[0][11]
        r_sh = pose_result.pose_landmarks[0][12]
        
        if (l_sh.visibility > 0.5) != (r_sh.visibility > 0.5):
            return False
            
        if l_sh.visibility > 0.5 and r_sh.visibility > 0.5:
            face_x = face_result.face_landmarks[0][5].x
            if not (r_sh.x < face_x < l_sh.x):
                return False
        return True

    def get_landmark_velocity(self, landmark_list):
        data = np.array(landmark_list) 
        if len(data) < 2: return np.zeros(len(data))
        data -= np.mean(data, axis=1, keepdims=True)
        diff = np.diff(data, axis=0)
        velocity = np.sqrt(np.sum(diff**2, axis=(1, 2)))
        velocity = np.convolve(velocity, np.ones(5)/5, mode='same')
        return np.pad(velocity, (0, 1), mode='edge')

    def process_single_video(self, video_path, relative_dir=""):
        # Load AI models if this process hasn't loaded them yet
        if not hasattr(self, 'face_landmarker'):
            self.init_models()

        video_filename = Path(video_path).name
        video_name = Path(video_path).stem
        
        # Mirror the input directory structure to prevent identical filename clashes
        video_output_dir = self.output_root / relative_dir / video_name
        raw_dir = video_output_dir / "raw_frames"
        vis_dir = video_output_dir / "visualized_frames"
        
        if raw_dir.exists(): shutil.rmtree(raw_dir)
        if vis_dir.exists(): shutil.rmtree(vis_dir)
        raw_dir.mkdir(parents=True, exist_ok=True)
        vis_dir.mkdir(parents=True, exist_ok=True)

        # 1. Pass 1: Scan video
        cap = cv2.VideoCapture(video_path)
        valid_indices = []
        valid_landmarks =[]
        mediapipe_features_all = {} 
        
        frame_idx = 0
        while cap.isOpened():
            # Zero-cost frame skipping
            if frame_idx % self.frame_skip != 0:
                has_frame = cap.grab()
                frame = None
            else:
                has_frame, frame = cap.read()
                
            if not has_frame: 
                break
                
            if frame is not None:
                # Downscale for faster MediaPipe processing
                h, w = frame.shape[:2]
                max_dim = 640
                if max(h, w) > max_dim:
                    scale = max_dim / max(h, w)
                    process_frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
                else:
                    process_frame = frame
                    
                image_rgb = cv2.cvtColor(process_frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
                
                pose_result = self.pose_landmarker.detect(mp_image)
                face_result = self.face_landmarker.detect(mp_image)
                
                feat = {'frame': frame_idx + 1}
                # Pose landmarks names map (rough mapping for original features)
                pose_names = {11:'LEFT_SHOULDER', 12:'RIGHT_SHOULDER', 13:'LEFT_ELBOW', 14:'RIGHT_ELBOW', 15:'LEFT_WRIST', 16:'RIGHT_WRIST', 23:'LEFT_HIP', 24:'RIGHT_HIP'}
                
                if pose_result.pose_landmarks:
                    for idx in self.upper_body_indices:
                        lm = pose_result.pose_landmarks[0][idx]
                        name = pose_names.get(idx, str(idx))
                        feat[f"MP_{name}_x"] = lm.x
                        feat[f"MP_{name}_y"] = lm.y
                        feat[f"MP_{name}_z"] = lm.z
                        feat[f"MP_{name}_v"] = lm.visibility
                else:
                    for idx in self.upper_body_indices:
                        name = pose_names.get(idx, str(idx))
                        feat[f"MP_{name}_x"], feat[f"MP_{name}_y"], feat[f"MP_{name}_z"] = np.nan, np.nan, np.nan
                        feat[f"MP_{name}_v"] = 0
                        
                mediapipe_features_all[frame_idx] = feat

                if self.is_frame_valid(face_result, pose_result):
                    valid_indices.append(frame_idx)
                    if face_result.face_landmarks:
                        lms = [[lm.x, lm.y] for lm in face_result.face_landmarks[0]]
                        valid_landmarks.append(lms)
            
            frame_idx += 1
        cap.release()

        # Selection logic
        selected_indices =[]
        if self.extraction_mode == "targeted":
            if valid_indices:
                first = valid_indices[0]
                last = valid_indices[-1]
                mid = valid_indices[len(valid_indices)//2]
                selected_indices = sorted(list(set([first, mid, last])))
        elif self.extraction_mode == "changepoint":
            if len(valid_indices) > self.num_changepoints:
                velocity = self.get_landmark_velocity(valid_landmarks)
                distance = max(1, 15 // self.frame_skip)
                peaks, _ = find_peaks(velocity, distance=distance)
                top_peaks = peaks[np.argsort(velocity[peaks])[-self.num_changepoints:]]
                selected_indices = sorted([valid_indices[p] for p in top_peaks])
            else:
                selected_indices = valid_indices

        if not selected_indices:
            # Clean up empty directories if skipped
            shutil.rmtree(raw_dir, ignore_errors=True)
            shutil.rmtree(vis_dir, ignore_errors=True)
            return None 

        # 2. Pass 2: Extract selected frames in O(1) time
        cap = cv2.VideoCapture(video_path)
        for idx in selected_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            success, frame = cap.read()
            if success:
                cv2.imwrite(str(raw_dir / f"frame_{idx:06d}.jpg"), frame)
        cap.release()

        # 3. Final Visualizations & Data Extraction
        final_features = []
        for i, idx in enumerate(selected_indices):
            frame_num = idx
            fname_stem = f"frame_{frame_num:06d}"
            
            clean_path = raw_dir / f"{fname_stem}.jpg"
            if not clean_path.exists(): continue
            
            clean_frame = cv2.imread(str(clean_path))
            if clean_frame is None: continue
            
            vis_frame = self.apply_rembg(clean_frame)
            image_rgb = cv2.cvtColor(vis_frame, cv2.COLOR_BGR2RGB)
            
            # Run MediaPipe PoseLandmarker (for body drawing)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            pose_result = self.pose_landmarker.detect(mp_image)
            
            # Run MediaPipe FaceLandmarker (for AUs, dense mesh, gaze)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            face_result = self.face_landmarker.detect(mp_image)
            
            combined_row = {'frame_id': frame_num}
            if self.labels_df is not None:
                video_labels = self.labels_df[self.labels_df['chunk'] == video_filename]
                if not video_labels.empty:
                    combined_row['label'] = video_labels.iloc[0]['label']
                else:
                    combined_row['label'] = np.nan

            if frame_num in mediapipe_features_all:
                combined_row.update(mediapipe_features_all[frame_num])

            blendshape_scores = {}
            if face_result.face_blendshapes:
                blendshapes = face_result.face_blendshapes[0]
                for category in blendshapes:
                    combined_row[f"AU_{category.category_name}"] = category.score
                    blendshape_scores[category.category_name] = category.score
                    
            if face_result.face_landmarks:
                landmarks = face_result.face_landmarks[0]
                for j, lm in enumerate(landmarks):
                    combined_row[f"FLM_x_{j}"] = lm.x
                    combined_row[f"FLM_y_{j}"] = lm.y
                    combined_row[f"FLM_z_{j}"] = lm.z

            final_features.append(combined_row)

            # Draw PoseLandmarker mesh
            if pose_result.pose_landmarks:
                h, w, _ = vis_frame.shape
                for lm in pose_result.pose_landmarks[0]:
                    cv2.circle(vis_frame, (int(lm.x * w), int(lm.y * h)), 2, (255, 0, 0), -1)

            # Draw FaceLandmarker dense mesh
            if face_result.face_landmarks:
                h, w, _ = vis_frame.shape
                for lm in face_result.face_landmarks[0]:
                    cv2.circle(vis_frame, (int(lm.x * w), int(lm.y * h)), 1, (0, 255, 0), -1)
                    
                # Highlight pupils (approx indices 468, 473 in dense mesh)
                for p_idx in [468, 473]:
                    if p_idx < len(face_result.face_landmarks[0]):
                        lm = face_result.face_landmarks[0][p_idx]
                        cv2.circle(vis_frame, (int(lm.x * w), int(lm.y * h)), 3, (0, 0, 255), -1)

            # Draw top blendshapes
            y_offset = 30
            cv2.putText(vis_frame, "MediaPipe Blendshapes (AUs)", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            curr_y = y_offset + 25
            if blendshape_scores:
                # Sort by highest score, skip 'neutral' and head rotations if present
                sorted_bs = sorted([(k, v) for k, v in blendshape_scores.items() if v > 0.05 and k != '_neutral'], key=lambda x: x[1], reverse=True)[:15]
                col1_x, col2_x = 15, 180
                for idx, (name, val) in enumerate(sorted_bs):
                    x_pos = col1_x if idx < 8 else col2_x
                    y_pos = curr_y if idx < 8 else y_offset + 25 + (idx - 8)*18
                    cv2.putText(vis_frame, f"{name}: {val:.2f}", (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                    if idx < 8: curr_y += 18

            cv2.imwrite(str(vis_dir / f"frame_{frame_num:06d}_vis.jpg"), vis_frame)

        if not final_features:
            return None

        df_final = pd.DataFrame(final_features)
        df_final.to_csv(video_output_dir / f"{video_name}_selected_features.csv", index=False)
        return df_final


# --- TOP LEVEL WORKER FUNCTION FOR MULTIPROCESSING ---
def worker_function(video_path, config, input_dir):
    try:
        extractor = VideoFeatureExtractor(
            output_root=config['output_root'],
            extraction_mode=config['extraction_mode'],
            num_changepoints=config['num_changepoints'],
            frame_skip=config['frame_skip'],
            fast_rembg=config['fast_rembg'],
            mp_complexity=config['mp_complexity'],
            labels_df=config['labels_df']
        )
        
        # Determine relative path structure
        rel_path = os.path.relpath(video_path, input_dir)
        relative_dir = Path(rel_path).parent
        
        df = extractor.process_single_video(video_path, relative_dir=relative_dir)
        
        if df is not None and not df.empty:
            # Extract person_id from EngageNet filename: subject_X_...
            vid_stem = Path(video_path).stem
            id_parts = vid_stem.split('_')
            person_id = f"subject_{id_parts[1]}" if len(id_parts) > 1 else vid_stem[:10]
            df.insert(0, 'person_id', person_id)
            df.insert(1, 'source_video_path', rel_path)
            return df
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error processing {Path(video_path).name}: {e}")
    return None

def process_task_wrapper(args):
    """Wrapper to unpack arguments and force memory cleanup."""
    vp, config, in_dir = args
    df = worker_function(vp, config, in_dir)
    
    # Force Python to clear leftover RAM immediately after every single video
    gc.collect()
    
    return vp, df

import pickle
def process_with_timeout_wrapper(args, temp_file):
    try:
        vp, df = process_task_wrapper(args)
        with open(temp_file, 'wb') as f:
            pickle.dump((vp, df), f)
    except Exception as e:
        with open(temp_file, 'wb') as f:
            pickle.dump((args[0], None), f)

if __name__ == "__main__":
    # REQUIRED FOR WINDOWS MULTIPROCESSING
    multiprocessing.freeze_support()
    
    import sys
    # --- CONFIGURATION ---
    SPLIT = sys.argv[1] if len(sys.argv) > 1 else "Validation"  # "Train", "Validation", or "Test"
    INPUT_DIR = str(DATA_ROOT / "raw_videos" / SPLIT)
    legacy_input_dir = str(REPO_ROOT / "dataset" / SPLIT)
    if not Path(INPUT_DIR).exists() and Path(legacy_input_dir).exists():
        INPUT_DIR = legacy_input_dir
    
    # EngageNet label files per split
    LABELS_MAP = {
        "Train": "train_engagement_labels.xlsx",
        "Validation": "validation_engagement_labels.xlsx",
        "Test": "test_engagement_labels.csv",
        "Test_Subset": "validation_engagement_labels.xlsx",
    }
    LABELS_FILE = LABELS_MAP[SPLIT]
    
    EXTRACTION_MODE = sys.argv[2] if len(sys.argv) > 2 else "targeted"  # "targeted" or "changepoint"
    NUM_CHANGEPOINTS = int(sys.argv[3]) if len(sys.argv) > 3 else 3 
    
    # --- PERFORMANCE & PARALLEL CONFIG ---
    FRAME_SKIP = 2         
    FAST_REMBG = True      
    MP_COMPLEXITY = 1      
    MAX_CONCURRENT_VIDEOS = 8  # Increased to 8 to utilize CPU cores
    # ------------------------------------
    
    output_subdir = f"{NUM_CHANGEPOINTS}_Changepoint_Dataset_{SPLIT}" if EXTRACTION_MODE == "changepoint" else f"Targeted_Dataset_{SPLIT}"
    OUTPUT_DIR = str(FEATURE_OUTPUT_ROOT / output_subdir)
    
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR, exist_ok=True)
        print(f"Directory created. Please place videos in: {INPUT_DIR}")
        sys.exit()

    # Pre-load EngageNet labels
    labels_df = None
    labels_path = LABELS_ROOT / LABELS_FILE
    if labels_path.exists():
        print(f"Loading labels from {labels_path}...")
        if LABELS_FILE.endswith('.xlsx'):
            labels_df = pd.read_excel(labels_path)
        else:
            labels_df = pd.read_csv(labels_path)
        if 'chunk' in labels_df.columns:
            labels_df['chunk'] = labels_df['chunk'].astype(str).str.strip()

    # Find videos
    video_paths =[]
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_paths.append(os.path.join(root, file))

    if not video_paths:
        print(f"No videos found in {INPUT_DIR}.")
        sys.exit()

    print(f"Found {len(video_paths)} videos. Starting parallel processing on {MAX_CONCURRENT_VIDEOS} workers...")

    # Pack config for workers
    worker_config = {
        'output_root': OUTPUT_DIR,
        'extraction_mode': EXTRACTION_MODE,
        'num_changepoints': NUM_CHANGEPOINTS,
        'frame_skip': FRAME_SKIP,
        'fast_rembg': FAST_REMBG,
        'mp_complexity': MP_COMPLEXITY,
        'labels_df': labels_df
    }

    # Bundle arguments for the pool map
    tasks =[(vp, worker_config, INPUT_DIR) for vp in video_paths]
    all_results =[]
    
    # START ROBUST PARALLEL PROCESSING (WITH HARD TIMEOUT TO PREVENT DEADLOCKS)
    import tempfile
    import time
    
    active_processes = []
    task_index = 0
    start_times = {}
    
    while task_index < len(tasks) or active_processes:
        # Fill the process queue up to MAX_CONCURRENT_VIDEOS
        while len(active_processes) < MAX_CONCURRENT_VIDEOS and task_index < len(tasks):
            task = tasks[task_index]
            temp_file = os.path.join(tempfile.gettempdir(), f"engagenet_temp_{task_index}.pkl")
            # Ensure clean start
            if os.path.exists(temp_file):
                try: os.remove(temp_file)
                except: pass
                
            p = multiprocessing.Process(target=process_with_timeout_wrapper, args=(task, temp_file))
            p.start()
            
            active_processes.append((p, temp_file, task, task_index))
            start_times[task_index] = time.time()
            task_index += 1
            
        # Check active processes
        still_active = []
        for p, temp_file, task, idx in active_processes:
            p.join(timeout=0.1)
            
            if p.is_alive():
                # Check for timeout (300 seconds)
                elapsed = time.time() - start_times[idx]
                if elapsed > 300:
                    print(f"[{idx+1}/{len(video_paths)}] TIMEOUT/FROZEN: {Path(task[0]).name}. Terminating...")
                    p.terminate()
                    p.join()
                    print(f"[{idx+1}/{len(video_paths)}] Skipped (Timeout): {Path(task[0]).name}")
                    if os.path.exists(temp_file):
                        try: os.remove(temp_file)
                        except: pass
                else:
                    still_active.append((p, temp_file, task, idx))
            else:
                # Process finished successfully or crashed
                if os.path.exists(temp_file):
                    try:
                        with open(temp_file, 'rb') as f:
                            video_path, df = pickle.load(f)
                        if df is not None:
                            all_results.append(df)
                            print(f"[{idx+1}/{len(video_paths)}] Successfully finished: {Path(video_path).name}")
                        else:
                            print(f"[{idx+1}/{len(video_paths)}] Skipped (No valid frames/error): {Path(task[0]).name}")
                    except Exception as e:
                        print(f"[{idx+1}/{len(video_paths)}] FAILED completely: {Path(task[0]).name} - {e}")
                    finally:
                        try: os.remove(temp_file)
                        except: pass
                else:
                    print(f"[{idx+1}/{len(video_paths)}] FAILED (Process crashed without temp file): {Path(task[0]).name}")
                    
        active_processes = still_active
        time.sleep(0.5)

    # Combine all DataFrames
    if all_results:
        print("\n--- Merging features into collective CSV ---")
        master_df = pd.concat(all_results, ignore_index=True)
        master_path = Path(OUTPUT_DIR) / "collective_features.csv"
        master_df.to_csv(master_path, index=False)
        print(f"Success! Master CSV saved to: {master_path}")
        print(f"Total extracted rows: {len(master_df)}")
    else:
        print("\nNo features were extracted from any videos.")