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




