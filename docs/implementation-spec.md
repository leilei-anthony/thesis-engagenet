# Implementation spec: main study

This is the spec for the code that runs the proposed study (manuscript Chapters 4 and 5). You write the code from it, module by module, in the order of Section 4. After each module, I review it against this spec and the manuscript. You commit.

Each module lists:
- the manuscript section it implements;
- what to reuse from the current code (now tagged `prelim-icce2026`);
- its interface and exact behavior;
- the test cases to turn into pytest.

When this spec and the manuscript disagree, the manuscript wins. Tell me, and I fix the spec.

---

## 1. The design in one table

| | |
|---|---|
| Selection conditions (10) | `sme3`; `pos3`, `pos5`, `pos7`; `rand3`, `rand5`, `rand7`; `cp3`, `cp5`, `cp7` |
| Feature sets (22) | One per condition. Random has one per draw: `rand5_d42` … `rand5_d46` |
| Configurations (140) | Per condition: LSTM × {mean, attention} + {MLP, SVM, RF} × {mean, concat, mean_change, mean_selfsim} = 14 |
| Versions | Version *i* (1–5) uses seed 41 + *i* and draw 41 + *i*. Neural networks: 5 versions. SVM/RF: 5 on random conditions, otherwise 1 |
| Training runs (476) | Neural: 6 × 10 × 5 = 300. SVM/RF: 8 × (7 + 3 × 5) = 176 |
| Comparisons (176) | Families 1–6: 12 + 12 + 12 + 36 + 4 + 100 (§4.6.2) |
| Task | Highly-Engaged (level 3) vs. levels 0–2; SNP clips removed |

Decisions this spec builds in (study guide §0, D34–D37):
- **Item 12:** velocity smoothing stays as in the preliminary study (zero-padded edges).
- **Item 13:** random draws are **nested**. Each draw seed gives one random ordering of the valid frames, and k = 3, 5, 7 take its first k frames.

---

## 2. Review findings: what changes from the preliminary code, and why

| # | Current code | Problem | New behavior |
|---|---|---|---|
| C1 | `feature_extraction.py:270` seeks with `CAP_PROP_POS_FRAMES` | Seeking in H.264 can land on a different frame than pass 1 validated | Pass 2 decodes sequentially, and checks each frame against a hash from pass 1 |
| C2 | `:273, 287, 361` write JPEGs and re-read them | Features come from a lossy copy. Face images are stored for every clip (§4.7) | Frames stay in memory. No images are written |
| C3 | `:295` runs the Pose Landmarker in pass 2 | Used only to draw overlays | Removed. §4.3: only the Face Landmarker reruns |
| C4 | Selection is inside extraction | Pass 1 is repeated for every condition. No outcome log (§4.2.3) | Pass 1 runs once per clip and is stored. All rules select from it, and every clip's outcome is logged |
| C5 | `:535` starts one process per clip | All models reload for every clip | Persistent workers with a per-clip timeout |
| C6 | `dataset.py:173` takes `df.columns[5:-1]` | Column positions depend on the first CSV row | Explicit `FEATURE_NAMES` |
| C7 | `dataset.py:53` caches the common set in JSON | The cache never invalidates | The common set is computed at assembly and written out |
| C8 | `train.py` defaults to class weights (class 0 × 2) and 50 epochs; SVM/RF use `class_weight='balanced'` | §4.5 says unweighted, ≤ 20 epochs | No weighting code at all |
| C9 | Only test predictions are saved, without the 4-level label | Best configuration (§4.6.6) and per-level errors (§4.6.1) can't be computed. No MCC | Validation and test predictions, with `level`. MCC |
| C10 | `model.py:131` averages inside the MLP | Only the mean combination is possible | The MLP takes a precomputed vector |
| C11 | `significance_tests.py` | Different families, single seed, no equivalence test | New analysis that follows §4.6 |
| C12 | One `conda run` subprocess per run, re-reading the CSVs | Far too slow for 476 runs | One process; each feature set is loaded once |
| C13 | `environment.yml` | Lists Python 3.10 (the env is 3.11), and lacks mediapipe, rembg, onnxruntime, opencv, openpyxl | Pin what is installed (Section 4.10) |
| C14 | `np.convolve(..., mode='same')` in `get_landmark_velocity` | With fewer than 6 valid frames, the result has length 6 instead of n. Peak positions shift or fall outside the clip, which affects only `cp3` when n is 4 or 5 | Formula that is identical for n ≥ 6 and correct below (Module 1) |

Kept as they are:
- the validity check (`is_frame_valid`);
- per-frame centering of landmarks;
- the peak distance of 7 scanned frames;
- the n ≤ k rule;
- SME positions;
- LSTM masking and attention;
- SMOTE on flattened sequences plus length;
- `set_seed`.

---

## 3. Conventions

- **Clip ID** is the `chunk` value from the label files, such as `subject_105_jwdq6sdejx_vid_0_0.mp4`. **Person ID** is the first two `_`-separated parts (`subject_105`).
- **Splits** are named `train`, `validation`, `test`. Videos are in `data/raw_videos/{Train,Validation,Test}/`.
- **Labels** come from `data/labels/train_engagement_labels.xlsx`, `validation_engagement_labels.xlsx`, and `test_engagement_labels.csv`, with columns `chunk` and `label` (the xlsx files also have `Unnamed: 0`). Use `LABEL_MAP`, and drop `SNP(Subject Not Present)`.
- **Frame index** is the 0-based frame number in the video, as in `frame_id` in the old CSVs. Clips are 30 fps and 300 frames at 1280×720. Pass 1 scans frames 0, 2, …, 298.
- **Positions:** the valid frames V = (f₁ … fₙ) are stored as `valid_idx`, an array of frame indices. Selection functions return **0-based positions into V**. Convert them with `valid_idx[positions]`.
- **Feature vector per frame**, 1,518 values, in the order of the old CSVs:
  1. 32 pose values: `MP_<NAME>_{x,y,z,v}` for LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, LEFT_HIP, RIGHT_HIP (MediaPipe indices 11, 12, 13, 14, 15, 16, 23, 24);
  2. 52 blendshapes: `AU_<name>`, in the model's order (listed below);
  3. 1,434 landmark values: `FLM_x_j, FLM_y_j, FLM_z_j` for j = 0 … 477.

  The blendshape order, taken from the old CSV header: `_neutral browDownLeft browDownRight browInnerUp browOuterUpLeft browOuterUpRight cheekPuff cheekSquintLeft cheekSquintRight eyeBlinkLeft eyeBlinkRight eyeLookDownLeft eyeLookDownRight eyeLookInLeft eyeLookInRight eyeLookOutLeft eyeLookOutRight eyeLookUpLeft eyeLookUpRight eyeSquintLeft eyeSquintRight eyeWideLeft eyeWideRight jawForward jawLeft jawOpen jawRight mouthClose mouthDimpleLeft mouthDimpleRight mouthFrownLeft mouthFrownRight mouthFunnel mouthLeft mouthLowerDownLeft mouthLowerDownRight mouthPressLeft mouthPressRight mouthPucker mouthRight mouthRollLower mouthRollUpper mouthShrugLower mouthShrugUpper mouthSmileLeft mouthSmileRight mouthStretchLeft mouthStretchRight mouthUpperUpLeft mouthUpperUpRight noseSneerLeft noseSneerRight`.

  Define `FEATURE_NAMES` (length 1,518) once, in `src/features.py` or at the top of `feature_extraction.py`. At runtime, assert that the model's blendshape names match this list.
- **Missing values** (no pose in pass 1, no face after background removal) are 0 in the assembled data (§4.3).
- **Storage** (none of it is tracked by git):
  ```
  artifacts/extraction/
    pass1/<split>/<clip_stem>.npz      first-pass store, one per clip
    pass2/<split>/<clip_stem>.npz      per-frame cache + this clip's selections, grows incrementally
    outcomes_<split>.csv               one row per clip per stage attempt
  data/processed/v2/<split>/
    frames.npy                         float32 [F, 1518], every frame used by any feature set
    frame_index.csv                    clip_id, frame_idx, row, face_found, pass2_seconds
    selections.json                    {feature_set_id: {clip_id: [frame_idx, ...]}}
    labels.csv                         clip_id, person_id, level (0-3), SNP removed
    common_clips.txt                   one clip_id per line, sorted
    exclusions.csv                     clip_id, reason
  artifacts/study/
    predictions/<config_id>/v<i>.csv   clip_id, split, level, y_true, y_pred, score
    runs.jsonl                         one line per training run
    analysis/                          outputs of analyze_study.py
  ```

---

## 4. Modules, in build order

### Module 1: `src/selection.py`

**Implements:** §4.4 and Algorithm 5.1.

**Imports:** numpy and scipy only, so it can be tested without MediaPipe.

```python
SCAN_STEP = 2                 # pass 1 reads every second frame
PEAK_DISTANCE = 7             # = max(1, 15 // SCAN_STEP), in scanned frames
DRAW_SEEDS = (42, 43, 44, 45, 46)

def landmark_velocity(landmarks: np.ndarray) -> np.ndarray
def smooth_velocity(v: np.ndarray) -> np.ndarray
def select_sme(n: int) -> list[int]
def select_positional(n: int, k: int) -> list[int]
def select_random(n: int, k: int, seed: int, clip_id: str) -> list[int]
def select_changepoint(smoothed: np.ndarray, k: int) -> list[int]

@dataclass(frozen=True)
class Condition:
    id: str        # "sme3", "pos5", "rand7", "cp3", ...
    rule: str      # "sme" | "positional" | "random" | "changepoint"
    k: int

CONDITIONS: tuple[Condition, ...]          # the 10 conditions, in the order of Table 4.1
def feature_sets() -> list[tuple[str, Condition, int | None]]
    # 22 entries: (feature_set_id, condition, draw_seed or None)
def select_for(fs_id: str, valid_idx: np.ndarray, smoothed: np.ndarray, clip_id: str) -> list[int]
    # returns sorted FRAME INDICES (valid_idx[positions])
```

**Behavior:**
- Every `select_*` returns sorted, distinct positions in `0 … n-1`. With n = 0 it returns `[]`, and with **n ≤ k it returns `list(range(n))`**. The n ≤ k check happens before anything else.
- `landmark_velocity`:
  - input: the 2-D landmarks of the valid frames, shape `[n, 478, 2]`;
  - center each frame, then compute Eq. 4.1;
  - returns `n − 1` values, **unsmoothed**;
  - port lines 146–150 of the old `get_landmark_velocity` (`feature_extraction.py:145–152`).
- `smooth_velocity(v)`:
  ```python
  s = np.convolve(v, np.ones(5) / 5, mode="full")[2 : 2 + len(v)]   # = mode="same" when len(v) >= 5 (C14)
  return np.pad(s, (0, 1), mode="edge")                              # length n; s[t] belongs to frame t
  ```
  When `len(v) == 0`, return `np.zeros(1)`. This keeps the preliminary study's behavior (item 12): the edges are zero-padded, and the velocity between f_t and f_{t+1} belongs to f_t.
- `select_sme(n)`: `[0, n // 2, n - 1]`; with n ≤ 3, all frames.
- `select_positional(n, k)`: `[((2*j - 1) * n) // (2 * k) for j in 1..k]`. Use integers only, never floats.
- `select_random(n, k, seed, clip_id)` (**nested**):
  ```python
  rng = np.random.default_rng([seed, zlib.crc32(clip_id.encode("utf-8"))])
  order = rng.permutation(n)
  return sorted(order[:k].tolist())
  ```
  The ordering depends only on (seed, clip, n), never on k, so the k = 3 frames are among the k = 5 frames, which are among the k = 7 frames. Never use Python's `hash()`, which changes between processes.
- `select_changepoint(smoothed, k)`, ported from `feature_extraction.py:247–251`:
  ```python
  peaks, _ = find_peaks(smoothed, distance=PEAK_DISTANCE)
  top = peaks[np.argsort(smoothed[peaks])[-k:]]   # default argsort kind, to reproduce the old choices
  return sorted(top.tolist())
  ```
  It can return fewer than k frames, or none. An empty result for n > k means the clip has no peak, and it leaves the common set.

**Test cases** (`tests/test_selection.py`):

| Input | Expected |
|---|---|
| `select_sme(20)` | `[0, 10, 19]` |
| `select_positional(20, 3)` | `[3, 10, 16]` (study guide §9.3, 0-based) |
| `select_positional(20, 5)` | `[2, 6, 10, 14, 18]` |
| `select_positional(20, 7)` | `[1, 4, 7, 10, 12, 15, 18]` |
| `select_positional(150, 3/5/7)` | `[25, 75, 125]`, `[15, 45, 75, 105, 135]`, `[10, 32, 53, 75, 96, 117, 139]` |
| any rule, n = 2, k = 3 | `[0, 1]` |
| any rule, n = 0 | `[]` |
| `select_random(150, k, 42, "a.mp4")` twice | identical |
| random, same seed and clip | k=3 result ⊂ k=5 ⊂ k=7 |
| random, seeds 42 vs 43 | different (for n = 150) |
| random | sorted, distinct, within range |
| changepoint, `s` of zeros with spikes s[5]=1, s[8]=3, s[20]=2, s[30]=0.5 (n = 40), k = 2 | `[8, 20]` (5 is within 7 of the higher 8) |
| same signal, k = 5 | `[8, 20, 30]` (fewer peaks than k) |
| flat signal, n = 40, k = 3 | `[]` |
| `smooth_velocity` vs the old function, random landmarks, n = 6, 8, 150 | identical |
| `smooth_velocity`, n = 4 and 5 | length n (the old function gives 6) |
| `len(CONDITIONS)`, `len(feature_sets())` | 10, 22 |

For the parity test, copy the old `get_landmark_velocity` into the test file as a reference.

### Module 2: `src/feature_extraction.py` (rewrite)

**Implements:** §4.3.

```python
class Models:
    """Loads MediaPipe and rembg once per worker process."""
    def __init__(self, stage: str)        # "pass1": pose + face; "pass2": rembg + face

def first_pass(video_path: str, models: Models, keep_landmarks: bool = False) -> dict
def second_pass(video_path: str, frame_indices: list[int], expected_hash: dict[int, int],
                models: Models) -> dict
```

**`first_pass`.** Port the loop at `feature_extraction.py:179–234` unchanged:
- `read()` on even frames and `grab()` on odd ones;
- resize so that the longer side is ≤ 640;
- pose, then face, on the same `mp.Image`;
- `is_frame_valid` (`:127–143`) as is.

Model options stay as in `init_models` (`:72–107`).

It returns (and the runner saves as `.npz`):

| Key | Type | Content |
|---|---|---|
| `n_frames` | int | frames read |
| `scanned_idx` | int16 [S] | 0, 2, … |
| `valid` | bool [S] | validity of each scanned frame |
| `pose` | float32 [S, 32] | x, y, z, v per keypoint. No pose gives NaN for x, y, z and 0 for v, as now |
| `velocity` | float64 [n_valid − 1] | `landmark_velocity` of the valid frames' 2-D landmarks (unsmoothed) |
| `frame_hash` | uint64 [S] | hash of the **full-resolution** BGR frame, computed before resizing: `int.from_bytes(hashlib.blake2b(frame.tobytes(), digest_size=8).digest(), "little")` |
| `seconds` | float | wall time of the pass |
| `landmarks` | float32 [n_valid, 478, 2] | only if `keep_landmarks`. Off by default (~0.6 MB per clip) |

**`second_pass`.**
- Open the video and step through it with `grab()`. At each index in `frame_indices`, `retrieve()` the frame. **Do not seek.**
- If the frame's hash differs from `expected_hash[idx]`, stop and report `hash_mismatch`.
- For each frame:
  1. Start a timer.
  2. Apply `apply_rembg`, ported from `:109–125` without alpha matting. Create the session with `new_session("u2net_human_seg", providers=["CPUExecutionProvider"])`; this ONNX Runtime install has no CUDA.
  3. Run the Face Landmarker on the RGB result.
  4. Collect 52 blendshapes and 478 × (x, y, z), 1,486 values. If no face is found, use zeros and set `face_found = False`.
  5. Stop the timer.
- Returns `frame_idx` int16 [m], `features` float32 [m, 1486], `face_found` bool [m], and `seconds` float64 [m], the per-frame time of rembg plus Face Landmarker only.
- Don't run the Pose Landmarker, and don't draw or write images.

**Tests:**
- An import test, `FEATURE_NAMES` has 1,518 entries and no duplicates, and the blendshape assertion.
- Real-video behavior is checked in the smoke test (Section 5), not in unit tests.

### Module 3: `scripts/extraction/run_extraction.py` (rewrite)

**Implements:** §4.2.3 (outcome log), §4.3 (pass-1 store, timing), Algorithm 5.1.

```
python scripts/extraction/run_extraction.py --stage pass1|pass2|assemble
    --splits Validation Test Train    --workers 8    --threads_per_worker 2
    --timeout 300    --limit N    --clips_file F    --out_root artifacts/extraction
    --data_out data/processed/v2    --keep_landmarks    --max_tasks_per_worker 200
```

**Task list.** Take the clips from the split's label file and skip SNP clips. A clip in the label file without a video is recorded as `missing_video`; this matters while the training download is pending. `--limit` takes the first N clips in sorted order, and `--clips_file` restricts the run to a list. A clip whose output already exists is skipped, so every stage can be resumed.

**Workers (Windows uses spawn).**
- Start `--workers` processes with the `spawn` context. **Each worker has its own `Pipe`.**
- The worker:
  - sets `OMP_NUM_THREADS` to `--threads_per_worker` before importing rembg (rembg reads it);
  - creates `Models(stage)` once;
  - loops: receive a clip, process it, write the `.npz` atomically (save to `*.tmp`, then `os.replace`), and send back a small status dict;
  - exits after `--max_tasks_per_worker` clips.
- The main process:
  - sends one clip at a time to each idle worker;
  - waits with `multiprocessing.connection.wait(conns, timeout=1)`;
  - kills a worker whose clip has run longer than `--timeout` (status `timeout`), and respawns any worker that died or retired.
- Per-worker pipes matter here. Killing a process that is using a shared queue can corrupt it (Python docs, `Process.terminate`); a killed worker's own pipe is simply discarded.
- Heavy imports (mediapipe, rembg) go inside the worker function, not at module level.
- Only the main process writes `outcomes_<split>.csv`, with columns clip_id, stage, status, n_scanned, n_valid, n_new_frames, seconds, message, timestamp. Status is one of `ok`, `no_valid_frame`, `no_peak`, `timeout`, `error`, `hash_mismatch`, `missing_video`.

**`--stage pass2`, per clip:**
1. Load the pass-1 store. If there are no valid frames, the status is `no_valid_frame`.
2. `smoothed = smooth_velocity(velocity)`.
3. For each of the 22 feature sets, compute `select_for(...)`.
4. Take the union of all selected frames, minus the frames already in the clip's pass-2 cache, and run `second_pass` on the missing ones.
5. Write the merged cache together with the selections.
6. If any changepoint set is empty, the status is `no_peak`, but still write the cache.
7. If anything fails mid-clip, write nothing for the clip (status `error`).

**`--stage assemble`, per split:**
- Build each frame's 1,518-vector: pass-1 pose for that frame (NaN → 0), then the pass-2 features. Write `frames.npy`, `frame_index.csv`, `selections.json`, and `labels.csv`.
- **Common set** (§4.2.3): clips that have a label, both stages `ok`, and a non-empty selection in **all 22** feature sets. Write `common_clips.txt`, and write `exclusions.csv` with the first failing reason per clip.
- Print the counts per exclusion reason, plus frames per clip per feature set (min, mean, max, and the number of clips with fewer than k).

**Tests:** run assemble on a fake pass-1/pass-2 tree in `tmp_path`. Check that:
- the common set excludes a `no_peak` clip and a `missing_video` clip;
- `frames.npy` rows match the per-clip caches;
- pose NaN becomes 0.

### Module 4: `src/dataset.py` (rewrite)

**Implements:** §4.2.

```python
LABEL_MAP, SNP_LABEL                     # keep
FEATURE_DIM = 1518

@dataclass
class FeatureSet:
    fs_id: str; split: str; k: int
    sequences: np.ndarray   # float32 [N, k, 1518]; rows past lengths[i] are 0
    lengths: np.ndarray     # int64 [N], 1..k
    level: np.ndarray       # int64 [N], 0..3
    clip_ids: list[str]     # sorted; identical across all 22 feature sets of a split
    person_ids: list[str]
    @property
    def y(self) -> np.ndarray: return (self.level >= 3).astype(np.int64)

def load_feature_set(fs_id: str, split: str, root: Path = DEFAULT_ROOT) -> FeatureSet
```

Open `frames.npy` with `mmap_mode="r"` and gather rows through `frame_index.csv` and `selections.json`. Restrict to `common_clips.txt` and sort by `clip_id`. Frames within a clip stay in temporal order, because selections are stored sorted.

**Tests:**
- On a fake store (fixture in `tests/conftest.py`, also used in Section 5): all 22 feature sets give the same `clip_ids`; `lengths ≤ k`; padding rows are 0; no SNP; `y` matches `level ≥ 3`.
- The same checks run on the real store, skipped when it is absent. They replace the old `test_dataset_integrity.py` data tests.

### Module 5: `src/combine.py`

**Implements:** §4.5, "Combining the selected frames", and §3.6.

```python
class FrameScaler:
    def fit(self, sequences, lengths) -> "FrameScaler"   # per-feature mean/std over REAL frames only; std == 0 -> 1
    def transform(self, sequences, lengths) -> np.ndarray  # standardized; positions >= length set to 0
    @classmethod
    def identity(cls, dim) -> "FrameScaler"               # mean 0, std 1, for tests

COMBINATIONS = ("mean", "concat", "mean_change", "mean_selfsim")
def combined_dim(method: str, k: int) -> int
def combine(sequences, lengths, method: str, scaler: FrameScaler) -> np.ndarray   # [N, combined_dim]
```

- Fit the scaler on the **real training clips of the same feature set, before SMOTE**. Reuse it for validation, test, and the synthetic sequences.
- **Always mask by `lengths`.** Don't assume positions past the length are 0: after SMOTE, a synthetic sequence can carry non-zero values there (one parent was longer).
- `mean`: the mean of the m raw frames.
- `concat`: the raw frames, with positions ≥ m set to 0, flattened to `1518 * k`.
- `mean_change`: the raw mean, then `(1/(m−1)) Σ |z_{t+1} − z_t|` over standardized frames z. It is 0 when m = 1. Length 3,036.
- `mean_selfsim`: the raw mean, then `cos(z_i, z_j)` for i < j in the order (0,1), (0,2), …, (0,k−1), (1,2), …. A pair involving a position ≥ m gives 0. Use `cos = z_i·z_j / (‖z_i‖‖z_j‖ + 1e-12)`. Length `1518 + k(k−1)/2`.

These definitions follow §4.5 literally: the mean and concatenation use raw features, and only the change and similarities use standardized frames. For the SVM and RF, the whole combined vector is standardized afterwards (Module 7).

**Test cases** (`tests/test_combine.py`, 2 features, `FrameScaler.identity(2)`):

| Frames (k = 3, m = 3) | mean | concat | change | similarities |
|---|---|---|---|---|
| (1,0), (0,1), (1,0) (Ch. 3 example) | (0.667, 0.333) | (1,0,0,1,1,0) | (1, 1) | [0, 1, 0] |
| (1,0), (1,0), (0,1) | (0.667, 0.333) | (1,0,1,0,0,1) | (0.5, 0.5) | [1, 0, 0] |

Further cases:
- k = 5 and m = 2: concat positions 2–4 are 0, and 9 of the 10 similarities are 0 (only pair (0,1) survives).
- m = 1: change = 0.
- Putting 999 past `lengths` changes nothing.
- `combined_dim`: 1518; 1518k; 3036; 1521, 1528, 1539 for k = 3, 5, 7.
- The scaler ignores padding.

### Module 6: `src/model.py`

**Implements:** §4.5 (classifier list).

- `EngagementLSTM`:
  - unchanged except for removing the unused options: `num_classes=2`, readouts `"mean"` and `"attention"` only, no regression mode;
  - input `[N, k, 1518]` raw, plus lengths.
- `EngagementMLP(input_dim)`:
  - `Linear(input_dim, 64) → ReLU → Linear(64, 32) → ReLU → Linear(32, 2)`;
  - input `[N, input_dim]`;
  - no averaging inside.

**Tests:**
- Keep `test_lstm_readouts_run_and_respect_padding` (`tests/test_dataset_integrity.py:174–200`), restricted to the two readouts.
- MLP output shape for `input_dim = 1539`.

### Module 7: `src/training.py`

**Implements:** §4.5 (training, SMOTE, fixed settings).

```python
@dataclass
class RunResult:
    val_pred: np.ndarray; val_score: np.ndarray
    test_pred: np.ndarray; test_score: np.ndarray
    fit_seconds: float; smote_seconds: float
    epochs_run: int | None; best_epoch: int | None; n_train: int

def set_seed(seed) -> torch.Generator      # port train.py:74-94, plus torch.use_deterministic_algorithms(True, warn_only=True)
def smote_sequences(sequences, lengths, y, random_state=42)   # port train.py:37-72; k_neighbors=5
def train_neural(arch, variant, train: FeatureSet, val: FeatureSet, test_sequences, test_lengths,
                 seed, scaler, device, epochs=20, smote_cache=None) -> RunResult
def train_sklearn(kind, combination, train: FeatureSet, val: FeatureSet, test_sequences, test_lengths,
                  scaler, smote_cache=None) -> RunResult
```

**The training functions never receive test labels.** Pass only test sequences and lengths, so that labels can't leak structurally.

**`train_neural`:**
1. `set_seed(seed)`. Set `CUBLAS_WORKSPACE_CONFIG=":4096:8"` before CUDA is first used.
2. SMOTE on the raw training sequences (`smote_sequences`, random state 42). The result is the same for every seed, so the driver caches it per feature set.
3. The LSTM gets the SMOTE sequences and lengths. The MLP gets `combine(SMOTE sequences, SMOTE lengths, variant, scaler)`.
4. DataLoader with batch 64, shuffle using the seeded generator, `drop_last=False`.
5. Unweighted `CrossEntropyLoss`; `AdamW(lr=1e-3, weight_decay=1e-4)`; `ReduceLROnPlateau(mode="min", factor=0.5, patience=3)` stepped on validation loss.
6. At most 20 epochs. Early stopping after 10 epochs without a strictly lower validation loss.
7. Keep the best `state_dict` in memory (`copy.deepcopy`); no checkpoint files are needed.
8. Predict validation and test with the best weights. `pred = argmax`, `score = softmax[:, 1]`.

**`train_sklearn`:**
1. Combine train, validation, and test.
2. Fit a `StandardScaler` on the real training vectors and transform all three.
3. `SMOTE(random_state=42, k_neighbors=5)` on the scaled training vectors. Cache it per (feature set, combination); the SVM and RF share it.
4. Fit `SVC(kernel="rbf", C=1.0, gamma="scale", random_state=42)` with `score = decision_function`, or `RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)` with `score = predict_proba[:, 1]`. No `class_weight`.
5. `fit_seconds` covers the classifier fit only; SMOTE time is reported separately.

**Tests:**
- `smote_sequences` gives balanced classes, lengths in [1, k], and the first N rows equal to the input (imblearn appends synthetic rows). It is deterministic.
- `train_neural` on a tiny synthetic set (2 epochs, CPU) twice with the same seed gives identical predictions; a different seed differs.
- `train_sklearn` is deterministic.

### Module 8: `scripts/experiments/run_study.py`

**Implements:** Algorithm 5.2.

```
python scripts/experiments/run_study.py [--dry_run] [--only REGEX] [--device cuda]
    [--epochs 20] [--data_root data/processed/v2] [--out artifacts/study] [--allow_dirty] [--force]
```

- **Enumeration:**
  - Config ID is `<condition>__<classifier>__<variant>`, e.g. `cp3__lstm__attention` or `rand5__svm__mean_selfsim`.
  - Versions follow Section 1.
  - `--dry_run` prints counts by classifier and must show **140 configurations and 476 runs**.
- **Loop order:** for each feature set, load train, validation, and test once, fit the `FrameScaler`, build the SMOTE caches, then run every (configuration, version) that uses this feature set. For random conditions, feature set `rand5_d44` is version 3 of all 14 `rand5` configurations.
- **Outputs:**
  - `predictions/<config_id>/v<i>.csv` with columns clip_id, split (`validation` or `test`), level, y_true, y_pred, score. The driver fills in the labels from the `FeatureSet`; the training functions never see them.
  - A line in `runs.jsonl` with:
    - config_id, condition, classifier, variant, version, seed, draw, fs_id;
    - n_train, epochs_run, best_epoch, fit_seconds, smote_seconds, device;
    - `git_commit`, and `git_dirty` from `git status --porcelain`;
    - `data_fingerprint`: the sha256 of each split's `selections.json` and `common_clips.txt`;
    - versions of torch, sklearn, imblearn, numpy, and `cv2.__version__`;
    - a timestamp.
- **Resumable:** skip a run whose predictions file exists, unless `--force`. Refuse to start with a dirty working tree unless `--allow_dirty`.

**Test:** the dry-run counts (140 and 476), and the version → (seed, draw) mapping.

### Module 9: `src/stats.py` and `scripts/analysis/analyze_study.py`

**Implements:** §4.6 (all subsections).

**`src/stats.py`:**
```python
def mcnemar_exact(correct_a, correct_b) -> tuple[int, int, float]   # port significance_tests.py:70-91
def holm(p_values) -> np.ndarray                                    # port significance_tests.py:113-123
def bootstrap_indices(n, n_resamples=10_000, seed=0) -> np.ndarray  # int32 [B, n], made once per analysis
def paired_bootstrap_ci(correct_a, correct_b, idx) -> tuple[float, float]   # 2.5/97.5 percentiles, in accuracy POINTS
def binary_metrics(y_true, y_pred, level) -> dict
```

`binary_metrics` returns:
- accuracy and macro F1 (`f1_score(average="macro")`);
- per-class F1;
- MCC (`matthews_corrcoef`);
- PCC (`pearsonr`), asserted equal to MCC within 1e-9 when both are defined;
- MSE and class-wise MSE;
- the confusion matrix `[[TN, FP], [FN, TP]]`;
- for levels 0, 1, 2, the share of clips predicted Highly-Engaged (§4.6.1).

**Test cases** (`tests/test_stats.py`); the first two are the manuscript's own examples (§3.8):

| Input | Expected |
|---|---|
| McNemar, b = 60, c = 40 | p = 0.0569 |
| Holm on [0.01, 0.03, 0.04] | [0.03, 0.06, 0.06]; only the first < 0.05 |
| b = c = 0 | p = 1 |
| random binary vectors | MCC = PCC; MSE = 1 − accuracy |
| hand example with levels | the per-level rates by hand |

**`analyze_study.py`** writes its outputs to `artifacts/study/analysis/`.

1. **Metrics.**
   - Per run and split → `metrics_runs.csv`.
   - Per configuration, mean ± SD over versions → `metrics_configs.csv`.
   - Frames per clip per feature set → `frames_per_clip.csv`.
   - Processing time → `processing_time.csv`: per clip and feature set, the pass-2 time is the sum of its frames' `pass2_seconds`; pass 1 per clip comes from the outcome logs and is reported once; training time comes from the manifest.
2. **Comparisons** (test predictions only). The families are declared as data:

   | Family | (a, b), for each classifier with the mean / averaging readout | Count |
   |---|---|---|
   | 1 Content vs. position | (cp*k*, pos*k*), k = 3, 5, 7 | 12 |
   | 2 Content vs. chance | (cp*k*, rand*k*) | 12 |
   | 3 Position vs. chance | (pos*k*, rand*k*) | 12 |
   | 4 Frame budget | rule ∈ {pos, rand, cp}: (3, 5), (3, 7), (5, 7) | 36 |
   | 5 Clip boundaries | (sme3, pos3) | 4 |
   | 6 Temporal representation | MLP, SVM, RF: (each of concat, mean_change, mean_selfsim; mean) × 10 conditions; LSTM: (attention, mean) × 10 | 100 |

   Assert the counts. The accuracy difference is a − b, in points.
3. **Versions.** A comparison has 5 versions if either side has 5; version *i* pairs version *i* of each side, and a 1-version side reuses its single run. Otherwise it has 1. Compute for every version: b, c, the McNemar p, the difference, and the bootstrap CI. Use **one** index matrix for all comparisons.
4. **Holm.** For each family and each version index *i* = 1…5, correct the family's p-values together:
   - a 5-version comparison contributes its version *i*;
   - a 1-version comparison contributes its single p in every pass, and counts as significant only if it is significant in all five passes.

   This is the rule proposed as manuscript item M3. It **must be settled before any real test predictions are analyzed** (Section 6).
5. **Outcome** for each comparison:
   - *reliable* = significant in every version **and** the same sign in every version;
   - *equivalent* = the CI lies within [−2, +2] points in every version;
   - the label is "reliable difference smaller than the margin" if both hold, "reliable difference" or "equivalent" if one holds, and "inconclusive" if neither holds.
6. **Table 4.4 pattern** for each (k, classifier), from families 1–3, as the first matching row in table order. → `patterns_table44.csv`
7. **Family 6 summary:**
   - for each classifier × representation, count the conditions where the representation is reliably better, equivalent, or reliably worse than the mean;
   - "improves on the mean" means ≥ 5 reliably better and 0 reliably worse. → `family6_summary.csv`
8. **Best configuration** (§4.6.6):
   - rank the 140 configurations by mean **validation** macro F1;
   - the selection code reads only `split == "validation"`;
   - write the ranking to `best_config.csv`, and print the top configuration's test metrics once.
9. Refuse to run unless the manifest has all 476 runs `ok`. Use `--allow_incomplete` for synthetic and smoke data.

**Tests:**
- Family counts (176).
- A hand-built mixed family for the Holm passes.
- Outcome labels from synthetic CIs, including the boundary at ±2.
- Shuffling the test predictions leaves the best-configuration choice unchanged.

### Module 10: housekeeping (do the tag first)

1. Tag the current state before removing anything:
   ```
   git tag -a prelim-icce2026 -m "Code state of the ICCE 2026 preliminary study" 24d65cf
   ```
   (or the HEAD you are on), and push the tag.
2. Remove, after the tag: `src/train.py`, `src/evaluate.py`, `src/train_traditional.py`, `scripts/experiments/run_ablation_threshold3.py`, and `scripts/analysis/{summarize_threshold3,smote_delta,significance_tests,analyze_rf_feature_importance}.py`. Also remove `scripts/extraction/benchmark_feature_extraction_time.py`, since the timing now comes from the outcome logs and `frame_index.csv`.
3. Update `environment.yml`:
   - `python=3.11`;
   - a `pip:` section pinned to the installed versions: `mediapipe==0.10.9`, `rembg==2.0.69`, `onnxruntime==1.16.3`, `opencv-python==4.13.0.90`, `opencv-contrib-python==4.13.0.90`, `opencv-python-headless==4.11.0.86`, `openpyxl==3.1.5`.

   Don't uninstall any of the three OpenCV packages: mediapipe requires the contrib build and rembg the headless one. The `cv2` actually loaded is **4.11.0**. Don't change the environment during the study, since decoding and resizing could change; the manifest records `cv2.__version__`.
4. Update README (pipeline and layout), AGENTS.md (condition IDs replace `SUPPORTED_SAMPLING_METHODS`; the dataset section points to `load_feature_set`), and `docs/experiments.md` (a main-study protocol section: the 22-feature-set common set, versions, output paths, the tag).

---

## 5. Verification and run order

1. **Unit tests:** `conda run -n thesis-engagenet python -m pytest tests/ -v`. Every case above passes without data.
2. **Synthetic end-to-end.** The fixture writes a fake `data/processed/v2` tree (~200 clips per split, random features). Then:
   - `run_study.py --data_root <fake> --out <tmp> --epochs 2 --allow_dirty` gives 476 runs;
   - `analyze_study.py --allow_incomplete` gives 176 comparisons and a best configuration chosen from validation only.
3. **Real-clip smoke test** (only after ethics approval; decided 16 Nov, and stated in the ethics forms and §4.7). Run 20 clips per split, with `--limit 20 --out_root` and `--data_out` pointing to a scratch folder, through all three stages. Check that:
   - every clip has an outcome row, and every hash check passes;
   - **the new `cp5` and `cp7` frame indices equal the `frame_id`s in `data/processed/{5,7}-changepoint-test.csv` for the same clips.** Pass 1 and smoothing are unchanged, so any difference is a bug, or a different OpenCV or MediaPipe build than in July;
   - pass-2 features are close to the old values (differences come only from dropping the JPEG round trip);
   - per-frame and per-clip times give the full extraction time: about 11,300 clips × (pass 1 + up to ~57 frames × pass-2 time) ÷ workers;
   - then you delete the scratch outputs.
4. **Full extraction** (after ethics approval). Run validation and test first, through pass 1 and pass 2. Run training when its download is complete. Then assemble all three splits.
5. `run_study.py` (476 runs), then `analyze_study.py`.
6. Log every real run in `docs/experiments.md` with its template.

**Budget.** About 73 GB is free on C:.
- The remaining training videos take ~13 GB.
- The pass-1 store takes ~0.3 GB without landmarks.
- The pass-2 cache takes ~4 GB, at ≤ 57 frames per clip, against 108 for the old per-condition extraction.
- `frames.npy` takes ~4 GB over the three splits.

In July, extraction ran at about 5 h per 2,250 clips on 8 workers, mostly pass 1, so one pass 1 over ~11,300 clips is about 25 h. The smoke test gives the pass-2 figure.

---

## 6. Settle before any real test predictions are analyzed

These are protocol choices. §1.4 says the protocol is fixed before results are seen, so settle them in writing first, then freeze the analysis code with a tag (e.g. `analysis-frozen`).

1. **M3:** the Holm rule for mixed families and the same-direction requirement (Module 9, step 4).
2. **A "reliable difference smaller than the margin" outcome in Table 4.4 and the family-6 counts:** does it count as ">" (reliable), as "≈" (equivalent), or separately? I suggest counting it as reliable for the patterns and listing it separately in the family-6 counts.
3. **Ties in the best-configuration ranking:** unlikely at four decimals. If they happen, report all tied configurations.

---

## 7. What I check when I review a module

- It does what the manuscript section says. Every test case from this spec is present and passes.
- No test labels reach training or selection, and validation alone chooses the best configuration.
- Seeds, draws, and the version pairing are right, and two runs give identical output.
- Edge cases: n = 0, n ≤ k, m = 1, and garbage past `lengths`.
- No images on disk, no dead options, and no hard-coded paths outside the CLI defaults.
