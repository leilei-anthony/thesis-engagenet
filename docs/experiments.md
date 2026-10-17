# Experiment Log (corrected protocol)

Run log for experiments under the post-remediation protocol. Pre-remediation runs are in [archive/docs/EXPERIMENTS.md](../archive/docs/EXPERIMENTS.md). Those were computed on mismatched evaluation sets and should not be compared with entries here.

## Protocol

Every entry must hold to these rules, or say explicitly where it departs from them:

- **Common video set.** All sampling conditions are trained and evaluated on the same clips (`--restrict_to_common`; 2,719 train / 867 validation / 2,005 test). See [methodology §3.4.2](methodology-and-results.md#342-the-evaluation-set-confound).
- **Seeded.** LSTM/MLP report mean ± SD over seeds 42–46. SVM/RF are deterministic (`random_state=42`) and run once.
- **Task.** Threshold 3 (`{0,1,2}` vs `{3}`), unweighted, ≤20 epochs, unless the entry says otherwise.
- **Sampling methods.** `targeted` (SME), `3-changepoint`, `5-changepoint`, `7-changepoint`. BOCPD is not implemented.
- **Outputs.** The sweep driver writes `artifacts/ablation_threshold3_<tag>.txt`, `..._<tag>_manifest.jsonl` and `predictions_threshold3_<tag>/`. Record the tag.

## Entry template

```markdown
### YYYY-MM-DD: <short title>

- **Command:** `python scripts/experiments/run_ablation_threshold3.py ...`
- **Tag / artifacts:** `<tag>`: artifacts/ablation_threshold3_<tag>.txt
- **Hyperparameters:** model, readout, epochs, lr, batch size, SMOTE on/off, seeds
- **Results:** accuracy, macro F1, per-class F1, PCC, MSE, class-wise MSE
- **Confusion matrix:** path or inline table
- **Notes:** what changed and why; anything surprising
```

## Runs

### Threshold 3 main sweep, seed sweep, readout ablation (reported 2026-08-06)

- **Commands:** the three `run_ablation_threshold3.py` invocations in the [README pipeline](../README.md#pipeline) (`--smote both`; `--tag seeds`; `--tag readout`).
- **Tag / artifacts:** `common`, `seeds`, `readout`: `artifacts/ablation_threshold3_{common,seeds,readout}.txt` with their manifests and prediction dumps.
- **Results:** full tables are in [methodology §4](methodology-and-results.md#4-results-and-discussion). Best cell is 3-changepoint SVM at 0.7017 accuracy. Significance tests are in §4.2–§4.4, the readout ablation in §4.5, SMOTE in §4.6.
