# Pre-registration — Explanation Shift Under Leakage-Controlled Evaluation

**Project:** ML + Explainable AI Network Intrusion Detection System  
**Working title:** Same Data, Different Conclusions: Measuring Explanation Shift Under Leakage-Controlled Evaluation of Flow-Based Intrusion Detection

**Pre-registration date:** 2026-09-20

---

## 1. Research Question

Do the features a model relies on change when leakage controls are applied, and does explanation divergence expose shortcut reliance that performance metrics do not?

---

## 2. Hypotheses

### H1

SHAP feature-ranking divergence between different evaluation configurations exceeds the within-configuration noise floor.

### H2

SHAP feature-ranking divergence can remain substantial between configurations whose performance, measured by macro-F1, is statistically tied.

### Falsification condition

The hypotheses will not be supported if cross-configuration SHAP rank-correlation distributions cannot be distinguished from the within-configuration variation observed under repeated runs of the same configuration.

---

## 3. Dataset

The primary dataset is the CIC-IDS2017 MachineLearningCSV dataset.

The dataset contains approximately 2.83 million network-flow records and 78 candidate features.

The raw CSV files are stored under:

`data/raw/`

Raw data will not be modified.

Processed versions will be created separately under:

`data/processed/`

---

## 4. Primary Task

The primary classification task is binary:

- BENIGN
- ATTACK

The secondary task will use seven coarse attack families.

Extremely rare classes such as Heartbleed, SQL Injection, and Infiltration will be excluded from the secondary task because their sample counts are too small for reliable evaluation. The exact exclusion and resulting class definitions will be documented before the secondary experiments.

---

## 5. Experimental Factors

The primary experiment uses four binary factors:

### Factor A — Exact duplicate rows

- Kept
- Removed before splitting

### Factor B — Destination Port

- Included
- Dropped

### Factor C — Split protocol

- Random stratified split
- Group-by-five-tuple split

### Factor D — Imbalance handling

- Class weights
- SMOTE applied inside the training pipeline

These factors produce:

2 × 2 × 2 × 2 = 16 configurations.

---

## 6. Models

Six models are planned:

1. Stratified dummy classifier
2. Logistic Regression
3. Decision Tree (maximum depth ≤ 6)
4. Random Forest
5. XGBoost
6. MLP

Random Forest and XGBoost will carry the main factorial experiment.

The other models will be evaluated at selected corner configurations.

---

## 7. Primary Measurements

Each experimental run will record:

- Macro-F1
- PR-AUC
- FPR at TPR = 0.95
- Confusion matrix
- Mean absolute SHAP feature importance
- SHAP feature ranking
- Training time
- Inference time

All headline results will be reported across multiple random seeds rather than from a single run.

---

## 8. SHAP Noise Floor

Before comparing different experimental configurations, SHAP ranking variability will be measured within a fixed reference configuration.

Three sources of variation will be investigated:

1. Training seed
2. SHAP background sample
3. Explanation sample

For each source of variation, pairwise ranking similarity will be measured using:

- Spearman rank correlation
- Kendall rank correlation
- Top-10 Jaccard overlap

The within-configuration variation will provide the baseline against which cross-configuration explanation changes are evaluated.

---

## 9. Cross-Configuration Analysis

For each relevant pair of configurations, SHAP feature rankings will be compared.

The primary comparison will be between the distribution of within-configuration ranking similarity and the distribution of cross-configuration ranking similarity.

A permutation-based statistical test will be used to evaluate whether observed differences are greater than expected under the null hypothesis.

---

## 10. Artefact Criterion

A feature may be classified as potentially artefact-driven only if all predefined criteria are satisfied.

The criteria will include:

1. A sufficiently large change in SHAP ranking after leakage controls are applied.
2. A sufficiently small performance cost when the feature is removed under the controlled protocol.
3. No documented attack mechanism providing a plausible reason for the feature's importance.

The numerical thresholds will be determined after the noise-floor experiment and then fixed before the main analysis.

They will not be changed based on the final results.

---

## 11. Leakage Controls

The following rules will be enforced:

- Duplicate handling occurs before the relevant split.
- Preprocessing is fitted only on training data.
- Resampling occurs only inside the training pipeline.
- Feature selection is performed without access to the test set.
- The test set is not used for hyperparameter tuning.
- SHAP background data comes from training data.
- IP addresses, timestamps, and flow identifiers are not used as model features.
- Group overlap between training and test data is explicitly measured.
- No seed will be selected because it produces a favorable result.
- Configurations will not be removed because their results are unfavorable.

---

## 12. Reproducibility

Every experimental result will record:

- configuration
- model
- random seed
- dataset version
- preprocessing decisions
- relevant hyperparameters
- evaluation protocol

Results will be stored in machine-readable files under:

`results/`

The repository will contain the code necessary to reproduce the reported experiments.

---

## 13. Reporting Negative Results

Results will be reported regardless of whether they support the hypotheses.

In particular:

- H1 may be unsupported.
- H2 may be unsupported.
- SHAP rankings may prove too unstable to detect protocol-level differences.
- Some leakage controls may have little effect.
- Some configurations may perform substantially worse.

Such results will not be removed from the study merely because they do not support the hypotheses.

---

## 14. Planned Experimental Stages

### Noise-floor experiment

10 repeated runs of a fixed reference configuration.

### Exploratory experiment

16 configurations × 2 main models × 3 seeds using a 500k-row subsample.

### Main experiment

Selected configurations × multiple seeds using the full dataset.

### Feature-transfer experiment

Features selected under a conventional evaluation protocol will be evaluated under the controlled protocol and compared with features selected natively under the controlled protocol.

---

## 15. Scope

The primary study will remain focused on:

- CIC-IDS2017
- flow-based intrusion detection
- leakage/evaluation protocols
- ML models
- SHAP explanations

Additional datasets, additional model families, and additional explanation methods will not be added unless explicitly justified and documented as future work or an approved scope change.

---

## 16. Changes to the Pre-registration

Any substantive change to the experimental design after this document is committed will be documented with:

- date
- reason for change
- original decision
- new decision
- potential effect on the study

The original committed version will not be silently rewritten.

---

## 17. Status

This document describes the planned methodology before the main experimental results are collected.

Supervisor approval is pending.