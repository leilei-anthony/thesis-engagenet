# Archive

Pre-remediation material, kept for the record. It is **not maintained**, may not run against the current code, and its results should not be cited alongside [docs/methodology-and-results.md](../docs/methodology-and-results.md).

The files were superseded for two reasons, both explained in methodology [§3.4](../docs/methodology-and-results.md#34-two-corrections-to-the-experimental-setup) and [§6](../docs/methodology-and-results.md#6-superseded-findings):

- **BOCPD was never implemented.** The `bocpd` sampling option loaded the 3-changepoint files, so "BOCPD" results were duplicates. `src/dataset.py` now rejects it.
- **Evaluation-set confound.** Targeted/3-changepoint were scored on 2,227 test clips and 5-/7-changepoint on 2,005. Every sampling comparison here mixes the sampling effect with test-set composition.

The full pre-remediation tree is at commit `f0d514a`.

## Contents

| File | What it was | Replaced by |
| :--- | :--- | :--- |
| `docs/EXPERIMENTS.md` | Run log and result tables for all five task formulations | `docs/experiments.md` + methodology §4 |
| `docs/PROJECT_SUMMARY.md` | Project overview as of 2026-08-03 | `README.md` + methodology |
| `docs/REFERENCES.md` | Dataset, sampling-method and metric definitions (describes BOCPD as Method B) | methodology §2–§3 |
| `scripts/run_all_experiments.py` | SVM/RF/MLP runner over targeted vs bocpd | `scripts/experiments/run_ablation_threshold3.py` |
| `scripts/run_ablation_targeted_3_5_7{,_smote}.py` | Duplicated baseline/SMOTE sweep pair | `scripts/experiments/run_ablation_threshold3.py --smote` |
| `scripts/run_extraction_pipeline{,_7}.py` | 5-/7-changepoint extract-then-train runners | `scripts/extraction/run_extraction.py` |
| `scripts/generate_{ablation,smote_comparison}_figures.py` | Figures parsed from the hand-maintained `EXPERIMENTS.md` tables | No figure equivalent yet. Results tables now come from `scripts/analysis/summarize_threshold3.py` |
