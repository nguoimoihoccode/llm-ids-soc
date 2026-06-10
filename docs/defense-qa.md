# Defense Q&A Notes

## 1. What is the main problem this thesis solves?

Answer:

> IDS and ML-based detectors can identify suspicious traffic, but their alerts are often difficult for analysts to understand quickly. This thesis addresses the gap between detection and analyst action by adding explainable alert intelligence and RAG-grounded LLM-style explanations.

## 2. What is the main contribution of the thesis?

Answer:

> The main contribution is an integrated research prototype that combines ML-based intrusion detection, explainable alert enrichment, RAG-grounded alert explanation, SOC dashboard visualization, and reproducible evaluation artifacts.

## 3. Why not let the LLM detect attacks directly?

Answer:

> Network-flow intrusion detection is a structured numerical classification problem. ML models can be evaluated with standard metrics such as accuracy, precision, recall, F1-score, and false positive rate. LLM outputs are harder to validate and may hallucinate. Therefore, this system uses the IDS/ML layer for detection and the LLM/RAG layer only for explanation and triage support.

## 4. What is the role of RAG in this system?

Answer:

> RAG retrieves relevant security playbooks before generating explanations. This grounds the explanation in known security guidance and helps reduce unsupported claims. The system compares template, no-RAG, and RAG-assisted explanations to evaluate whether RAG improves groundedness and actionability.

## 5. Does RAG completely prevent hallucination?

Answer:

> No. RAG reduces hallucination risk by providing trusted context, but it does not guarantee correctness. The quality of the explanation still depends on the retrieved documents, prompt design, and model behavior. That is why the system includes a hallucination safety criterion in the evaluation rubric.

## 6. How do you evaluate the IDS component?

Answer:

> The IDS component is evaluated using standard classification metrics: accuracy, precision, recall, F1-score, false positive rate, and confusion matrix. The system also exports model comparison tables and feature importance artifacts. The current fixture validates the pipeline; final experiments should use full UNSW-NB15 and CICIDS2017 or CSE-CIC-IDS2018 datasets.

## 7. The fixture models have perfect scores. Does that prove the model is excellent?

Answer:

> No. The perfect fixture scores only show that the pipeline works correctly on a small deterministic dataset. They should not be interpreted as final research performance. Real conclusions require full benchmark datasets with realistic class imbalance, noise, false positives, and false negatives.

## 8. Why use UNSW-NB15 and CICIDS2017?

Answer:

> They are widely used public IDS datasets with labeled traffic. UNSW-NB15 is suitable as a primary benchmark because it contains modern attack categories and network-flow features. CICIDS2017 or CSE-CIC-IDS2018 can be used as a secondary benchmark to test whether the workflow generalizes beyond one dataset.

## 9. What are the limitations of public IDS datasets?

Answer:

> Public IDS datasets may not fully represent real enterprise networks. They can contain synthetic traffic, outdated attack patterns, class imbalance, or dataset-specific artifacts. Therefore, results on public datasets should be interpreted as benchmark evidence, not proof of production readiness.

## 10. What is the difference between explainability and LLM explanation?

Answer:

> Explainability refers to technical evidence that supports a detection, such as feature importance, top features, confidence, and model metrics. LLM explanation converts this evidence into natural language, connects it with security knowledge, and recommends response actions. Explainability supports evidence; LLM explanation supports communication and triage.

## 11. How does the system improve alert interpretability?

Answer:

> Each alert is enriched with severity, confidence, technical reason, top evidence features, MITRE ATT&CK mapping, and triage priority. This gives analysts more context than a simple attack label and helps them understand why an alert matters.

## 12. Why include MITRE ATT&CK mapping?

Answer:

> MITRE ATT&CK provides a common language for describing attacker behavior. Mapping alerts to MITRE techniques helps analysts connect low-level network evidence to known adversary tactics and response playbooks.

## 13. How do you evaluate the LLM/RAG explanation component?

Answer:

> The explanation component is evaluated using a rubric with correctness, completeness, groundedness, actionability, hallucination safety, and latency. The system exports rubric scores, a RAG vs no-RAG summary, and incident case studies.

## 14. Why compare template, no-RAG, and RAG-assisted explanations?

Answer:

> The comparison separates the effect of each explanation strategy. Template explanations are deterministic and safe but limited. No-RAG explanations can be more fluent but may lack grounding. RAG-assisted explanations include retrieved security context and are expected to improve groundedness and actionability.

## 15. What is the role of the SOC dashboard?

Answer:

> The dashboard demonstrates how an analyst would view alerts, model metrics, evidence features, MITRE mappings, and explanation comparisons. It is not the main research contribution by itself; it is a presentation and triage interface for the backend workflow.

## 16. Is this system production-ready?

Answer:

> No. It is a research prototype. It does not include real-time packet capture, production SIEM integration, automatic containment, enterprise authentication, or production-scale monitoring. Its purpose is to demonstrate and evaluate the proposed architecture.

## 17. What makes this thesis different from a normal IDS project?

Answer:

> A normal IDS project usually focuses mainly on detection metrics. This thesis combines detection with explainable alert enrichment, RAG-grounded explanation, explanation-mode comparison, SOC visualization, and reproducible thesis artifacts. The contribution is the integrated workflow from detection to analyst understanding.

## 18. What makes this thesis different from a normal LLM chatbot project?

Answer:

> The LLM is not used as a generic chatbot or detector. It is constrained by structured alert fields and retrieved security playbooks. The system evaluates explanation quality using a rubric and keeps final detection responsibility in the measurable IDS/ML layer.

## 19. Why use baseline models instead of only deep learning?

Answer:

> Baseline models such as Logistic Regression, Decision Tree, and Random Forest are easier to train, interpret, and compare. They provide a reliable starting point for tabular IDS data. More advanced models such as XGBoost, LightGBM, or neural networks can be added later if they clearly improve the research evaluation.

## 20. Why is false positive rate important in IDS?

Answer:

> False positives are important because SOC analysts may receive many alerts. A detector with too many false positives creates alert fatigue and wastes investigation time. Therefore, IDS evaluation should consider not only accuracy but also precision, recall, F1-score, and false positive rate.

## 21. How does the system support reproducibility?

Answer:

> The project includes scripts for preprocessing, model training, report export, LLM rubric evaluation, RAG summary generation, and case study generation. It also saves artifacts such as metrics JSON, model comparison CSV, confusion matrix SVGs, feature importance CSVs, rubric scores, and markdown reports.

## 22. What would you improve first if you had more time?

Answer:

> The first priority would be full dataset evaluation using UNSW-NB15 and CICIDS2017 or CSE-CIC-IDS2018. The second priority would be adding instance-level explainability such as SHAP or LIME. The third priority would be integrating a real LLM provider or local LLM runtime and evaluating explanations with human review.

## 23. What are the biggest limitations of the current prototype?

Answer:

> The current prototype uses a small fixture dataset, baseline models, local-template LLM behavior, a small markdown playbook knowledge base, and deterministic rubric scoring. It does not yet include full benchmark experiments, real LLM evaluation, expert review, real-time traffic capture, or SIEM/SOAR integration.

## 24. How would you handle sensitive data if deployed in a real SOC?

Answer:

> Sensitive logs and network data should be minimized, anonymized, and protected. If an external LLM provider is used, sensitive fields should be redacted or processed locally. A local LLM or private deployment may be more appropriate for sensitive SOC environments.

## 25. Could the LLM give dangerous response recommendations?

Answer:

> Yes, if it is unconstrained. That is why the system grounds recommendations in playbooks and treats LLM output as analyst support, not automatic action. The prototype does not perform automatic blocking or containment. A human analyst remains responsible for final decisions.

## 26. Why include incident case studies?

Answer:

> Case studies help show how the system behaves for concrete alerts. They combine alert details, evidence features, MITRE mapping, explanation, recommended response, explanation comparison, and rubric scores. This supports qualitative analysis in addition to numerical metrics.

## 27. What are your final thesis claims?

Answer:

> The thesis claims that an integrated workflow combining ML-based IDS, explainable alert intelligence, RAG-grounded explanations, and SOC dashboard presentation is feasible and useful as a research prototype. It does not claim production readiness or final benchmark superiority until full dataset experiments are completed.

## 28. What is the safest one-sentence summary for the defense?

Answer:

> The IDS/ML layer detects suspicious traffic, while the RAG/LLM layer explains the alert and supports analyst triage without replacing human judgment or measurable detection.
