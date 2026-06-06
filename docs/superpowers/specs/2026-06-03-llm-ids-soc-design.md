# LLM IDS SOC Design

## Objective

Build a new research prototype named `llm-ids-soc` for a master's thesis on combining machine learning and large language models in intrusion detection and network security.

The expanded 5-6 month scope is a balanced research system: multi-dataset ML IDS, explainable alert intelligence, RAG-backed LLM analysis, SOC dashboard, and formal evaluation.

## Scope

The system focuses on offline network-flow IDS datasets, not realtime packet capture. Machine learning performs detection/classification. LLM/RAG performs explanation, incident summarization, response recommendation, and report generation.

In scope for the full thesis:

- UNSW-NB15 preprocessing and model evaluation.
- CICIDS2017 or CSE-CIC-IDS2018 secondary benchmark.
- Logistic Regression, Random Forest, and XGBoost or LightGBM comparison.
- Explainability with feature importance and optional SHAP/LIME.
- Alert intelligence with severity, confidence, MITRE mapping, and triage priority.
- RAG over local playbooks and selected MITRE/OWASP/CISA notes.
- LLM evaluation using correctness, completeness, groundedness, actionability, hallucination, and latency.

Out of scope for the first thesis version:

- Production realtime packet capture.
- Full SIEM replacement.
- LLM fine-tuning.
- Automated containment in a real network.

## Architecture

```text
Dataset CSV
  -> preprocessing/training pipeline
  -> IDS prediction output
  -> alert generator
  -> FastAPI backend
  -> React SOC dashboard
  -> LLM/RAG explanation module
```

## Components

- Data module: load, validate, clean, and normalize IDS-style CSV rows.
- IDS module: expose a stable interface for rule-based MVP now and ML models later.
- Alert module: convert detections into structured security alerts.
- LLM module: generate grounded explanations from alert context and playbooks.
- RAG module: retrieve relevant markdown playbook snippets by attack type.
- Dashboard: show overview cards, alert table, alert detail, metrics placeholder, and LLM explanation.

## Research Questions

- RQ1: How do traditional ML models compare on network-flow intrusion detection across public datasets?
- RQ2: Can explainability signals improve analyst understanding of IDS alerts?
- RQ3: Does RAG improve LLM alert explanations compared with a plain LLM prompt and template-only explanation?
- RQ4: Can the combined prototype support a SOC-style incident triage workflow at research prototype level?

## Data Plan

Development starts with sample CSV logs. Research evaluation should use UNSW-NB15 first and CICIDS2017 for stronger evaluation once preprocessing is stable.

Dataset phases:

- Phase 1: sample CSV for deterministic MVP and UI demos.
- Phase 2: UNSW-NB15 for first reproducible ML experiments.
- Phase 3: CICIDS2017 or CSE-CIC-IDS2018 for secondary validation.
- Phase 4: curated incident cases derived from model predictions for LLM/RAG evaluation.

## Evaluation Plan

IDS evaluation uses accuracy, precision, recall, F1-score, false positive rate, and confusion matrix. LLM evaluation uses correctness, completeness, groundedness, actionability, hallucination, and response latency. Compare template explanations, LLM without RAG, and LLM with RAG.

Required thesis artifacts:

- Dataset summary tables.
- Model comparison tables.
- Confusion matrices.
- Feature importance or SHAP/LIME figures.
- LLM/RAG evaluation rubric table.
- Incident case-study appendix.
- Dashboard screenshots.

## Constraints

- Do not claim the LLM is the primary detector.
- Keep MVP offline and reproducible.
- Avoid fine-tuning in the first implementation.
- Keep dashboard features limited to thesis/demo needs.
