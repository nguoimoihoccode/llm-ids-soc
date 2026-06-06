# Evaluation Plan

## IDS Evaluation

Datasets:

- UNSW-NB15.
- CICIDS2017 or CSE-CIC-IDS2018.

Models:

- Logistic Regression.
- Decision Tree.
- Random Forest.
- XGBoost or LightGBM.

Metrics:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- ROC-AUC where applicable.
- False positive rate.
- Confusion matrix.
- Training time.
- Prediction latency.

Required outputs:

- `models/metrics/<dataset>-<model>.json`.
- `reports/figures/<dataset>-<model>-confusion-matrix.png`.
- `reports/evaluation/model-comparison.csv`.

## Explainability Evaluation

Methods:

- Built-in feature importance for tree models.
- SHAP or LIME if time allows.

Outputs:

- Top features per attack class.
- Top features per selected incident.
- Explanation screenshots in dashboard.

## LLM/RAG Evaluation

Modes:

- Template only.
- LLM without RAG.
- LLM with RAG.

Rubric, 1-5 scale:

- Correctness: explanation matches attack type and evidence.
- Completeness: includes cause, impact, and response.
- Groundedness: stays within alert and retrieved context.
- Actionability: recommendations are concrete and feasible.
- Hallucination: avoids invented facts, tools, IPs, or CVEs.
- Latency: response time is acceptable for analyst workflow.

Case study size:

- Minimum: 20 incidents.
- Target: 50 incidents.

Required outputs:

- `reports/evaluation/llm-rubric-scores.csv`.
- `reports/evaluation/incident-case-studies.md`.
- `reports/evaluation/rag-vs-no-rag-summary.md`.
