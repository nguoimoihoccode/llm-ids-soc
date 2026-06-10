# Defense Demo Script

## Demo Goal

Show that the system supports a SOC-style workflow:

```text
Network events -> IDS alerts -> alert intelligence -> RAG/LLM explanation -> evaluation artifacts
```

The main message is that machine learning and rules detect suspicious traffic, while LLM/RAG explains and supports incident triage. The LLM is not the primary detector.

## Setup Before Demo

Open two terminals.

Terminal 1, backend:

```bash
cd /Users/nguyenthucphuc/project/llm-ids-soc/backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Terminal 2, frontend:

```bash
cd /Users/nguyenthucphuc/project/llm-ids-soc/frontend
npm run dev
```

Open:

```text
http://localhost:5173
```

Optional API docs:

```text
http://localhost:8000/docs
```

## Step 1: Introduce The Problem

Suggested speech:

> Intrusion detection systems can produce technical alerts, but analysts still need to understand what happened, why it matters, and what response actions are appropriate. This prototype combines IDS detection, alert intelligence, and LLM/RAG explanation to support SOC triage.

Point to:

- Dashboard title.
- Total alerts.
- High severity count.
- Model accuracy card.

## Step 2: Show Dataset Registry

Open API:

```text
GET http://localhost:8000/datasets
```

Explain:

> The system starts with sample data for deterministic demonstration. The thesis plan includes UNSW-NB15 as the primary dataset and CICIDS2017 as a secondary benchmark.

Mention:

- `sample`: ready.
- `unsw-nb15`: planned/primary thesis dataset.
- `cicids2017`: planned secondary validation.

## Step 3: Show Alerts

Open dashboard alert table or API:

```text
GET http://localhost:8000/alerts
```

Explain:

> Raw network events are converted into structured security alerts. Each alert includes attack type, severity, confidence, technical evidence, MITRE mapping, and triage priority.

Use the Brute Force case:

- Attack type: Brute Force.
- Severity: High.
- Confidence: 94%.
- MITRE: T1110 - Brute Force.
- Priority: P1.
- Evidence features: `failed_login_count`, `dst_port`, `flow_packets_s`.

## Step 4: Show Grounded LLM Explanation

Open:

```text
GET http://localhost:8000/alerts/alert-evt-002/explanation
```

Explain:

> The LLM explanation is grounded by alert fields and playbook context. It uses top features, MITRE mapping, triage priority, and retrieved security knowledge. This reduces uncontrolled hallucination because the LLM is constrained by structured context.

Emphasize:

- Evidence features are included.
- MITRE mapping is included.
- Playbook context is retrieved.
- Recommended response is generated.

## Step 5: Show Explanation Comparison

Open dashboard section `Explanation Comparison` or API:

```text
GET http://localhost:8000/alerts/alert-evt-002/explanation/comparison
```

Explain:

> The system compares three explanation modes: template, LLM without RAG, and LLM with RAG. This is used later for rubric-based evaluation.

Compare:

- `template`: short, deterministic, limited context.
- `llm_without_rag`: uses alert fields but no retrieved playbook.
- `llm_with_rag`: uses alert fields and retrieved security playbook.

## Step 6: Show Model Metrics

Show dashboard model comparison table or API:

```text
GET http://localhost:8000/ml/metrics
```

Explain:

> The current metrics are generated from fixture data to validate the pipeline. For the thesis, the same training and evaluation pipeline will be applied to UNSW-NB15 and CICIDS2017.

Mention generated artifacts:

```text
models/metrics/*.json
reports/evaluation/model-comparison.csv
reports/figures/*-confusion-matrix.svg
reports/evaluation/feature-importance/*.csv
```

## Step 7: Show Evaluation Artifacts

Open files:

```text
reports/evaluation/model-comparison.csv
reports/evaluation/llm-rubric-scores.csv
reports/evaluation/rag-vs-no-rag-summary.md
reports/evaluation/incident-case-studies.md
```

Explain:

> The project does not stop at a UI demo. It produces reproducible artifacts for thesis evaluation: model comparison, confusion matrices, feature importance, LLM rubric scores, RAG comparison summary, and incident case studies.

## Step 8: Close With Contribution

Suggested speech:

> The contribution is a combined research prototype: IDS detection and model evaluation, explainable alert intelligence, RAG-backed LLM explanation, and evaluation artifacts for comparing explanation strategies. The design separates detection from explanation, which makes the system safer and easier to evaluate.

## Commands To Regenerate Artifacts

Preprocess fixture:

```bash
backend/.venv/bin/python scripts/preprocess_unsw_nb15.py \
  --input data/samples/unsw_nb15_fixture.csv \
  --output data/processed/unsw_nb15_fixture_processed.csv
```

Train models:

```bash
backend/.venv/bin/python scripts/train_models.py \
  --dataset-id fixture \
  --input data/processed/unsw_nb15_fixture_processed.csv \
  --metrics-dir models/metrics \
  --models-dir models/trained
```

Export model comparison:

```bash
backend/.venv/bin/python scripts/export_model_comparison.py \
  --metrics-dir models/metrics \
  --output reports/evaluation/model-comparison.csv
```

Export confusion matrices:

```bash
backend/.venv/bin/python scripts/export_confusion_matrices.py \
  --metrics-dir models/metrics \
  --figures-dir reports/figures
```

Export feature importance:

```bash
backend/.venv/bin/python scripts/export_feature_importance.py \
  --dataset-id fixture \
  --input data/processed/unsw_nb15_fixture_processed.csv \
  --models-dir models/trained \
  --output-dir reports/evaluation/feature-importance
```

Evaluate LLM modes:

```bash
backend/.venv/bin/python scripts/evaluate_llm.py \
  --output reports/evaluation/llm-rubric-scores.csv
```

Export RAG summary:

```bash
backend/.venv/bin/python scripts/export_rag_summary.py \
  --scores reports/evaluation/llm-rubric-scores.csv \
  --output reports/evaluation/rag-vs-no-rag-summary.md
```

Export case studies:

```bash
backend/.venv/bin/python scripts/export_case_studies.py \
  --output reports/evaluation/incident-case-studies.md
```
