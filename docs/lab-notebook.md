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