# Data Preparation Log

## Current status

P1 (research-dataset preparation) is in progress. The older preprocessing
run is complete, but the identified-flow version still needs its own
validated processing pipeline.

## Dataset versions

### Old processed dataset

- File: `data/processed/clean_flows.parquet`
- Shape: 2,827,876 rows x 68 columns.
- Exact duplicate rows reported by pandas: 329,896.
- These duplicate counts were calculated across all columns in the old
  processed file. They are not yet directly comparable to a count that
  includes the new identifiers.

### New identified-flow dataset

- Directory: `data/raw_identified_flows/`
- CSV files: 8.
- Header columns in first file: 85.
- Valid labeled rows across files: 2,830,743.
- The Thursday morning WebAttacks CSV contains 288,602 completely empty
  trailing rows. They are excluded from label counts; the raw file is
  kept unchanged.
- The other seven files had no completely empty rows in our check.
- The five-tuple fields, Flow ID, Timestamp, and Label were present and
  non-empty in all valid labeled rows during the earlier field audit.

## Label count comparison

The label names are normalized for comparison only: surrounding
whitespace and the observed misdecoded dash in web-attack labels are
standardized. Raw files are not changed.

                            New identified  Old processed  New minus old
BENIGN                             2273097        2271320           1777
DoS Hulk                            231073         230124            949
PortScan                            158930         158804            126
DDoS                                128027         128025              2
DoS GoldenEye                        10293          10293              0
FTP-Patator                           7938           7935              3
SSH-Patator                           5897           5897              0
DoS slowloris                         5796           5796              0
DoS Slowhttptest                      5499           5499              0
Bot                                   1966           1956             10
Web Attack - Brute Force              1507           1507              0
Web Attack - XSS                       652            652              0
Infiltration                            36             36              0
Web Attack - Sql Injection              21             21              0
Heartbleed                              11             11              0

The old processed dataset has fewer rows because the earlier cleaning
pipeline removed 2,867 rows with invalid numeric values. Matching label
counts by themselves does not establish row-by-row correspondence between
the two versions.

## Five-tuple diagnostic

The earlier diagnostic on the identified-flow data found:

- Valid rows: 2,830,743.
- Unique five-tuples: 1,457,288.
- Repeated five-tuple groups: 473,246.
- Rows belonging to repeated groups: 1,846,701.
- Five-tuples associated with multiple labels: 13,069.

A five-tuple can recur at different times and can have records with
different labels. It must not be assumed to uniquely identify one
network flow for all time. The grouping method requires a documented
definition and validation before it is used for final evaluation.

## Initial duplicate diagnostic

The old processed dataset reported 329,896 exact duplicate rows using
all 68 columns, including the label. This is an initial diagnostic, not
the final duplicate policy for the experiments.

For a fair comparison, duplicate handling must be defined on the
chosen model features and label, separately from identifier fields.
The experiment should preserve both duplicate-kept and duplicate-removed
conditions if both remain part of the research design.

## Decisions so far

1. Preserve all original raw CSV files.
2. Do not overwrite `clean_flows.parquet`.
3. Use the identified-flow version as the starting point for experiments
   that require network identifiers.
4. Keep identifiers for grouping and analysis; do not automatically
   feed them to the model as predictive features.
5. Record cleaning and label-normalization decisions.
6. Do not describe any split as completely leakage-free without evidence.

## Remaining P1 work

1. Complete the schema and label comparison.
2. Build a reproducible preprocessing pipeline for the identified-flow
   version and save a separate processed Parquet file.
3. Apply and record numeric cleaning, column-selection, and dtype rules.
4. Define and measure exact duplicates on the final model features and
   label, without using identifiers to define feature-row equality.
5. Validate the grouping strategy and split integrity.
6. Verify output shape, labels, missing values, and saved-file reload.

## Commit policy

Commit the audit documentation and relevant code/notebook changes as a
small milestone. Never commit the raw dataset files or large generated
Parquet files unless the repository policy explicitly calls for them.

## Current status

P1 (research-dataset preparation) is in progress.

The identified-flow preprocessing script is implemented at
`src/prepare_identified_flows.py`. It reads the eight source CSV files,
normalizes labels, removes rows with invalid numeric values, drops the
documented columns, downcasts numeric columns, and writes a separate
processed dataset.

The processed identified-flow dataset has been generated and reloaded
successfully. The data loader has also passed initial checks for feature
and label dimensions, missing values, and the destination-port option.

## Verified identified-flow processing output

- Processed file: `data/processed/identified_flows.parquet`
- Shape: 2,827,876 rows x 74 columns.
- Columns: 7 identifier columns, 1 label column, and 66 candidate
  numeric model features.
- Labels: 15.
- Missing values after preprocessing: 0.
- Exact duplicate rows across all saved columns: 199.
- Saved-file reload verification: passed.

The data loader returns `(X, y, groups)`. Its default configuration
returns 67 model features when Destination Port is included and 66
when it is excluded. In both cases, labels, group keys, and row counts
remain unchanged. The six other identifier columns are excluded from
the model features.

The grouping key is a five-tuple of source IP, source port, destination
IP, destination port, and protocol. This is a candidate grouping key,
not proof of leakage-free evaluation: tuples can recur at different
times and may be associated with different labels. Split integrity and
the grouping strategy still require dedicated validation.

## Remaining P1 work

1. Review the raw-to-processed schema and label comparisons for
   consistency.
2. Document and test the data loader's contract and failure cases.
3. Define exact duplicate handling on model features plus label,
   separately from identifier fields.
4. Validate the grouping strategy and measure train/test group overlap.
5. Build and test the planned evaluation pipelines, including
   preprocessing and resampling fitted only on training data.
6. Reconcile the README and lab notebook with the implemented pipeline.
7. Review all new and modified files before staging or committing.

## Row-count reconciliation (identified-flow CSVs)

Measured on 2026-10-30 with `scripts/count_row_removals.py` (read-only; per-file output saved in `results/row_removal_counts.txt`). Steps are applied in the same order as `src/prepare_identified_flows.py`.

| Stage | Rows removed | Rows left |
|---|---|---|
| Rows read from the 8 CSVs | - | 3,119,345 |
| Completely empty rows (all in Thursday-Morning-WebAttacks) | 288,602 | 2,830,743 |
| Missing or empty `Label` | 0 | 2,830,743 |
| Infinite or missing numeric feature values | 2,867 | 2,827,876 |

The plan's 2,830,743 flows is the count after the empty rows are removed. The final 2,827,876 rows match `data/processed/identified_flows.parquet`. The removals add up exactly, with no row counted twice.

## Canonical dataset

`data/processed/identified_flows.parquet` (2,827,876 rows, 74 columns, identifiers kept) is the official starting point for all experiments. `data/processed/clean_flows.parquet` (68 columns, no identifiers) is legacy and must not be used or overwritten.

The identifier columns (`Flow ID`, `Source IP`, `Source Port`, `Destination IP`, `Destination Port`, `Protocol`, `Timestamp`) are used only to build five-tuple groups and are never model features. The only code that still references the legacy file is the historical backup notebook `notebooks/backups/01_dataset_inspection_before_cleanup.ipynb`, which must not be run.