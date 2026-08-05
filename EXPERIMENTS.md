# Experimental Log - Student Engagement Ablation Study

This file serves as the log for all training runs, ablation studies, and evaluation experiments comparing **Targeted Sampling** vs **BOCPD**.

## Summary Table

| Run ID | Sampling Method | Task Mode | Epochs | Val Loss | Overall MSE | PCC | Class 0 MSE | Class 1 MSE | Class 2 MSE | Class 3 MSE | Notes / Hyperparameters |
|--------|-----------------|-----------|--------|----------|-------------|-----|-------------|-------------|-------------|-------------|------------------------|
| Run 1  | Targeted        | Classify  | 10 (ES:1) | 1.3923 | 5.4459      | 0.0000 | 0.0000      | 1.0000      | 4.0000      | 9.0000      | Batch=64, lr=1e-3, Weight_0=3.03 |
| Run 2  | BOCPD           | Classify  | 10 (ES:1) | 1.3954 | 5.4459      | 0.0000 | 0.0000      | 1.0000      | 4.0000      | 9.0000      | Batch=64, lr=1e-3, Weight_0=3.03 |
| Run 3  | Targeted        | Regress   | 50        | 1.7361 | 1.5598      | nan    | 2.5605      | 0.3602      | 0.1599      | 1.9596      | Batch=64, lr=1e-3, Weighted MSE |
| Run 4  | BOCPD           | Regress   | 50        | 1.8515 | 1.6752      | nan    | 2.1865      | 0.2291      | 0.2718      | 2.3144      | Batch=64, lr=1e-3, Weighted MSE |
| Run 5  | Targeted        | Classify  | 20 (ES:12)| 0.4298 | 0.2510      | 0.3365 | 0.7938      | 0.0155      | -           | -           | Binarized Thresh 2, Unweighted, Batch=64 |
| Run 6  | BOCPD           | Classify  | 20 (ES:9) | 0.4458 | 0.2766      | 0.2283 | 0.8487      | 0.0283      | -           | -           | Binarized Thresh 2, Unweighted, Batch=64 |
| Run 7  | Targeted        | Classify  | 20 (ES:19)| 0.2172 | 0.1527      | 0.4086 | 0.7593      | 0.0083      | -           | -           | Binarized Thresh 1, Unweighted, Batch=64 |
| Run 8  | BOCPD           | Classify  | 20 (ES:17)| 0.2293 | 0.1558      | 0.3932 | 0.7360      | 0.0178      | -           | -           | Binarized Thresh 1, Unweighted, Batch=64 |
| Run 9  | Targeted        | Classify  | 20 (ES:5) | 0.6571 | 0.3467      | 0.3105 | 0.4575      | 0.2399      | -           | -           | Binarized Thresh 3, Unweighted, Batch=64 |
| Run 10 | BOCPD           | Classify  | 20 (ES:7) | 0.6539 | 0.3467      | 0.3099 | 0.4520      | 0.2451      | -           | -           | Binarized Thresh 3, Unweighted, Batch=64 |

## Detailed Evaluation Metrics

| Run ID | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | Class 2 F1 | Class 3 F1 | PCC (p-value) | Overall MSE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Run 1** (Targeted Multi-class) | 0.1922 | 0.0806 | 0.0620 | 0.3224 | 0.0000 | 0.0000 | 0.0000 | 0.0000 (1.0) | 5.4459 |
| **Run 2** (BOCPD Multi-class) | 0.1922 | 0.0806 | 0.0620 | 0.3224 | 0.0000 | 0.0000 | 0.0000 | 0.0000 (1.0) | 5.4459 |
| **Run 3** (Targeted Regression) | 0.1881 | 0.0792 | 0.0596 | 0.0000 | 0.0000 | 0.3167 | 0.0000 | nan (nan) | 1.5598 |
| **Run 4** (BOCPD Regression) | 0.1105 | 0.0498 | 0.0220 | 0.0000 | 0.1990 | 0.0000 | 0.0000 | nan (nan) | 1.6752 |
| **Run 5** (Targeted Binary Thresh 2) | 0.7490 | 0.5888 | 0.6901 | 0.3321 | 0.8455 | - | - | 0.3365 ($4.32\times 10^{-60}$) | 0.2510 |
| **Run 6** (BOCPD Binary Thresh 2) | 0.7234 | 0.5396 | 0.6544 | 0.2488 | 0.8305 | - | - | 0.2283 ($1.01\times 10^{-27}$) | 0.2766 |
| **Run 7** (Targeted Binary Thresh 1) | **0.8473** | 0.6451 | 0.8100 | 0.3773 | **0.9130** | - | - | **0.4086 ($2.20\times 10^{-90}$)** | **0.1527** |
| **Run 8** (BOCPD Binary Thresh 1) | 0.8442 | **0.6525** | **0.8114** | **0.3944** | 0.9106 | - | - | 0.3932 ($2.94\times 10^{-83}$) | 0.1558 |
| **Run 9** (Targeted Binary Thresh 3) | 0.6533 | 0.6482 | 0.6490 | 0.6057 | **0.6907** | - | - | **0.3105 ($5.82\times 10^{-51}$)** | 0.3467 |
| **Run 10** (BOCPD Binary Thresh 3) | 0.6533 | **0.6487** | **0.6494** | **0.6081** | 0.6892 | - | - | 0.3099 ($8.94\times 10^{-51}$) | 0.3467 |

---

## Run Details

### Run 1: Targeted Sampling Classification (Multi-class)
- **Date / Time**: 2026-07-09
- **Command**: `python src/train.py --sampling_method targeted --mode classification --epochs 10 --batch_size 64`
- **Hyperparameters**:
  - Learning Rate: `1e-3`, Optimizer: `AdamW`, Scheduler: `ReduceLROnPlateau`, Batch Size: `64`, Hidden Dimension: `64`
- **Confusion Matrix**:
  ```
  [[ 428    0    0    0],
   [ 246    0    0    0],
   [ 419    0    0    0],
   [1134    0    0    0]]
  ```
- **Evaluation Metrics**:
  - **Accuracy**: `0.1922`
  - **Overall MSE**: `5.4459`
  - **Pearson Correlation (PCC)**: `0.0000` (p-value: `1.0`)
  - **Class-wise Metrics**:
    - Class 0 (Not-Engaged): Precision = `0.1922`, Recall = `1.0000`, F1-score = `0.3224` (Support = `428`)
    - Class 1 (Barely-engaged): Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `246`)
    - Class 2 (Engaged): Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `419`)
    - Class 3 (Highly-Engaged): Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `1134`)
  - **Macro F1-score**: `0.0806`
  - **Weighted F1-score**: `0.0620`
  - **Class-wise MSE**: Class 0 = `0.0000`, Class 1 = `1.0000`, Class 2 = `4.0000`, Class 3 = `9.0000`
- **Observations & Insights**:
  - Early stopping was triggered as validation loss did not improve beyond the first epoch.
  - The model predicted all samples as Class 0 (Not-Engaged). This is because Class 0 has a very high computed loss weight (3.03) to penalize misclassifying it, causing the model to converge to predicting only Class 0 initially.

### Run 2: BOCPD Sampling Classification (Multi-class)
- **Date / Time**: 2026-07-09
- **Command**: `python src/train.py --sampling_method bocpd --mode classification --epochs 10 --batch_size 64`
- **Hyperparameters**:
  - Learning Rate: `1e-3`, Optimizer: `AdamW`, Scheduler: `ReduceLROnPlateau`, Batch Size: `64`, Hidden Dimension: `64`
- **Confusion Matrix**:
  ```
  [[ 428    0    0    0],
   [ 246    0    0    0],
   [ 419    0    0    0],
   [1134    0    0    0]]
  ```
- **Evaluation Metrics**:
  - **Accuracy**: `0.1922`
  - **Overall MSE**: `5.4459`
  - **Pearson Correlation (PCC)**: `0.0000` (p-value: `1.0`)
  - **Class-wise Metrics**:
    - Class 0 (Not-Engaged): Precision = `0.1922`, Recall = `1.0000`, F1-score = `0.3224` (Support = `428`)
    - Class 1 (Barely-engaged): Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `246`)
    - Class 2 (Engaged): Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `419`)
    - Class 3 (Highly-Engaged): Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `1134`)
  - **Macro F1-score**: `0.0806`
  - **Weighted F1-score**: `0.0620`
  - **Class-wise MSE**: Class 0 = `0.0000`, Class 1 = `1.0000`, Class 2 = `4.0000`, Class 3 = `9.0000`
- **Observations & Insights**:
  - Identical behavior to Targeted Sampling was observed due to identical initial loss optimization favoring Class 0.

### Run 3: Targeted Sampling Regression
- **Date / Time**: 2026-07-09
- **Command**: `python src/train.py --sampling_method targeted --mode regression --epochs 50 --batch_size 64`
- **Hyperparameters**:
  - Learning Rate: `1e-3`, Optimizer: `AdamW`, Scheduler: `ReduceLROnPlateau`, Batch Size: `64`, Hidden Dimension: `64`
- **Confusion Matrix** (discrete rounded):
  ```
  [[   0    0  428    0],
   [   0    0  246    0],
   [   0    0  419    0],
   [   0 1134    0    0]]
  ```
- **Evaluation Metrics**:
  - **Overall MSE**: `1.5598`
  - **Pearson Correlation (PCC)**: `nan`
  - **Accuracy** (discrete rounded): `0.1881`
  - **Class-wise Metrics** (discrete rounded):
    - Class 0: Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `428`)
    - Class 1: Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `246`)
    - Class 2: Precision = `0.1881`, Recall = `1.0000`, F1-score = `0.3167` (Support = `419`)
    - Class 3: Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `1134`)
  - **Macro F1-score**: `0.0792`
  - **Weighted F1-score**: `0.0596`
  - **Class-wise MSE**: Class 0 = `2.5605`, Class 1 = `0.3602`, Class 2 = `0.1599`, Class 3 = `1.9596`
- **Observations & Insights**:
  - Training completed all 50 epochs; validation loss successfully decreased from 5.03 to 1.73.
  - The model predicted all samples close to 2.0 (which rounds to Class 2, Engaged). Since the average label index in the dataset is 2.014, the model collapsed into outputting the mean prediction to minimize MSE, yielding `nan` correlation (PCC) because predicted variance is zero.

### Run 4: BOCPD Sampling Regression
- **Date / Time**: 2026-07-09
- **Command**: `python src/train.py --sampling_method bocpd --mode regression --epochs 50 --batch_size 64`
- **Hyperparameters**:
  - Learning Rate: `1e-3`, Optimizer: `AdamW`, Scheduler: `ReduceLROnPlateau`, Batch Size: `64`, Hidden Dimension: `64`
- **Confusion Matrix** (discrete rounded):
  ```
  [[   0  428    0    0],
   [   0  246    0    0],
   [   0  419    0    0],
   [   0 1134    0    0]]
  ```
- **Evaluation Metrics**:
  - **Overall MSE**: `1.6752`
  - **Pearson Correlation (PCC)**: `nan`
  - **Accuracy** (discrete rounded): `0.1105`
  - **Class-wise Metrics** (discrete rounded):
    - Class 0: Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `428`)
    - Class 1: Precision = `0.1105`, Recall = `1.0000`, F1-score = `0.1990` (Support = `246`)
    - Class 2: Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `419`)
    - Class 3: Precision = `0.0000`, Recall = `0.0000`, F1-score = `0.0000` (Support = `1134`)
  - **Macro F1-score**: `0.0498`
  - **Weighted F1-score**: `0.0220`
  - **Class-wise MSE**: Class 0 = `2.1865`, Class 1 = `0.2291`, Class 2 = `0.2718`, Class 3 = `2.3144`
- **Observations & Insights**:
  - Training completed all 50 epochs; validation loss successfully decreased from 6.06 to 1.85.
  - The model predicted all samples close to 1.48 (which rounds to Class 1, Barely Engaged). Because of the 2.0x custom loss penalty on Class 0 predictions, predicting around 1.48 achieves a lower weighted MSE than the actual mean of 2.014. The model collapsed to predicting a constant value, resulting in `nan` PCC.

### Run 5: Targeted Sampling Binary Classification (Threshold = 2)
- **Date / Time**: 2026-07-09
- **Command**: `python src/train.py --sampling_method targeted --mode classification --binarize_threshold 2 --no_class_weights --epochs 20 --batch_size 64`
- **Hyperparameters**:
  - Learning Rate: `1e-3`, Optimizer: `AdamW`, Scheduler: `ReduceLROnPlateau`, Batch Size: `64`, Hidden Dimension: `64`
- **Confusion Matrix**:
  ```
  [[ 139  535]
   [  24 1529]]
  ```
- **Evaluation Metrics**:
  - **Accuracy**: `0.7490`
  - **Overall MSE**: `0.2510`
  - **Pearson Correlation (PCC)**: **`0.3365`** (p-value: `4.322e-60`)
  - **Class-wise Metrics**:
    - Class 0 (Disengaged): Precision = `0.8528`, Recall = `0.2062`, F1-score = `0.3321` (Support = `674`)
    - Class 1 (Engaged): Precision = `0.7408`, Recall = `0.9845`, F1-score = `0.8455` (Support = `1553`)
  - **Macro F1-score**: **`0.5888`**
  - **Weighted F1-score**: **`0.6901`**
  - **Class-wise MSE**: Class 0 = `0.7938`, Class 1 = `0.0155`
- **Observations & Insights**:
  - Training completed successfully with best validation loss at epoch 12 (`0.4298`).
  - Resolving the NaN feature values completely unlocked weight training. The model achieved a highly statistically significant Pearson Correlation (PCC) of **`0.3365`** (p-value = `4.322e-60`) and **`74.90%`** overall test accuracy.
  - The model does not collapse to a constant prediction, successfully discriminating between Disengaged and Engaged classes (Precision = `85.28%` on Class 0).

### Run 6: BOCPD Sampling Binary Classification (Threshold = 2)
- **Date / Time**: 2026-07-09
- **Command**: `python src/train.py --sampling_method bocpd --mode classification --binarize_threshold 2 --no_class_weights --epochs 20 --batch_size 64`
- **Hyperparameters**:
  - Learning Rate: `1e-3`, Optimizer: `AdamW`, Scheduler: `ReduceLROnPlateau`, Batch Size: `64`, Hidden Dimension: `64`
- **Confusion Matrix**:
  ```
  [[ 102  572]
   [  44 1509]]
  ```
- **Evaluation Metrics**:
  - **Accuracy**: `0.7234`
  - **Overall MSE**: `0.2766`
  - **Pearson Correlation (PCC)**: **`0.2283`** (p-value: `1.005e-27`)
  - **Class-wise Metrics**:
    - Class 0 (Disengaged): Precision = `0.6986`, Recall = `0.1513`, F1-score = `0.2488` (Support = `674`)
    - Class 1 (Engaged): Precision = `0.7251`, Recall = `0.9717`, F1-score = `0.8305` (Support = `1553`)
  - **Macro F1-score**: **`0.5396`**
  - **Weighted F1-score**: **`0.6544`**
  - **Class-wise MSE**: Class 0 = `0.8487`, Class 1 = `0.0283`
- **Observations & Insights**:
  - Early stopping triggered at epoch 19; best validation loss at epoch 9 (`0.4458`).
  - Achieved a Pearson Correlation (PCC) of **`0.2283`** (p-value = `1.005e-27`) and **`72.34%`** accuracy.
  - Comparison shows that **Targeted Sampling (Run 5) significantly outperforms BOCPD Sampling (Run 6)** across all metrics (PCC, Accuracy, and Class 0 / Class 1 F1 scores).

### Run 7: Targeted Sampling Binary Classification (Threshold = 1)
- **Date / Time**: 2026-07-09
- **Command**: `python src/train.py --sampling_method targeted --mode classification --binarize_threshold 1 --no_class_weights --epochs 20 --batch_size 64`
- **Hyperparameters**:
  - Learning Rate: `1e-3`, Optimizer: `AdamW`, Scheduler: `ReduceLROnPlateau`, Batch Size: `64`, Hidden Dimension: `64`
- **Confusion Matrix**:
  ```
  [[ 103  325]
   [  15 1784]]
  ```
- **Evaluation Metrics**:
  - **Accuracy**: `0.8473`
  - **Overall MSE**: `0.1527`
  - **Pearson Correlation (PCC)**: **`0.4086`** (p-value: `2.201e-90`)
  - **Class-wise Metrics**:
    - Class 0 (Not-Engaged): Precision = `0.8729`, Recall = `0.2407`, F1-score = `0.3773` (Support = `428`)
    - Class 1 (Engaged): Precision = `0.8459`, Recall = `0.9917`, F1-score = `0.9130` (Support = `1799`)
  - **Macro F1-score**: `0.6451`
  - **Weighted F1-score**: `0.8100`
  - **Class-wise MSE**: Class 0 = `0.7593`, Class 1 = `0.0083`
- **Observations & Insights**:
  - Best validation loss achieved at epoch 19 (`0.2172`).
  - Achieved the highest Pearson Correlation Coefficient (PCC = `0.4086`) and accuracy (`84.73%`) among all binary setups. 

### Run 8: BOCPD Sampling Binary Classification (Threshold = 1)
- **Date / Time**: 2026-07-09
- **Command**: `python src/train.py --sampling_method bocpd --mode classification --binarize_threshold 1 --no_class_weights --epochs 20 --batch_size 64`
- **Hyperparameters**:
  - Learning Rate: `1e-3`, Optimizer: `AdamW`, Scheduler: `ReduceLROnPlateau`, Batch Size: `64`, Hidden Dimension: `64`
- **Confusion Matrix**:
  ```
  [[ 113  315]
   [  32 1767]]
  ```
- **Evaluation Metrics**:
  - **Accuracy**: `0.8442`
  - **Overall MSE**: `0.1558`
  - **Pearson Correlation (PCC)**: `0.3932` (p-value: `2.941e-83`)
  - **Class-wise Metrics**:
    - Class 0 (Not-Engaged): Precision = `0.7793`, Recall = `0.2640`, F1-score = `0.3944` (Support = `428`)
    - Class 1 (Engaged): Precision = `0.8487`, Recall = `0.9822`, F1-score = `0.9106` (Support = `1799`)
  - **Macro F1-score**: `0.6525`
  - **Weighted F1-score**: `0.8114`
  - **Class-wise MSE**: Class 0 = `0.7360`, Class 1 = `0.0178`
- **Observations & Insights**:
  - Best validation loss achieved at epoch 17 (`0.2293`).
  - The model slightly underperforms Run 7 (Targeted) on overall accuracy and PCC, but achieves a slightly higher Macro F1-score (`0.6525` vs `0.6451`) due to better recall on Class 0.

### Run 9: Targeted Sampling Binary Classification (Threshold = 3)
- **Date / Time**: 2026-07-09
- **Command**: `python src/train.py --sampling_method targeted --mode classification --binarize_threshold 3 --no_class_weights --epochs 20 --batch_size 64`
- **Hyperparameters**:
  - Learning Rate: `1e-3`, Optimizer: `AdamW`, Scheduler: `ReduceLROnPlateau`, Batch Size: `64`, Hidden Dimension: `64`
- **Confusion Matrix**:
  ```
  [[593 500]
   [272 862]]
  ```
- **Evaluation Metrics**:
  - **Accuracy**: `0.6533`
  - **Overall MSE**: `0.3467`
  - **Pearson Correlation (PCC)**: **`0.3105`** (p-value: `5.816e-51`)
  - **Class-wise Metrics**:
    - Class 0 (Disengaged): Precision = `0.6855`, Recall = `0.5425`, F1-score = `0.6057` (Support = `1093`)
    - Class 1 (Engaged): Precision = `0.6329`, Recall = `0.7601`, F1-score = `0.6907` (Support = `1134`)
  - **Macro F1-score**: `0.6482`
  - **Weighted F1-score**: `0.6490`
  - **Class-wise MSE**: Class 0 = `0.4575`, Class 1 = `0.2399`
- **Observations & Insights**:
  - Early stopping triggered at epoch 15; best validation loss achieved at epoch 5 (`0.6571`).
  - This balanced configuration (threshold = 3: Levels 0/1/2 vs 3) yields high and stable F1-scores across both disengaged and engaged groups (`0.6057` vs `0.6907`).

### Run 10: BOCPD Sampling Binary Classification (Threshold = 3)
- **Date / Time**: 2026-07-09
- **Command**: `python src/train.py --sampling_method bocpd --mode classification --binarize_threshold 3 --no_class_weights --epochs 20 --batch_size 64`
- **Hyperparameters**:
  - Learning Rate: `1e-3`, Optimizer: `AdamW`, Scheduler: `ReduceLROnPlateau`, Batch Size: `64`, Hidden Dimension: `64`
- **Confusion Matrix**:
  ```
  [[599 494]
   [278 856]]
  ```
- **Evaluation Metrics**:
  - **Accuracy**: `0.6533`
  - **Overall MSE**: `0.3467`
  - **Pearson Correlation (PCC)**: `0.3099` (p-value: `8.943e-51`)
  - **Class-wise Metrics**:
    - Class 0 (Disengaged): Precision = `0.6830`, Recall = `0.5480`, F1-score = `0.6081` (Support = `1093`)
    - Class 1 (Engaged): Precision = `0.6341`, Recall = `0.7549`, F1-score = `0.6892` (Support = `1134`)
  - **Macro F1-score**: `0.6487`
  - **Weighted F1-score**: `0.6494`
  - **Class-wise MSE**: Class 0 = `0.4520`, Class 1 = `0.2451`
- **Observations & Insights**:
  - Early stopping triggered at epoch 17; best validation loss achieved at epoch 7 (`0.6539`).
  - Performance is extremely similar to Run 9 (Targeted) due to the highly balanced class ratios.


## Baseline Model Comparison (MLP, SVM, Random Forest)

To establish robust benchmarks, we evaluated three additional machine learning models:
1. **Neural Network (MLP)**: A PyTorch-based model consisting of a temporal average pooling layer, followed by fully-connected layers (`input_dim (1518) -> hidden_dim (64) -> hidden_dim/2 (32) -> output_dim`).
2. **SVM**: An RBF-kernel Support Vector Machine trained on standard-scaled temporally average-pooled features.
3. **Random Forest (RF)**: An ensemble of 100 decision trees trained on average-pooled features.

### Comparison Tables

> **Update (2026-07-23)**: The `Targeted`, `3-Changepoint`, `5-Changepoint`, and `7-Changepoint` rows below were regenerated by a full ablation sweep (`scripts/run_ablation_targeted_3_5_7.py`, 84 train+eval runs across LSTM/MLP/SVM/RF) after fixing a bug in `src/dataset.py` where sequences were always zero-padded/truncated to a fixed length of 3 frames regardless of `sampling_method` — this silently discarded frames 4+ for the 5- and 7-changepoint LSTM/MLP models. Sequence padding now dynamically matches the changepoint count. `3-Changepoint` results are new (previously undocumented). `BOCPD` rows are unchanged from the original study — note that `src/dataset.py` maps `bocpd` to the same underlying `3-changepoint-*.csv` files as `3-changepoint`, so their SVM/RF numbers (deterministic given identical data) match exactly; only LSTM/MLP differ, from training-run stochasticity (no fixed seed).
>
> **Update (2026-08-03)**: Re-ran the same sweep (`Targeted`/`3`/`5`/`7`-Changepoint × LSTM/MLP/SVM/RF, 84 train+eval runs) with training-time instrumentation added to `src/train.py` (wall-clock across all epochs), `src/train_traditional.py` (`model.fit()` wall-clock), and `src/evaluate.py` (surfaces the time recorded on the checkpoint). All metrics below reflect this fresh run — absolute numbers shift slightly from the 07-23 run due to training-run stochasticity (no fixed random seed on the LSTM/MLP side), but the qualitative pattern is unchanged (see Key Observations). A new **Training Time (s)** column was added to every table. `BOCPD` LSTM/MLP rows are still the original legacy runs (no timing data was ever collected for them, marked `N/A (legacy run)`); `BOCPD` SVM/RF training time is reported as identical to `3-Changepoint` SVM/RF, for the same identical-underlying-data reason as their accuracy metrics. Raw run log: `artifacts/ablation_targeted_3_5_7_changepoint_results.txt`.

### Figures

Generated by `scripts/generate_ablation_figures.py` (parses the tables below directly, so they always stay in sync — re-run after any table edit). Bars/lines are colored by sampling method: **Targeted** (blue), **BOCPD** (orange), **3-Changepoint** (aqua), **5-Changepoint** (yellow), **7-Changepoint** (magenta). Note that BOCPD and 3-Changepoint overlap almost exactly on SVM/RF panels since they read identical underlying data (see note above).

![Multi-class classification: accuracy and macro F1 by sampling method and model](artifacts/figures/fig1_multiclass_classification.png)

![Regression: PCC and MSE by sampling method and model](artifacts/figures/fig2_regression.png)

![Binary classification (Threshold 3): accuracy and macro F1 by sampling method and model](artifacts/figures/fig3_binary_threshold3.png)

![Training time by sampling method and model, summed across all 5 tasks (log scale)](artifacts/figures/fig4_training_time.png)

#### 1. Multi-class Classification (All Sampling Methods)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | PCC (p-value) | Overall MSE | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 0.4912 | 0.3738 | 0.4905 | 0.4776 (2.8e-127) | 1.2726 | 15.3 |
| **Targeted** | MLP | 0.4800 | 0.3678 | 0.4831 | 0.4777 (2.4e-127) | 1.2721 | 21.1 |
| **Targeted** | SVM | 0.4782 | 0.4329 | 0.5089 | 0.5014 (4.0e-142) | 1.3395 | 4.8 |
| **Targeted** | Random Forest | 0.5388 | 0.3961 | 0.5174 | 0.5101 (8.5e-148) | 1.3507 | 2.4 |
| **BOCPD** | LSTM (Run 2) | 0.1922 | 0.0806 | 0.0620 | 0.0000 (1.0) | 5.4459 | N/A (legacy run) |
| **BOCPD** | MLP | 0.4526 | 0.3289 | 0.4371 | 0.2075 (4.4e-23) | 2.4360 | N/A (legacy run) |
| **BOCPD** | SVM | 0.4558 | 0.4112 | 0.4941 | 0.4911 (1.6e-135) | 1.3696 | 5.9 |
| **BOCPD** | Random Forest | 0.5339 | 0.4152 | 0.5283 | 0.5263 (6.1e-159) | 1.2591 | 2.2 |
| **3-Changepoint** | LSTM | 0.4912 | 0.2788 | 0.4218 | 0.1936 (3.0e-20) | 2.3211 | 34.0 |
| **3-Changepoint** | MLP | 0.4881 | 0.3055 | 0.4403 | 0.2303 (3.5e-28) | 2.4288 | 10.6 |
| **3-Changepoint** | SVM | 0.4558 | 0.4112 | 0.4941 | 0.4911 (1.6e-135) | 1.3696 | 5.9 |
| **3-Changepoint** | Random Forest | 0.5339 | 0.4152 | 0.5283 | 0.5263 (6.1e-159) | 1.2591 | 2.2 |
| **5-Changepoint** | LSTM | 0.5102 | 0.3160 | 0.4491 | 0.3248 (1.8e-50) | 2.0015 | 13.1 |
| **5-Changepoint** | MLP | 0.4539 | 0.3421 | 0.4511 | 0.2891 (6.5e-40) | 1.8459 | 13.6 |
| **5-Changepoint** | SVM | 0.4559 | 0.4158 | 0.4908 | 0.4379 (1.0e-94) | 1.3980 | 6.3 |
| **5-Changepoint** | Random Forest | 0.4893 | 0.3825 | 0.4860 | 0.4601 (1.4e-105) | 1.2953 | 2.2 |
| **7-Changepoint** | LSTM | 0.5012 | 0.3530 | 0.4730 | 0.3367 (2.4e-54) | 2.0214 | 17.3 |
| **7-Changepoint** | MLP | 0.4479 | 0.3269 | 0.4383 | 0.2802 (1.7e-37) | 1.7721 | 13.0 |
| **7-Changepoint** | SVM | 0.4329 | 0.4039 | 0.4677 | 0.4355 (1.4e-93) | 1.3960 | 5.7 |
| **7-Changepoint** | Random Forest | 0.5067 | 0.3855 | 0.4942 | 0.4464 (8.4e-99) | 1.3830 | 2.9 |

#### 2. Regression (All Sampling Methods)
| Sampling Method | Model | Overall MSE | Pearson Correlation (PCC) | Discrete Accuracy | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 1.1274 | 0.4636 (4.3e-119) | 0.3947 | 21.8 |
| **Targeted** | MLP | 1.1367 | 0.4277 (9.7e-100) | 0.2964 | 11.5 |
| **Targeted** | SVM | 0.9009 | 0.5941 (1.3e-212) | 0.3947 | 3.0 |
| **Targeted** | Random Forest | 1.0032 | 0.5495 (6.2e-176) | 0.2299 | 115.8 |
| **BOCPD** | LSTM (Run 4) | 1.6752 | nan (nan) | 0.1105 | N/A (legacy run) |
| **BOCPD** | MLP | 1.1901 | 0.3787 (7.5e-77) | 0.2717 | N/A (legacy run) |
| **BOCPD** | SVM | 0.8668 | 0.6213 (5.4e-238) | 0.4158 | 4.3 |
| **BOCPD** | Random Forest | 1.0457 | 0.5066 (1.8e-145) | 0.2524 | 121.6 |
| **3-Changepoint** | LSTM | 1.0648 | 0.4981 (5.6e-140) | 0.3758 | 18.4 |
| **3-Changepoint** | MLP | 1.2528 | 0.3598 (4.7e-69) | 0.2079 | 10.9 |
| **3-Changepoint** | SVM | 0.8668 | 0.6213 (5.4e-238) | 0.4158 | 4.3 |
| **3-Changepoint** | Random Forest | 1.0457 | 0.5066 (1.8e-145) | 0.2524 | 121.6 |
| **5-Changepoint** | LSTM | 1.1001 | 0.4250 (9.4e-89) | 0.2788 | 15.3 |
| **5-Changepoint** | MLP | 1.2984 | 0.3095 (9.2e-46) | 0.2603 | 15.9 |
| **5-Changepoint** | SVM | 0.9153 | 0.5560 (4.3e-163) | 0.3810 | 3.5 |
| **5-Changepoint** | Random Forest | 1.0627 | 0.4450 (4.4e-98) | 0.2479 | 92.8 |
| **7-Changepoint** | LSTM | 1.1152 | 0.4068 (8.6e-81) | 0.3516 | 18.1 |
| **7-Changepoint** | MLP | 1.1870 | 0.3399 (2.0e-55) | 0.2893 | 10.7 |
| **7-Changepoint** | SVM | 0.9485 | 0.5351 (6.1e-149) | 0.3556 | 3.5 |
| **7-Changepoint** | Random Forest | 1.0509 | 0.4570 (5.1e-104) | 0.2559 | 92.3 |

#### 3. Binary Classification (Threshold = 1)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | PCC (p-value) | Overall MSE | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 0.8258 | 0.5704 | 0.7743 | 0.2392 | 0.9016 | 0.2738 (1.4e-39) | 0.1742 | 23.9 |
| **Targeted** | MLP | 0.8285 | 0.5604 | 0.7718 | 0.2172 | 0.9037 | 0.2919 (5.5e-45) | 0.1715 | 11.3 |
| **Targeted** | SVM | 0.8702 | 0.7609 | 0.8604 | 0.5992 | 0.9226 | 0.5384 (1.3e-167) | 0.1298 | 1.0 |
| **Targeted** | Random Forest | 0.8693 | 0.7496 | 0.8562 | 0.5764 | 0.9228 | 0.5269 (2.4e-159) | 0.1307 | 3.0 |
| **BOCPD** | LSTM (Run 8) | 0.8442 | 0.6525 | 0.8114 | 0.3944 | 0.9106 | 0.3932 (2.9e-83) | 0.1558 | N/A (legacy run) |
| **BOCPD** | MLP | 0.8159 | 0.5414 | 0.7598 | 0.1865 | 0.8962 | 0.2033 (3.3e-22) | 0.1841 | N/A (legacy run) |
| **BOCPD** | SVM | 0.8729 | 0.7535 | 0.8591 | 0.5820 | 0.9251 | 0.5394 (2.5e-168) | 0.1271 | 1.8 |
| **BOCPD** | Random Forest | 0.8568 | 0.7312 | 0.8443 | 0.5475 | 0.9149 | 0.4826 (2.6e-130) | 0.1432 | 4.0 |
| **3-Changepoint** | LSTM | 0.8357 | 0.5975 | 0.7881 | 0.2879 | 0.9071 | 0.3399 (2.3e-61) | 0.1643 | 12.5 |
| **3-Changepoint** | MLP | 0.8181 | 0.5210 | 0.7533 | 0.1438 | 0.8983 | 0.2053 (1.3e-22) | 0.1819 | 10.8 |
| **3-Changepoint** | SVM | 0.8729 | 0.7535 | 0.8591 | 0.5820 | 0.9251 | 0.5394 (2.5e-168) | 0.1271 | 1.8 |
| **3-Changepoint** | Random Forest | 0.8568 | 0.7312 | 0.8443 | 0.5475 | 0.9149 | 0.4826 (2.6e-130) | 0.1432 | 4.0 |
| **5-Changepoint** | LSTM | 0.8519 | 0.6246 | 0.8171 | 0.3326 | 0.9167 | 0.3390 (4.3e-55) | 0.1481 | 16.9 |
| **5-Changepoint** | MLP | 0.8234 | 0.5312 | 0.7751 | 0.1611 | 0.9013 | 0.1379 (5.6e-10) | 0.1766 | 11.7 |
| **5-Changepoint** | SVM | 0.8678 | 0.6978 | 0.8471 | 0.4711 | 0.9245 | 0.4460 (1.4e-98) | 0.1322 | 1.7 |
| **5-Changepoint** | Random Forest | 0.8618 | 0.6914 | 0.8425 | 0.4621 | 0.9207 | 0.4226 (1.1e-87) | 0.1382 | 2.4 |
| **7-Changepoint** | LSTM | 0.8539 | 0.6463 | 0.8248 | 0.3753 | 0.9173 | 0.3611 (8.2e-63) | 0.1461 | 19.1 |
| **7-Changepoint** | MLP | 0.8394 | 0.5427 | 0.7854 | 0.1744 | 0.9110 | 0.2239 (3.4e-24) | 0.1606 | 11.6 |
| **7-Changepoint** | SVM | 0.8743 | 0.7179 | 0.8563 | 0.5078 | 0.9280 | 0.4808 (1.7e-116) | 0.1257 | 1.1 |
| **7-Changepoint** | Random Forest | 0.8623 | 0.6990 | 0.8451 | 0.4773 | 0.9207 | 0.4309 (1.9e-91) | 0.1377 | 2.5 |

#### 4. Binary Classification (Threshold = 2)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | PCC (p-value) | Overall MSE | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 0.7566 | 0.6053 | 0.7017 | 0.3608 | 0.8497 | 0.3654 (2.6e-71) | 0.2434 | 13.8 |
| **Targeted** | MLP | 0.7458 | 0.5855 | 0.6873 | 0.3278 | 0.8433 | 0.3226 (4.3e-55) | 0.2542 | 9.6 |
| **Targeted** | SVM | 0.7899 | 0.7092 | 0.7696 | 0.5560 | 0.8624 | 0.4625 (2.0e-118) | 0.2101 | 1.8 |
| **Targeted** | Random Forest | 0.7625 | 0.7037 | 0.7558 | 0.5717 | 0.8357 | 0.4125 (3.1e-92) | 0.2375 | 3.1 |
| **BOCPD** | LSTM (Run 6) | 0.7234 | 0.5396 | 0.6544 | 0.2488 | 0.8305 | 0.2283 (1.0e-27) | 0.2766 | N/A (legacy run) |
| **BOCPD** | MLP | 0.7535 | 0.6082 | 0.7024 | 0.3697 | 0.8468 | 0.3490 (8.9e-65) | 0.2465 | N/A (legacy run) |
| **BOCPD** | SVM | 0.7777 | 0.7007 | 0.7606 | 0.5488 | 0.8525 | 0.4310 (1.9e-101) | 0.2223 | 3.7 |
| **BOCPD** | Random Forest | 0.7364 | 0.6775 | 0.7319 | 0.5396 | 0.8154 | 0.3570 (6.7e-68) | 0.2636 | 3.7 |
| **3-Changepoint** | LSTM | 0.7485 | 0.6068 | 0.7000 | 0.3708 | 0.8429 | 0.3290 (2.2e-57) | 0.2515 | 11.9 |
| **3-Changepoint** | MLP | 0.7378 | 0.5777 | 0.6803 | 0.3178 | 0.8377 | 0.2887 (5.2e-44) | 0.2622 | 11.5 |
| **3-Changepoint** | SVM | 0.7777 | 0.7007 | 0.7606 | 0.5488 | 0.8525 | 0.4310 (1.9e-101) | 0.2223 | 3.7 |
| **3-Changepoint** | Random Forest | 0.7364 | 0.6775 | 0.7319 | 0.5396 | 0.8154 | 0.3570 (6.6e-68) | 0.2636 | 3.7 |
| **5-Changepoint** | LSTM | 0.7421 | 0.6055 | 0.7022 | 0.3733 | 0.8377 | 0.2838 (1.8e-38) | 0.2579 | 14.5 |
| **5-Changepoint** | MLP | 0.7157 | 0.5599 | 0.6690 | 0.2980 | 0.8218 | 0.1896 (1.1e-17) | 0.2843 | 13.4 |
| **5-Changepoint** | SVM | 0.7741 | 0.6661 | 0.7452 | 0.4763 | 0.8560 | 0.3935 (3.1e-75) | 0.2259 | 1.7 |
| **5-Changepoint** | Random Forest | 0.7456 | 0.6556 | 0.7290 | 0.4796 | 0.8317 | 0.3303 (3.0e-52) | 0.2544 | 2.4 |
| **7-Changepoint** | LSTM | 0.7471 | 0.6225 | 0.7128 | 0.4056 | 0.8394 | 0.3057 (1.3e-44) | 0.2529 | 18.6 |
| **7-Changepoint** | MLP | 0.7212 | 0.5598 | 0.6708 | 0.2933 | 0.8263 | 0.2020 (6.7e-20) | 0.2788 | 10.7 |
| **7-Changepoint** | SVM | 0.7761 | 0.6718 | 0.7488 | 0.4869 | 0.8568 | 0.4005 (4.1e-78) | 0.2239 | 1.8 |
| **7-Changepoint** | Random Forest | 0.7576 | 0.6648 | 0.7383 | 0.4884 | 0.8412 | 0.3568 (2.8e-61) | 0.2424 | 2.5 |

#### 5. Binary Classification (Threshold = 3)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | PCC (p-value) | Overall MSE | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 0.6349 | 0.6295 | 0.6303 | 0.5846 | 0.6744 | 0.2727 (2.8e-39) | 0.3651 | 52.5 |
| **Targeted** | MLP | 0.6668 | 0.6655 | 0.6659 | 0.6443 | 0.6867 | 0.3337 (4.8e-59) | 0.3332 | 8.4 |
| **Targeted** | SVM | 0.6933 | 0.6921 | 0.6918 | 0.7112 | 0.6730 | 0.3933 (2.7e-83) | 0.3067 | 2.8 |
| **Targeted** | Random Forest | 0.6147 | 0.5926 | 0.5909 | 0.6875 | 0.4977 | 0.2725 (3.2e-39) | 0.3853 | 2.4 |
| **BOCPD** | LSTM (Run 10) | 0.6533 | 0.6487 | 0.6494 | 0.6081 | 0.6892 | 0.3099 (8.9e-51) | 0.3467 | N/A (legacy run) |
| **BOCPD** | MLP | 0.6960 | 0.6910 | 0.6918 | 0.6519 | 0.7302 | 0.3989 (7.8e-86) | 0.3040 | N/A (legacy run) |
| **BOCPD** | SVM | 0.6902 | 0.6879 | 0.6874 | 0.7146 | 0.6611 | 0.3910 (2.9e-82) | 0.3098 | 3.8 |
| **BOCPD** | Random Forest | 0.6098 | 0.5848 | 0.5830 | 0.6866 | 0.4830 | 0.2660 (2.3e-37) | 0.3902 | 2.7 |
| **3-Changepoint** | LSTM | 0.6843 | 0.6793 | 0.6800 | 0.6389 | 0.7196 | 0.3747 (3.5e-75) | 0.3157 | 13.8 |
| **3-Changepoint** | MLP | 0.6286 | 0.6160 | 0.6173 | 0.5464 | 0.6857 | 0.2674 (9.3e-38) | 0.3714 | 9.6 |
| **3-Changepoint** | SVM | 0.6902 | 0.6879 | 0.6874 | 0.7146 | 0.6611 | 0.3910 (2.9e-82) | 0.3098 | 3.8 |
| **3-Changepoint** | Random Forest | 0.6098 | 0.5848 | 0.5830 | 0.6866 | 0.4830 | 0.2660 (2.2e-37) | 0.3902 | 2.7 |
| **5-Changepoint** | LSTM | 0.6479 | 0.6466 | 0.6462 | 0.6679 | 0.6253 | 0.3015 (2.1e-43) | 0.3521 | 16.7 |
| **5-Changepoint** | MLP | 0.6474 | 0.6472 | 0.6470 | 0.6556 | 0.6387 | 0.2968 (4.6e-42) | 0.3526 | 13.8 |
| **5-Changepoint** | SVM | 0.6973 | 0.6966 | 0.6963 | 0.7111 | 0.6820 | 0.3995 (1.1e-77) | 0.3027 | 3.3 |
| **5-Changepoint** | Random Forest | 0.5910 | 0.5612 | 0.5589 | 0.6756 | 0.4467 | 0.2290 (2.8e-25) | 0.4090 | 2.2 |
| **7-Changepoint** | LSTM | 0.6454 | 0.6449 | 0.6452 | 0.6322 | 0.6577 | 0.2902 (3.3e-40) | 0.3546 | 14.7 |
| **7-Changepoint** | MLP | 0.6519 | 0.6514 | 0.6511 | 0.6644 | 0.6383 | 0.3070 (5.1e-45) | 0.3481 | 12.4 |
| **7-Changepoint** | SVM | 0.6898 | 0.6884 | 0.6880 | 0.7091 | 0.6677 | 0.3871 (1.1e-72) | 0.3102 | 2.8 |
| **7-Changepoint** | Random Forest | 0.5890 | 0.5610 | 0.5588 | 0.6720 | 0.4499 | 0.2213 (1.2e-23) | 0.4110 | 2.1 |

### Key Observations & Insights

*(Updated 2026-08-03 after re-running the full sweep with training-time instrumentation — see the 08-03 note above the comparison tables. LSTM/MLP figures below are from the latest run; SVM/RF figures are deterministic — same `random_state=42` on identical pooled features — so they are byte-for-byte unchanged from the 07-23 run.)*

- **The original LSTM collapse (Run 1/2) was a training-instability artifact, not a sequence-length limitation**: With the padding fix, `Targeted` LSTM multi-class accuracy jumped from 19.22% (constant-Class-0 collapse) to **49.12%** in this run (53.08% in the prior 07-23 re-run) — using the *same* 3-frame sequence length as before, with no fixed random seed. The ~4-point spread between re-runs is itself useful evidence: it confirms the collapse was a training-trajectory issue, not a hard architectural ceiling at 3 frames.
- **Sequence length (3 vs 5 vs 7 changepoints) has only a modest, non-monotonic effect once training is stable**: LSTM multi-class accuracy is 49.12% (3-CP), 51.02% (5-CP), 50.12% (7-CP) in this run — still no clean "more frames = better" trend, just reshuffled within the same narrow band as the 07-23 run (49.26% / 45.59% / 51.02%). Regression PCC shows the same flat, non-monotonic pattern (0.498 / 0.425 / 0.407 for 3/5/7-CP). Differences across changepoint counts remain within run-to-run training noise (no fixed random seed) — consistent across both re-runs.
- **`BOCPD` and `3-Changepoint` share identical underlying data**: `src/dataset.py` maps `sampling_method == 'bocpd'` to the same `3-changepoint-*.csv` files as `3-changepoint`. SVM/RF are deterministic given identical pooled features, so their BOCPD and 3-Changepoint rows (including training time) are numerically identical in every table above; only LSTM/MLP rows differ (from training stochasticity). Treat `BOCPD` as effectively a duplicate of `3-Changepoint` for traditional-model comparisons, not an independent sampling method.
- **Traditional models (SVM/RF) remain competitive or superior to LSTM/MLP across all sequence lengths**: SVM/RF accuracy stays in the same 43–54% band as LSTM/MLP for multi-class classification, and SVM has the best (lowest) regression MSE at every changepoint count (0.87–0.95 vs. 1.1–1.3 for LSTM/MLP). The previously reported "LSTM overtakes traditional models at longer sequences" trend did not reproduce.
- **Optimal Thresholds**: Binary classification accuracy still peaks around **Threshold 1** (up to **87.43%** for 7-Changepoint SVM), followed by Threshold 2 and 3, consistent across all sampling methods.

**New: Training time (added 2026-08-03).** See `fig4_training_time.png` above and the *Training Time (s)* column in every table (summed per model across all 5 tasks: multi-class, regression, and 3 binary thresholds).

- **SVM is dramatically cheaper to train than every other model, without sacrificing accuracy**: averaged **3.2s per run** (64s total across all 20 Targeted/3/5/7-CP runs) vs. **19.1s** for LSTM, **12.1s** for MLP, and **23.3s** for Random Forest. Combined with SVM's consistently top-tier accuracy (see above), it's the strongest model on *both* axes for this dataset — not just "competitive," but strictly more compute-efficient too.
- **Random Forest has the highest total training cost of the four models (465s across 20 runs), driven almost entirely by regression fits**: RF regression takes **93–122 seconds** per run (vs. 2–4s for its own classification configs, and 3–5s for SVM regression) because fitting 100 trees with `sample_weight` on continuous targets is far more expensive than classification with `class_weight='balanced'`. This is a real practical cost, not just an accuracy-vs-architecture tradeoff — RF is the worst choice by wall-clock time whenever the regression task is in scope.
- **LSTM training time doesn't track sequence length or epoch budget in any clean way**: the single slowest LSTM run (Targeted, Binary Threshold 3, 52.5s) used the same 20-epoch budget as several LSTM runs that finished in 12–19s — the spread comes from early-stopping patience (`patience=10`) triggering at different epochs depending on how validation loss happens to plateau, not from a fixed compute cost per config.
- **Total sweep cost by sampling method is roughly flat** (Targeted 329s, 3-CP 298s, 5-CP 263s, 7-CP 263s, summed across all 4 models × 5 tasks) — longer changepoint sequences do **not** noticeably increase training cost despite carrying more frames per sample, since the pooled/LSTM computation per epoch is dominated by the fixed 1518-dim feature width rather than the (very short, ≤7-frame) sequence length.

## SMOTE Ablation Comparison

> **Update (2026-08-05)**: Both the baseline and SMOTE sweeps were re-run end-to-end in the same session (back-to-back, same machine) specifically to produce a matched pair of runs for this comparison — the tables and deltas below are computed from that paired rerun (`artifacts/ablation_targeted_3_5_7_changepoint_results.txt` / `..._smote.txt`), not from the earlier 08-03 baseline numbers used elsewhere in this document. SVM/RF rows are deterministic (`random_state=42` on identical pooled features) and reproduce the 08-03 numbers exactly; LSTM/MLP rows differ run-to-run since no fixed seed is used. One qualitative finding did **not** reproduce: the previous rerun showed SMOTE giving the minority "Barely-engaged" class a clear F1 gain (+0.045) at the smaller cost of the "Not-Engaged" class (−0.013). In this rerun, **both** minority classes lose F1 under SMOTE (see the Delta Summary below) — treat the earlier "SMOTE selectively helps the least-weighted class" story as not reproduced, another instance of LSTM/MLP run-to-run noise swamping a headline finding, consistent with this project's other stochasticity caveats.

Adds `imblearn.SMOTE` oversampling of the minority engagement classes to the **training split only** (never validation/test), as an alternative/complement to the existing inverse-frequency class weighting. Implemented in `src/train.py` (LSTM/MLP — sequences are flattened to `(max_seq_len × feature_dim)` vectors, with each sample's valid length appended as an extra column so it interpolates consistently with SMOTE's synthetic samples, then reshaped back) and `src/train_traditional.py` (SVM/RF — applied directly to the scaled, pooled feature vectors). `k_neighbors` is auto-capped to `min(5, smallest_class_count - 1)`. Regression is skipped (SMOTE requires discrete labels) with a printed message rather than a silent no-op. Full sweep: `scripts/run_ablation_targeted_3_5_7_smote.py` (84 train+eval runs, same `Targeted`/`3`/`5`/`7`-Changepoint × LSTM/MLP/SVM/RF scope as the baseline sweep — `BOCPD` was not part of either automated sweep). Checkpoints get a `_smote` filename suffix so they don't overwrite the non-SMOTE baseline checkpoints, enabling direct comparison. Raw run log: `artifacts/ablation_targeted_3_5_7_changepoint_results_smote.txt`.

**Important caveat on the Multi-class table**: that config keeps class-weighted loss active (the sweep's `CONFIGS` only passes `--no_class_weights` for the binary-threshold configs, inherited unchanged from the baseline sweep), so its SMOTE numbers reflect **SMOTE + class-weighting combined**, not SMOTE in isolation. The three binary-threshold tables run with `--no_class_weights`, so they isolate the effect of SMOTE alone — treat those as the cleaner signal.

### Figures

![SMOTE vs. baseline: accuracy and macro F1 by task and model, averaged across all 4 sampling methods](artifacts/figures/fig7_smote_accuracy_comparison.png)

![SMOTE vs. baseline: training time by task and model, averaged across all 4 sampling methods](artifacts/figures/fig8_smote_training_time_comparison.png)

### Delta Summary (SMOTE − Baseline, averaged across 4 sampling methods × 4 models, 2026-08-05 paired rerun)

| Task | Δ Accuracy | Δ Macro F1 | Δ Training Time (s) |
| :--- | :--- | :--- | :--- |
| Multi-class (weighted loss + SMOTE) | −0.0150 | −0.0211 | +1.72 |
| Binary Threshold 1 (SMOTE only) | −0.0147 | +0.0142 | +1.13 |
| Binary Threshold 2 (SMOTE only) | −0.0235 | +0.0000 | +0.08 |
| Binary Threshold 3 (SMOTE only) | −0.0028 | −0.0037 | −0.73 |

**By model** (averaged across all 4 methods × 4 classification tasks):

| Model | Δ Accuracy | Δ Macro F1 | Δ Training Time (s) |
| :--- | :--- | :--- | :--- |
| LSTM | +0.0008 | +0.0108 | +0.04 |
| MLP | −0.0027 | −0.0102 | +0.30 |
| SVM | −0.0240 | −0.0059 | +2.10 |
| Random Forest | −0.0302 | −0.0052 | −0.23 |

**Multi-class minority-class F1** (the two smallest raw classes — this is where SMOTE should help most):

| Class | Δ F1 (SMOTE − Baseline) |
| :--- | :--- |
| Class 0 (Not-Engaged) | −0.0471 |
| Class 1 (Barely-engaged) | −0.0264 |

#### 1. Multi-class Classification (SMOTE, All Sampling Methods)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | PCC (p-value) | Overall MSE | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 0.5321 | 0.3541 | 0.4899 | 0.3962 (1.3e-84) | 1.6224 | 16.0 |
| **Targeted** | MLP | 0.5029 | 0.3442 | 0.4729 | 0.4057 (5.5e-89) | 1.5002 | 16.2 |
| **Targeted** | SVM | 0.4773 | 0.4210 | 0.5075 | 0.4780 (1.6e-127) | 1.4423 | 11.2 |
| **Targeted** | Random Forest | 0.4899 | 0.4269 | 0.5126 | 0.5395 (1.9e-168) | 1.2573 | 2.8 |
| **3-Changepoint** | LSTM | 0.4459 | 0.2947 | 0.4223 | 0.2268 (2.2e-27) | 2.2622 | 12.9 |
| **3-Changepoint** | MLP | 0.5128 | 0.3205 | 0.4654 | 0.3749 (3.0e-75) | 1.6610 | 13.8 |
| **3-Changepoint** | SVM | 0.4567 | 0.4095 | 0.4970 | 0.4699 (1.0e-122) | 1.4347 | 11.3 |
| **3-Changepoint** | Random Forest | 0.4315 | 0.3870 | 0.4646 | 0.4974 (1.6e-139) | 1.3211 | 2.8 |
| **5-Changepoint** | LSTM | 0.4733 | 0.3145 | 0.4435 | 0.2707 (5.3e-35) | 1.8449 | 10.5 |
| **5-Changepoint** | MLP | 0.4314 | 0.3030 | 0.4210 | 0.2915 (1.4e-40) | 1.5401 | 9.7 |
| **5-Changepoint** | SVM | 0.4274 | 0.3937 | 0.4638 | 0.4187 (6.0e-86) | 1.4135 | 9.4 |
| **5-Changepoint** | Random Forest | 0.4120 | 0.3686 | 0.4410 | 0.3982 (3.8e-77) | 1.4379 | 2.7 |
| **7-Changepoint** | LSTM | 0.5247 | 0.3172 | 0.4511 | 0.3106 (4.4e-46) | 2.0050 | 11.8 |
| **7-Changepoint** | MLP | 0.4868 | 0.3231 | 0.4566 | 0.2652 (1.3e-33) | 1.7197 | 12.8 |
| **7-Changepoint** | SVM | 0.4349 | 0.4002 | 0.4680 | 0.4360 (8.4e-94) | 1.4185 | 9.7 |
| **7-Changepoint** | Random Forest | 0.4444 | 0.3811 | 0.4664 | 0.4546 (8.0e-103) | 1.3611 | 2.8 |

#### 2. Binary Classification (SMOTE, Threshold = 1)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | PCC (p-value) | Overall MSE | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 0.8662 | 0.7223 | 0.8454 | 0.5224 | 0.9222 | 0.5041 (6.9e-144) | 0.1338 | 18.6 |
| **Targeted** | MLP | 0.8262 | 0.5587 | 0.7702 | 0.2150 | 0.9023 | 0.2742 (1.0e-39) | 0.1738 | 12.0 |
| **Targeted** | SVM | 0.8653 | 0.7838 | 0.8655 | 0.6512 | 0.9165 | 0.5677 (3.3e-190) | 0.1347 | 2.5 |
| **Targeted** | Random Forest | 0.8213 | 0.6907 | 0.8144 | 0.4897 | 0.8917 | 0.3853 (9.5e-80) | 0.1787 | 2.0 |
| **3-Changepoint** | LSTM | 0.8433 | 0.7193 | 0.8342 | 0.5328 | 0.9059 | 0.4479 (2.4e-110) | 0.1567 | 14.8 |
| **3-Changepoint** | MLP | 0.7916 | 0.5593 | 0.7563 | 0.2393 | 0.8793 | 0.1582 (6.0e-14) | 0.2084 | 8.4 |
| **3-Changepoint** | SVM | 0.8307 | 0.7373 | 0.8337 | 0.5806 | 0.8940 | 0.4758 (3.6e-126) | 0.1693 | 2.8 |
| **3-Changepoint** | Random Forest | 0.8312 | 0.7195 | 0.8285 | 0.5426 | 0.8965 | 0.4398 (5.1e-106) | 0.1688 | 4.0 |
| **5-Changepoint** | LSTM | 0.8574 | 0.6335 | 0.8222 | 0.3470 | 0.9199 | 0.3703 (3.4e-66) | 0.1426 | 12.9 |
| **5-Changepoint** | MLP | 0.8299 | 0.5673 | 0.7894 | 0.2302 | 0.9044 | 0.2047 (2.0e-20) | 0.1701 | 15.0 |
| **5-Changepoint** | SVM | 0.8334 | 0.7056 | 0.8334 | 0.5117 | 0.8996 | 0.4113 (1.1e-82) | 0.1666 | 2.5 |
| **5-Changepoint** | Random Forest | 0.8384 | 0.6716 | 0.8258 | 0.4375 | 0.9056 | 0.3555 (8.4e-61) | 0.1616 | 1.9 |
| **7-Changepoint** | LSTM | 0.8339 | 0.6620 | 0.8208 | 0.4209 | 0.9031 | 0.3362 (3.6e-54) | 0.1661 | 14.8 |
| **7-Changepoint** | MLP | 0.8040 | 0.5548 | 0.7743 | 0.2218 | 0.8879 | 0.1368 (7.7e-10) | 0.1960 | 15.0 |
| **7-Changepoint** | SVM | 0.8284 | 0.7030 | 0.8302 | 0.5100 | 0.8960 | 0.4063 (1.5e-80) | 0.1716 | 2.5 |
| **7-Changepoint** | Random Forest | 0.8439 | 0.6954 | 0.8355 | 0.4826 | 0.9081 | 0.3973 (8.9e-77) | 0.1561 | 2.1 |

#### 3. Binary Classification (SMOTE, Threshold = 2)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | PCC (p-value) | Overall MSE | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 0.7818 | 0.6783 | 0.7503 | 0.4959 | 0.8607 | 0.4392 (1.1e-105) | 0.2182 | 17.3 |
| **Targeted** | MLP | 0.7526 | 0.5962 | 0.6954 | 0.3448 | 0.8475 | 0.3505 (2.2e-65) | 0.2474 | 10.8 |
| **Targeted** | SVM | 0.7252 | 0.6797 | 0.7274 | 0.5591 | 0.8004 | 0.3600 (4.0e-69) | 0.2748 | 3.8 |
| **Targeted** | Random Forest | 0.6794 | 0.6430 | 0.6880 | 0.5290 | 0.7570 | 0.2946 (7.6e-46) | 0.3206 | 2.4 |
| **3-Changepoint** | LSTM | 0.7140 | 0.6018 | 0.6852 | 0.3904 | 0.8131 | 0.2406 (1.1e-30) | 0.2860 | 10.1 |
| **3-Changepoint** | MLP | 0.7441 | 0.6187 | 0.7050 | 0.4000 | 0.8373 | 0.3158 (9.1e-53) | 0.2559 | 10.3 |
| **3-Changepoint** | SVM | 0.7351 | 0.6979 | 0.7397 | 0.5920 | 0.8039 | 0.3992 (5.9e-86) | 0.2649 | 3.5 |
| **3-Changepoint** | Random Forest | 0.7306 | 0.6858 | 0.7326 | 0.5671 | 0.8044 | 0.3720 (4.7e-74) | 0.2694 | 1.9 |
| **5-Changepoint** | LSTM | 0.7406 | 0.6434 | 0.7210 | 0.4572 | 0.8296 | 0.3106 (4.2e-46) | 0.2594 | 8.0 |
| **5-Changepoint** | MLP | 0.7012 | 0.5753 | 0.6716 | 0.3439 | 0.8066 | 0.1818 (2.3e-16) | 0.2988 | 8.9 |
| **5-Changepoint** | SVM | 0.7282 | 0.6733 | 0.7290 | 0.5393 | 0.8072 | 0.3466 (1.1e-57) | 0.2718 | 3.2 |
| **5-Changepoint** | Random Forest | 0.7387 | 0.6775 | 0.7360 | 0.5371 | 0.8179 | 0.3557 (7.2e-61) | 0.2613 | 1.7 |
| **7-Changepoint** | LSTM | 0.7357 | 0.5790 | 0.6860 | 0.3223 | 0.8358 | 0.2526 (1.5e-30) | 0.2643 | 14.6 |
| **7-Changepoint** | MLP | 0.7122 | 0.5330 | 0.6535 | 0.2438 | 0.8223 | 0.1584 (9.8e-13) | 0.2878 | 10.8 |
| **7-Changepoint** | SVM | 0.7072 | 0.6495 | 0.7087 | 0.5071 | 0.7918 | 0.2991 (1.0e-42) | 0.2928 | 3.2 |
| **7-Changepoint** | Random Forest | 0.7362 | 0.6681 | 0.7307 | 0.5178 | 0.8184 | 0.3387 (5.3e-55) | 0.2638 | 1.8 |

#### 4. Binary Classification (SMOTE, Threshold = 3)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | PCC (p-value) | Overall MSE | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 0.6466 | 0.6401 | 0.6410 | 0.5916 | 0.6886 | 0.2982 (5.7e-47) | 0.3534 | 10.6 |
| **Targeted** | MLP | 0.6686 | 0.6639 | 0.6647 | 0.6242 | 0.7036 | 0.3415 (6.2e-62) | 0.3314 | 9.7 |
| **Targeted** | SVM | 0.6924 | 0.6913 | 0.6909 | 0.7101 | 0.6724 | 0.3914 (2.1e-82) | 0.3076 | 2.2 |
| **Targeted** | Random Forest | 0.6017 | 0.5798 | 0.5781 | 0.6757 | 0.4840 | 0.2411 (8.2e-31) | 0.3983 | 1.5 |
| **3-Changepoint** | LSTM | 0.6538 | 0.6459 | 0.6469 | 0.5931 | 0.6987 | 0.3151 (1.6e-52) | 0.3462 | 10.1 |
| **3-Changepoint** | MLP | 0.6210 | 0.6018 | 0.6034 | 0.5144 | 0.6892 | 0.2583 (2.8e-35) | 0.3790 | 8.1 |
| **3-Changepoint** | SVM | 0.6888 | 0.6865 | 0.6860 | 0.7135 | 0.6595 | 0.3884 (4.5e-81) | 0.3112 | 2.1 |
| **3-Changepoint** | Random Forest | 0.6390 | 0.6205 | 0.6190 | 0.7042 | 0.5369 | 0.3225 (4.6e-55) | 0.3610 | 1.4 |
| **5-Changepoint** | LSTM | 0.6324 | 0.6302 | 0.6307 | 0.6014 | 0.6590 | 0.2647 (1.7e-33) | 0.3676 | 7.4 |
| **5-Changepoint** | MLP | 0.6449 | 0.6418 | 0.6412 | 0.6749 | 0.6088 | 0.3001 (5.3e-43) | 0.3551 | 8.7 |
| **5-Changepoint** | SVM | 0.6943 | 0.6936 | 0.6933 | 0.7077 | 0.6796 | 0.3932 (4.0e-75) | 0.3057 | 2.4 |
| **5-Changepoint** | Random Forest | 0.5955 | 0.5671 | 0.5649 | 0.6780 | 0.4561 | 0.2379 (3.4e-27) | 0.4045 | 1.4 |
| **7-Changepoint** | LSTM | 0.6479 | 0.6426 | 0.6435 | 0.5993 | 0.6859 | 0.2990 (1.1e-42) | 0.3521 | 12.0 |
| **7-Changepoint** | MLP | 0.6499 | 0.6499 | 0.6499 | 0.6472 | 0.6525 | 0.2999 (6.0e-43) | 0.3501 | 9.6 |
| **7-Changepoint** | SVM | 0.6873 | 0.6860 | 0.6856 | 0.7063 | 0.6656 | 0.3818 (1.4e-70) | 0.3127 | 2.1 |
| **7-Changepoint** | Random Forest | 0.6090 | 0.5855 | 0.5836 | 0.6841 | 0.4869 | 0.2620 (7.8e-33) | 0.3910 | 1.4 |

### Key Observations & Insights

*(Numbers below reflect the 2026-08-05 paired rerun; see the update note above the Delta Summary tables for what changed from the prior pass.)*

- **SMOTE does not clearly improve this task — mostly a small accuracy-for-balance trade, and it's a losing trade for SVM/RF specifically.** Averaged across all 4 sampling methods, accuracy moves in the **negative** direction for every task (−0.3 to −2.4 points), while macro F1 is roughly a wash and noisier in sign (+0.014 on Threshold 1, ≈0.000 on Threshold 2, −0.004 on Threshold 3, −0.021 on multi-class). This is not the clean "oversampling fixes imbalance" story — on this dataset/feature setup, the existing class-weighted loss (already in place for the multi-class config) was already doing most of the useful work.
- **SVM and Random Forest lose the most accuracy from SMOTE** (−0.024 and −0.030 average, respectively — identical to the prior pass, since both are deterministic given `random_state=42`), and both were the two best-performing, cheapest-to-train models in the non-SMOTE ablation — so SMOTE actively erodes SVM's and RF's edge rather than extending it. LSTM and MLP are roughly accuracy-neutral (+0.001 and −0.003) but their macro F1 deltas diverge (LSTM +0.011, MLP −0.010) — small enough to be within run-to-run noise for both.
- **The "SMOTE selectively helps the under-weighted minority class" story from the prior pass did not reproduce.** In that earlier rerun, multi-class Class 1 ("Barely-engaged," the smallest raw class and the only one with no extra loss-weight boost) gained F1 from SMOTE while Class 0 ("Not-Engaged," which already gets a 2× loss-weight multiplier) lost a little. In this paired rerun, **both classes lose F1 under SMOTE** (Class 0: −0.047, Class 1: −0.026) — a genuine sign flip on Class 1, not just a magnitude shift. Since LSTM/MLP have no fixed seed, this class-level breakdown (computed from just 4 sampling methods × 4 models = 16 paired runs) is evidently too noisy to support a directional claim about which class SMOTE helps; the only conclusion that survives both passes is that SMOTE does **not** reliably help either minority class here.
- **Training-time cost is model-dependent, not uniform, and the LSTM/MLP deltas in particular should be read as noisy.** SVM again pays the largest average time penalty (+2.10s/run, fit cost scales with training-set size and SMOTE inflates it); MLP sees a small increase (+0.30s); Random Forest is essentially flat and, in this pass, slightly *faster* on average (−0.23s); LSTM is close to flat (+0.04s, vs. −3.79s in the prior pass) — the LSTM swing between passes is consistent with early-stopping timing being sensitive to run-to-run training trajectory rather than a real SMOTE effect. The qualitative training-time ranking from the non-SMOTE sweep is unchanged either way (SVM still cheapest per-run in absolute terms, RF/LSTM/MLP still the more expensive tier for the classification tasks studied here).
- **Binary Threshold 3 barely moves** (Δaccuracy −0.003, Δmacro F1 −0.004) — consistent with the prior pass. This config was already close to naturally balanced (1093 vs. 1134 train-adjacent samples), so there was very little class imbalance left for SMOTE to correct, and the numbers confirm it across both reruns: SMOTE has essentially nothing to do here.
- **Bottom line for this dataset**: the existing class-weighted loss (or `class_weight='balanced'` for SVM/RF) is doing the imbalance-handling job at least as well as SMOTE, at no training-time advantage for SMOTE. The SVM/RF accuracy cost is the one finding that reproduces cleanly across both passes (expected, since those models are deterministic); the LSTM/MLP and per-class findings are noisy enough between runs that they should not be treated as settled without a multi-seed rerun (see Limitations). SMOTE remains available as a flag (`--use_smote` on `train.py` / `train_traditional.py`) for future experimentation but is not recommended as the default.

## Random Forest Feature Importance Analysis

Since Random Forest is consistently competitive with (and sometimes beats) the LSTM despite discarding all temporal ordering — see above — it's worth inspecting *which* pooled input features it actually splits on. `src/train_traditional.py` does not persist the fitted sklearn model to disk, so `scripts/analyze_rf_feature_importance.py` retrains a Random Forest with identical hyperparameters (`n_estimators=100`, `random_state=42`, same `StandardScaler` + temporal-average-pooling pipeline) for a given config, then reports `feature_importances_` and renders one example tree.

Config used below: **Targeted sampling, binary classification, Threshold 3** (`{0,1,2}` vs `{3}`, unweighted — matching the Threshold 3 ablation row above).

![Random Forest feature importance, top 25 features (Targeted, Threshold 3)](artifacts/figures/fig5_rf_feature_importance_targeted_classification_thresh3.png)

**Top 15 features by Gini importance:**

| Rank | Feature | Importance |
|---|---|---|
| 1 | `AU_browOuterUpRight` | 0.0100 |
| 2 | `AU_cheekSquintLeft` | 0.0100 |
| 3 | `MP_LEFT_WRIST_v` | 0.0081 |
| 4 | `AU_browInnerUp` | 0.0071 |
| 5 | `AU_browDownRight` | 0.0058 |
| 6 | `AU_mouthUpperUpRight` | 0.0057 |
| 7 | `AU_mouthSmileRight` | 0.0050 |
| 8 | `MP_RIGHT_WRIST_y` | 0.0049 |
| 9 | `FLM_x_136` | 0.0048 |
| 10 | `FLM_x_138` | 0.0043 |
| 11 | `AU_mouthUpperUpLeft` | 0.0042 |
| 12 | `MP_LEFT_SHOULDER_v` | 0.0041 |
| 13 | `AU_mouthSmileLeft` | 0.0041 |
| 14 | `FLM_z_82` | 0.0039 |
| 15 | `AU_eyeWideRight` | 0.0037 |

**Observations:**
- **Facial Action Units (AUs) dominate over raw pose/landmark coordinates.** 10 of the top 15 features are `AU_*` (eyebrow, cheek, mouth, eye), vs. only 4 raw facial-landmark (`FLM_*`) coordinates and 3 MediaPipe pose features (`MP_*`) in the top 15. For distinguishing "Highly-Engaged" from everything else, **eyebrow movement** (`browOuterUpRight`, `browInnerUp`, `browDownRight`) and **mouth/smile activity** (`mouthUpperUp*`, `mouthSmile*`) carry the most signal — not gross body pose.
- **Wrist visibility/position sneaks into the top 10** (`MP_LEFT_WRIST_v`, `MP_RIGHT_WRIST_y`) — plausibly a proxy for hand-raising or note-taking behavior correlating with high engagement.
- No single feature dominates: the top importance is only 0.0100 out of 1517 total pooled features, so the RF's decisions are spread thin across many weakly-informative facial/pose signals rather than relying on one strong predictor.

![Example tree from the Random Forest — tree #0 of 100, display truncated to depth 3 (Targeted, Threshold 3)](artifacts/figures/fig6_rf_example_tree_targeted_classification_thresh3.png)

**Caveats on the tree figure:**
- The forest has **100 unpruned trees** (`max_depth=None`); a fully rendered tree would be thousands of nodes, so this shows only the first 3 levels of one representative tree (`estimators_[0]`), truncated for legibility — not the full decision logic.
- This single tree's top splits (`FLM_z_317`, `FLM_y_216`, `FLM_x_223` — raw landmark coordinates) don't match the *forest-wide* importance ranking above (which is AU-dominated). That's expected: importance is averaged across all 100 bootstrap-sampled trees, while any one tree's early splits reflect whatever separated its particular bootstrap sample best. Don't read this one tree as "the model's logic" — use the feature-importance chart for that.

Regenerate for another sampling method / task / threshold with:
```bash
conda run -n thesis-engagenet python scripts/analyze_rf_feature_importance.py \
  --sampling_method <targeted|bocpd|3-changepoint|5-changepoint|7-changepoint> \
  --mode <classification|regression> --binarize_threshold <1|2|3>
```





