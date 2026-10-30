# Lab Notebook — ML + Explainable AI Network Intrusion Detection System

## 2026-09-16 — Dataset acquisition

### Objective
Download and verify the CIC-IDS2017 MachineLearningCSV dataset for the bachelor thesis.

### Dataset
CIC-IDS2017 — MachineLearningCSV

Source:
University of New Brunswick / Canadian Institute for Cybersecurity

### Files downloaded

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv | 77123859 | 6FF1580F5F81C0AE28A26F7631721018577F5F7C5E0FEAC28B795FCFE7B411EE |
| Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv | 76906168 | CA1824C51BFBB7B3C72290A11BE04366BA8815878C6A1CC5C44CB1CEE269E99B |
| Friday-WorkingHours-Morning.pcap_ISCX.csv | 58316725 | 53A41C24D570EA83B7AC55B2E94DF94E7A8216AEB80A2AF0246B6BC8BB543000 |
| Monday-WorkingHours.pcap_ISCX.csv | 176927918 | 852C4BEB34EDA186F32561FA79DF7A0747E92E1A6535B01270820DD9FFE17F34 |
| Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv | 83102436 | 6BCDA3857C2504676034E3EA57762D38393CC734CB377A726BD5CB153961B1B5 |
| Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv | 52023263 | D67066211FB1689C78406F1506F4C44704ECB92088353D5C96D96D6474EB819D |
| Tuesday-WorkingHours.pcap_ISCX.csv | 135078995 | 52B8692AE8C7D2ED04671FE2B98335693C0A92C7AB157D8C8B534D6523080851 |
| Wednesday-workingHours.pcap_ISCX.csv | 225166395 | 893C27DC968BF7A8ADEF1689F90BE55CA4A4DC3088FB63D6FF247AC56856DF2A |

### Verification
SHA-256 checksums were calculated for all eight CSV files using PowerShell.

### Notes
The raw dataset files are stored under `data/raw/` and are excluded from Git using `.gitignore`.

The raw PCAP files were not downloaded at this stage.

### Next step
Inspect the structure and contents of the eight CSV files without modifying the raw data.

## 2026-09-19 — Dataset structure and class distribution

### Objective
Inspect the structure and label distribution of the eight CIC-IDS2017 MachineLearningCSV files without modifying the raw data.

### Dataset structure

The eight CSV files contain a total of **2,830,743 flow records**.

The inspected files contain **79 columns**:
- 78 traffic-related features
- 1 target column: `Label`

The features describe characteristics of network flows, including:
- flow duration
- forward and backward packet counts
- byte counts
- packet sizes
- packet timing / inter-arrival times
- TCP flag counts
- packet and byte rates

### Class distribution

| Label | Number of samples |
|---|---:|
| BENIGN | 2,273,097 |
| DoS Hulk | 231,073 |
| PortScan | 158,930 |
| DDoS | 128,027 |
| DoS GoldenEye | 10,293 |
| FTP-Patator | 7,938 |
| SSH-Patator | 5,897 |
| DoS slowloris | 5,796 |
| DoS Slowhttptest | 5,499 |
| Bot | 1,966 |
| Web Attack – Brute Force | 1,507 |
| Web Attack – XSS | 652 |
| Infiltration | 36 |
| Web Attack – SQL Injection | 21 |
| Heartbleed | 11 |

### Observations

The dataset is highly imbalanced. `BENIGN` is by far the largest class, while several attack classes contain very few samples.

The smallest classes are:
- Heartbleed: 11 samples
- Web Attack – SQL Injection: 21 samples
- Infiltration: 36 samples

This class imbalance will need to be considered when designing the evaluation methodology. Accuracy alone will not be sufficient to evaluate the intrusion detection models.

The dataset is also organized by capture day and attack scenario. This structure may be relevant when designing train/test splits and investigating whether random splitting produces overly optimistic results.

### Data integrity

The raw CSV files were inspected without modifying them. Any future cleaning or preprocessing will be performed on derived/processed data rather than the original files.

### Next step
Continue dataset inspection by examining missing values, infinite values, and other data-quality issues before beginning preprocessing.

## 2026-10-02 — Raw data quality pass (P1)

- Row-level NaN/Inf check: 2,867 / 2,830,743 rows (0.10%) contain
  at least one NaN or Inf value across the 78 numeric features.
  Worst file: Wednesday-workingHours.pcap_ISCX.csv (1,297 rows).
  Breakdown by label confirmed all affected rows belong to BENIGN
  or large attack classes (DoS Hulk, PortScan, DDoS, Bot,
  FTP-Patator) -- none fall in Heartbleed, SQL Injection, or
  Infiltration.
  Decision: drop all 2,867 affected rows uniformly. No special
  handling needed for rare classes.

- Fwd Header Length.1: confirmed via .equals() to be an exact
  duplicate of Fwd Header Length in all 8 files.
  Decision: drop Fwd Header Length.1.

- Zero-variance check (per file): 8 columns are constant in every
  one of the 8 files -- Bwd PSH Flags, Bwd URG Flags,
  Fwd Avg Bytes/Bulk, Fwd Avg Packets/Bulk, Fwd Avg Bulk Rate,
  Bwd Avg Bytes/Bulk, Bwd Avg Packets/Bulk, Bwd Avg Bulk Rate.
  Decision: drop these 8 (zero information for any classifier).
  Two further columns -- Fwd URG Flags and CWE Flag Count -- are
  constant in 7/8 files but NOT constant in
  Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv.
  Not dropping yet -- investigating whether this is a genuine
  Infiltration-specific signal or just noise (see next entry).

  - Fwd URG Flags / CWE Flag Count: cross-tab against Label in the
  Infiltration file shows all 315 rows with value 1 are BENIGN;
  all 36 Infiltration rows are 0 on both columns. The variation is
  not attack-related -- it's noise from that day's benign traffic.
  Decision: drop both columns.

Final column drop list (11 total): Fwd Header Length.1,
Bwd PSH Flags, Fwd URG Flags, Bwd URG Flags, CWE Flag Count,
Fwd Avg Bytes/Bulk, Fwd Avg Packets/Bulk, Fwd Avg Bulk Rate,
Bwd Avg Bytes/Bulk, Bwd Avg Packets/Bulk, Bwd Avg Bulk Rate.