import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LOGS_DIR = REPO_ROOT / 'artifacts' / 'experiment_logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# List of configurations
# (model, sampling_method, mode, binarize_threshold, extra_args)
configs = [
    # Multi-class
    ('targeted', 'classification', None, []),
    ('bocpd', 'classification', None, []),
    
    # Regression
    ('targeted', 'regression', None, ['--epochs', '50']),
    ('bocpd', 'regression', None, ['--epochs', '50']),
    
    # Binary threshold 2
    ('targeted', 'classification', 2, ['--no_class_weights', '--epochs', '20']),
    ('bocpd', 'classification', 2, ['--no_class_weights', '--epochs', '20']),
    
    # Binary threshold 1
    ('targeted', 'classification', 1, ['--no_class_weights', '--epochs', '20']),
    ('bocpd', 'classification', 1, ['--no_class_weights', '--epochs', '20']),
    
    # Binary threshold 3
    ('targeted', 'classification', 3, ['--no_class_weights', '--epochs', '20']),
    ('bocpd', 'classification', 3, ['--no_class_weights', '--epochs', '20']),
]

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR: Command failed with code {res.returncode}")
        print(res.stderr)
        return False, res.stdout + "\n" + res.stderr
    return True, res.stdout

def main():
    print("Starting experiment runner...")
    out_file = REPO_ROOT / 'artifacts' / 'baseline_experiments_results.txt'
    with open(out_file, 'w') as f_out:
        # Traditional baselines: SVM, RF
        for model in ['svm', 'rf']:
            f_out.write(f"\n========================================\n")
            f_out.write(f"MODEL: {model.upper()}\n")
            f_out.write(f"========================================\n")
            print(f"\n=== Running {model.upper()} baselines ===")
            for sampling, mode, thresh, extra in configs:
                cmd = [
                    'conda', 'run', '-n', 'thesis-engagenet', 'python', 'src/train_traditional.py',
                    '--sampling_method', sampling,
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
                
        # MLP baseline (Neural Network)
        f_out.write(f"\n========================================\n")
        f_out.write(f"MODEL: MLP\n")
        f_out.write(f"========================================\n")
        print("\n=== Running MLP baselines ===")
        for sampling, mode, thresh, extra in configs:
            # 1. Train MLP
            train_cmd = [
                'conda', 'run', '-n', 'thesis-engagenet', 'python', 'src/train.py',
                '--model', 'mlp',
                '--sampling_method', sampling,
                '--mode', mode
            ]
            if thresh is not None:
                train_cmd += ['--binarize_threshold', str(thresh)]
            train_cmd += extra
            
            success, train_output = run_cmd(train_cmd)
            if not success:
                continue
                
            # 2. Evaluate MLP
            eval_cmd = [
                'conda', 'run', '-n', 'thesis-engagenet', 'python', 'src/evaluate.py',
                '--model', 'mlp',
                '--sampling_method', sampling,
                '--mode', mode
            ]
            if thresh is not None:
                eval_cmd += ['--binarize_threshold', str(thresh)]
            if '--no_class_weights' in extra:
                eval_cmd += ['--no_class_weights']
                
            success, eval_output = run_cmd(eval_cmd)
            f_out.write(eval_output)
            f_out.flush()
            
    print(f"All experiments finished! Results saved to {out_file}")

if __name__ == '__main__':
    main()
