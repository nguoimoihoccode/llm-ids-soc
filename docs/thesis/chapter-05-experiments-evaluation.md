# Chapter 5: Experiments And Evaluation

## 5.1 Introduction

This chapter presents the experimental design and evaluation artifacts for the proposed prototype. The evaluation is divided into two main parts. The first part evaluates the IDS and machine-learning pipeline using model metrics and explainability artifacts. The second part evaluates the LLM/RAG explanation workflow using explanation comparison, rubric scores, RAG summaries, and incident case studies.

The current prototype uses deterministic fixture data to validate the pipeline and benchmark datasets to produce preliminary research results. Fixture results are not intended to represent final research performance. They prove that preprocessing, model training, metric generation, explanation comparison, and report export work correctly. UNSW-NB15 and CICIDS2017 results provide the current baseline evidence for thesis discussion.

## 5.2 Evaluation Objectives

The experiments are designed to answer the research questions introduced in Chapter 1.

The IDS evaluation objectives are:

1. Verify that IDS-style data can be preprocessed into a trainable format.
2. Train baseline supervised ML models.
3. Export standard classification metrics.
4. Generate confusion matrix figures.
5. Generate feature importance artifacts for explainability.

The LLM/RAG evaluation objectives are:

1. Generate alert explanations using multiple modes.
2. Compare template, no-RAG, and RAG-assisted explanations.
3. Score each explanation mode using a rubric.
4. Summarize RAG vs no-RAG performance.
5. Produce incident case studies for qualitative review.

## 5.3 Experimental Setup

### 5.3.1 Hardware And Software Environment

The current prototype is developed and tested locally. The backend is implemented in Python using FastAPI, pandas, scikit-learn, joblib, and pytest. The frontend is implemented with React, TypeScript, and Vite.

Key software components:

- Python 3.9+.
- FastAPI.
- pandas.
- scikit-learn.
- XGBoost.
- joblib.
- pytest.
- React.
- Vite.

### 5.3.2 Dataset Setup

The evaluation uses three dataset levels.

Fixture data is located in:

```text
data/samples/unsw_nb15_fixture.csv
data/processed/unsw_nb15_fixture_processed.csv
```

The fixture contains a small number of samples and is used only to validate the experimental pipeline.

UNSW-NB15 is used as the primary benchmark with its published train/test split:

```text
data/raw/UNSW_NB15_training-set.csv
data/raw/UNSW_NB15_testing-set.csv
```

CICIDS2017 is used as a secondary benchmark after normalizing and merging the public multi-day CICFlowMeter CSV files:

```text
data/processed/cicids2017_full_normalized.csv
```

The current benchmark evaluation uses:

- UNSW-NB15 as the primary dataset.
- CICIDS2017 as the secondary dataset.

### 5.3.3 Models Evaluated

The current baseline models are:

- Logistic Regression.
- Decision Tree.
- Random Forest.
- XGBoost.

These models were selected because they represent simple, interpretable, tree-based, ensemble, and boosted supervised learning baselines for tabular IDS data.

### 5.3.4 Explanation Modes Evaluated

The LLM/RAG evaluation compares three explanation modes:

| Mode | Description |
|---|---|
| Template | Deterministic explanation using alert fields only |
| LLM without RAG | LLM-style explanation using alert context but no retrieved playbook |
| LLM with RAG | LLM-style explanation using alert context and retrieved playbook context |

The current implementation uses a deterministic local-template provider. The system is structured so that external LLM providers such as Gemini, OpenAI, or Ollama can be added later.

## 5.4 IDS Evaluation Methodology

The IDS evaluation pipeline follows these steps:

```text
Raw CSV
        -> validation/profile
        -> preprocessing
        -> train/test split or official split
        -> model training
        -> prediction
        -> metrics export
        -> report generation
```

For UNSW-NB15 official split evaluation, the pipeline command is:

```bash
backend/.venv/bin/python scripts/run_dataset_pipeline.py \
  --dataset-id unsw-nb15-official \
  --train-input data/raw/UNSW_NB15_training-set.csv \
  --test-input data/raw/UNSW_NB15_testing-set.csv \
  --output-dir reports/pipeline/unsw-nb15-official \
  --models logistic_regression,decision_tree,random_forest,xgboost
```

For CICIDS2017 random split evaluation, the pipeline command is:

```bash
backend/.venv/bin/python scripts/run_dataset_pipeline.py \
  --dataset-id cicids2017-full \
  --input data/processed/cicids2017_full_normalized.csv \
  --output-dir reports/pipeline/cicids2017-full \
  --models logistic_regression,decision_tree,random_forest \
  --test-size 0.2 \
  --random-state 42
```

The main metrics are:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- False positive rate.
- Confusion matrix.

## 5.5 IDS Evaluation Results

Model comparison artifacts are exported to:

```text
reports/pipeline/unsw-nb15-official/reports/model-comparison.csv
reports/pipeline/cicids2017-full/reports/model-comparison.csv
```

### 5.5.1 UNSW-NB15 Official Split Results

UNSW-NB15 was evaluated using the official training and testing files. The target is binary detection, where `label=0` is normal and `label=1` is attack. The attack-category field is used only for profiling and is explicitly removed from training features to avoid label leakage.

| Dataset | Model | Accuracy | Precision | Recall | F1-score | False Positive Rate |
|---|---|---:|---:|---:|---:|---:|
| UNSW-NB15 | Decision Tree | 0.5241 | 0.6042 | 0.3932 | 0.4764 | 0.3156 |
| UNSW-NB15 | Logistic Regression | 0.6159 | 0.6313 | 0.7268 | 0.6757 | 0.5201 |
| UNSW-NB15 | Random Forest | 0.5741 | 0.6626 | 0.4614 | 0.5440 | 0.2879 |
| UNSW-NB15 | XGBoost | 0.5294 | 0.5975 | 0.4453 | 0.5103 | 0.3675 |

The strongest current UNSW-NB15 baseline by F1-score is Logistic Regression. XGBoost was added as a boosted baseline, but with the current simple feature handling and default-like configuration it does not outperform Logistic Regression. This suggests that further work should focus on scaling, feature selection, and hyperparameter tuning before making final claims about boosted models.

### 5.5.2 CICIDS2017 Full Random Split Results

CICIDS2017 was evaluated after normalizing the public multi-day CICFlowMeter CSV files into the project schema. The current split is a generated stratified random split with 80% training data and 20% testing data.

| Dataset | Model | Accuracy | Precision | Recall | F1-score | False Positive Rate |
|---|---|---:|---:|---:|---:|---:|
| CICIDS2017 | Decision Tree | 0.9987 | 0.9968 | 0.9968 | 0.9968 | 0.0008 |
| CICIDS2017 | Logistic Regression | 0.9013 | 0.8713 | 0.5857 | 0.7005 | 0.0212 |
| CICIDS2017 | Random Forest | 0.9989 | 0.9972 | 0.9971 | 0.9972 | 0.0007 |

The tree-based models achieve very high scores on the current CICIDS2017 random split. These results should be interpreted with caution because random splits can place very similar flows in both training and testing sets. A temporal or day-based split would be a stronger test of generalization and should be considered for final thesis work.

### 5.5.3 Fixture Results

Fixture results are still used only as a pipeline smoke test. They should not be interpreted as final IDS performance.

## 5.6 Confusion Matrix Artifacts

Confusion matrix figures are exported to:

```text
reports/figures/
```

Generated fixture figures include:

```text
fixture-decision_tree-confusion-matrix.svg
fixture-logistic_regression-confusion-matrix.svg
fixture-random_forest-confusion-matrix.svg
```

These figures are useful in the thesis because they show the distribution of true positives, false positives, true negatives, and false negatives for each model.

## 5.7 Feature Importance Artifacts

Feature importance reports are exported to:

```text
reports/evaluation/feature-importance/
```

Generated fixture reports include:

```text
fixture-decision_tree-feature-importance.csv
fixture-random_forest-feature-importance.csv
```

Feature importance supports the explainability objective of the thesis. Tree-based models provide importance scores that identify which features contributed most strongly to model decisions. These scores can later be connected with alert `top_features` and used to support analyst explanations.

Logistic Regression is not included in the feature importance export because the current implementation focuses on tree-model `feature_importances_`. Coefficient-based explanations for Logistic Regression can be added in future work.

## 5.8 Alert Intelligence Evaluation

The alert intelligence layer enriches each alert with:

- Severity.
- Confidence.
- Technical reason.
- Top features.
- MITRE ATT&CK mapping.
- Triage priority.

Example Brute Force alert:

```text
Attack type: Brute Force
Severity: High
Confidence: 94%
MITRE: T1110 - Brute Force
Priority: P1
Evidence features: failed_login_count, dst_port, flow_packets_s
```

This enrichment improves interpretability because analysts can see not only that an attack was detected, but also why the system considers it suspicious.

## 5.9 LLM/RAG Evaluation Methodology

The LLM/RAG evaluation pipeline follows these steps:

```text
Alert
        -> template explanation
        -> LLM-style explanation without RAG
        -> LLM-style explanation with RAG
        -> rubric scoring
        -> summary and case study reports
```

The rubric criteria are:

| Criterion | Meaning |
|---|---|
| Correctness | Explanation matches the alert and attack type |
| Completeness | Explanation includes cause, evidence, and response guidance |
| Groundedness | Explanation stays within alert context and retrieved knowledge |
| Actionability | Recommendations are concrete and useful |
| Hallucination safety | Explanation avoids unsupported or invented claims |
| Latency | Response mode is practical for analyst workflow |

The evaluation command is:

```bash
backend/.venv/bin/python scripts/evaluate_llm.py \
  --output reports/evaluation/llm-rubric-scores.csv
```

## 5.10 LLM Rubric Results

The rubric scores are exported to:

```text
reports/evaluation/llm-rubric-scores.csv
```

The current fixture evaluation contains 9 rows:

```text
3 alerts x 3 explanation modes = 9 rubric rows
```

The system also exports a summary report:

```text
reports/evaluation/rag-vs-no-rag-summary.md
```

The current deterministic scoring is designed to validate the evaluation workflow. For final thesis evaluation, this rubric should be extended with expert or advisor review for a larger set of incidents.

## 5.11 RAG vs No-RAG Summary

The RAG summary report aggregates rubric scores by explanation mode. It is used to compare whether RAG-assisted explanation improves groundedness and actionability.

The current result indicates that RAG-backed explanations achieve the highest groundedness score because they include retrieved playbook context. This supports the intuition that RAG can help constrain LLM outputs and improve evidence-based explanation.

However, because the current scores are deterministic and based on fixture examples, the final thesis should evaluate more cases and include expert validation.

## 5.12 Incident Case Studies

Incident case studies are exported to:

```text
reports/evaluation/incident-case-studies.md
```

Each case study contains:

- Alert information.
- Source and destination.
- Severity and confidence.
- MITRE mapping.
- Evidence features.
- Grounded explanation.
- Recommended response.
- Explanation comparison.
- Rubric scores.

The case study report supports qualitative analysis and can be used in the thesis appendix or defense demonstration.

## 5.13 Discussion Of Current Results

The current results demonstrate that the project pipeline works end-to-end. The system can preprocess data, train models, export metrics, generate explainability artifacts, enrich alerts, compare explanation modes, score LLM outputs, and produce case study reports.

The fixture dataset results are intentionally simple. They validate correctness of the workflow rather than proving final model performance. The main value of the current results is that they establish a reproducible experimental framework that can be scaled to full IDS datasets.

The LLM/RAG results also demonstrate the evaluation methodology. The RAG-assisted mode receives stronger groundedness because it includes retrieved playbook context. This supports the thesis direction, but final claims should be based on larger incident sets and possibly human evaluation.

## 5.14 Threats To Validity

Several threats to validity must be considered.

### 5.14.1 Dataset Validity

The current fixture dataset is too small for final conclusions. Full experiments must use larger public datasets such as UNSW-NB15 and CICIDS2017.

### 5.14.2 Model Generalization

Models trained on one public dataset may not generalize to real enterprise networks. Dataset bias and class imbalance may affect results.

### 5.14.3 LLM Evaluation Bias

The current rubric is deterministic and useful for pipeline validation. Final evaluation should include more incident cases and, if possible, expert review.

### 5.14.4 RAG Knowledge Quality

The quality of RAG output depends on the quality of retrieved playbooks. Future work should include a richer security knowledge base.

## 5.15 Summary

This chapter presented the evaluation methodology and current fixture-based results. The IDS pipeline produces model metrics, confusion matrices, and feature importance artifacts. The LLM/RAG pipeline produces explanation comparisons, rubric scores, RAG summaries, and incident case studies. The current results validate the research workflow and provide a foundation for full dataset experiments in the final thesis.
