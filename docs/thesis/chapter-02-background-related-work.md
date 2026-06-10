# Chapter 2: Background And Related Work

## 2.1 Introduction

This chapter presents the background knowledge and related work required for the proposed system. The thesis combines multiple areas: network intrusion detection, machine learning for IDS, explainable AI, Large Language Models, Retrieval-Augmented Generation, and SOC-style alert triage. Each area contributes a different part of the final research prototype.

The chapter first introduces intrusion detection concepts and IDS categories. It then discusses network-flow datasets and common machine learning approaches for IDS. Next, it reviews explainability in ML-based security systems, followed by the role of LLMs and RAG in cybersecurity. The chapter concludes by identifying the research gap addressed by this thesis.

## 2.2 Intrusion Detection Systems

An Intrusion Detection System (IDS) is designed to monitor activity in a network or host environment and identify signs of malicious or policy-violating behavior. IDS technologies are commonly used in enterprise networks, cloud environments, and security operations centers to detect attacks such as port scanning, brute force login attempts, denial-of-service attacks, malware communication, and exploitation attempts.

IDS approaches can be categorized in several ways.

### 2.2.1 Signature-Based Detection

Signature-based IDS detects attacks by matching traffic or events against known patterns. These patterns may include byte sequences, protocol behaviors, known exploit indicators, or rule definitions. Signature-based methods are effective for known attacks and often provide precise alerts when the signature is well defined.

However, signature-based detection has limitations. It may fail to detect unknown attacks, modified attack variants, or zero-day techniques. It also requires continuous rule updates. In modern environments where attackers can change tactics quickly, signature-based detection alone is not sufficient.

### 2.2.2 Anomaly-Based Detection

Anomaly-based IDS attempts to model normal behavior and identify deviations. For example, a sudden increase in connection attempts, unusual traffic volume, or abnormal protocol usage may indicate suspicious activity. Machine learning is commonly applied to anomaly-based detection because ML models can learn statistical patterns from data.

The advantage of anomaly-based detection is its potential to detect unknown attacks. The challenge is that it can produce false positives, especially in dynamic network environments where normal behavior changes over time.

### 2.2.3 Network-Based And Host-Based IDS

Network-based IDS monitors network traffic, while host-based IDS monitors activity on individual systems. This thesis focuses on network-flow intrusion detection, where each record summarizes communication behavior between endpoints over a time window. Network-flow data is suitable for ML experiments because it can be represented as structured numerical and categorical features.

## 2.3 Network-Flow Data For IDS

Network-flow datasets represent traffic using features such as:

- Protocol.
- Source and destination ports.
- Flow duration.
- Packet counts.
- Byte counts.
- Packet rate.
- TCP flag counts.
- Service or state fields.
- Attack label.

Compared with raw packet payloads, network-flow features are easier to process for machine learning and often preserve useful behavioral signals. They also reduce privacy concerns because they may omit packet payload content.

However, network-flow data has limitations. It may lose payload-level details needed to detect some application-layer attacks. Dataset quality also matters because public benchmark datasets may not fully represent modern enterprise networks.

## 2.4 Public IDS Datasets

Public datasets are widely used for IDS research because they provide labeled data and allow reproducible experiments. This thesis considers the following datasets.

### 2.4.1 UNSW-NB15

UNSW-NB15 is a modern IDS dataset created to represent normal and attack traffic using network-flow features. It contains attack categories such as Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode, and Worms [Ref].

UNSW-NB15 is suitable for this thesis because it provides structured features and labels that can be used for supervised ML experiments. It is selected as the primary dataset for the full research implementation.

### 2.4.2 CICIDS2017

CICIDS2017 is another widely used IDS benchmark dataset. It includes benign traffic and multiple attack scenarios such as brute force, DDoS, DoS, botnet, infiltration, web attacks, and port scanning [Ref].

CICIDS2017 is useful as a secondary benchmark because it includes attack types that are intuitive for SOC-style demonstration and alert explanation.

### 2.4.3 NSL-KDD

NSL-KDD is an improved version of the older KDD Cup 1999 dataset. It has been used extensively in IDS research, but it is relatively outdated compared with modern network traffic [Ref]. For this thesis, NSL-KDD may be discussed as a historical baseline but is not the main evaluation target.

## 2.5 Machine Learning For Intrusion Detection

Machine learning has been widely applied to IDS because network-flow data can be represented as feature vectors. Supervised learning models can classify traffic as benign or malicious, or classify specific attack categories.

### 2.5.1 Logistic Regression

Logistic Regression is a simple supervised learning model often used as a baseline for binary classification. It is interpretable and computationally efficient. However, it may not capture complex nonlinear relationships in network traffic.

In this thesis, Logistic Regression is used as a baseline model to compare against tree-based models.

### 2.5.2 Decision Tree

Decision Tree models classify data by learning a tree of feature-based decisions. They are easy to interpret because the decision path can be inspected. However, single trees can overfit training data if not controlled.

Decision Trees are useful for demonstrating explainability because feature splits can be linked to alert evidence.

### 2.5.3 Random Forest

Random Forest is an ensemble of decision trees. It often performs better than a single tree because it reduces variance by aggregating multiple models. Random Forest also provides feature importance scores, which are useful for explainable IDS.

In this thesis, Random Forest is one of the main baseline models because it balances performance, robustness, and explainability.

### 2.5.4 Advanced Models

Advanced models such as XGBoost and LightGBM are frequently used in tabular classification problems and may provide strong IDS performance [Ref]. These models are considered optional extensions depending on time and dependency stability.

## 2.6 Evaluation Metrics For IDS

IDS evaluation must consider more than accuracy. In cybersecurity, false positives and false negatives have different operational impacts.

Common metrics include:

- **Accuracy**: proportion of correctly classified samples.
- **Precision**: proportion of predicted attacks that are truly attacks.
- **Recall**: proportion of actual attacks detected by the model.
- **F1-score**: harmonic mean of precision and recall.
- **False Positive Rate**: proportion of benign traffic incorrectly flagged as malicious.
- **Confusion Matrix**: detailed counts of true positives, false positives, true negatives, and false negatives.

For IDS, recall is important because missed attacks are dangerous. Precision and false positive rate are also important because too many false alerts can overload analysts.

## 2.7 Explainable AI For IDS

Machine learning models may detect suspicious traffic, but analysts need to understand why a model produced an alert. Explainable AI (XAI) addresses this issue by identifying important features, decision paths, or local explanations.

In IDS, explainability may answer questions such as:

- Which traffic features contributed most to the prediction?
- Was the alert caused by packet rate, failed login count, port behavior, or protocol state?
- Is the model relying on meaningful security evidence or dataset artifacts?

Tree-based models can provide feature importance scores. More advanced methods such as SHAP and LIME can provide local explanations for individual predictions [Ref]. This thesis currently implements top feature evidence and feature importance exports, with SHAP/LIME considered as future work.

## 2.8 Alert Intelligence And MITRE ATT&CK Mapping

Raw ML outputs such as labels and confidence scores are not always sufficient for SOC workflows. Alert intelligence enriches alerts with context that helps analysts prioritize and understand them.

Useful alert intelligence fields include:

- Attack type.
- Severity.
- Confidence.
- Top evidence features.
- MITRE ATT&CK technique mapping.
- Triage priority.
- Recommended response.

MITRE ATT&CK is a widely used knowledge base of adversary tactics and techniques [Ref]. Mapping alerts to ATT&CK techniques helps standardize incident communication and response planning. For example, brute force activity can be mapped to `T1110 - Brute Force`, while network service scanning can be mapped to `T1046 - Network Service Discovery`.

## 2.9 Large Language Models In Cybersecurity

Large Language Models can generate, summarize, and explain natural language. In cybersecurity, LLMs have potential applications in:

- Alert explanation.
- Incident summarization.
- Security report generation.
- Threat intelligence summarization.
- Analyst question answering.
- Response playbook assistance.

However, LLMs also introduce risks. They may hallucinate facts, generate unsupported recommendations, or expose sensitive data if used with external APIs. Therefore, LLMs should be integrated with clear boundaries and evaluation methods.

This thesis does not use the LLM as the final detector. Instead, the LLM is used after detection to explain structured alerts and support analyst understanding.

## 2.10 Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) combines information retrieval with text generation. Instead of relying only on model parameters, the system retrieves relevant documents and provides them as context to the language model.

In security alert analysis, RAG can retrieve:

- Attack playbooks.
- MITRE ATT&CK notes.
- OWASP guidance.
- CISA advisories.
- Internal response procedures.

RAG is useful because it can ground LLM responses in explicit knowledge. In this thesis, RAG is implemented using local markdown playbooks. The system compares explanations with and without RAG to evaluate whether retrieved context improves groundedness and actionability.

## 2.11 SOC Workflow And Alert Triage

A Security Operations Center is responsible for monitoring, detecting, investigating, and responding to security incidents. In a typical SOC workflow, analysts review alerts, determine their severity, investigate evidence, and recommend response actions.

The proposed system supports a simplified SOC workflow:

```text
Alert generation -> Alert enrichment -> Explanation -> Comparison -> Evaluation -> Report
```

The dashboard is not intended to replace a full SIEM platform. Instead, it demonstrates how detection outputs, explanation, and evaluation artifacts can be integrated into a research prototype.

## 2.12 Related Work Themes

Existing research can be grouped into several themes:

1. **ML-based IDS research**: focuses on improving detection accuracy using public datasets and different classifiers.
2. **Explainable IDS research**: focuses on interpreting model predictions and identifying important traffic features.
3. **LLM for cybersecurity research**: focuses on summarization, threat intelligence, alert triage, and security copilots.
4. **RAG-based security assistants**: focuses on grounding model responses using external cybersecurity knowledge.

Many studies address one of these areas independently. Fewer systems combine ML-based detection, explainable alert intelligence, RAG-grounded explanation, dashboard visualization, and reproducible evaluation artifacts in one workflow.

## 2.13 Research Gap

The main gap addressed by this thesis is the integration gap between detection, explanation, and evaluation.

Traditional IDS and ML studies often focus on classification metrics but may not provide analyst-friendly explanations. LLM-based cybersecurity assistants may generate useful summaries but are difficult to evaluate and should not replace measurable detection. Explainability methods can identify important features but may not translate them into natural language response guidance.

This thesis addresses the gap by combining:

- ML-based intrusion detection.
- Explainable alert evidence.
- MITRE-style mapping and triage priority.
- RAG-grounded LLM explanation.
- Rubric-based LLM evaluation.
- SOC dashboard and thesis-ready artifacts.

## 2.14 Summary

This chapter reviewed the background and related work for the proposed system. IDS and ML models provide measurable detection capabilities, while explainability and alert intelligence help analysts understand model outputs. LLMs and RAG can support natural language explanation and response guidance, but they must be constrained and evaluated carefully. The next chapter presents the proposed architecture that integrates these components into a unified research prototype.
