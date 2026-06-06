# Six-Month Thesis Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the current MVP into a 5-6 month thesis-grade research project with ML IDS, explainability, RAG/LLM analysis, dashboard, and evaluation.

**Architecture:** Keep the current FastAPI/React MVP as the product shell. Add research modules incrementally: dataset preprocessing, model training, metrics artifacts, explainability, alert intelligence, RAG/LLM providers, and evaluation reports.

**Tech Stack:** FastAPI, pytest, pandas, scikit-learn, optional XGBoost/LightGBM, optional SHAP/LIME, React/Vite, markdown playbooks, optional ChromaDB/FAISS.

---

## File Structure

- Create `backend/app/services/datasets.py` for dataset metadata and supported dataset registry.
- Create `backend/app/services/preprocessing.py` for reusable cleaning functions.
- Create `backend/app/services/model_training.py` for supervised model training interfaces.
- Create `backend/app/services/model_metrics.py` for metrics calculation and artifact writing.
- Create `backend/app/services/explainability.py` for feature importance and SHAP/LIME integration.
- Create `backend/app/services/mitre_mapping.py` for attack-to-technique mapping.
- Create `backend/app/services/llm_providers.py` for Gemini/OpenAI/Ollama/local-template adapters.
- Create `scripts/preprocess_unsw_nb15.py` for UNSW-NB15 preprocessing.
- Create `scripts/train_models.py` for model training and evaluation.
- Create `scripts/evaluate_llm.py` for case-study scoring.
- Create `models/trained/.gitkeep` and `models/metrics/.gitkeep` for model artifacts.
- Create `reports/evaluation/.gitkeep` and `reports/figures/.gitkeep` for thesis artifacts.

## Milestone 1: Dataset Registry

- [x] Write failing tests for dataset registry listing `sample`, `unsw-nb15`, and `cicids2017`.
- [x] Implement dataset registry.
- [x] Add `GET /datasets` endpoint.
- [x] Verify backend tests pass.

## Milestone 2: UNSW-NB15 Preprocessing

- [x] Write tests for cleaning NaN, Infinity, categorical protocol fields, and label encoding.
- [x] Implement reusable preprocessing functions.
- [x] Add `scripts/preprocess_unsw_nb15.py` with CLI args for raw input and processed output.
- [x] Verify script on a small fixture CSV.

## Milestone 3: Model Training

- [x] Write tests for metrics calculation on known labels/predictions.
- [x] Implement model metrics service.
- [x] Add Logistic Regression, Decision Tree, and Random Forest training.
- [x] Save metrics JSON under `models/metrics`.
- [x] Save trained model files under `models/trained`.

## Milestone 4: Advanced Model and Cross-Dataset Evaluation

- [ ] Add XGBoost or LightGBM if dependency installation is stable.
- [ ] Add CICIDS2017/CSE-CIC-IDS2018 preprocessing path.
- [x] Generate model comparison CSV.
- [x] Export confusion matrix SVG figures from saved metrics.
- [x] Add dashboard metrics section consuming saved metrics.

## Milestone 5: Explainability and Alert Intelligence

- [x] Add top-feature extraction for tree models.
- [ ] Add optional SHAP/LIME artifact generation.
- [x] Extend alert schema with `top_features`, `mitre_technique`, and `triage_priority`.
- [x] Add `top_features` evidence to alerts and dashboard.
- [ ] Add alert detail page showing feature evidence.

## Milestone 6: LLM/RAG Provider Layer

- [ ] Add provider interface for `local-template`, `gemini`, `openai`, and `ollama`.
- [ ] Add environment-based config.
- [ ] Add RAG retrieval mode over local markdown playbooks.
- [x] Add comparison endpoint for template vs LLM vs LLM+RAG.
- [x] Ground local-template explanations with top features, MITRE mapping, and triage priority.

## Milestone 7: LLM Evaluation Framework

- [x] Create incident case-study fixture set from current sample alerts.
- [x] Implement rubric scoring CSV schema.
- [x] Add evaluation script for cached LLM outputs.
- [x] Generate `reports/evaluation/llm-rubric-scores.csv`.
- [x] Generate `reports/evaluation/rag-vs-no-rag-summary.md`.
- [x] Generate `reports/evaluation/incident-case-studies.md`.

## Milestone 8: Thesis and Defense Artifacts

- [ ] Generate architecture diagram source.
- [ ] Export experiment tables.
- [ ] Add demo script.
- [ ] Add defense Q&A notes.

## Verification Gates

- Backend: `.venv/bin/pytest` must pass before each milestone closes.
- Frontend: `npm run build` must pass before UI milestone closes.
- Research scripts: each CLI script must run on a small fixture before running on full datasets.
