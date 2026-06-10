# Chapter 3: Proposed System Architecture

## 3.1 Introduction

This chapter presents the proposed system architecture for the thesis. The system is designed as a research prototype that combines machine-learning-based intrusion detection, explainable alert intelligence, Retrieval-Augmented Generation (RAG), and LLM-style alert explanation. The goal is not to replace a production IDS or SIEM platform, but to demonstrate how detection, explanation, triage, and evaluation can be integrated into a SOC-style workflow.

The proposed system follows a separation-of-responsibilities design. The IDS and ML components perform detection and classification. The alert intelligence layer enriches detection outputs with evidence and security context. The LLM/RAG layer explains alerts and recommends response actions based on structured context and retrieved playbooks. The dashboard presents the workflow to analysts and supports defense demonstration.

## 3.2 Design Principles

The system is based on five design principles.

### 3.2.1 Detection And Explanation Are Separated

The LLM is not used as the final intrusion detector. Detection is handled by rule-based or machine-learning components that can be evaluated using standard metrics. The LLM is used after detection to explain alerts, summarize evidence, and provide response guidance.

This separation is important because IDS detection is a structured classification problem, while LLM generation is probabilistic and may hallucinate. Keeping detection separate makes the system easier to evaluate and safer to reason about.

### 3.2.2 Alerts Must Be Enriched Before Explanation

Raw detection outputs such as `Attack` or `Brute Force` are not sufficient for analyst workflows. The system enriches alerts with:

- Severity.
- Confidence.
- Technical reason.
- Top evidence features.
- MITRE ATT&CK mapping.
- Triage priority.

This enriched alert becomes the structured input for the explanation layer.

### 3.2.3 LLM Outputs Must Be Grounded

LLM explanations should be grounded in explicit alert context and retrieved security knowledge. The system provides the LLM-style explanation layer with alert features, MITRE mapping, triage priority, and RAG playbook context.

This reduces the risk of unsupported statements and provides a basis for evaluation.

### 3.2.4 Evaluation Artifacts Are First-Class Outputs

The system is built for a thesis project, so it must produce reproducible artifacts. These include:

- Model metrics JSON.
- Model comparison CSV.
- Confusion matrix figures.
- Feature importance reports.
- LLM rubric scores.
- RAG vs no-RAG summaries.
- Incident case studies.

These artifacts support the experimental chapter and defense presentation.

### 3.2.5 The Prototype Should Support A SOC Workflow

The dashboard and API are designed to demonstrate a simplified SOC analyst workflow:

```text
View alerts -> inspect evidence -> read explanation -> compare explanation modes -> review reports
```

## 3.3 High-Level Architecture

The proposed system consists of seven major layers:

1. Data layer.
2. Preprocessing layer.
3. IDS and ML detection layer.
4. Alert intelligence layer.
5. RAG and LLM explanation layer.
6. Backend API and dashboard layer.
7. Evaluation and reporting layer.

The high-level architecture is:

```text
Network-flow data
        -> preprocessing
        -> IDS/ML detection
        -> enriched alert generation
        -> RAG retrieval
        -> LLM-style explanation
        -> SOC dashboard
        -> evaluation reports
```

The detailed Mermaid source diagrams are available in `docs/architecture-diagram.md`.

## 3.4 Data Layer

The data layer stores sample and processed IDS-style data. The current prototype includes deterministic sample data for demonstration and testing. The full thesis plan includes UNSW-NB15 as the primary dataset and CICIDS2017 or CSE-CIC-IDS2018 as a secondary benchmark.

Current data files include:

```text
data/samples/network_events.csv
data/samples/unsw_nb15_fixture.csv
data/processed/unsw_nb15_fixture_processed.csv
```

The sample network events represent benign and malicious traffic such as brute force, DDoS, and port scanning. These samples allow the prototype to demonstrate the complete workflow without requiring a large external dataset.

## 3.5 Preprocessing Layer

The preprocessing layer prepares IDS-style CSV files for model training. It performs operations such as:

- Reading CSV input.
- Replacing NaN values.
- Replacing infinite values.
- Encoding categorical fields.
- Preserving the supervised learning label.
- Exporting processed CSV data.

The preprocessing pipeline is exposed through the script:

```text
scripts/preprocess_unsw_nb15.py
```

The output of this layer is a processed dataset that can be consumed by the model training pipeline.

## 3.6 IDS And ML Detection Layer

The IDS and ML detection layer is responsible for identifying suspicious network behavior. The current prototype contains two detection paths.

### 3.6.1 Rule-Based Demo Detector

The rule-based detector is used for deterministic demonstration. It converts labeled sample events into alerts and assigns confidence values based on simple feature conditions. For example:

- High failed login count indicates brute force behavior.
- High packet rate indicates possible DDoS behavior.
- SYN flag and short flow duration indicate port scanning.

This detector is not intended as the final research model. It exists to demonstrate the full alert explanation workflow before full dataset experiments are added.

### 3.6.2 Baseline ML Models

The prototype includes a training pipeline for baseline supervised models:

- Logistic Regression.
- Decision Tree.
- Random Forest.

The training script is:

```text
scripts/train_models.py
```

The model outputs include trained model files and metrics artifacts:

```text
models/trained/
models/metrics/
```

For the full thesis, this layer will be extended to full UNSW-NB15 and a secondary dataset benchmark.

## 3.7 Alert Intelligence Layer

The alert intelligence layer converts detection results into enriched security alerts. This is a central part of the proposed system because it bridges the gap between raw model outputs and analyst-friendly context.

Each alert contains:

- `alert_id`: unique alert identifier.
- `event_id`: original event identifier.
- `timestamp`: event time.
- `src_ip` and `dst_ip`: source and destination addresses.
- `attack_type`: predicted or labeled attack type.
- `severity`: Low, Medium, High, or Critical-style severity.
- `confidence`: confidence score.
- `reason`: short technical reason.
- `top_features`: evidence features supporting the alert.
- `mitre_technique`: mapped MITRE ATT&CK technique.
- `triage_priority`: analyst priority such as P1, P2, or P3.

Example alert:

```json
{
  "attack_type": "Brute Force",
  "severity": "High",
  "confidence": 0.94,
  "reason": "80 failed login attempts against port 22.",
  "top_features": ["failed_login_count", "dst_port", "flow_packets_s"],
  "mitre_technique": "T1110 - Brute Force",
  "triage_priority": "P1"
}
```

The alert intelligence layer gives the LLM explanation module structured context and gives analysts more interpretable alerts.

## 3.8 RAG And LLM Explanation Layer

The RAG and LLM explanation layer generates natural language explanations for enriched alerts.

### 3.8.1 Local Playbook Retrieval

The prototype currently uses local markdown playbooks as the retrieval knowledge base:

```text
knowledge_base/playbooks/brute-force.md
knowledge_base/playbooks/ddos.md
knowledge_base/playbooks/port-scan.md
```

When an alert is generated, the system retrieves the relevant playbook according to the attack type. This retrieved context is included in the explanation output.

### 3.8.2 Grounded Explanation

The explanation endpoint returns:

- Summary.
- Why the alert is suspicious.
- Evidence features.
- MITRE technique.
- Triage priority.
- Recommended response.
- Retrieved knowledge context.

This design ensures that the generated explanation is grounded in alert evidence and playbook context.

### 3.8.3 Explanation Comparison Modes

The system compares three explanation modes:

1. Template explanation.
2. LLM-style explanation without RAG.
3. LLM-style explanation with RAG.

This comparison supports the research question of whether RAG improves explanation quality.

## 3.9 Backend API Layer

The backend is implemented using FastAPI. It exposes endpoints for health checks, events, datasets, alerts, explanations, and metrics.

Key endpoints include:

| Endpoint | Purpose |
|---|---|
| `/health` | Service health check |
| `/events` | Return sample network events |
| `/datasets` | Return dataset registry |
| `/alerts` | Generate enriched alerts |
| `/alerts/{alert_id}` | Return one alert |
| `/alerts/{alert_id}/explanation` | Return grounded explanation |
| `/alerts/{alert_id}/explanation/comparison` | Compare explanation modes |
| `/ml/evaluate` | Evaluate rule-based baseline |
| `/ml/metrics` | Return saved model metrics |

The API allows the frontend dashboard and evaluation scripts to interact with the same backend logic.

## 3.10 SOC Dashboard Layer

The frontend dashboard is implemented using React and Vite. It presents a simplified SOC interface that includes:

- Alert overview cards.
- Alert table.
- Severity and priority information.
- LLM analysis panel.
- Evidence features.
- MITRE mapping.
- Model comparison table.
- Explanation comparison section.

The dashboard supports defense demonstration by showing the end-to-end workflow in a visual form.

## 3.11 Evaluation And Reporting Layer

The evaluation layer produces artifacts for thesis experiments and reporting.

### 3.11.1 IDS Evaluation Artifacts

The IDS evaluation artifacts include:

- `models/metrics/*.json`
- `reports/evaluation/model-comparison.csv`
- `reports/figures/*-confusion-matrix.svg`
- `reports/evaluation/feature-importance/*.csv`

These artifacts support the evaluation of model performance and explainability.

### 3.11.2 LLM/RAG Evaluation Artifacts

The LLM/RAG artifacts include:

- `reports/evaluation/llm-rubric-scores.csv`
- `reports/evaluation/rag-vs-no-rag-summary.md`
- `reports/evaluation/incident-case-studies.md`

These artifacts support comparison between template, no-RAG, and RAG-assisted explanation modes.

## 3.12 Security And Reliability Considerations

The system includes several design choices to reduce risk:

- The LLM does not make final detection decisions.
- LLM outputs are grounded using structured alert context.
- RAG retrieves explicit playbook context.
- Evaluation artifacts are reproducible.
- The system is scoped as an offline research prototype.

Potential future risks include dataset bias, LLM hallucination, external API privacy concerns, and generalization limitations. These are addressed in the discussion chapter and future work.

## 3.13 Summary

This chapter presented the proposed system architecture. The system integrates preprocessing, IDS/ML detection, alert intelligence, RAG-grounded explanation, SOC dashboard visualization, and reproducible evaluation artifacts. The key design decision is to separate detection from explanation: ML handles measurable detection, while LLM/RAG supports analyst interpretation and response recommendation. The next chapter describes the implementation details of the prototype.
