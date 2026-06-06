# LLM-Assisted Intrusion Detection SOC

Prototype for a master's thesis project about network intrusion detection, explainable machine learning, and LLM/RAG-assisted security alert analysis.

The system demonstrates a mini Security Operations Center (SOC) workflow: network-flow events are loaded, suspicious activity is converted into IDS alerts, ML evaluation artifacts are generated, and an LLM-style assistant explains alerts with security playbook context.

## Why This Project Exists

Traditional IDS and ML-based detectors can identify suspicious traffic, but their outputs are often difficult for analysts to triage quickly. This project explores how a detection engine can be combined with explainability features and retrieval-augmented alert explanations.

The thesis focus is not to let an LLM decide whether traffic is malicious. The IDS/ML layer performs detection and classification. The LLM/RAG layer supports analysts by explaining evidence, mapping alerts to security knowledge, and recommending response steps.

## Core Capabilities

- Load sample IDS-style network-flow events.
- Generate rule-based demo alerts for attacks such as brute force, DDoS, and port scanning.
- Register research datasets such as sample data, UNSW-NB15, and CICIDS2017.
- Preprocess UNSW-NB15-style CSV files for model training.
- Train baseline ML models including Logistic Regression, Decision Tree, and Random Forest.
- Export model metrics, model comparison tables, confusion matrix figures, and feature importance artifacts.
- Display SOC dashboard cards, alert tables, ML metrics, and LLM explanations.
- Map alerts to MITRE ATT&CK-style techniques and triage priority values.
- Compare explanation modes: template, no-RAG, and RAG-assisted explanations.
- Export LLM rubric scores, RAG summaries, and incident case study reports for thesis evaluation.

## Architecture

```text
Network-flow data / sample CSV
        |
        v
Preprocessing and feature preparation
        |
        v
IDS detection and ML evaluation layer
        |
        v
Alert enrichment: severity, confidence, top features, MITRE mapping, priority
        |
        v
LLM/RAG explanation layer using local security playbooks
        |
        v
FastAPI backend API + React SOC dashboard + thesis report exports
```

Main components:

- **Backend**: FastAPI service that exposes events, alerts, explanations, datasets, and metrics.
- **Frontend**: React + Vite dashboard for viewing alerts, model metrics, and explanation comparisons.
- **Scripts**: CLI tools for preprocessing, model training, evaluation export, and report generation.
- **Knowledge base**: Local markdown playbooks used as grounding context for alert explanations.
- **Artifacts**: Generated model metrics, trained models, figures, and evaluation reports.

## Repository Structure

```text
.
├── backend/                 # FastAPI application, domain models, services, tests
├── data/                    # Sample and processed IDS datasets
├── docs/                    # Thesis outline, roadmap, evaluation plan, design notes
├── frontend/                # React/Vite SOC dashboard
├── knowledge_base/          # Local security playbooks for RAG-style grounding
├── models/                  # Generated metrics and trained model artifacts
├── reports/                 # Generated evaluation reports and figures
├── scripts/                 # Preprocessing, training, and export CLIs
├── .gitignore               # Excludes local envs, dependencies, generated data/artifacts
└── README.md
```

## Tech Stack

- **Backend**: Python, FastAPI, Pydantic, pandas, scikit-learn, joblib, pytest.
- **Frontend**: React, TypeScript, Vite.
- **ML/IDS**: rule-based baseline plus baseline supervised models for research comparison.
- **LLM/RAG prototype**: local template explanation and markdown playbook retrieval. External LLM providers can be added later.
- **Research outputs**: CSV, JSON metrics, markdown reports, and figure exports.

## Quick Start

### 1. Start the Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend default URL:

```text
http://localhost:8000
```

Health check:

```bash
curl http://localhost:8000/health
```

### 2. Start the Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend default URL:

```text
http://localhost:5173
```

The dashboard calls the backend at `http://localhost:8000`. If the backend is offline, the frontend falls back to sample dashboard data.

### 3. Run Backend Tests

```bash
cd backend
pytest
```

## API Overview

The FastAPI backend currently exposes these main endpoints:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Service health check. |
| `GET` | `/events` | Return sample network-flow events. |
| `GET` | `/datasets` | List supported/registered datasets. |
| `GET` | `/alerts` | Generate demo IDS alerts from sample events. |
| `GET` | `/alerts/{alert_id}` | Get one alert by ID. |
| `GET` | `/alerts/{alert_id}/explanation` | Explain one alert with local LLM/RAG-style context. |
| `GET` | `/alerts/{alert_id}/explanation/comparison` | Compare template, no-RAG, and RAG-style explanations. |
| `GET` | `/metrics` | Return fixed demo IDS metrics. |
| `GET` | `/ml/evaluate` | Evaluate the rule-based baseline on sample events. |
| `GET` | `/ml/metrics` | Return saved ML metric artifacts. |

FastAPI also provides interactive API documentation when the backend is running:

```text
http://localhost:8000/docs
```

## Main Research Workflows

Run these commands from the repository root unless noted otherwise.

### Preprocess UNSW-NB15 Fixture Data

```bash
python scripts/preprocess_unsw_nb15.py \
  --input data/samples/unsw_nb15_fixture.csv \
  --output data/processed/unsw_nb15_fixture_processed.csv
```

### Train Baseline Models

```bash
backend/.venv/bin/python scripts/train_models.py \
  --dataset-id fixture \
  --input data/processed/unsw_nb15_fixture_processed.csv \
  --metrics-dir models/metrics \
  --models-dir models/trained
```

### Export Model Comparison CSV

```bash
backend/.venv/bin/python scripts/export_model_comparison.py \
  --metrics-dir models/metrics \
  --output reports/evaluation/model-comparison.csv
```

### Export Confusion Matrix Figures

```bash
backend/.venv/bin/python scripts/export_confusion_matrices.py \
  --metrics-dir models/metrics \
  --figures-dir reports/figures
```

### Export Feature Importance

```bash
backend/.venv/bin/python scripts/export_feature_importance.py \
  --dataset-id fixture \
  --input data/processed/unsw_nb15_fixture_processed.csv \
  --models-dir models/trained \
  --output-dir reports/evaluation/feature-importance
```

### Evaluate LLM Explanation Modes

```bash
backend/.venv/bin/python scripts/evaluate_llm.py \
  --output reports/evaluation/llm-rubric-scores.csv
```

### Export RAG vs No-RAG Summary

```bash
backend/.venv/bin/python scripts/export_rag_summary.py \
  --scores reports/evaluation/llm-rubric-scores.csv \
  --output reports/evaluation/rag-vs-no-rag-summary.md
```

### Export Incident Case Studies

```bash
backend/.venv/bin/python scripts/export_case_studies.py \
  --output reports/evaluation/incident-case-studies.md
```

## Evaluation Plan

IDS model evaluation is designed around common supervised-learning metrics:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- False positive rate.
- Confusion matrix.
- Training and prediction cost where applicable.

LLM/RAG explanation evaluation is designed around a rubric:

- Correctness: the explanation matches the alert and evidence.
- Completeness: it includes cause, impact, and response guidance.
- Groundedness: it stays within the alert and retrieved context.
- Actionability: recommendations are concrete and feasible.
- Hallucination control: it avoids invented facts, tools, IPs, or CVEs.
- Latency: response time is acceptable for analyst workflow.

See `docs/evaluation-plan.md` for more detail.

## Thesis Scope

Proposed English thesis title:

> An Explainable Machine Learning and Retrieval-Augmented Large Language Model System for Network Intrusion Detection and Security Alert Analysis.

The expected contribution is a prototype that connects these areas:

- Network intrusion detection using IDS-style flow data.
- Baseline machine-learning model comparison.
- Explainable alert evidence through top features and model artifacts.
- LLM/RAG-assisted alert explanation and response recommendation.
- SOC dashboard and exported evaluation artifacts for thesis discussion.

Important scope boundary:

- The IDS/ML layer is responsible for detection and classification.
- The LLM layer is responsible for explanation, summarization, mapping to knowledge, and response suggestions.
- The LLM should not be treated as the final security decision-maker.

## Current Status

This repository is an MVP/prototype. It already contains a working FastAPI backend, React dashboard, sample alert flow, baseline model training scripts, evaluation export scripts, markdown playbooks, and thesis planning documents.

Planned future improvements include:

- Add full UNSW-NB15 and CICIDS2017/CSE-CIC-IDS2018 dataset processing.
- Add XGBoost or LightGBM model experiments.
- Add SHAP or LIME explainability if time allows.
- Replace local-template explanations with Gemini, OpenAI, or Ollama adapters.
- Add a vector database for stronger RAG retrieval.
- Expand incident case studies for thesis evaluation.

## Git and Artifact Notes

The `.gitignore` is configured to avoid committing local dependencies, virtual environments, build outputs, and large generated artifacts such as raw data, processed data, trained models, and reports.

Before pushing or sharing the repository, review whether any generated files under `data/`, `models/`, or `reports/` should be intentionally included as small reproducible examples. By default, large datasets and generated artifacts should stay out of git.
