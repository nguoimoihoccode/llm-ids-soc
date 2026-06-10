# Thesis Proposal Draft

## Proposed Vietnamese Title

Xây dựng hệ thống phát hiện xâm nhập mạng kết hợp học máy có giải thích và mô hình ngôn ngữ lớn tăng cường truy hồi hỗ trợ phân tích cảnh báo an ninh.

## Proposed English Title

An Explainable Machine Learning and Retrieval-Augmented Large Language Model System for Network Intrusion Detection and Security Alert Analysis.

## 1. Background And Motivation

Network intrusion detection remains a critical task in cybersecurity operations. Intrusion Detection Systems (IDS) and machine learning models can identify suspicious network flows, but their outputs are often technical, fragmented, and difficult to triage quickly. Security analysts need not only a detection result, but also an explanation of why an event is suspicious, how it maps to known attack techniques, and what response actions should be considered.

Large Language Models (LLMs) provide strong natural language explanation and summarization capabilities. However, using an LLM as the primary detector for network-flow data is risky because IDS data is structured and numerical, while LLM outputs may hallucinate or be difficult to evaluate. A safer and more measurable design is to use machine learning for detection and classification, then use LLM/RAG as a post-detection assistant for explanation, triage, and response recommendation.

This thesis proposes a research prototype that combines ML-based intrusion detection, explainable alert intelligence, Retrieval-Augmented Generation (RAG), and a SOC-style dashboard.

## 2. Problem Statement

Existing IDS outputs often answer the question:

```text
Is this event suspicious?
```

But security operations also require answers to:

```text
Why is it suspicious?
Which evidence supports the alert?
Which MITRE ATT&CK technique is relevant?
How should the analyst prioritize it?
What response actions are recommended?
Does RAG improve LLM explanation quality?
```

The research problem is how to design and evaluate an IDS support system that preserves measurable ML-based detection while improving alert explanation and analyst triage through explainability and RAG-grounded LLM outputs.

## 3. Research Objectives

The main objective is to build and evaluate a research prototype for intrusion detection and security alert analysis.

Specific objectives:

1. Build a preprocessing and evaluation pipeline for IDS-style network-flow datasets.
2. Train and compare baseline ML models for intrusion detection.
3. Enrich IDS alerts with severity, confidence, top features, MITRE mapping, and triage priority.
4. Implement RAG-grounded LLM-style alert explanation.
5. Compare template, no-RAG, and RAG-assisted explanation modes.
6. Export reproducible evaluation artifacts for ML and LLM components.
7. Provide a SOC-style dashboard and defense-ready reports for demonstration.

## 4. Research Questions

RQ1: How do baseline ML models perform on IDS-style network-flow data using standard classification metrics?

RQ2: Can alert intelligence fields such as top features, MITRE mapping, and triage priority improve the interpretability of IDS alerts?

RQ3: Does RAG-grounded explanation improve LLM output quality compared with template-only and no-RAG explanations?

RQ4: Can the proposed prototype support a SOC-style incident triage workflow at research prototype level?

## 5. Scope

In scope:

- Offline IDS-style CSV datasets.
- Sample fixture dataset for deterministic demonstration.
- UNSW-NB15 as primary thesis dataset.
- CICIDS2017 or CSE-CIC-IDS2018 as secondary benchmark if time allows.
- Baseline ML models: Logistic Regression, Decision Tree, Random Forest.
- Optional advanced model: XGBoost or LightGBM.
- Alert intelligence: severity, confidence, top features, MITRE mapping, triage priority.
- RAG using local security playbooks and later MITRE/OWASP/CISA notes.
- LLM explanation comparison and rubric-based evaluation.
- SOC dashboard and exported reports.

Out of scope for the first version:

- Production realtime packet capture.
- Automatic response or blocking in a real network.
- Full SIEM/SOAR replacement.
- LLM fine-tuning.
- Claims that the LLM is the primary intrusion detector.

## 6. Proposed Methodology

### 6.1 Data Pipeline

The system loads IDS-style CSV data and applies preprocessing steps:

- Remove or replace NaN and infinite values.
- Encode categorical fields.
- Preserve labels for supervised learning.
- Export processed data for reproducible training.

### 6.2 ML-Based IDS Evaluation

The system trains and evaluates baseline models:

- Logistic Regression.
- Decision Tree.
- Random Forest.
- Optional XGBoost/LightGBM.

Metrics:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- False positive rate.
- Confusion matrix.

Artifacts:

- Metrics JSON.
- Model comparison CSV.
- Confusion matrix SVG.
- Feature importance CSV.

### 6.3 Alert Intelligence

Detection outputs are converted into enriched alerts containing:

- Attack type.
- Severity.
- Confidence.
- Technical reason.
- Top features.
- MITRE ATT&CK mapping.
- Triage priority.

### 6.4 LLM/RAG Explanation

The explanation layer compares three modes:

- Template explanation.
- LLM-style explanation without RAG.
- LLM-style explanation with RAG context.

RAG context comes from local playbooks and can later be extended with MITRE ATT&CK, OWASP, and CISA guidance.

### 6.5 LLM Evaluation

The LLM explanation outputs are evaluated using a rubric:

- Correctness.
- Completeness.
- Groundedness.
- Actionability.
- Hallucination safety.
- Latency.

Artifacts:

- LLM rubric scores CSV.
- RAG vs no-RAG summary report.
- Incident case studies report.

## 7. System Architecture

The system follows this high-level architecture:

```text
Dataset / Network Events
        -> Preprocessing
        -> IDS / ML Detection
        -> Alert Intelligence
        -> RAG Retrieval
        -> LLM Explanation
        -> SOC Dashboard
        -> Evaluation Reports
```

Detailed Mermaid diagrams are available in:

```text
docs/architecture-diagram.md
```

## 8. Expected Contributions

1. A reproducible IDS research pipeline for preprocessing, training, evaluation, and artifact export.
2. An alert intelligence layer that connects IDS output with explainable evidence and MITRE mapping.
3. A RAG-grounded LLM explanation workflow for security alert analysis.
4. A rubric-based framework for comparing template, no-RAG, and RAG-assisted explanations.
5. A SOC-style dashboard and defense-ready reports for demonstrating the approach.

## 9. Expected Results

Expected technical outputs:

- Working backend API.
- Working SOC dashboard.
- Processed dataset artifacts.
- Trained baseline models.
- Model comparison table.
- Confusion matrix figures.
- Feature importance reports.
- LLM rubric scores.
- RAG vs no-RAG summary.
- Incident case studies.

Expected research outcome:

- Evidence that ML is suitable for structured IDS detection.
- Evidence that RAG-grounded explanation improves groundedness and actionability compared with template-only or no-RAG explanations.

## 10. Six-Month Timeline

| Month | Focus | Main Deliverables |
|---|---|---|
| 1 | Literature review and architecture | Proposal, system design, MVP demo |
| 2 | Dataset preprocessing and baseline ML | UNSW-NB15 preprocessing, baseline metrics |
| 3 | Model evaluation and artifacts | Model comparison, confusion matrices, feature importance |
| 4 | Alert intelligence and explainability | MITRE mapping, top features, triage priority |
| 5 | RAG/LLM assistant and dashboard | Explanation comparison, rubric scoring, SOC UI |
| 6 | Evaluation and thesis preparation | Final reports, case studies, slides, defense demo |

## 11. Current Prototype Status

Implemented:

- FastAPI backend.
- React SOC dashboard.
- Sample IDS events.
- Dataset registry.
- UNSW-NB15-style preprocessing fixture.
- Baseline model training on fixture data.
- Metrics export.
- Confusion matrix export.
- Feature importance export.
- Alert intelligence fields.
- RAG-style local playbooks.
- Grounded explanation endpoint.
- Explanation comparison endpoint.
- LLM rubric scoring.
- RAG summary report.
- Incident case studies report.
- Demo script and defense Q&A notes.

Remaining major work:

- Full UNSW-NB15 dataset ingestion.
- Secondary dataset benchmark.
- More robust model validation.
- Optional SHAP/LIME.
- External LLM provider adapter.
- Larger expert-reviewed LLM evaluation set.

## 12. Risks And Mitigation

| Risk | Mitigation |
|---|---|
| Dataset is large or inconsistent | Start with UNSW-NB15, then use curated subsets if needed |
| ML scores are unstable | Compare multiple models and report limitations |
| LLM hallucination | Use structured alert context, RAG playbooks, and hallucination safety rubric |
| Scope becomes too broad | Keep realtime capture, fine-tuning, and production SIEM integration out of scope |
| API quota limits | Use local-template/Ollama or cached responses for evaluation |

## 13. Conclusion

This thesis proposes a balanced research prototype that combines measurable ML-based intrusion detection with explainable, RAG-grounded LLM alert analysis. The system is designed to support SOC-style triage while maintaining a clear separation between detection and explanation.
