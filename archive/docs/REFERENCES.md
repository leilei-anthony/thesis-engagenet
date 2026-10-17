# Methodology and References - Student Engagement Prediction

This document provides a summary of the methodology, literature, and sampling techniques analyzed in this thesis project.

## 1. EngageNet Dataset
EngageNet is a dataset containing video recordings of students during online learning activities, annotated for engagement level on a 4-point scale:
- **0: Completely Disengaged** (represented as `Not-Engaged` in raw logs)
- **1: Barely Engaged** (represented as `Barely-engaged` in raw logs)
- **2: Engaged** (represented as `Engaged` in raw logs)
- **3: Highly Engaged** (represented as `Highly-Engaged` in raw logs)

## 2. Temporal Sampling Methods
To extract representative temporal frames for deep learning training (LSTM), two distinct sampling techniques are analyzed:

### Method A (Baseline): Targeted Sampling
- Focuses on Subject Matter Expert (SME) selected frames or valid frames where facial/behavioral features are successfully detected.
- Sequence lengths can vary dynamically based on the number of valid frames.

### Method B (Proposed): Bayesian Online Changepoint Detection (BOCPD)
- An online Bayesian algorithm that identifies points in time where the underlying generative process of the sequence changes.
- Exactly 3 changepoint frames are selected per sequence, yielding fixed-length input sequences ($L = 3$) for the LSTM network.

## 3. Evaluation Metrics in Affective Computing
To measure performance in predicting engagement, we employ metrics standard in affective computing literature:
- **Overall Mean Squared Error (MSE)**: Measures overall prediction error.
- **Class-wise Mean Squared Error (MSE)**: Shows error separately for each of the 4 classes to evaluate performance on the minority class.
- **Pearson's Correlation Coefficient (PCC)**: Computes the linear correlation between true and predicted levels (ranging from -1 to 1).
- **Confusion Matrix**: Visualizes misclassifications, particularly checking if errors occur between adjacent engagement levels.
