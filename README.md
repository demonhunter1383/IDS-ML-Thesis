# ML + Explainable AI Network Intrusion Detection System

Bachelor thesis project at Khaje Nasir University of Technology (KNTU).

## Research Question

How much of the reported near-perfect performance of machine-learning-based intrusion detection systems on CIC-IDS2017 survives a leakage-free evaluation protocol, and what does SHAP reveal about whether the models learn attack behaviour or dataset artefacts?

## Objectives

- Build a reproducible machine-learning pipeline for network intrusion detection.
- Investigate data leakage and its effect on reported performance.
- Compare classical machine learning and deep learning approaches.
- Evaluate how well models generalize to an attack class not seen during training.
- Use SHAP to explain model predictions and investigate important features.
- Compare model explanations with documented characteristics of network attacks.

## Dataset

The primary dataset is **CIC-IDS2017**, provided by the Canadian Institute for Cybersecurity.

The dataset will be stored locally under:

`data/raw/`

Dataset files are excluded from Git using `.gitignore`.

## Planned Models

The project will investigate a model ladder including:

- Logistic Regression
- Random Forest
- Gradient Boosting
- Neural Network / Deep Learning model

The exact models may be refined during the research.

## Project Structure

```text
data/          Dataset files
notebooks/     Exploratory analysis and experiments
src/           Python source code
models/        Trained models
results/       Figures and tables
docs/          Thesis documentation
Environment

Python 3.11

Main libraries:

NumPy
Pandas
Scikit-learn
Matplotlib
Seaborn
JupyterLab

Install dependencies with:
python -m pip install -r requirements.txt
Reproducibility

The project uses a Python virtual environment and a pinned requirements.txt file to make the software environment reproducible.

Status

Phase: Project setup and research preparation

Planned duration: September 2026 – February 2027
