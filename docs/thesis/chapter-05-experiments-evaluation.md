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

The evaluation uses two benchmark datasets and a fixture for pipeline validation.

Fixture data is located in:

```text
data/samples/unsw_nb15_fixture.csv
```

The fixture contains a small number of samples and is used only to validate the experimental pipeline.

UNSW-NB15 is used as the primary benchmark with its published train/test split:

```text
data/raw/UNSW_NB15_training-set.csv  (175,341 rows, 45 columns)
data/raw/UNSW_NB15_testing-set.csv   (82,332 rows, 45 columns)
```

CICIDS2017 is used as a secondary benchmark after normalizing and merging the public multi-day CICFlowMeter CSV files into the project schema:

```text
data/processed/cicids2017_full_normalized.csv  (2,830,743 rows, 80 columns)
```

The attack-category field (`attack_cat`) is used for profiling and reporting only. It is explicitly dropped before feature encoding to prevent label leakage — a research-quality issue that was identified and fixed during development. A regression test verifies that no `attack_cat_*` columns appear in processed features.

### 5.3.3 Models Evaluated

The current baseline models are:

- Logistic Regression.
- Logistic Regression with StandardScaler.
- Decision Tree.
- Random Forest.
- XGBoost (default configuration).
- XGBoost Tuned (hyperparameter-optimized via RandomizedSearchCV).

Hyperparameter tuning is implemented as a separate pipeline step using `RandomizedSearchCV` with 3-fold cross-validation and F1 scoring. The tuning script supports all model types with per-model parameter grids including regularization strength (C), tree depth, ensemble size, learning rate, subsampling ratio, and regularization parameters. Best parameters are saved as JSON artifacts and can be loaded by the training pipeline via `--tuning-dir`.

```bash
backend/.venv/bin/python scripts/tune_hyperparameters.py \
  --processed-train-path data/processed/unsw_nb15_train_processed.csv \
  --output-dir reports/evaluation/tuning \
  --models xgboost,random_forest,decision_tree,logistic_regression_scaled \
  --n-iter 40 --cv 3
```

These models were selected because they represent simple, interpretable, tree-based, ensemble, and boosted supervised learning baselines for tabular IDS data.

### 5.3.4 Explanation Modes Evaluated

The LLM/RAG evaluation compares three explanation modes:

| Mode | Description |
|---|---|
| Template | Deterministic explanation using alert fields only |
| LLM without RAG | LLM-generated explanation using alert context but no retrieved playbook |
| LLM with RAG | LLM-generated explanation using alert context and retrieved playbook context |

The system supports a pluggable LLM provider architecture with the following backends:

- **LocalTemplateProvider** (default): Deterministic, no external API dependency. Returns the prompt as-is for testing and offline evaluation.
- **OpenAIProvider**: GPT-4o-mini via OpenAI API. Configured via `OPENAI_API_KEY`.
- **GeminiProvider**: Gemini 2.0 Flash via Google Generative AI SDK. Configured via `GEMINI_API_KEY`.
- **OllamaProvider**: Local models (e.g., Llama 3) via Ollama. Configured via `OLLAMA_BASE_URL`.

The provider is selected via the `LLM_PROVIDER` environment variable. Each provider implements a common `LLMProvider` interface with a `generate(prompt)` method. Tests are written against the deterministic local-template provider so they do not require external API calls.

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
  --models logistic_regression,logistic_regression_scaled,decision_tree,random_forest,xgboost,xgboost_tuned
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
| UNSW-NB15 | Logistic Regression + Scaling | 0.7326 | 0.7416 | 0.7894 | 0.7647 | 0.3371 |
| UNSW-NB15 | Random Forest | 0.5741 | 0.6626 | 0.4614 | 0.5440 | 0.2879 |
| UNSW-NB15 | XGBoost | 0.5294 | 0.5975 | 0.4453 | 0.5103 | 0.3675 |
| UNSW-NB15 | XGBoost Tuned | 0.5047 | 0.5726 | 0.3966 | 0.4686 | 0.3627 |

The strongest current UNSW-NB15 baseline by F1-score is Logistic Regression with StandardScaler. Scaling improves the baseline from `0.6757` F1-score to `0.7647`, showing that feature scale has a significant effect on linear models for this dataset. XGBoost and the current tuned XGBoost configuration do not outperform scaled Logistic Regression. This suggests that further work should focus on richer hyperparameter search, feature selection, and protocol-specific tuning before making final claims about boosted models.

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

## 5.7 Explainability Artifacts

### 5.7.1 Feature Importance

Feature importance reports are exported to:

```text
reports/pipeline/{dataset-id}/reports/feature-importance/
```

Generated reports include per-model CSV files listing each feature and its importance score. Tree-based models (Decision Tree, Random Forest, XGBoost) provide native `feature_importances_` scores. These scores identify which features contributed most strongly to model decisions.

### 5.7.2 SHAP Explanations

SHAP (SHapley Additive exPlanations) is integrated to provide instance-level and global model explainability. The system supports TreeExplainer for tree-based models, LinearExplainer for Logistic Regression, and KernelExplainer as a fallback.

**Global SHAP summary plots** visualize the overall impact of each feature on model predictions across a sample of the test set:

```bash
backend/.venv/bin/python scripts/export_shap_explanations.py \
  --dataset-id cicids2017-full \
  --processed-path data/processed/cicids2017_test_processed.csv \
  --models-dir reports/pipeline/cicids2017-full/models \
  --output-dir reports/pipeline/cicids2017-full/shap
```

**Per-instance SHAP values** are exported as JSON, recording for each test instance the true label, predicted label, and top contributing features with their SHAP values and direction (toward "attack" or "benign").

**Real-time SHAP in inference**: The model inference endpoint computes SHAP values for each sample prediction. The `top_features` field in `InferenceResult` now carries ranked `FeatureImportance` objects (feature name + SHAP value) instead of plain column names. The SOC dashboard renders these as weighted bar charts, showing the analyst which features pushed the prediction toward attack (red) or benign (blue).

```text
FeatureImportance schema:
  feature: "Flow Bytes/s"
  importance: 0.0823  (positive = toward attack, negative = toward benign)
```

This connects model-level explainability (global SHAP) with alert-level explainability (per-instance SHAP), supporting the thesis claim that analysts can understand *why* a specific alert was classified as suspicious.

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
        -> LLM-generated explanation without RAG
        -> LLM-generated explanation with RAG
        -> rubric scoring
        -> summary and case study reports
```

The RAG retrieval layer has two operating modes:

1. **Keyword-based retrieval** (default): Matches the alert's attack type to a playbook filename (e.g., `brute-force.md`). Simple, deterministic, and always available.

2. **Vector-based semantic retrieval**: Chunks all playbook markdown files, computes embeddings using sentence-transformers (`all-MiniLM-L6-v2`) or TF-IDF as a fallback, and retrieves top-k relevant chunks via cosine similarity. The vector index is pre-built using:

```bash
backend/.venv/bin/python scripts/build_vector_index.py \
  --playbook-dir knowledge_base/playbooks \
  --output-dir knowledge_base/vector_index
```

The `rag_service.py` module attempts vector retrieval first, then falls back to exact filename lookup if the index is not available. This layered design ensures the system works immediately after setup (keyword mode) and gains semantic retrieval capability when the vector index is built.

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

The current results demonstrate that the project pipeline works end-to-end across two benchmark datasets. The system can:

1. Validate and profile raw IDS datasets.
2. Normalize heterogeneous schemas (CICFlowMeter to project schema).
3. Preprocess data while preventing label leakage (`attack_cat` exclusion).
4. Train five supervised model types with standardized metric export.
5. Tune hyperparameters via RandomizedSearchCV with reproducible parameter artifacts.
6. Export model metrics, confusion matrix SVGs, and feature importance CSVs.
7. Generate global SHAP summary plots and per-instance SHAP explanations.
8. Enrich alerts with severity, confidence, MITRE ATT&CK mapping, and triage priority.
9. Connect SHAP feature contributions to alert evidence in the dashboard.
10. Compare three explanation modes (template, no-RAG, RAG) with a pluggable LLM provider architecture.
11. Retrieve security context via keyword-based or vector-based semantic search over local playbooks.
12. Score explanation quality using a multi-criterion rubric.
13. Export incident case studies and RAG vs no-RAG summary reports.

The strongest UNSW-NB15 baseline is Logistic Regression with StandardScaler at F1=0.7647. The strongest CICIDS2017 baseline is Random Forest at F1=0.9972. The gap between datasets highlights the importance of multi-dataset evaluation and cautions against over-claiming based on a single benchmark.

The RAG-assisted explanation mode achieves stronger groundedness scores because it includes retrieved playbook context. The SHAP integration makes alert-level explainability concrete: each prediction is accompanied by ranked feature contributions showing which features pushed the decision toward attack or benign.

The current implementation uses a deterministic local-template LLM provider by default. The provider abstraction is ready for OpenAI, Gemini, or Ollama backends when API keys are configured. This design preserves reproducibility while enabling future experiments with real LLM outputs.

## 5.14 Threats To Validity

Several threats to validity must be considered.

### 5.14.1 Dataset Validity

The project evaluates two public benchmark datasets (UNSW-NB15 and CICIDS2017) with different characteristics. UNSW-NB15 uses a published train/test split; CICIDS2017 uses a generated stratified random split. Random splits on CICIDS2017 may place similar flows in both training and testing sets, inflating apparent performance. A temporal or day-based split would be a stronger generalization test.

### 5.14.2 Model Generalization

Models trained on public datasets may not generalize to real enterprise networks. Dataset bias, class imbalance, and protocol distribution differences between academic benchmarks and production traffic remain open concerns. The gap between UNSW-NB15 (best F1=0.7647) and CICIDS2017 (best F1=0.9972) illustrates this point.

### 5.14.3 Label Leakage Control

The `attack_cat` field, which encodes attack family labels, is explicitly dropped before feature encoding. A regression test enforces this. Without this control, models could achieve misleading near-perfect metrics by learning the attack category as a feature.

### 5.14.4 LLM Evaluation Bias

The deterministic rubric is useful for pipeline validation but does not substitute for human expert review. Future work should include at least one external evaluator scoring explanation quality across a representative set of 10-20 incident cases.

### 5.14.5 RAG Knowledge Quality

The quality of RAG output depends on the quality and coverage of retrieved playbooks. The current knowledge base covers three attack types (Brute Force, DDoS, Port Scan). Expanding to more attack families would improve explanation completeness for diverse alert types.

### 5.14.6 SHAP Approximation

SHAP values for tree-based models are exact (TreeExplainer). For Logistic Regression, LinearExplainer provides model-agnostic approximations. The KernelExplainer fallback is computationally expensive and is used only when no more specific explainer is available. Instance-level SHAP for the inference endpoint uses a small background sample, which trades precision for responsiveness.

## 5.15 Summary

This chapter presented the experimental design and evaluation results for the LLM-assisted IDS/SOC prototype. The IDS pipeline was evaluated on two benchmark datasets (UNSW-NB15 and CICIDS2017) across five model types with standardized metric export, confusion matrices, and explainability artifacts. The LLM/RAG explanation workflow was evaluated across three explanation modes using a six-criterion rubric, with supporting RAG summary and incident case study reports.

Key findings include: (1) feature scaling substantially improves linear models on UNSW-NB15 (F1 from 0.6757 to 0.7647), (2) tree-based models achieve near-perfect scores on CICIDS2017 random splits but this should be interpreted cautiously, (3) SHAP-based instance explanations connect model decisions to alert evidence with ranked feature contributions, and (4) the RAG-assisted explanation mode achieves higher groundedness scores by incorporating retrieved playbook context.

The evaluation framework is reproducible: every artifact can be traced to a specific CLI command, and all metrics, figures, and SHAP explanations are exported to versioned output directories. The system is ready for final experiments with real LLM providers and human expert evaluation.
