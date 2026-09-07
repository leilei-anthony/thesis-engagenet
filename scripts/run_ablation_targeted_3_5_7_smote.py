import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

SAMPLING_METHODS = ["targeted", "3-changepoint", "5-changepoint", "7-changepoint"]
MODELS = ["lstm", "mlp", "svm", "rf"]

# (mode, binarize_threshold, extra_args)
# Same sweep as scripts/run_ablation_targeted_3_5_7.py, but every command additionally
# gets --use_smote. Regression configs pass it too for symmetry with the baseline sweep;
# train.py / train_traditional.py auto-skip SMOTE for regression (discrete labels only)
# and print a message rather than silently no-op.
CONFIGS = [
    ("classification", None, []),
    ("regression", None, ["--epochs", "50"]),
    ("classification", 2, ["--no_class_weights", "--epochs", "20"]),
    ("classification", 1, ["--no_class_weights", "--epochs", "20"]),
    ("classification", 3, ["--no_class_weights", "--epochs", "20"]),
]


def run_cmd(cmd):
    print(f"\n>>> Running: {' '.join(cmd)}", flush=True)
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0
    if res.returncode != 0:
        print(f"ERROR: Command failed with code {res.returncode} after {dt:.1f}s", flush=True)
        print(res.stderr, flush=True)
        return False, res.stdout + "\n" + res.stderr
    print(f"SUCCESS ({dt:.1f}s)", flush=True)
    return True, res.stdout


def check_data_present(sampling_method):
    for split in ["train", "validation", "test"]:
        f = PROCESSED_DIR / f"{sampling_method}-{split}.csv"
        if not f.exists():
            print(f"ERROR: missing required data file {f}", flush=True)
            return False
    return True


def main():
    out_file = REPO_ROOT / "artifacts" / "ablation_targeted_3_5_7_changepoint_results_smote.txt"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    print("==================================================", flush=True)
    print("ABLATION SWEEP (SMOTE): targeted, 3/5/7-changepoint", flush=True)
    print(f"Sampling methods: {SAMPLING_METHODS}", flush=True)
    print(f"Models: {MODELS}", flush=True)
    print(f"Results file: {out_file}", flush=True)
    print("==================================================", flush=True)

    for sm in SAMPLING_METHODS:
        if not check_data_present(sm):
            print(f"Pipeline stopped: data missing for sampling_method={sm}", flush=True)
            sys.exit(1)

    with open(out_file, "w") as f_out:
        for sampling_method in SAMPLING_METHODS:
            for model in MODELS:
                f_out.write("\n========================================\n")
                f_out.write(f"SAMPLING METHOD: {sampling_method.upper()} | MODEL: {model.upper()}\n")
                f_out.write("========================================\n")
                f_out.flush()
                print(f"\n=== {sampling_method.upper()} / {model.upper()} (SMOTE) ===", flush=True)

                for mode, thresh, extra in CONFIGS:
                    if model in ["svm", "rf"]:
                        cmd = [
                            "conda", "run", "-n", "thesis-engagenet", "python", "src/train_traditional.py",
                            "--sampling_method", sampling_method,
                            "--mode", mode,
                            "--model", model,
                            "--use_smote",
                        ]
                        if thresh is not None:
                            cmd += ["--binarize_threshold", str(thresh)]
                        if "--no_class_weights" in extra:
                            cmd += ["--no_class_weights"]

                        success, output = run_cmd(cmd)
                        f_out.write(output)
                        f_out.flush()
                    else:
                        train_cmd = [
                            "conda", "run", "-n", "thesis-engagenet", "python", "src/train.py",
                            "--model", model,
                            "--sampling_method", sampling_method,
                            "--mode", mode,
                            "--use_smote",
                        ]
                        if thresh is not None:
                            train_cmd += ["--binarize_threshold", str(thresh)]
                        train_cmd += extra

                        success, train_output = run_cmd(train_cmd)
                        if not success:
                            print(f"Training failed for {sampling_method}/{model}, mode={mode}, thresh={thresh}", flush=True)
                            f_out.write(train_output)
                            f_out.flush()
                            continue

                        eval_cmd = [
                            "conda", "run", "-n", "thesis-engagenet", "python", "src/evaluate.py",
                            "--model", model,
                            "--sampling_method", sampling_method,
                            "--mode", mode,
                            "--use_smote",
                        ]
                        if thresh is not None:
                            eval_cmd += ["--binarize_threshold", str(thresh)]
                        if "--no_class_weights" in extra:
                            eval_cmd += ["--no_class_weights"]

                        success, eval_output = run_cmd(eval_cmd)
                        f_out.write(eval_output)
                        f_out.flush()

    print(f"\nAll SMOTE ablation experiments completed! Results saved to {out_file}", flush=True)


if __name__ == "__main__":
    main()
