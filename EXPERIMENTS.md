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

#### 1. Multi-class Classification (Targeted vs BOCPD)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | PCC (p-value) | Overall MSE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM (Run 1) | 0.1922 | 0.0806 | 0.0620 | 0.0000 (1.0) | 5.4459 |
| | MLP | 0.4926 | 0.3820 | 0.4938 | 0.4315 ($1.12\times 10^{-101}$) | 1.4284 |
| | SVM | 0.4782 | **0.4329** | 0.5089 | 0.5014 ($3.96\times 10^{-142}$) | 1.3395 |
| | Random Forest | **0.5388** | 0.3961 | **0.5174** | **0.5101 ($8.46\times 10^{-148}$)** | **1.3507** |
| **BOCPD** | LSTM (Run 2) | 0.1922 | 0.0806 | 0.0620 | 0.0000 (1.0) | 5.4459 |
| | MLP | 0.4526 | 0.3289 | 0.4371 | 0.2075 ($4.44\times 10^{-23}$) | 2.4360 |
| | SVM | 0.4558 | **0.4112** | 0.4941 | 0.4911 ($1.59\times 10^{-135}$) | 1.3696 |
| | Random Forest | **0.5339** | 0.4152 | **0.5283** | **0.5263 ($6.06\times 10^{-159}$)** | **1.2591** |

#### 2. Regression (Targeted vs BOCPD)
| Sampling Method | Model | Overall MSE | Pearson Correlation (PCC) | Discrete Accuracy |
| :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM (Run 3) | 1.5598 | nan (nan) | 0.1881 |
| | MLP | 1.1337 | 0.4337 ($7.87\times 10^{-103}$) | 0.3282 |
| | SVM | **0.9009** | **0.5941 ($1.27\times 10^{-212}$)** | **0.3947** |
| | Random Forest | 1.0032 | 0.5495 ($6.24\times 10^{-176}$) | 0.2299 |
| **BOCPD** | LSTM (Run 4) | 1.6752 | nan (nan) | 0.1105 |
| | MLP | 1.1901 | 0.3787 ($7.52\times 10^{-77}$) | 0.2717 |
| | SVM | **0.8668** | **0.6213 ($5.38\times 10^{-238}$)** | **0.4158** |
| | Random Forest | 1.0457 | 0.5066 ($1.81\times 10^{-145}$) | 0.2524 |

#### 3. Binary Classification (Threshold = 1)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | PCC (p-value) | Overall MSE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM (Run 7) | 0.8473 | 0.6451 | 0.8100 | 0.3773 | 0.9130 | 0.4086 ($2.20\times 10^{-90}$) | 0.1527 |
| | MLP | 0.8258 | 0.5470 | 0.7658 | 0.1917 | 0.9024 | 0.2717 ($5.40\times 10^{-39}$) | 0.1742 |
| | SVM | **0.8702** | **0.7609** | **0.8604** | **0.5992** | **0.9226** | **0.5384 ($1.30\times 10^{-167}$)** | **0.1298** |
| | Random Forest | 0.8693 | 0.7496 | 0.8562 | 0.5764 | 0.9228 | 0.5269 ($2.36\times 10^{-159}$) | 0.1307 |
| **BOCPD** | LSTM (Run 8) | 0.8442 | 0.6525 | 0.8114 | 0.3944 | 0.9106 | 0.3932 ($2.94\times 10^{-83}$) | 0.1558 |
| | MLP | 0.8159 | 0.5414 | 0.7598 | 0.1865 | 0.8962 | 0.2033 ($3.27\times 10^{-22}$) | 0.1841 |
| | SVM | **0.8729** | **0.7535** | **0.8591** | **0.5820** | **0.9251** | **0.5394 ($2.52\times 10^{-168}$)** | **0.1271** |
| | Random Forest | 0.8568 | 0.7312 | 0.8443 | 0.5475 | 0.9149 | 0.4826 ($2.61\times 10^{-130}$) | 0.1432 |

#### 4. Binary Classification (Threshold = 2)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | PCC (p-value) | Overall MSE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM (Run 5) | 0.7490 | 0.5888 | 0.6901 | 0.3321 | 0.8455 | 0.3365 ($4.32\times 10^{-60}$) | 0.2510 |
| | MLP | 0.7414 | 0.5687 | 0.6764 | 0.2958 | 0.8416 | 0.3077 ($4.81\times 10^{-50}$) | 0.2586 |
| | SVM | **0.7899** | **0.7092** | **0.7696** | **0.5560** | **0.8624** | **0.4625 ($1.97\times 10^{-118}$)** | **0.2101** |
| | Random Forest | 0.7625 | 0.7037 | 0.7558 | 0.5717 | 0.8357 | 0.4125 ($3.06\times 10^{-92}$) | 0.2375 |
| **BOCPD** | LSTM (Run 6) | 0.7234 | 0.5396 | 0.6544 | 0.2488 | 0.8305 | 0.2283 ($1.01\times 10^{-27}$) | 0.2766 |
| | MLP | 0.7535 | 0.6082 | 0.7024 | 0.3697 | 0.8468 | 0.3490 ($8.89\times 10^{-65}$) | 0.2465 |
| | SVM | **0.7777** | **0.7007** | **0.7606** | **0.5488** | **0.8525** | **0.4310 ($1.94\times 10^{-101}$)** | **0.2223** |
| | Random Forest | 0.7364 | 0.6775 | 0.7319 | 0.5396 | 0.8154 | 0.3570 ($6.65\times 10^{-68}$) | 0.2636 |

#### 5. Binary Classification (Threshold = 3)
| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | PCC (p-value) | Overall MSE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM (Run 9) | 0.6533 | 0.6482 | 0.6490 | 0.6057 | 0.6907 | 0.3105 ($5.82\times 10^{-51}$) | 0.3467 |
| | MLP | 0.6071 | 0.5998 | 0.6008 | 0.5459 | 0.6537 | 0.2165 ($4.86\times 10^{-25}$) | 0.3929 |
| | SVM | **0.6933** | **0.6921** | **0.6918** | **0.7112** | **0.6730** | **0.3933 ($2.73\times 10^{-83}$)** | **0.3067** |
| | Random Forest | 0.6147 | 0.5926 | 0.5909 | 0.6875 | 0.4977 | 0.2725 ($3.16\times 10^{-39}$) | 0.3853 |
| **BOCPD** | LSTM (Run 10) | 0.6533 | 0.6487 | 0.6494 | 0.6081 | 0.6892 | 0.3099 ($8.94\times 10^{-51}$) | 0.3467 |
| | MLP | **0.6960** | **0.6910** | **0.6918** | 0.6519 | **0.7302** | **0.3989 ($7.76\times 10^{-86}$)** | **0.3040** |
| | SVM | 0.6902 | 0.6879 | 0.6874 | **0.7146** | 0.6611 | 0.3910 ($2.94\times 10^{-82}$) | 0.3098 |
| | Random Forest | 0.6098 | 0.5848 | 0.5830 | 0.6866 | 0.4830 | 0.2660 ($2.25\times 10^{-37}$) | 0.3902 |

### Key Observations & Insights

- **Baseline Superiority**: Traditional models (SVM and Random Forest) trained on average-pooled features significantly outperform deep learning sequence models (LSTM and MLP) on this task. 
- **LSTM Optimization Challenges**: In multi-class classification and regression, the LSTM struggled with model collapse (converging to constant predictions, leading to `nan` PCC). In contrast, SVM (PCC up to `0.6213` in regression) and Random Forest (accuracy up to `53.88%` in multi-class classification) handled the temporal segments robustly.
- **Why Traditional Models Perform Better**: Because the sequence length in the temporal subsets is extremely short (at most 3 frames), the sequence modeling capabilities of LSTM provide little advantage, while the high feature dimensionality (1518 dimensions) combined with standard scaling makes SVM with RBF kernels highly effective.
- **Targeted vs BOCPD**: The relative performance of Targeted Sampling vs BOCPD remains close across baseline models, with Targeted showing slight advantages in threshold 1 & 2 binary tasks, whereas BOCPD shows higher performance in threshold 3 tasks (especially with the MLP).





