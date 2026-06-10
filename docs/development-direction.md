# Development Direction

## Purpose

This document defines the next development direction for the LLM-Assisted Intrusion Detection SOC project. The goal is to move the repository from an MVP research prototype toward a stronger thesis-grade and GitHub-showcase project.

The core positioning remains unchanged:

```text
IDS/ML detects suspicious activity.
RAG/LLM explains alerts and supports analyst triage.
Human analysts remain responsible for final decisions.
```

## Current Baseline

The project currently includes:

- FastAPI backend APIs for events, alerts, datasets, explanations, and metrics.
- React/Vite SOC dashboard.
- Sample IDS-style event flow.
- UNSW-NB15-style preprocessing fixture.
- Baseline ML training for Logistic Regression, Decision Tree, and Random Forest.
- Model metrics, model comparison, confusion matrix, and feature importance exports.
- Local markdown playbooks for RAG-style grounding.
- Template, no-RAG, and RAG-assisted explanation comparison.
- Rubric-based LLM explanation evaluation.
- Incident case study export.
- Thesis documents from abstract through Chapter 7.
- Defense Q&A and demo script.

This is a strong MVP. The next work should focus on research validity, explanation depth, real LLM/RAG behavior, and demo polish.

## Direction 1: Full Dataset Evaluation

### Goal

Replace fixture-only evaluation with full benchmark experiments.

### Work Items

- Add full UNSW-NB15 ingestion.
- Add CICIDS2017 or CSE-CIC-IDS2018 as a secondary benchmark.
- Support curated sampled datasets if raw files are too large.
- Track train/test split strategy.
- Track class distribution and imbalance.
- Export dataset summary reports.

Current foundation:

```bash
backend/.venv/bin/python scripts/profile_dataset.py \
  --input data/samples/unsw_nb15_fixture.csv \
  --output reports/evaluation/dataset-summary.json
```

This profiles row count, column count, label distribution, attack category distribution, class percentages, imbalance ratios, missing values, and source columns before preprocessing.

Dataset split foundation:

```bash
backend/.venv/bin/python scripts/split_dataset.py \
  --input data/samples/unsw_nb15_fixture.csv \
  --train-output data/processed/unsw_nb15_fixture_train.csv \
  --test-output data/processed/unsw_nb15_fixture_test.csv \
  --summary-output reports/evaluation/dataset-split-summary.json \
  --test-size 0.33 \
  --random-state 42
```

This exports train/test files and a split summary with label distributions, split strategy, and stratification status, making evaluation setup easier to document. If stratified splitting is not possible on a small dataset, the service falls back to a non-stratified split and records `fallback_non_stratified`.

Explicit train/test training foundation:

```bash
backend/.venv/bin/python scripts/train_models.py \
  --dataset-id fixture-split \
  --train-input data/processed/unsw_nb15_fixture_train.csv \
  --test-input data/processed/unsw_nb15_fixture_test.csv \
  --metrics-dir models/metrics \
  --models-dir models/trained
```

This mode evaluates models on the test CSV instead of the training CSV and is the preferred path for full benchmark experiments.

End-to-end pipeline foundation:

```bash
backend/.venv/bin/python scripts/run_dataset_pipeline.py \
  --dataset-id fixture-pipeline \
  --input data/samples/unsw_nb15_fixture.csv \
  --output-dir reports/pipeline/fixture-pipeline \
  --models decision_tree \
  --test-size 0.33 \
  --random-state 42
```

This command runs profiling, split, preprocessing, training, test-set evaluation, JSON summary export, a thesis-ready `pipeline-report.md`, `reports/model-comparison.csv`, confusion matrix SVG figures, and tree-model feature importance CSV files in one reproducible workflow. The markdown report includes a `Generated Artifacts` section so thesis tables, figures, and appendices can be traced back to exact files.

### Deliverables

- `data/raw/` dataset instructions.
- `data/processed/` processed benchmark files.
- Model metrics per dataset.
- Model comparison table across datasets.
- Confusion matrix figures.
- Dataset summary report.

### Success Criteria

- At least one full public IDS dataset is processed end-to-end.
- At least three supervised models are evaluated.
- Metrics are reproducible from CLI commands.
- Chapter 5 can replace fixture-only results with benchmark results.

### Thesis Impact

Very high. This is the most important step for turning the project from MVP into thesis-grade empirical work.

## Direction 2: Stronger ML Models

### Goal

Add stronger tabular ML baselines beyond the current models.

### Work Items

- Add XGBoost or LightGBM.
- Optionally add CatBoost.
- Keep Logistic Regression, Decision Tree, and Random Forest as interpretable baselines.
- Compare performance, training time, and inference latency.

### Deliverables

- Extended training service.
- Extended CLI model selection.
- Metrics JSON for new models.
- Updated model comparison CSV.

### Success Criteria

- New models train with the same command structure.
- Metrics are exported in the same format as existing models.
- Model comparison report shows both baseline and stronger models.

### Thesis Impact

High. Stronger models make the IDS evaluation more credible and provide a better comparison section.

## Direction 3: Instance-Level Explainability

### Goal

Explain why each specific alert was classified as suspicious.

### Work Items

- Add SHAP for tree-based models.
- Export global SHAP summary.
- Export local SHAP explanation per alert or sample.
- Connect local feature attribution to alert `top_features`.
- Optionally add LIME if SHAP setup is difficult.

### Deliverables

- SHAP artifact exports.
- Per-alert feature contribution report.
- Updated alert explanation payload.
- Dashboard panel: `Why this alert?`.

### Success Criteria

- Each selected alert has ranked contributing features.
- Analyst-facing explanation can reference actual feature contributions.
- Chapter 5 and Chapter 6 can discuss model-level and alert-level explainability.

### Thesis Impact

Very high. This directly strengthens the explainable AI contribution.

## Direction 4: Real LLM Provider Integration

### Goal

Move from deterministic local-template behavior to real LLM evaluation.

### Work Items

- Define an `LLMProvider` interface.
- Keep `LocalTemplateProvider` for deterministic tests.
- Add one real provider:
  - Gemini.
  - OpenAI.
  - Ollama local model.
- Add provider config through environment variables.
- Add safe fallback to local template when provider is unavailable.

### Deliverables

- Provider abstraction.
- Real provider implementation.
- Example `.env` documentation.
- Updated explanation comparison.
- Latency tracking.

### Success Criteria

- Same alert can be explained by template and real LLM provider.
- Tests do not require external API calls.
- Real LLM outputs can be cached or exported for evaluation.

### Thesis Impact

High. This enables stronger claims about LLM/RAG behavior, as long as evaluation is carefully scoped.

## Direction 5: Vector-Based RAG

### Goal

Improve retrieval quality beyond simple local playbook lookup.

### Work Items

- Add FAISS or ChromaDB.
- Chunk markdown playbooks.
- Generate embeddings.
- Retrieve top-k relevant chunks for each alert.
- Include retrieved context in explanation output.
- Track retrieved document IDs for auditability.

### Deliverables

- Vector index build script.
- Retrieval service.
- Retrieved context metadata.
- RAG evaluation artifacts.

### Success Criteria

- Alert-specific context is retrieved semantically.
- Explanation output includes the retrieved evidence source.
- RAG vs no-RAG comparison uses real retrieved context.

### Thesis Impact

High. This makes the RAG component more technically convincing.

## Direction 6: Expanded Security Knowledge Base

### Goal

Make RAG useful across more attack types.

### Work Items

- Add playbooks for more attack families:
  - Brute Force.
  - DDoS.
  - Port Scan.
  - SQL Injection.
  - Botnet.
  - Malware.
  - Data Exfiltration.
  - Privilege Escalation.
  - Lateral Movement.
- Use a consistent playbook template.
- Add MITRE ATT&CK technique references.
- Add false positive notes.

### Deliverables

- Expanded markdown playbooks.
- Knowledge base index.
- MITRE mapping table.

### Success Criteria

- Each supported attack type has an associated playbook.
- RAG retrieval can cite the relevant playbook section.
- Explanations become more complete and actionable.

### Thesis Impact

Medium to high. This improves qualitative explanation quality and demo realism.

## Direction 7: Human Expert Evaluation

### Goal

Validate whether generated explanations are useful to humans.

### Work Items

- Select 10-20 representative alerts.
- Generate explanations in three modes:
  - Template.
  - LLM without RAG.
  - LLM with RAG.
- Create an evaluator scoring sheet.
- Ask an advisor, instructor, or security practitioner to score outputs.
- Compare expert scores with deterministic rubric scores.

### Deliverables

- Evaluation form.
- Expert score CSV.
- Summary report.
- Case study appendix.

### Success Criteria

- At least one external evaluator reviews explanation quality.
- RAG and no-RAG outputs are compared using the same criteria.
- Chapter 5 includes qualitative and quantitative explanation evaluation.

### Thesis Impact

Very high. This provides human evidence for the SOC-assistance claim.

## Direction 8: SOC Dashboard Polish

### Goal

Make the demo more impressive and easier to understand.

### Work Items

- Add alert detail page.
- Add attack timeline.
- Add severity distribution chart.
- Add model comparison chart.
- Add explanation comparison side-by-side.
- Add `Why this alert?` panel.
- Add incident report export button.

### Deliverables

- Improved dashboard UI.
- Better demo screenshots.
- Updated demo script.

### Success Criteria

- A reviewer can understand the full workflow from the dashboard.
- Demo can be completed in 5-7 minutes.
- README can include screenshots for GitHub profile impact.

### Thesis Impact

Medium. This improves presentation and defense, but it should not replace research evaluation.

## Direction 9: Incident Report Generator

### Goal

Convert enriched alerts and explanations into analyst-ready incident reports.

### Work Items

- Generate incident summary.
- Include evidence features.
- Include MITRE mapping.
- Include retrieved RAG context.
- Include recommended response.
- Add analyst notes placeholder.
- Export Markdown first, PDF later if needed.

### Deliverables

- Incident report service.
- Report export CLI.
- Dashboard export action.

### Success Criteria

- Each alert can produce a structured incident report.
- Reports can be used in defense demo and thesis appendix.

### Thesis Impact

Medium to high. This strengthens the SOC workflow story.

## Direction 10: SIEM Integration Path

### Goal

Define a realistic path from prototype to SOC tool integration.

### Work Items

- Add simulated SIEM ingestion endpoint.
- Document adapters for tools such as Wazuh, Elastic SIEM, Splunk, Suricata, or Zeek.
- Keep automatic containment out of scope unless explicitly required.

### Deliverables

- SIEM integration design note.
- Simulated ingestion API.
- Example alert payload schema.

### Success Criteria

- The project can explain how it would fit into a real SOC pipeline.
- Production boundaries remain clear.

### Thesis Impact

Medium. Useful for future work and defense questions, but less urgent than dataset and explainability work.

## Recommended Priority Order

### Must Do Next

1. Full UNSW-NB15 evaluation.
2. Full model metrics and confusion matrices.
3. Update Chapter 5 with benchmark results.

### Strong Thesis Upgrade

4. Add XGBoost or LightGBM.
5. Add SHAP local explanations.
6. Connect SHAP output to alert `top_features`.

### Strong LLM/RAG Upgrade

7. Add real LLM provider.
8. Add vector-based RAG.
9. Expand playbooks.
10. Run RAG vs no-RAG comparison on 10-20 cases.

### Strong Demo Upgrade

11. Improve dashboard alert detail view.
12. Add incident report generator.
13. Add screenshots to README.

## Suggested Milestones

| Milestone | Focus | Output |
|---|---|---|
| M1 | Full dataset pipeline | UNSW-NB15 processed and evaluated |
| M2 | Stronger ML | XGBoost/LightGBM comparison |
| M3 | Explainability | SHAP artifacts and per-alert evidence |
| M4 | Real LLM/RAG | Provider adapter and vector retrieval |
| M5 | Human evaluation | Expert scores and case study report |
| M6 | Demo polish | Dashboard, incident reports, README screenshots |

## Final Target State

The ideal final project should be describable as:

```text
A research-grade SOC assistant prototype that combines measurable ML-based intrusion detection, explainable alert evidence, RAG-grounded LLM explanations, human-centered triage support, and reproducible thesis evaluation artifacts.
```

The strongest final defense message should remain:

```text
The LLM is not the detector. The IDS/ML layer performs detection, and the RAG/LLM layer explains alerts using structured evidence and retrieved security knowledge.
```
