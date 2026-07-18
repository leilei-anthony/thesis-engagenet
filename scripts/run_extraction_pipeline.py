import subprocess
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FEATURE_OUTPUT_ROOT = REPO_ROOT / "artifacts" / "feature_extraction"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

def run_cmd(cmd):
    print(f"\n>>> Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR: Command failed with code {res.returncode}")
        print(res.stderr)
        return False, res.stdout + "\n" + res.stderr
    print("SUCCESS")
    return True, res.stdout

def copy_processed_file(split):
    src = FEATURE_OUTPUT_ROOT / f"5_Changepoint_Dataset_{split}" / "collective_features.csv"
    dest = PROCESSED_DIR / f"5-changepoint-{split.lower()}.csv"
    print(f"Copying {src} -> {dest}")
    if src.exists():
        shutil.copy(src, dest)
        return True
    else:
        print(f"ERROR: Source file {src} does not exist!")
        return False

def main():
    print("==================================================")
    print("STARTING 5-CHANGEPOINT FEATURE EXTRACTION PIPELINE")
    print("==================================================")
    
    # 1. Feature Extraction
    splits = ["Validation", "Test", "Train"]
    for split in splits:
        print(f"\n--- Extracting features for split: {split} ---")
        cmd = [
            'conda', 'run', '-n', 'thesis-engagenet', 'python', 'scripts/feature_extraction.py',
            split, 'changepoint', '5'
        ]
        success, output = run_cmd(cmd)
        if not success:
            print(f"Pipeline stopped: Feature extraction failed for split {split}")
            sys.exit(1)
            
        # Copy to data/processed
        if not copy_processed_file(split):
            print(f"Pipeline stopped: Copying features failed for split {split}")
            sys.exit(1)
            
    print("\n==================================================")
    print("FEATURE EXTRACTION COMPLETED SUCCESSFULLY!")
    print("STARTING BASELINE TRAINING & EVALUATION ON 5-CHANGEPOINT")
    print("==================================================")
    
    out_file = REPO_ROOT / 'artifacts' / '5_changepoint_experiments_results.txt'
    
    # Define experiment runs
    # (model, sampling_method, mode, binarize_threshold, extra_args)
    configs = [
        # Multi-class
        ('classification', None, []),
        # Regression
        ('regression', None, ['--epochs', '50']),
        # Binary threshold 2
        ('classification', 2, ['--no_class_weights', '--epochs', '20']),
        # Binary threshold 1
        ('classification', 1, ['--no_class_weights', '--epochs', '20']),
        # Binary threshold 3
        ('classification', 3, ['--no_class_weights', '--epochs', '20']),
    ]
    
    with open(out_file, 'w') as f_out:
        # Loop over all models
        for model in ['lstm', 'mlp', 'svm', 'rf']:
            f_out.write(f"\n========================================\n")
            f_out.write(f"MODEL: {model.upper()} on 5-CHANGEPOINT\n")
            f_out.write(f"========================================\n")
            print(f"\n=== Running {model.upper()} baselines ===")
            
            for mode, thresh, extra in configs:
                if model in ['svm', 'rf']:
                    # Traditional baselines
                    cmd = [
                        'conda', 'run', '-n', 'thesis-engagenet', 'python', 'src/train_traditional.py',
                        '--sampling_method', '5-changepoint',
                        '--mode', mode,
                        '--model', model
                    ]
                    if thresh is not None:
                        cmd += ['--binarize_threshold', str(thresh)]
                    if '--no_class_weights' in extra:
                        cmd += ['--no_class_weights']
                        
                    success, output = run_cmd(cmd)
                    f_out.write(output)
                    f_out.flush()
                else:
                    # PyTorch models: LSTM, MLP
                    # Train
                    train_cmd = [
                        'conda', 'run', '-n', 'thesis-engagenet', 'python', 'src/train.py',
                        '--model', model,
                        '--sampling_method', '5-changepoint',
                        '--mode', mode
                    ]
                    if thresh is not None:
                        train_cmd += ['--binarize_threshold', str(thresh)]
                    train_cmd += extra
                    
                    success, train_output = run_cmd(train_cmd)
                    if not success:
                        print(f"Training failed for model={model}, mode={mode}, thresh={thresh}")
                        continue
                        
                    # Evaluate
                    eval_cmd = [
                        'conda', 'run', '-n', 'thesis-engagenet', 'python', 'src/evaluate.py',
                        '--model', model,
                        '--sampling_method', '5-changepoint',
                        '--mode', mode
                    ]
                    if thresh is not None:
                        eval_cmd += ['--binarize_threshold', str(thresh)]
                    if '--no_class_weights' in extra:
                        eval_cmd += ['--no_class_weights']
                        
                    success, eval_output = run_cmd(eval_cmd)
                    f_out.write(eval_output)
                    f_out.flush()
                    
    print(f"\nAll experiments on 5-changepoint completed! Results saved to {out_file}")

if __name__ == "__main__":
    main()
