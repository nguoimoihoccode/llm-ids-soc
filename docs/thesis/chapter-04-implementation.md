# Chapter 4: Implementation

## 4.1 Introduction

This chapter describes the implementation of the proposed research prototype. The system is implemented as a modular application consisting of a FastAPI backend, a React dashboard, preprocessing and training scripts, local RAG playbooks, and report export utilities. The implementation is designed to support both demonstration and thesis evaluation.

The prototype implements the end-to-end workflow described in Chapter 3:

```text
Network-flow data
        -> preprocessing
        -> IDS/ML detection
        -> enriched alert generation
        -> RAG/LLM explanation
        -> SOC dashboard
        -> evaluation reports
```

## 4.2 Project Structure

The project is organized into focused directories:

```text
llm-ids-soc/
  backend/                 FastAPI backend and tests
  frontend/                React/Vite dashboard
  data/                    Sample and processed datasets
  knowledge_base/          Local RAG playbooks
  models/                  Trained models and metrics artifacts
  reports/                 Evaluation reports and figures
  scripts/                 CLI scripts for preprocessing, training, and reporting
  docs/                    Thesis, design, roadmap, and defense materials
```

This structure separates runtime services, research scripts, generated artifacts, and documentation. The separation makes the project easier to test, demonstrate, and extend.

## 4.3 Backend Implementation

The backend is implemented using FastAPI. It exposes API endpoints for events, dataset registry, alerts, explanations, model metrics, and evaluation artifacts.

Main backend files:

```text
backend/app/main.py
backend/app/models.py
backend/app/services/
backend/tests/
```

### 4.3.1 Data Models

The backend uses Pydantic models to define structured data exchanged between services and API endpoints. Important models include:

- `NetworkEvent`: represents one network-flow event.
- `Alert`: represents an enriched security alert.
- `Explanation`: represents a grounded alert explanation.
- `ExplanationComparison`: represents multiple explanation modes for one alert.
- `DatasetInfo`: represents registered datasets.
- `ModelEvaluation`: represents baseline evaluation output.
- `PreprocessingSummary`: represents preprocessing output.

The `Alert` model is central to the prototype. It contains both detection output and analyst-oriented context:

```text
alert_id
event_id
timestamp
src_ip
dst_ip
attack_type
severity
confidence
reason
mitre_technique
triage_priority
```

## 4.4 Dataset Registry

The dataset registry is implemented in:

```text
backend/app/services/datasets.py
```

It currently registers:

- `sample`: deterministic sample data used by the prototype.
- `unsw-nb15`: primary planned thesis dataset.
- `cicids2017`: secondary planned benchmark.

The API endpoint is:

```text
GET /datasets
```

This endpoint allows the dashboard and thesis demonstration to show which datasets are supported and which are planned for full evaluation.

## 4.5 Data Loading And Sample Events

Sample network events are stored in:

```text
data/samples/network_events.csv
```

The loader is implemented in:

```text
backend/app/services/data_loader.py
```

The sample data includes benign and malicious events, including brute force, DDoS, and port scan examples. This allows the prototype to demonstrate the full workflow without depending on a large external dataset during development.

## 4.6 Preprocessing Implementation

The preprocessing service is implemented in:

```text
backend/app/services/preprocessing.py
```

The CLI script is:

```text
scripts/preprocess_unsw_nb15.py
```

The preprocessing pipeline performs:

- CSV loading.
- Replacement of NaN values.
- Replacement of infinite values.
- One-hot encoding of categorical columns.
- Output of processed CSV data.
- Summary generation.

Example command:

```bash
backend/.venv/bin/python scripts/preprocess_unsw_nb15.py \
  --input data/samples/unsw_nb15_fixture.csv \
  --output data/processed/unsw_nb15_fixture_processed.csv
```

The current fixture validates the pipeline. The same structure will be used for the full UNSW-NB15 dataset.

## 4.7 IDS And Model Training Implementation

The prototype includes both a deterministic rule-based alert generator and a baseline ML training pipeline.

### 4.7.1 Rule-Based Alert Generator

The rule-based alert generator is implemented in:

```text
backend/app/services/detector.py
```

It converts sample events labeled as attacks into enriched alerts. The current logic assigns confidence and severity based on attack type and key traffic features.

For example:

- Brute force alerts use `failed_login_count`, `dst_port`, and `flow_packets_s`.
- DDoS alerts use `flow_packets_s`, `total_fwd_packets`, and `flow_bytes_s`.
- Port scan alerts use `syn_flag_count`, `dst_port`, and `flow_duration_ms`.

### 4.7.2 Baseline ML Training

The model training service is implemented in:

```text
backend/app/services/model_training.py
```

The training CLI is:

```text
scripts/train_models.py
```

The current implementation trains:

- Logistic Regression.
- Decision Tree.
- Random Forest.

Example command:

```bash
backend/.venv/bin/python scripts/train_models.py \
  --dataset-id fixture \
  --input data/processed/unsw_nb15_fixture_processed.csv \
  --metrics-dir models/metrics \
  --models-dir models/trained
```

The script saves:

```text
models/trained/*.joblib
models/metrics/*.json
```

## 4.8 Model Metrics Implementation

Model metrics are calculated in:

```text
backend/app/services/model_metrics.py
```

The metrics include:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- False positive rate.
- Confusion matrix.

Saved metric artifacts can be read through:

```text
backend/app/services/metric_artifacts.py
```

And exposed through:

```text
GET /ml/metrics
```

## 4.9 Alert Intelligence Implementation

Alert intelligence is implemented as part of the alert generation flow. Each alert includes:

- Top evidence features.
- MITRE ATT&CK technique mapping.
- Triage priority.

Current mapping examples:

| Attack Type | MITRE Mapping | Priority Example |
|---|---|---|
| Brute Force | T1110 - Brute Force | P1 |
| DDoS | T1498 - Network Denial of Service | P1 |
| Port Scan | T1046 - Network Service Discovery | P2 |

This layer prepares structured context for the LLM/RAG explanation layer.

## 4.10 RAG And LLM Explanation Implementation

The local RAG retrieval service is implemented in:

```text
backend/app/services/rag_service.py
```

The local playbooks are stored in:

```text
knowledge_base/playbooks/
```

Current playbooks include:

- Brute force.
- DDoS.
- Port scan.

The explanation service is implemented in:

```text
backend/app/services/llm_service.py
```

The system provides two key endpoints:

```text
GET /alerts/{alert_id}/explanation
GET /alerts/{alert_id}/explanation/comparison
```

The first endpoint returns a grounded explanation for a single alert. The second endpoint compares three modes:

- Template explanation.
- LLM-style explanation without RAG.
- LLM-style explanation with RAG.

The current implementation uses a deterministic local-template provider. External providers such as Gemini, OpenAI, or Ollama can be added later through a provider adapter layer.

## 4.11 Frontend Dashboard Implementation

The frontend is implemented using React, TypeScript, and Vite.

Main frontend files:

```text
frontend/src/main.tsx
frontend/src/styles.css
```

The dashboard displays:

- Project overview.
- Alert statistics.
- Alert table.
- Severity and priority.
- LLM analysis.
- Evidence features.
- MITRE mapping.
- Model comparison table.
- Explanation comparison cards.

The frontend calls the backend at:

```text
http://localhost:8000
```

If the backend is unavailable, the frontend uses fallback sample data. This makes the UI easier to demonstrate during development.

## 4.12 Reporting And Evaluation Scripts

The project includes several scripts for reproducible thesis artifacts.

### 4.12.1 Model Comparison Export

Script:

```text
scripts/export_model_comparison.py
```

Output:

```text
reports/evaluation/model-comparison.csv
```

### 4.12.2 Confusion Matrix Export

Script:

```text
scripts/export_confusion_matrices.py
```

Output:

```text
reports/figures/*-confusion-matrix.svg
```

### 4.12.3 Feature Importance Export

Script:

```text
scripts/export_feature_importance.py
```

Output:

```text
reports/evaluation/feature-importance/*.csv
```

### 4.12.4 LLM Rubric Evaluation

Script:

```text
scripts/evaluate_llm.py
```

Output:

```text
reports/evaluation/llm-rubric-scores.csv
```

### 4.12.5 RAG Summary Export

Script:

```text
scripts/export_rag_summary.py
```

Output:

```text
reports/evaluation/rag-vs-no-rag-summary.md
```

### 4.12.6 Incident Case Studies Export

Script:

```text
scripts/export_case_studies.py
```

Output:

```text
reports/evaluation/incident-case-studies.md
```

## 4.13 Testing Implementation

The backend includes automated tests using pytest. The tests cover:

- API endpoints.
- Dataset registry.
- Preprocessing.
- Model metrics.
- Model training.
- Report exports.
- Confusion matrix exports.
- Feature importance exports.
- LLM rubric evaluation.
- RAG summary generation.
- Incident case study reports.

The frontend is verified through the production build command.

Backend verification:

```bash
cd backend
.venv/bin/pytest
```

Frontend verification:

```bash
cd frontend
npm run build
```

## 4.14 Current Implementation Limitations

The current implementation is a research prototype. Its limitations include:

- The current sample dataset is small and used only for deterministic workflow validation.
- Full UNSW-NB15 and CICIDS2017 ingestion are planned but not yet complete.
- The LLM provider is currently local-template rather than an external LLM API.
- RAG retrieval uses local markdown playbooks rather than a vector database.
- SHAP/LIME explainability is planned as optional future work.
- The dashboard is intended for demonstration, not production SOC operations.

## 4.15 Summary

This chapter described the implementation of the research prototype. The backend provides modular services and APIs for data loading, detection, alert enrichment, explanation, metrics, and report generation. The frontend provides a SOC-style dashboard. The scripts produce reproducible evaluation artifacts for both IDS and LLM/RAG components. The next chapter presents the experiments and evaluation results generated by this implementation.
