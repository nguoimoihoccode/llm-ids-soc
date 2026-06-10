# Chapter 6: Discussion

## 6.1 Introduction

This chapter discusses the meaning of the results and implementation described in the previous chapters. Chapter 5 presented the current fixture-based evaluation artifacts for the IDS pipeline, explainability outputs, and LLM/RAG explanation workflow. Because the current results are based on a small deterministic fixture dataset, the discussion focuses on what the prototype demonstrates, what cannot yet be concluded, and how the system can be interpreted as a research platform for the final thesis experiments.

The main argument of this chapter is that the project should be understood as an integrated SOC-oriented workflow rather than as only a model accuracy experiment. The IDS and ML layer performs detection and classification. The alert intelligence layer converts detection output into analyst-readable context. The RAG/LLM layer explains the alert using retrieved security knowledge. The dashboard and reports then make the result visible and reproducible.

## 6.2 Interpretation Of IDS Results

The current IDS results show that the preprocessing and model evaluation workflow is functional. The system can load IDS-style CSV data, process categorical and numerical features, train baseline supervised models, calculate classification metrics, and export model artifacts. This is an important result because it confirms that the technical foundation for full dataset experiments is already in place.

The current fixture metrics show perfect scores for Logistic Regression, Decision Tree, and Random Forest. These scores should not be interpreted as final research performance. They are a consequence of using a very small fixture dataset designed to validate the pipeline. In a full dataset such as UNSW-NB15 or CICIDS2017, the expected results will be more realistic and will likely include false positives, false negatives, class imbalance effects, and differences between model families.

The value of the current IDS results is therefore procedural rather than statistical. They demonstrate that:

- The preprocessing pipeline produces trainable data.
- Multiple supervised models can be trained consistently.
- Metrics are exported in a reproducible format.
- Confusion matrices and feature importance artifacts can be generated.
- The evaluation workflow can be repeated when larger datasets are added.

This distinction is important for the thesis defense. The prototype has not yet proven that one model is superior on real traffic. It has proven that the research workflow needed to make that comparison is implemented.

## 6.3 Interpretation Of Explainability Results

Explainability is addressed at two levels in the prototype. The first level is model-oriented explainability, represented by feature importance artifacts for tree-based models. The second level is alert-oriented explainability, represented by top evidence features, MITRE ATT&CK mapping, severity, confidence, and triage priority.

Feature importance artifacts help identify which features influence the trained model. For example, in a tree-based model, high-importance features may indicate that packet rate, byte rate, protocol, port, or connection duration are useful for distinguishing malicious and benign samples. These artifacts are useful for model inspection and for validating whether the model relies on plausible network-security features.

Alert-oriented explainability has a different purpose. It is designed for analysts rather than model developers. Instead of exposing only raw model internals, the system presents evidence in a SOC-friendly form:

```text
Attack type
Severity
Confidence
Top evidence features
MITRE ATT&CK mapping
Triage priority
Recommended response
```

This design helps bridge the gap between ML output and analyst action. A model prediction alone may say that traffic is malicious. An enriched alert explains why the event matters, what behavior it resembles, and how it should be prioritized.

The current implementation uses deterministic mappings and sample evidence features. In the final system, these fields can be connected more directly to model explanations such as SHAP values, LIME explanations, or model-specific feature contributions. This would strengthen the connection between ML explainability and analyst-facing explanations.

## 6.4 Interpretation Of LLM/RAG Results

The LLM/RAG evaluation demonstrates that explanation quality can be compared across different explanation modes. The prototype compares template explanations, LLM-style explanations without RAG, and LLM-style explanations with RAG context. The current rubric evaluates correctness, completeness, groundedness, actionability, hallucination safety, and latency.

The most important finding from the current prototype is not that the local template provider behaves like a production LLM. Instead, the important finding is that the system has a repeatable mechanism for comparing explanation strategies. Each alert can be passed through multiple explanation modes, scored using the same rubric, and exported into evaluation artifacts.

The RAG-assisted explanation mode is expected to perform better on groundedness because it includes retrieved playbook context. This is aligned with the thesis motivation: LLMs can produce fluent but unsupported explanations if they are not constrained by trusted knowledge. RAG helps reduce this risk by attaching explanation output to explicit security playbooks.

However, RAG does not automatically guarantee correctness. The explanation is only as reliable as the retrieved context and the prompt design. If the knowledge base is incomplete, outdated, or mismatched to the alert, the generated explanation may still be weak. For this reason, the final thesis should treat RAG as a grounding mechanism, not as a complete solution to hallucination.

The safest interpretation is:

- The IDS/ML layer detects suspicious events.
- The RAG layer retrieves relevant security knowledge.
- The LLM layer explains the alert using alert evidence and retrieved context.
- The analyst remains responsible for final judgment and response.

This keeps the system aligned with SOC practice and avoids overstating the role of the LLM.

## 6.5 Practical Value For SOC Analysts

The prototype is designed around SOC analyst workflow. In many environments, analysts receive a large number of alerts with limited context. Raw alerts often require manual investigation before the analyst can understand the likely attack type, severity, affected assets, and recommended response. This creates alert fatigue and slows triage.

The proposed system provides practical value in several ways.

First, enriched alerts reduce the amount of manual interpretation required. The analyst can immediately see severity, confidence, evidence features, MITRE mapping, and triage priority.

Second, RAG-assisted explanations provide a readable summary of the incident. Instead of forcing the analyst to manually connect raw features to attack behavior, the system explains the likely meaning of the alert and recommends response steps.

Third, the dashboard provides a single view of alert information, model metrics, and explanation comparison. This supports both operational demonstration and research evaluation.

Fourth, the report artifacts support reproducibility. Model comparison tables, confusion matrices, feature importance files, rubric scores, RAG summaries, and case studies can be included in the thesis or appendix.

The practical contribution is therefore not only detection. The system improves the path from detection to understanding.

## 6.6 Limitations Of The Current Prototype

The current prototype has several limitations that must be acknowledged.

### 6.6.1 Fixture Dataset Limitation

The current experiments use a small fixture dataset. This dataset is useful for development and pipeline validation, but it cannot support final claims about model accuracy, robustness, or generalization. Full experiments must use larger public IDS datasets.

### 6.6.2 Limited Model Coverage

The current models are Logistic Regression, Decision Tree, and Random Forest. These are useful baselines, but the final thesis may benefit from additional models such as XGBoost, LightGBM, or neural network baselines. More advanced models should be added only if they contribute clearly to the research questions.

### 6.6.3 Limited Explainability Depth

Feature importance is currently exported for tree-based models. This provides basic explainability, but it does not fully explain individual predictions. Instance-level explainability using SHAP or LIME would make the system stronger because it could show which features influenced a specific alert.

### 6.6.4 Local LLM Simulation

The current LLM behavior is implemented through deterministic local templates. This is useful for reproducible development and testing, but it does not measure real LLM behavior. Final evaluation should include an external provider or local model runtime if the thesis claims involve LLM quality.

### 6.6.5 Limited RAG Knowledge Base

The current RAG knowledge base uses local markdown playbooks. These playbooks demonstrate the concept but are not yet a complete security knowledge base. A richer knowledge base could include more attack types, MITRE techniques, response procedures, and organization-specific playbooks.

### 6.6.6 Lack Of Human Expert Evaluation

The current rubric is deterministic. It validates the evaluation workflow, but final claims about explanation usefulness should ideally involve human review from a security practitioner, advisor, or evaluator.

### 6.6.7 No Real-Time Network Capture

The prototype works with CSV-style network-flow data and sample events. It does not yet capture live traffic or integrate with real SIEM tooling. This is acceptable for the thesis scope, but it limits operational realism.

## 6.7 Research Implications

The project supports several research implications.

First, IDS research should not focus only on classification metrics. Accuracy, precision, recall, F1-score, and false positive rate are important, but SOC usefulness also depends on interpretability, prioritization, and response guidance.

Second, LLMs are more appropriate as an analyst-assistance layer than as the primary detector. Detection requires consistent and measurable behavior. LLM-generated text is better suited for explanation, summarization, and guidance when constrained by structured alert evidence and retrieved knowledge.

Third, RAG provides a practical way to connect LLM explanations with domain knowledge. In a security context, this is especially important because unsupported claims can mislead analysts. Grounding explanations in playbooks makes the output easier to audit.

Fourth, the integration of IDS, explainability, RAG, and dashboard artifacts creates a broader evaluation problem. The final thesis should evaluate not only whether the detector works, but also whether explanations are grounded, actionable, and useful for triage.

## 6.8 Engineering Implications

From an engineering perspective, the prototype shows the value of modular design. The backend separates data loading, preprocessing, model training, metric calculation, alert generation, RAG retrieval, explanation generation, and report export into focused services. This makes the system easier to test and extend.

The CLI scripts also support reproducibility. A researcher can rerun preprocessing, model training, report export, LLM scoring, RAG summary generation, and case study generation using explicit commands. This is important because thesis results should be repeatable rather than manually assembled.

The frontend dashboard supports demonstration. It gives a clear visual explanation of the system workflow and makes the project easier to present during defense. However, the dashboard should remain secondary to the research contribution. Its purpose is to expose and demonstrate the backend workflow, not to become the main thesis claim.

The current architecture also makes future extensions feasible. Full datasets, additional models, SHAP/LIME explanations, vector database retrieval, real LLM providers, and SIEM integrations can be added without rewriting the entire system.

## 6.9 Comparison With Traditional IDS Workflow

A traditional IDS workflow often produces alerts with limited explanation. The analyst receives fields such as source IP, destination IP, port, signature, severity, and timestamp. The analyst must then manually investigate logs, search documentation, map the event to attack behavior, and decide how to respond.

The proposed workflow adds several layers:

| Workflow Element | Traditional IDS | Proposed Prototype |
|---|---|---|
| Detection | Signature or ML output | Rule-based demo plus ML pipeline |
| Alert context | Basic fields | Severity, confidence, top features, MITRE, priority |
| Explanation | Often manual | Template and RAG-assisted explanation |
| Knowledge support | Analyst searches manually | Retrieved playbook context |
| Evaluation | Detection metrics | Detection metrics plus explanation rubric |
| Reporting | Tool-specific output | Reproducible CSV, JSON, SVG, and Markdown artifacts |

The proposed system does not replace IDS tools. Instead, it adds an intelligence layer above detection output. This makes the system more suitable for explaining alerts and supporting triage.

## 6.10 Lessons Learned

Several lessons emerged from the prototype implementation.

First, an end-to-end research workflow is more valuable than isolated components. A model training script alone is not enough for a thesis about SOC assistance. The project needs preprocessing, detection, explainability, RAG, dashboard presentation, and evaluation artifacts.

Second, reproducibility should be designed from the beginning. Exported metrics, reports, figures, and case studies make it easier to support thesis claims with evidence.

Third, fixture data is useful for development but dangerous if misinterpreted. It helps validate the pipeline quickly, but final claims require larger benchmark datasets.

Fourth, LLM integration must be scoped carefully. The LLM should not be presented as a detector. Its strongest role is explanation and triage support, especially when grounded by retrieved playbooks.

Fifth, the dashboard is useful for communication. It helps reviewers and examiners understand the system workflow quickly, but the thesis must still be supported by rigorous experiments and evaluation artifacts.

## 6.11 Summary

This chapter discussed the meaning of the current prototype results. The IDS results validate the preprocessing, training, and metric export workflow, but they do not yet represent final model performance. The explainability layer improves analyst understanding through feature importance artifacts, top evidence features, MITRE mapping, and triage priority. The LLM/RAG layer demonstrates a structured approach to generating grounded alert explanations, while keeping detection responsibility in the IDS/ML layer.

The chapter also identified important limitations, including the small fixture dataset, limited model coverage, local LLM simulation, limited RAG knowledge base, lack of human expert evaluation, and absence of real-time traffic capture. These limitations define the next steps for completing the thesis evaluation.

Overall, the prototype demonstrates a feasible architecture for combining ML-based IDS, explainable alerts, RAG-assisted explanations, and SOC dashboard presentation. The next chapter concludes the thesis and outlines future work.
