# Project Progress Summary

This document summarizes the implemented work, current research status, generated outputs, and remaining tasks for the LLM-assisted IDS/SOC thesis project.

## Current State

The project is a working MVP for a master's thesis prototype. It demonstrates an end-to-end IDS/SOC research workflow:

1. Load IDS-style network-flow data.
2. Validate and profile benchmark datasets.
3. Preprocess UNSW-NB15-style CSV data.
4. Train baseline supervised ML models.
5. Evaluate models on a separate test split.
6. Export metrics, figures, and feature-importance artifacts.
7. Generate IDS alerts from sample events.
8. Explain alerts with local playbooks and RAG-style context.
9. Display the SOC workflow in a React dashboard.

The core thesis boundary is preserved: the IDS/ML layer performs detection and classification; the LLM/RAG layer explains alerts and supports analyst triage. The LLM is not treated as the detector or final decision-maker.

## Implemented Backend

The backend is a FastAPI application with APIs for sample events, alerts, explanations, datasets, metrics, and ML evaluation.

Implemented endpoints include:

- `GET /health`
- `GET /events`
- `GET /datasets`
- `GET /alerts`
- `GET /alerts/{alert_id}`
- `GET /alerts/{alert_id}/explanation`
- `GET /alerts/{alert_id}/explanation/comparison`
- `GET /metrics`
- `GET /ml/evaluate`
- `GET /ml/metrics`

Important backend services include:

- Dataset validation: checks raw IDS CSV files before running experiments.
- Dataset profiling: exports row count, column count, label distribution, attack-category distribution, imbalance ratios, missing values, and column lists.
- Dataset splitting: creates train/test splits with stratification when possible and records fallback strategy when needed.
- UNSW-NB15-style preprocessing: cleans missing/non-finite values, encodes categorical features, and writes processed CSV files for scikit-learn.
- Model training: trains Logistic Regression, Decision Tree, and Random Forest baselines.
- Metric export: writes accuracy, precision, recall, F1-score, false positive rate, sample count, and confusion matrix.
- Report export: writes model comparison CSV, confusion matrix SVGs, and tree-model feature importance CSVs.
- Alert intelligence: maps alerts to severity, confidence, top evidence features, triage priority, and MITRE ATT&CK-style techniques.
- LLM/RAG explanation: compares template, no-RAG, and RAG-assisted explanations using local markdown playbooks.
- LLM rubric evaluation: scores explanation correctness, completeness, groundedness, actionability, hallucination control, and latency.

## Implemented Frontend

The frontend is a React + Vite + TypeScript SOC dashboard.

Implemented dashboard capabilities include:

- Overview cards for SOC-level status.
- Alert table with severity and confidence.
- Triage priority display.
- MITRE ATT&CK-style technique display.
- Evidence feature display for alerts.
- LLM/RAG explanation panel.
- Explanation-mode comparison.
- Model metrics and comparison display.
- Backend fallback behavior for demo usage.

## Implemented Dataset Workflow

The dataset workflow now supports both generated splits and official benchmark splits.

Generated split mode:

```bash
backend/.venv/bin/python scripts/run_dataset_pipeline.py \
  --dataset-id fixture-pipeline \
  --input data/samples/unsw_nb15_fixture.csv \
  --output-dir reports/pipeline/fixture-pipeline \
  --models decision_tree \
  --test-size 0.33 \
  --random-state 42
```

Official train/test split mode:

```bash
backend/.venv/bin/python scripts/run_dataset_pipeline.py \
  --dataset-id unsw-nb15-official \
  --train-input data/raw/UNSW_NB15_training-set.csv \
  --test-input data/raw/UNSW_NB15_testing-set.csv \
  --output-dir reports/pipeline/unsw-nb15-official \
  --models logistic_regression,decision_tree,random_forest
```

Pipeline outputs include:

- `pipeline-summary.json`
- `pipeline-report.md`
- `reports/dataset-profile.json`
- `reports/dataset-split-summary.json`
- `processed/train.csv`
- `processed/test.csv`
- `metrics/*.json`
- `models/*.joblib`
- `reports/model-comparison.csv`
- `figures/*-confusion-matrix.svg`
- `reports/feature-importance/*-feature-importance.csv`

## UNSW-NB15 Work Completed

UNSW-NB15 was downloaded from a public Hugging Face mirror and stored locally under `data/raw/`.

Local raw files:

- `data/raw/UNSW_NB15_training-set.csv`
- `data/raw/UNSW_NB15_testing-set.csv`

Validation results:

- Training split: `175,341` rows, `45` columns, valid required columns.
- Testing split: `82,332` rows, `45` columns, valid required columns.
- Required columns: `label`, `attack_cat`.

Generated local outputs:

- `reports/evaluation/unsw-nb15-training-validation.json`
- `reports/evaluation/unsw-nb15-testing-validation.json`
- `reports/evaluation/unsw-nb15-training-profile.json`
- `reports/evaluation/unsw-nb15-testing-profile.json`
- `data/processed/unsw_nb15_train_processed.csv`
- `data/processed/unsw_nb15_test_processed.csv`
- `reports/evaluation/unsw-nb15/model-comparison.csv`
- `reports/evaluation/unsw-nb15/metrics/*.json`
- `reports/evaluation/unsw-nb15/figures/*.svg`
- `reports/evaluation/unsw-nb15/feature-importance/*.csv`

Generated raw data, processed data, trained models, and reports are intentionally ignored by git unless a small artifact is explicitly selected for sharing.

## Data Leakage Fix

A major research-quality issue was found and fixed.

Issue:

- The original preprocessing encoded `attack_cat` as one-hot features.
- Since `attack_cat` is an attack-family label, using it as a feature to predict binary `label` leaked ground-truth information into the model.
- This produced misleading perfect or near-perfect metrics.

Fix:

- `attack_cat` is now used only for dataset summary/reporting.
- `attack_cat` is dropped before feature encoding and model training.
- A regression test verifies that processed features do not include `attack_cat_*` columns.

This correction makes benchmark results more defensible for thesis evaluation.

## Current UNSW-NB15 Baseline Results

After removing attack-category leakage, current official split results are:

| Model | Accuracy | Precision | Recall | F1-score | False Positive Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Decision Tree | 0.5241 | 0.6042 | 0.3932 | 0.4764 | 0.3156 |
| Logistic Regression | 0.6159 | 0.6313 | 0.7268 | 0.6757 | 0.5201 |
| Logistic Regression + Scaling | 0.7326 | 0.7416 | 0.7894 | 0.7647 | 0.3371 |
| Random Forest | 0.5741 | 0.6626 | 0.4614 | 0.5440 | 0.2879 |
| XGBoost | 0.5294 | 0.5975 | 0.4453 | 0.5103 | 0.3675 |
| XGBoost Tuned | 0.5047 | 0.5726 | 0.3966 | 0.4686 | 0.3627 |

Current best F1-score is Logistic Regression with StandardScaler at `0.7647`.

These results should be treated as baseline results, not final optimized thesis results. Scaling substantially improves Logistic Regression. The current tuned XGBoost configuration does not improve over the default XGBoost baseline, so future work should use broader hyperparameter search and feature selection.

## CICIDS2017 Work Completed

CICIDS2017 support now covers the public multi-day MachineLearningCSV files mirrored on Hugging Face. The workflow downloads the daily CSV files, normalizes their CICFlowMeter schema, merges them into one project-compatible IDS CSV, validates it, and runs the standard benchmark pipeline.

Local raw files:

- `data/raw/CICIDS2017-Monday.csv`
- `data/raw/CICIDS2017-Tuesday.csv`
- `data/raw/CICIDS2017-Wednesday.csv`
- `data/raw/CICIDS2017-Thursday-Morning-WebAttacks.csv`
- `data/raw/CICIDS2017-Thursday-Afternoon-Infilteration.csv`
- `data/raw/CICIDS2017-Friday-Morning.csv`
- `data/raw/CICIDS2017-Friday-DDos.csv`
- `data/raw/CICIDS2017-Friday-PortScan.csv`

Normalization step:

```bash
backend/.venv/bin/python scripts/normalize_cicids.py \
  --input data/raw/CICIDS2017-Monday.csv \
  --input data/raw/CICIDS2017-Tuesday.csv \
  --input data/raw/CICIDS2017-Wednesday.csv \
  --input data/raw/CICIDS2017-Thursday-Morning-WebAttacks.csv \
  --input data/raw/CICIDS2017-Thursday-Afternoon-Infilteration.csv \
  --input data/raw/CICIDS2017-Friday-Morning.csv \
  --input data/raw/CICIDS2017-Friday-DDos.csv \
  --input data/raw/CICIDS2017-Friday-PortScan.csv \
  --output data/processed/cicids2017_full_normalized.csv
```

The normalizer converts CICIDS/CICFlowMeter schema into the project IDS schema:

- Strips whitespace from column names.
- Converts original `Label` into binary `label`.
- Copies original attack name into `attack_cat`.
- Maps `BENIGN` to `0` and non-benign labels to `1`.
- Replaces infinite and missing values for downstream preprocessing.

Validation result:

- `2,830,743` rows.
- `80` columns after normalization.
- Required columns present: `label`, `attack_cat`.
- Attack categories: `BENIGN`, `Bot`, `DDoS`, `DoS GoldenEye`, `DoS Hulk`, `DoS Slowhttptest`, `DoS slowloris`, `FTP-Patator`, `Heartbleed`, `Infiltration`, `PortScan`, `SSH-Patator`, `Web Attack Brute Force`, `Web Attack Sql Injection`, `Web Attack XSS`.

Generated local outputs:

- `reports/evaluation/cicids2017-full-validation.json`
- `reports/evaluation/cicids2017-full-profile.json`
- `reports/pipeline/cicids2017-full/pipeline-summary.json`
- `reports/pipeline/cicids2017-full/pipeline-report.md`
- `reports/pipeline/cicids2017-full/reports/model-comparison.csv`
- `reports/pipeline/cicids2017-full/metrics/*.json`
- `reports/pipeline/cicids2017-full/figures/*.svg`
- `reports/pipeline/cicids2017-full/reports/feature-importance/*.csv`

Current full CICIDS2017 random-split baseline results are:

| Model | Accuracy | Precision | Recall | F1-score | False Positive Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Decision Tree | 0.99874 | 0.99683 | 0.99676 | 0.99680 | 0.00078 |
| Logistic Regression | 0.90134 | 0.87127 | 0.58570 | 0.70050 | 0.02123 |
| Random Forest | 0.99888 | 0.99721 | 0.99712 | 0.99717 | 0.00068 |

These CICIDS2017 results use the full multi-day CSV collection with a generated stratified random split. They are stronger than the earlier single-day DDoS milestone, but thesis reporting should still clearly state the split protocol and avoid comparing them directly with papers that use temporal or per-day evaluation protocols.

## Implemented Documentation

Documentation already created or expanded includes:

- `README.md`: project overview, architecture, workflows, API overview, thesis scope.
- `docs/datasets.md`: dataset source, placement, validation, and official split workflow.
- `docs/roadmap-6-months.md`: six-month roadmap.
- `docs/thesis-outline.md`: thesis structure.
- `docs/evaluation-plan.md`: IDS and LLM/RAG evaluation plan.
- `docs/demo-script.md`: demo flow.
- `docs/defense-qa.md`: defense questions and answers.
- `docs/architecture-diagram.md`: architecture notes.
- `docs/thesis-proposal.md`: proposal draft.
- `docs/development-direction.md`: technical direction.
- `docs/thesis/abstract.md`: thesis abstract draft.
- `docs/thesis/chapter-01-introduction.md`: Chapter 1 draft.
- `docs/thesis/chapter-02-background-related-work.md`: Chapter 2 draft.
- `docs/thesis/chapter-03-proposed-system.md`: Chapter 3 draft.
- `docs/thesis/chapter-04-implementation.md`: Chapter 4 draft.
- `docs/thesis/chapter-05-experiments-evaluation.md`: Chapter 5 draft.
- `docs/thesis/chapter-06-discussion.md`: Chapter 6 draft.
- `docs/thesis/chapter-07-conclusion-future-work.md`: Chapter 7 draft.

## Verification Status

Latest verified commands:

```bash
cd backend
.venv/bin/pytest
```

Result:

```text
48 passed in 9.06s
```

```bash
cd frontend
npm run build
```

Result:

```text
✓ built in 102ms
```

## Git Status

Recent pushed commits include:

- `17e998f feat: support official train test pipeline splits`
- `2631746 fix: prevent attack category leakage in preprocessing`
- `4f5f6ac feat: add raw dataset validation workflow`
- `38f69d7 docs: improve project showcase README`
- `41e5400 feat: add reproducible dataset evaluation pipeline`
- `b229ad6 docs: add thesis and defense materials`

The latest pushed branch is `main` on `origin`.

## Remaining Work

Important unfinished work:

- Add hyperparameter tuning for XGBoost and tree-based models.
- Add feature scaling and hyperparameter tuning.
- Add SHAP or LIME explainability.
- Add Gemini, OpenAI, or Ollama provider adapter for real LLM outputs.
- Add vector database retrieval using FAISS or ChromaDB.
- Add human/analyst evaluation for explanation quality.
- Add dashboard screenshots or demo GIFs for GitHub presentation.
- Decide which small generated artifacts should be committed as reproducible examples.
- Update thesis Chapter 5 with final benchmark tables, figures, and interpretation.
- Format thesis content according to the university template.

## Recommended Next Step

The next best technical step is to add a stronger baseline such as XGBoost or LightGBM, then rerun the official UNSW-NB15 pipeline and compare results against the current three baseline models.
