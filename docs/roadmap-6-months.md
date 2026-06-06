# Six-Month Thesis Roadmap

## Target

Build a balanced master's thesis project: ML-based IDS, explainable alert intelligence, RAG/LLM incident analysis, SOC dashboard, and reproducible evaluation.

## Month 1: Foundation and Literature

Goals:

- Finalize research questions and thesis title.
- Review IDS, ML, XAI, SOC automation, and LLM/RAG cybersecurity literature.
- Stabilize project architecture and sample-data MVP.

Deliverables:

- Thesis proposal draft.
- System architecture diagram.
- Dataset selection note.
- Running MVP with sample alerts.

Exit criteria:

- Backend tests pass.
- Frontend builds.
- Advisor can understand the research contribution from the proposal.

## Month 2: UNSW-NB15 Data Pipeline and Baselines

Goals:

- Add UNSW-NB15 ingestion.
- Clean missing, infinite, and categorical fields.
- Train baseline models.

Models:

- Logistic Regression.
- Decision Tree.
- Random Forest.

Deliverables:

- Processed dataset artifacts.
- Baseline metrics JSON/CSV.
- Confusion matrices.

Exit criteria:

- Reproducible command trains and evaluates models.
- Metrics are saved under `models/metrics`.

## Month 3: Advanced IDS and Cross-Dataset Validation

Goals:

- Add XGBoost or LightGBM.
- Add CICIDS2017 or CSE-CIC-IDS2018 benchmark.
- Compare model robustness across datasets.

Deliverables:

- Multi-model comparison table.
- Secondary dataset preprocessing notes.
- Best-model selection rationale.

Exit criteria:

- At least two datasets evaluated.
- At least three supervised models compared.

## Month 4: Explainability and Alert Intelligence

Goals:

- Add feature importance and optional SHAP/LIME.
- Convert predictions into enriched alerts.
- Add MITRE mapping and triage priority.

Deliverables:

- Alert schema v2.
- Feature attribution artifacts.
- MITRE mapping playbooks.
- Alert detail dashboard page.

Exit criteria:

- Each alert can explain why the model classified it as suspicious.
- Alerts contain severity, confidence, top features, and response priority.

## Month 5: RAG/LLM Security Assistant and Dashboard

Goals:

- Integrate Gemini/OpenAI/Ollama provider adapter.
- Add RAG over playbooks and security notes.
- Complete SOC dashboard workflows.

LLM comparison modes:

- Template explanation.
- LLM without RAG.
- LLM with RAG.

Deliverables:

- LLM explanation API.
- RAG retrieval module.
- Incident report generator.
- Dashboard for alerts, metrics, explanations, and reports.

Exit criteria:

- Same alert can be explained using all three modes.
- Dashboard can support a full demo script.

## Month 6: Evaluation, Thesis Writing, and Defense Prep

Goals:

- Evaluate IDS and LLM components.
- Write thesis chapters.
- Harden demo.
- Prepare slides and defense answers.

Deliverables:

- Final experiment results.
- LLM rubric scores for 20-50 incident cases.
- Thesis draft.
- Defense slide deck.
- Demo script.

Exit criteria:

- All experiments reproducible.
- Thesis has clear contribution, limitations, and future work.
- Demo runs from clean setup instructions.

## Risk Control

- If CICIDS2017 processing is too heavy, use a curated subset or CSE-CIC-IDS2018 sampled CSV.
- If XGBoost/LightGBM setup is slow, keep Random Forest as primary model.
- If vector RAG is unstable, use deterministic keyword retrieval over curated playbooks.
- If LLM API quota is limited, cache case-study responses for evaluation.
