# Leakage Self-Audit Checklist

Use this checklist for every final experimental configuration.

## Data handling

- [ ] Raw dataset files were not modified.
- [ ] Any duplicate removal was performed before the relevant data split.
- [ ] Cleaning decisions were applied consistently and documented.
- [ ] Test data was not used to make preprocessing decisions.

## Train / validation / test separation

- [ ] The test set was not used for model tuning.
- [ ] The test set was not used to select features.
- [ ] Scalers and other preprocessing steps were fitted using training data only.
- [ ] Any resampling was performed only on training data.
- [ ] Validation data was not used as training data.

## Grouping and leakage control

- [ ] The grouping key was constructed correctly.
- [ ] Train/test group overlap was explicitly measured.
- [ ] No group appears in both training and test sets when using the group split.
- [ ] Destination Port was excluded from the feature set when required by the grouping protocol.
- [ ] Source/destination IP addresses were not used as model features.
- [ ] Timestamps were not used as model features.
- [ ] Flow identifiers were not used as model features.

## Model selection

- [ ] No random seed was selected because it produced a favorable result.
- [ ] Hyperparameters were selected without using the final test set.
- [ ] Configurations were not removed because they produced unfavorable results.
- [ ] All planned configurations are reported or explicitly documented.

## SHAP / explanation analysis

- [ ] SHAP background data was drawn from training data only.
- [ ] The explanation sample was kept separate from the final test evaluation where appropriate.
- [ ] SHAP randomness was measured through the noise-floor experiment.
- [ ] Explanation differences were compared against the measured noise floor.
- [ ] Correlated features were considered when interpreting SHAP rankings.

## Reporting

- [ ] Random seeds are recorded.
- [ ] Configuration details are recorded.
- [ ] Dataset version is recorded.
- [ ] Preprocessing decisions are recorded.
- [ ] Negative results are included.
- [ ] No result was removed simply because it did not support the hypotheses.

## Final audit

- [ ] The complete experiment can be traced from its result back to its configuration and seed.
- [ ] The reported numbers match the stored experiment results.
- [ ] No manual changes were made to experimental results.