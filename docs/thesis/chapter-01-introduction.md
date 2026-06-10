# Chapter 1: Introduction

## 1.1 Background

Cybersecurity has become an essential concern for modern organizations as networked systems continue to grow in scale, complexity, and exposure. Organizations depend on distributed applications, cloud infrastructure, remote access services, Internet-facing APIs, and interconnected enterprise systems. These environments increase productivity and flexibility, but they also expand the attack surface available to adversaries.

Network intrusion detection is one of the core tasks in security monitoring. Intrusion Detection Systems (IDS) are designed to identify suspicious or malicious activity by analyzing network traffic, logs, or host events. Traditional IDS approaches include signature-based detection, which identifies known patterns of attacks, and anomaly-based detection, which identifies deviations from normal behavior. Machine learning has been widely studied as a way to improve intrusion detection, especially for network-flow datasets where features such as packet counts, byte rates, connection duration, protocol, and flag counts can indicate suspicious behavior.

However, detection alone is not enough in practical security operations. Security analysts in a Security Operations Center (SOC) must understand the meaning of alerts, determine their priority, map them to known attack techniques, and decide response actions. IDS and ML-based systems often produce outputs such as class labels, probabilities, or technical feature values. These outputs may be useful for detection, but they are not always easy to interpret or act upon.

Recent advances in Large Language Models (LLMs) have created new opportunities for cybersecurity workflows. LLMs can summarize technical information, generate natural language explanations, answer analyst questions, and produce incident reports. Nevertheless, using LLMs directly as intrusion detectors is risky because network-flow detection is primarily a structured numerical classification problem, while LLM responses may be difficult to validate and may suffer from hallucination. A more reliable approach is to separate detection and explanation: machine learning performs the detection task, while LLMs assist with post-detection explanation and triage.

This thesis investigates such a combined approach. It proposes a research prototype that integrates ML-based intrusion detection, explainable alert intelligence, Retrieval-Augmented Generation (RAG), and LLM-style alert explanation within a SOC dashboard.

## 1.2 Problem Statement

IDS alerts often answer whether an event may be suspicious, but analysts also need to understand why an event is suspicious and how to respond. A basic alert such as `Brute Force` or `DDoS` may not provide enough context for effective triage. Analysts need information such as:

- Which technical features contributed to the detection?
- How confident is the detection?
- What is the severity and triage priority?
- Which MITRE ATT&CK technique is relevant?
- What response actions should be considered?
- Can an explanation be generated in a way that is grounded in the alert evidence and security knowledge?

At the same time, LLM-generated explanations must be handled carefully. If an LLM produces unsupported claims, invented indicators, or generic recommendations, it may reduce trust and introduce operational risk. Therefore, an effective system should constrain LLM outputs using structured alert context and retrieved security knowledge.

The central problem addressed in this thesis is how to design and evaluate a system that combines measurable ML-based intrusion detection with explainable, RAG-grounded LLM support for security alert analysis.

## 1.3 Research Objectives

The main objective of this thesis is to build and evaluate a research prototype for network intrusion detection and alert analysis that combines machine learning, explainable alert evidence, and LLM/RAG-based explanation.

The specific objectives are:

1. Develop a data preprocessing pipeline for IDS-style network-flow datasets.
2. Train and compare baseline ML models for intrusion detection.
3. Generate enriched security alerts from detection results.
4. Add explainable alert intelligence, including top features, severity, confidence, MITRE mapping, and triage priority.
5. Implement RAG-grounded LLM-style explanations for alerts.
6. Compare template, no-RAG, and RAG-assisted explanation modes.
7. Evaluate LLM explanations using a rubric covering correctness, completeness, groundedness, actionability, hallucination safety, and latency.
8. Provide a SOC-style dashboard and reproducible evaluation artifacts for demonstration and thesis discussion.

## 1.4 Research Questions

This thesis is guided by the following research questions:

**RQ1:** How do baseline machine learning models perform on IDS-style network-flow data using standard classification metrics?

**RQ2:** Can alert intelligence fields such as top features, MITRE mapping, and triage priority improve the interpretability of IDS alerts?

**RQ3:** Does RAG-grounded explanation improve LLM output quality compared with template-only and no-RAG explanation modes?

**RQ4:** Can the proposed prototype support a SOC-style incident triage workflow at research prototype level?

## 1.5 Scope Of The Study

This thesis focuses on offline IDS-style network-flow analysis and alert explanation. The detection component is based on structured network-flow data and supervised machine learning models. The explanation component uses structured alert context and retrieved security playbooks to generate grounded natural language explanations.

The project includes:

- Sample IDS-style events for deterministic demonstration.
- UNSW-NB15-style preprocessing support.
- Planned extension to full UNSW-NB15 and CICIDS2017 or CSE-CIC-IDS2018.
- Baseline ML models such as Logistic Regression, Decision Tree, and Random Forest.
- Alert enrichment with severity, confidence, evidence features, MITRE mapping, and triage priority.
- Local playbook retrieval for RAG-style grounding.
- Explanation comparison across template, no-RAG, and RAG-assisted modes.
- SOC dashboard visualization.
- Exported evaluation artifacts including metrics, confusion matrices, feature importance, rubric scores, RAG summaries, and case studies.

The project does not aim to build a production-grade IDS or SIEM platform. The following are outside the primary scope:

- Realtime packet capture.
- Automatic blocking or containment in a real network.
- Full SIEM/SOAR integration.
- LLM fine-tuning.
- Treating the LLM as the final detector or decision-maker.

## 1.6 Proposed Approach

The proposed system separates detection from explanation. The IDS/ML layer is responsible for detecting suspicious events and producing measurable outputs. The alert intelligence layer enriches detections with evidence and security context. The LLM/RAG layer then generates explanations and response recommendations based on that structured information.

The high-level workflow is:

```text
Network-flow data
        -> preprocessing
        -> ML/IDS detection
        -> alert intelligence
        -> RAG retrieval
        -> LLM explanation
        -> dashboard and evaluation reports
```

This design provides two advantages. First, detection remains measurable using established ML evaluation metrics. Second, LLM outputs can be grounded using alert fields and retrieved playbooks, which helps reduce hallucination and improves interpretability.

## 1.7 Expected Contributions

The expected contributions of this thesis are:

1. A reproducible research prototype for ML-based network intrusion detection and alert analysis.
2. An alert intelligence layer that connects IDS outputs with explainable evidence, MITRE mapping, and triage priority.
3. A RAG-grounded LLM explanation workflow for security alerts.
4. A rubric-based evaluation framework for comparing explanation modes.
5. A SOC-style dashboard and exported artifacts that support thesis experimentation and defense demonstration.

## 1.8 Thesis Organization

The thesis is organized as follows:

- **Chapter 1** introduces the research background, problem statement, objectives, research questions, scope, and contributions.
- **Chapter 2** reviews related work on IDS, machine learning for intrusion detection, explainable AI, LLMs, and RAG in cybersecurity.
- **Chapter 3** presents the proposed system architecture and main design decisions.
- **Chapter 4** describes the implementation of the backend, frontend, preprocessing pipeline, model training, RAG playbooks, and reporting scripts.
- **Chapter 5** presents experiments and evaluation results for IDS models and LLM explanation modes.
- **Chapter 6** discusses findings, limitations, security considerations, and threats to validity.
- **Chapter 7** concludes the thesis and proposes future work.

## 1.9 Summary

This chapter introduced the motivation and problem addressed by the thesis. IDS and ML models can support intrusion detection, but their outputs require interpretation before analysts can act effectively. LLMs can help explain alerts, but they should not replace measurable detection mechanisms. The proposed approach combines ML-based IDS, explainable alert intelligence, RAG-grounded LLM explanation, and SOC-style visualization to support security alert analysis in a research prototype.
