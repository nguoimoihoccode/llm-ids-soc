# Backend Domain Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split backend schemas into domain modules and centralize project path resolution without changing behavior.

**Architecture:** Move schema definitions out of the monolithic `models.py` into a small package with domain files and a re-exporting `__init__.py` so existing imports keep working. Add one shared `paths.py` module for project/data/report roots, then update services to import those constants instead of recomputing repository roots.

**Tech Stack:** Python 3.9, FastAPI, Pydantic, pytest.

---

## File Structure

- Create `backend/app/models/alerts.py`: alert, event, and explanation schemas.
- Create `backend/app/models/datasets.py`: dataset and preprocessing schemas.
- Create `backend/app/models/ml.py`: ML and inference schemas.
- Create `backend/app/models/__init__.py`: re-export public schema names.
- Delete `backend/app/models.py`: replace the monolithic module with the package above.
- Create `backend/app/paths.py`: shared repository path constants.
- Modify `backend/app/services/data_loader.py`: use `PROJECT_ROOT` or `DATA_ROOT` from the helper module.
- Modify `backend/app/services/rag_service.py`: use `PLAYBOOKS_ROOT` from the helper module.
- Modify `backend/app/services/metric_artifacts.py`: use `MODELS_ROOT` from the helper module.
- Modify `backend/app/services/model_inference.py`: use `REPORTS_ROOT` from the helper module.
- Modify any other backend service that currently computes `parents[3]` manually if it appears in the same cleanup pass.
- Modify `backend/app/main.py`: keep imports working through the re-export package.
- Modify backend tests only if import paths need updating, but behavior must stay the same.

---

### Task 1: Split Schema Modules

**Files:**
- Create: `backend/app/models/alerts.py`
- Create: `backend/app/models/datasets.py`
- Create: `backend/app/models/ml.py`
- Create: `backend/app/models/__init__.py`
- Delete: `backend/app/models.py`
- Test: `backend/tests/test_api.py`

- [ ] **Step 1: Write a failing import test**

Add this test to `backend/tests/test_api.py`:

```python
def test_models_package_reexports_domain_schemas() -> None:
    from app.models import Alert, DatasetInfo, InferenceResult, NetworkEvent

    assert Alert.__name__ == "Alert"
    assert DatasetInfo.__name__ == "DatasetInfo"
    assert InferenceResult.__name__ == "InferenceResult"
    assert NetworkEvent.__name__ == "NetworkEvent"
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
cd backend
.venv/bin/pytest tests/test_api.py::test_models_package_reexports_domain_schemas -v
```

Expected: FAIL because `app.models` is still a module, not a package, so the re-export path is missing.

- [ ] **Step 3: Create domain model files**

Create `backend/app/models/alerts.py` with:

```python
from pydantic import BaseModel


class NetworkEvent(BaseModel):
    event_id: str
    timestamp: str
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    flow_duration_ms: int
    total_fwd_packets: int
    total_bwd_packets: int
    flow_bytes_s: float
    flow_packets_s: float
    syn_flag_count: int
    failed_login_count: int
    label: str
    attack_type: str


class Alert(BaseModel):
    alert_id: str
    event_id: str
    timestamp: str
    src_ip: str
    dst_ip: str
    attack_type: str
    severity: str
    confidence: float
    reason: str
    top_features: list[str]
    mitre_technique: str
    triage_priority: str


class Explanation(BaseModel):
    alert_id: str
    provider: str
    summary: str
    why_suspicious: str
    evidence_features: list[str]
    mitre_technique: str
    triage_priority: str
    recommended_response: list[str]
    knowledge_context: str


class ExplanationComparisonItem(BaseModel):
    mode: str
    uses_rag: bool
    summary: str
    knowledge_context: str


class ExplanationComparison(BaseModel):
    alert_id: str
    comparisons: list[ExplanationComparisonItem]
```

Create `backend/app/models/datasets.py` with:

```python
from pydantic import BaseModel


class DatasetInfo(BaseModel):
    dataset_id: str
    name: str
    status: str
    source_url: str
    purpose: str


class PreprocessingSummary(BaseModel):
    row_count: int
    feature_count: int
    label_column: str
    attack_categories: list[str]


class DatasetProfile(BaseModel):
    row_count: int
    column_count: int
    columns: list[str]
    label_distribution: dict[str, int]
    label_percentages: dict[str, float]
    label_imbalance_ratio: float
    attack_category_distribution: dict[str, int]
    attack_category_percentages: dict[str, float]
    attack_category_imbalance_ratio: float
    missing_value_count: int


class DatasetSplitSummary(BaseModel):
    total_rows: int
    train_rows: int
    test_rows: int
    label_column: str
    test_size: float
    random_state: int
    stratified: bool
    split_strategy: str
    train_label_distribution: dict[str, int]
    test_label_distribution: dict[str, int]


class DatasetValidationResult(BaseModel):
    valid: bool
    row_count: int
    column_count: int
    required_columns: list[str]
    missing_required_columns: list[str]
    errors: list[str]
```

Create `backend/app/models/ml.py` with:

```python
from typing import Optional

from pydantic import BaseModel


class ModelEvaluation(BaseModel):
    model_name: str
    sample_count: int
    accuracy: float
    attack_recall: float
    benign_recall: float


class InferenceModelInfo(BaseModel):
    dataset_id: str
    model_name: str
    model_path: str
    available: bool
    status: str


class InferenceResult(BaseModel):
    dataset_id: str
    model_name: str
    model_available: bool
    prediction: int
    prediction_label: str
    confidence: float
    attack_probability: Optional[float]
    top_features: list[str]
    status: str
```

Create `backend/app/models/__init__.py` with:

```python
from .alerts import Alert, Explanation, ExplanationComparison, ExplanationComparisonItem, NetworkEvent
from .datasets import DatasetInfo, DatasetProfile, DatasetSplitSummary, DatasetValidationResult, PreprocessingSummary
from .ml import InferenceModelInfo, InferenceResult, ModelEvaluation

__all__ = [
    "Alert",
    "DatasetInfo",
    "DatasetProfile",
    "DatasetSplitSummary",
    "DatasetValidationResult",
    "Explanation",
    "ExplanationComparison",
    "ExplanationComparisonItem",
    "InferenceModelInfo",
    "InferenceResult",
    "ModelEvaluation",
    "NetworkEvent",
    "PreprocessingSummary",
]
```

Delete `backend/app/models.py` after the package is in place so `app.models` resolves to the package:

```bash
rm backend/app/models.py
```

- [ ] **Step 4: Run the import test to verify it passes**

Run:

```bash
cd backend
.venv/bin/pytest tests/test_api.py::test_models_package_reexports_domain_schemas -v
```

Expected: PASS.

- [ ] **Step 5: Commit Task 1**

Run:

```bash
git add backend/app/models.py backend/app/models/__init__.py backend/app/models/alerts.py backend/app/models/datasets.py backend/app/models/ml.py backend/tests/test_api.py
git commit -m "refactor: split backend schemas by domain"
```

---

### Task 2: Centralize Project Paths

**Files:**
- Create: `backend/app/paths.py`
- Modify: `backend/app/services/data_loader.py`
- Modify: `backend/app/services/rag_service.py`
- Modify: `backend/app/services/metric_artifacts.py`
- Modify: `backend/app/services/model_inference.py`
- Test: `backend/tests/test_api.py`

- [ ] **Step 1: Write a failing path helper test**

Add this test to `backend/tests/test_api.py`:

```python
def test_paths_module_exposes_project_roots() -> None:
    from app.paths import DATA_ROOT, MODELS_ROOT, PROJECT_ROOT, REPORTS_ROOT, PLAYBOOKS_ROOT

    assert PROJECT_ROOT.name == "llm-ids-soc"
    assert DATA_ROOT.name == "data"
    assert MODELS_ROOT.name == "models"
    assert REPORTS_ROOT.name == "reports"
    assert PLAYBOOKS_ROOT.name == "playbooks"
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
cd backend
.venv/bin/pytest tests/test_api.py::test_paths_module_exposes_project_roots -v
```

Expected: FAIL because `app.paths` does not exist yet.

- [ ] **Step 3: Create the path helper**

Create `backend/app/paths.py` with:

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / "data"
RAW_DATA_ROOT = DATA_ROOT / "raw"
PROCESSED_DATA_ROOT = DATA_ROOT / "processed"
MODELS_ROOT = PROJECT_ROOT / "models"
REPORTS_ROOT = PROJECT_ROOT / "reports"
KNOWLEDGE_BASE_ROOT = PROJECT_ROOT / "knowledge_base"
PLAYBOOKS_ROOT = KNOWLEDGE_BASE_ROOT / "playbooks"
```

- [ ] **Step 4: Update services to use shared paths**

Update `backend/app/services/data_loader.py`:

```python
from app.paths import DATA_ROOT

SAMPLE_DATA_PATH = DATA_ROOT / "samples" / "network_events.csv"
```

Update `backend/app/services/rag_service.py`:

```python
from app.paths import PLAYBOOKS_ROOT

PLAYBOOK_DIR = PLAYBOOKS_ROOT
```

Update `backend/app/services/metric_artifacts.py`:

```python
from app.paths import MODELS_ROOT

DEFAULT_METRICS_DIR = MODELS_ROOT / "metrics"
```

Update `backend/app/services/model_inference.py`:

```python
from app.paths import PROJECT_ROOT, REPORTS_ROOT

DEFAULT_MODEL_PATH = (
    REPORTS_ROOT
    / "pipeline"
    / "cicids2017-full"
    / "models"
    / "cicids2017-full-random_forest.joblib"
)
```

Adjust any other service in this pass that still uses `Path(__file__).resolve().parents[3]` the same way, replacing it with a constant from `app.paths`.

- [ ] **Step 5: Run the path test to verify it passes**

Run:

```bash
cd backend
.venv/bin/pytest tests/test_api.py::test_paths_module_exposes_project_roots -v
```

Expected: PASS.

- [ ] **Step 6: Commit Task 2**

Run:

```bash
git add backend/app/paths.py backend/app/services/data_loader.py backend/app/services/rag_service.py backend/app/services/metric_artifacts.py backend/app/services/model_inference.py backend/tests/test_api.py
git commit -m "refactor: centralize backend path helpers"
```

---

### Task 3: Final Verification

**Files:**
- Verify all changed backend files.

- [ ] **Step 1: Run the backend test suite**

Run:

```bash
cd backend
.venv/bin/pytest
```

Expected: all tests pass.

- [ ] **Step 2: Check git status**

Run:

```bash
git status --short
```

Expected: clean tracked state after commits.
