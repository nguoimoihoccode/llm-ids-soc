# Chapter 7: Conclusion And Future Work

## 7.1 Introduction

This chapter concludes the thesis by summarizing the research, answering the research questions, restating the main contributions, and identifying future work. The thesis investigated how machine-learning-based intrusion detection can be combined with explainable alert intelligence and RAG-grounded LLM-style explanations to support SOC alert analysis.

The project was implemented as a research prototype rather than a production IDS or SIEM platform. The prototype demonstrates an end-to-end workflow from IDS-style data processing to alert generation, explanation, dashboard visualization, and evaluation artifact export.

## 7.2 Summary Of The Research

The thesis started from the observation that IDS alerts often provide insufficient context for analysts. A detector may identify suspicious traffic, but the analyst still needs to understand why the event is suspicious, how serious it is, which attack technique it resembles, and what response actions should be considered.

To address this problem, the thesis proposed a layered architecture:

```text
Network-flow data
        -> preprocessing
        -> IDS/ML detection and evaluation
        -> alert intelligence
        -> RAG retrieval
        -> LLM-style explanation
        -> SOC dashboard and report artifacts
```

The detection layer is responsible for measurable intrusion detection using structured data and supervised machine-learning models. The alert intelligence layer enriches alerts with severity, confidence, evidence features, MITRE ATT&CK mapping, and triage priority. The RAG/LLM layer generates analyst-readable explanations using structured alert context and retrieved security playbooks. The dashboard and exported reports support demonstration, evaluation, and thesis defense.

The prototype currently includes:

- FastAPI backend APIs for events, alerts, datasets, explanations, and metrics.
- React/Vite frontend dashboard for SOC-style visualization.
- UNSW-NB15-style preprocessing support.
- Baseline ML model training for Logistic Regression, Decision Tree, and Random Forest.
- Exported model metrics, model comparison reports, confusion matrices, and feature importance artifacts.
- Local playbook-based RAG context.
- Template, no-RAG, and RAG-assisted explanation comparison.
- Rubric-based LLM explanation scoring.
- RAG summary and incident case study exports.

## 7.3 Answers To Research Questions

This section answers the research questions introduced in Chapter 1.

### 7.3.1 RQ1: How Do Baseline Machine Learning Models Perform On IDS-Style Network-Flow Data?

The prototype demonstrates that IDS-style data can be preprocessed, used to train baseline supervised models, and evaluated with standard classification metrics. The current fixture-based evaluation produced complete metric artifacts for Logistic Regression, Decision Tree, and Random Forest.

However, the current fixture results should not be interpreted as final model performance because the fixture dataset is intentionally small and deterministic. The main result for RQ1 at the current stage is that the model evaluation workflow is operational and reproducible. Final performance claims require full experiments using UNSW-NB15 and CICIDS2017 or CSE-CIC-IDS2018.

### 7.3.2 RQ2: Can Alert Intelligence Fields Improve The Interpretability Of IDS Alerts?

The prototype shows that alert intelligence fields can make IDS alerts easier to understand. Instead of presenting only a class label or attack name, the system enriches each alert with severity, confidence, technical reason, top evidence features, MITRE ATT&CK mapping, and triage priority.

These fields help translate detection output into analyst-oriented context. They do not replace formal model explainability, but they provide a practical bridge between ML results and SOC triage. In future work, these alert fields can be strengthened by connecting them to instance-level explainability methods such as SHAP or LIME.

### 7.3.3 RQ3: Does RAG-Grounded Explanation Improve LLM Output Quality Compared With Template-Only And No-RAG Modes?

The current prototype provides a repeatable framework for comparing explanation modes. It generates template, no-RAG, and RAG-assisted explanations for the same alerts and scores them using a rubric that includes correctness, completeness, groundedness, actionability, hallucination safety, and latency.

The current deterministic evaluation indicates that RAG-assisted explanations provide stronger grounding because they include retrieved playbook context. This supports the research motivation that RAG can help constrain LLM-style explanations and make them more evidence-based.

However, final claims about LLM quality require evaluation with a real LLM provider or local model runtime, a larger incident set, and preferably human expert review. Therefore, the answer to RQ3 is that RAG-grounded explanation is promising and the prototype provides the framework to evaluate it, but stronger empirical validation is required.

### 7.3.4 RQ4: Can The Proposed Prototype Support A SOC-Style Incident Triage Workflow At Research Prototype Level?

The prototype supports a SOC-style triage workflow at research prototype level. It allows suspicious events to be converted into enriched alerts, explains the alerts using structured evidence and retrieved knowledge, displays the results in a dashboard, and exports reports for evaluation.

The prototype does not aim to replace a production SIEM or IDS. It does not perform real-time packet capture, automatic containment, or full enterprise integration. Its contribution is to demonstrate how IDS/ML output can be connected with explainability, RAG-assisted explanation, and analyst-facing presentation.

## 7.4 Main Contributions

The thesis makes the following contributions.

First, it provides a reproducible research prototype for ML-based network intrusion detection and alert analysis. The prototype includes backend services, frontend dashboard, scripts, tests, and generated artifacts.

Second, it implements an alert intelligence layer that enriches IDS alerts with evidence features, severity, confidence, MITRE mapping, and triage priority. This improves the interpretability of alerts for SOC-style analysis.

Third, it proposes and implements a RAG-grounded explanation workflow for security alerts. The system retrieves local security playbooks and uses them to produce grounded explanations and response recommendations.

Fourth, it introduces an evaluation workflow for comparing explanation modes. Template, no-RAG, and RAG-assisted explanations can be compared using a rubric and exported as reproducible reports.

Fifth, it provides thesis-supporting artifacts such as model comparison CSV files, confusion matrix figures, feature importance reports, LLM rubric scores, RAG summaries, incident case studies, and dashboard views.

## 7.5 Limitations

Several limitations remain.

The current dataset is a small fixture dataset. It is useful for validating the pipeline, but it is not sufficient for final research conclusions about detection performance.

The current model set is limited to baseline models. Logistic Regression, Decision Tree, and Random Forest are useful starting points, but additional experiments may be needed to compare stronger models.

The current explainability artifacts are basic. Tree-based feature importance helps with model inspection, but it does not fully explain individual predictions.

The current LLM behavior is implemented using deterministic local templates. This allows reproducible testing, but it does not measure the behavior of real LLM systems.

The current RAG knowledge base is small. A larger playbook collection would improve coverage across more attack techniques and response scenarios.

The current LLM evaluation rubric is deterministic and does not yet include human expert review. Expert feedback would be valuable for validating explanation usefulness and actionability.

The prototype does not include real-time network capture, production SIEM/SOAR integration, or automatic incident response. These are outside the current thesis scope.

## 7.6 Future Work

Future work can improve the project in several directions.

### 7.6.1 Full Dataset Evaluation

The most important next step is to run full experiments on public IDS datasets such as UNSW-NB15 and CICIDS2017 or CSE-CIC-IDS2018. This would allow the thesis to report realistic accuracy, precision, recall, F1-score, false positive rate, and confusion matrix results.

### 7.6.2 Additional Machine Learning Models

Future experiments can include stronger tabular models such as XGBoost, LightGBM, or CatBoost. These models often perform well on structured cybersecurity datasets and would provide a stronger comparison against baseline models.

### 7.6.3 Instance-Level Explainability

The explainability layer can be improved using SHAP or LIME. These methods would allow the system to explain why a specific alert was classified as malicious, not only which features are globally important.

### 7.6.4 Real LLM Provider Integration

The local-template explanation provider can be replaced or extended with real LLM providers such as Gemini, OpenAI, or a local Ollama model. This would allow the thesis to evaluate actual LLM behavior, latency, and hallucination risks.

### 7.6.5 Stronger RAG Retrieval

The current markdown playbook retrieval can be extended with a vector database such as FAISS or ChromaDB. This would support semantic retrieval and improve the quality of context passed to the LLM.

### 7.6.6 Expanded Security Knowledge Base

The knowledge base can be expanded with more MITRE ATT&CK techniques, response playbooks, detection notes, and incident handling procedures. A richer knowledge base would make RAG explanations more useful across more alert types.

### 7.6.7 Human Expert Evaluation

Future work should include evaluation by security practitioners, instructors, or advisors. Human review can assess whether explanations are understandable, actionable, and trustworthy in realistic SOC triage scenarios.

### 7.6.8 SIEM And SOC Tool Integration

The prototype can eventually be integrated with SIEM or log management tools. This could allow alerts from real security tools to be enriched and explained using the proposed workflow.

### 7.6.9 Real-Time And Streaming Extension

A future version could process streaming logs or network-flow records in near real time. This would make the system closer to operational SOC usage, although it would require additional engineering for scalability, reliability, and latency control.

## 7.7 Final Remarks

This thesis explored the integration of ML-based intrusion detection, explainable alert intelligence, RAG-grounded LLM-style explanation, and SOC dashboard visualization. The key principle of the work is the separation of detection and explanation. The IDS/ML layer remains responsible for detecting suspicious activity, while the LLM/RAG layer assists analysts by explaining alerts and suggesting response actions based on retrieved security knowledge.

The current prototype demonstrates that this architecture is feasible and can be evaluated through reproducible artifacts. Although full dataset experiments and real LLM evaluation remain future work, the project establishes a strong foundation for studying how explainable ML and grounded language models can support security alert analysis.

The final conclusion is that LLMs should not replace measurable IDS detection mechanisms. Instead, they are most useful as a controlled explanation and triage support layer when combined with structured alert evidence, security knowledge retrieval, and analyst oversight.
