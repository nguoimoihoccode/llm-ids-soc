# CICIDS2017 Model Inference Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add CICIDS2017 Random Forest model inference to the backend API and show its status/result in the React dashboard.

**Architecture:** The backend gets a focused `model_inference` service that owns default model configuration, artifact availability checks, sample-row prediction, and safe unavailable responses. FastAPI exposes two read-only endpoints for default model metadata and sample inference. The frontend renders these responses without needing to know filesystem paths or fallback rules.

**Tech Stack:** Python 3.9, FastAPI, Pydantic, pandas, joblib, scikit-learn, pytest, React, TypeScript, Vite.

---

## File Structure

- Create `backend/app/services/model_inference.py`: default CICIDS2017 model config, model loading, sample feature construction, prediction, and fallback status.
- Modify `backend/app/models.py`: add `InferenceModelInfo` and `InferenceResult` response models.
- Modify `backend/app/main.py`: add `/ml/inference/default-model` and `/ml/inference/sample`.
- Create `backend/tests/test_model_inference.py`: service-level tests for missing model and temporary trained model.
- Modify `backend/tests/test_api.py`: API tests for default metadata and sample inference schema.
- Modify `frontend/src/main.tsx`: add inference types, state, API call, fallback data, and dashboard panel.
- Modify `frontend/src/styles.css`: add minor styles for the inference panel if existing styles are insufficient.

---

### Task 1: Backend Inference Schemas And Service

**Files:**
- Create: `backend/app/services/model_inference.py`
- Modify: `backend/app/models.py`
- Test: `backend/tests/test_model_inference.py`

- [ ] **Step 1: Write failing service tests**

Create `backend/tests/test_model_inference.py`:

```python
from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier

from app.services.model_inference import (
    InferenceModelConfig,
    get_default_model_info,
    run_sample_inference,
)


def test_default_model_info_reports_cicids2017_random_forest() -> None:
    info = get_default_model_info()

    assert info.dataset_id == "cicids2017-full"
    assert info.model_name == "random_forest"
    assert "cicids2017-full-random_forest.joblib" in info.model_path
    assert info.status in {"available", "missing model artifact"}


def test_sample_inference_returns_unavailable_when_model_is_missing(tmp_path: Path) -> None:
    config = InferenceModelConfig(
        dataset_id="cicids2017-full",
        model_name="random_forest",
        model_path=tmp_path / "missing.joblib",
    )

    result = run_sample_inference(config)

    assert result.dataset_id == "cicids2017-full"
    assert result.model_name == "random_forest"
    assert result.model_available is False
    assert result.prediction == 0
    assert result.prediction_label == "unavailable"
    assert result.confidence == 0.0
    assert result.attack_probability is None
    assert result.top_features == []
    assert result.status == "missing model artifact"


def test_sample_inference_loads_model_and_predicts(tmp_path: Path) -> None:
    model_path = tmp_path / "demo-random_forest.joblib"
    frame = pd.DataFrame(
        [
            {"Flow Duration": 1.0, "Total Fwd Packets": 1.0, "Flow Bytes/s": 10.0},
            {"Flow Duration": 1000.0, "Total Fwd Packets": 500.0, "Flow Bytes/s": 50000.0},
            {"Flow Duration": 1200.0, "Total Fwd Packets": 700.0, "Flow Bytes/s": 80000.0},
            {"Flow Duration": 2.0, "Total Fwd Packets": 1.0, "Flow Bytes/s": 12.0},
        ]
    )
    labels = [0, 1, 1, 0]
    model = RandomForestClassifier(n_estimators=5, random_state=42)
    model.fit(frame, labels)
    dump(model, model_path)
    config = InferenceModelConfig(
        dataset_id="demo",
        model_name="random_forest",
        model_path=model_path,
    )

    result = run_sample_inference(config)

    assert result.dataset_id == "demo"
    assert result.model_name == "random_forest"
    assert result.model_available is True
    assert result.prediction in {0, 1}
    assert result.prediction_label in {"benign", "attack"}
    assert 0.0 <= result.confidence <= 1.0
    assert result.attack_probability is not None
    assert 0.0 <= result.attack_probability <= 1.0
    assert result.top_features == ["Flow Duration", "Total Fwd Packets", "Flow Bytes/s"]
    assert result.status == "ok"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
cd backend
.venv/bin/pytest tests/test_model_inference.py -v
```

Expected: FAIL during import because `app.services.model_inference` does not exist.

- [ ] **Step 3: Add Pydantic response models**

Append to `backend/app/models.py`:

```python
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
    attack_probability: float | None
    top_features: list[str]
    status: str
```

- [ ] **Step 4: Implement minimal inference service**

Create `backend/app/services/model_inference.py`:

```python
from dataclasses import dataclass
from pathlib import Path

import joblib
import pandas as pd

from app.models import InferenceModelInfo, InferenceResult


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL_PATH = (
    PROJECT_ROOT
    / "reports"
    / "pipeline"
    / "cicids2017-full"
    / "models"
    / "cicids2017-full-random_forest.joblib"
)


@dataclass(frozen=True)
class InferenceModelConfig:
    dataset_id: str
    model_name: str
    model_path: Path


DEFAULT_MODEL_CONFIG = InferenceModelConfig(
    dataset_id="cicids2017-full",
    model_name="random_forest",
    model_path=DEFAULT_MODEL_PATH,
)


def get_default_model_info(config: InferenceModelConfig = DEFAULT_MODEL_CONFIG) -> InferenceModelInfo:
    available = config.model_path.exists()
    return InferenceModelInfo(
        dataset_id=config.dataset_id,
        model_name=config.model_name,
        model_path=str(config.model_path),
        available=available,
        status="available" if available else "missing model artifact",
    )


def run_sample_inference(config: InferenceModelConfig = DEFAULT_MODEL_CONFIG) -> InferenceResult:
    if not config.model_path.exists():
        return _unavailable_result(config, "missing model artifact")

    try:
        model = joblib.load(config.model_path)
    except Exception as exc:
        return _unavailable_result(config, f"failed to load model: {exc}")

    sample = _sample_frame_for_model(model)
    prediction = int(model.predict(sample)[0])
    attack_probability = _attack_probability(model, sample, prediction)
    confidence = attack_probability if prediction == 1 and attack_probability is not None else None
    if confidence is None and attack_probability is not None:
        confidence = 1.0 - attack_probability
    if confidence is None:
        confidence = 1.0

    return InferenceResult(
        dataset_id=config.dataset_id,
        model_name=config.model_name,
        model_available=True,
        prediction=prediction,
        prediction_label="attack" if prediction == 1 else "benign",
        confidence=float(confidence),
        attack_probability=attack_probability,
        top_features=list(sample.columns[:5]),
        status="ok",
    )


def _sample_frame_for_model(model) -> pd.DataFrame:
    feature_names = list(getattr(model, "feature_names_in_", []))
    if not feature_names:
        feature_names = ["Flow Duration", "Total Fwd Packets", "Flow Bytes/s"]

    row = {feature: 0.0 for feature in feature_names}
    defaults = {
        "Flow Duration": 1200.0,
        "Total Fwd Packets": 700.0,
        "Total Backward Packets": 5.0,
        "Flow Bytes/s": 80000.0,
        "Flow Packets/s": 3000.0,
        "SYN Flag Count": 1.0,
    }
    for feature, value in defaults.items():
        if feature in row:
            row[feature] = value
    return pd.DataFrame([row], columns=feature_names)


def _attack_probability(model, sample: pd.DataFrame, prediction: int) -> float | None:
    if not hasattr(model, "predict_proba"):
        return None
    probabilities = model.predict_proba(sample)[0]
    classes = list(getattr(model, "classes_", []))
    if 1 in classes:
        return float(probabilities[classes.index(1)])
    return float(probabilities[prediction]) if prediction < len(probabilities) else None


def _unavailable_result(config: InferenceModelConfig, status: str) -> InferenceResult:
    return InferenceResult(
        dataset_id=config.dataset_id,
        model_name=config.model_name,
        model_available=False,
        prediction=0,
        prediction_label="unavailable",
        confidence=0.0,
        attack_probability=None,
        top_features=[],
        status=status,
    )
```

- [ ] **Step 5: Run service tests to verify they pass**

Run:

```bash
cd backend
.venv/bin/pytest tests/test_model_inference.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit Task 1**

Run:

```bash
git add backend/app/models.py backend/app/services/model_inference.py backend/tests/test_model_inference.py
git commit -m "feat: add model inference service"
```

---

### Task 2: API Endpoints

**Files:**
- Modify: `backend/app/main.py`
- Modify: `backend/tests/test_api.py`

- [ ] **Step 1: Write failing API tests**

Append to `backend/tests/test_api.py`:

```python
def test_default_inference_model_endpoint_reports_cicids2017_model() -> None:
    response = client.get("/ml/inference/default-model")

    assert response.status_code == 200
    payload = response.json()
    assert payload["dataset_id"] == "cicids2017-full"
    assert payload["model_name"] == "random_forest"
    assert "cicids2017-full-random_forest.joblib" in payload["model_path"]
    assert isinstance(payload["available"], bool)
    assert isinstance(payload["status"], str)


def test_sample_inference_endpoint_returns_structured_result() -> None:
    response = client.get("/ml/inference/sample")

    assert response.status_code == 200
    payload = response.json()
    assert payload["dataset_id"] == "cicids2017-full"
    assert payload["model_name"] == "random_forest"
    assert isinstance(payload["model_available"], bool)
    assert isinstance(payload["prediction"], int)
    assert isinstance(payload["prediction_label"], str)
    assert isinstance(payload["confidence"], float)
    assert "top_features" in payload
    assert isinstance(payload["status"], str)
```

- [ ] **Step 2: Run API tests to verify they fail**

Run:

```bash
cd backend
.venv/bin/pytest tests/test_api.py::test_default_inference_model_endpoint_reports_cicids2017_model tests/test_api.py::test_sample_inference_endpoint_returns_structured_result -v
```

Expected: FAIL with HTTP 404 because the endpoints are not registered.

- [ ] **Step 3: Add endpoint imports and handlers**

Modify imports in `backend/app/main.py`:

```python
from app.models import (
    Alert,
    DatasetInfo,
    Explanation,
    ExplanationComparison,
    InferenceModelInfo,
    InferenceResult,
    ModelEvaluation,
    NetworkEvent,
)
from app.services.model_inference import get_default_model_info, run_sample_inference
```

Add handlers near existing ML endpoints:

```python
@app.get("/ml/inference/default-model", response_model=InferenceModelInfo)
def ml_inference_default_model() -> InferenceModelInfo:
    return get_default_model_info()


@app.get("/ml/inference/sample", response_model=InferenceResult)
def ml_inference_sample() -> InferenceResult:
    return run_sample_inference()
```

- [ ] **Step 4: Run API tests to verify they pass**

Run:

```bash
cd backend
.venv/bin/pytest tests/test_api.py::test_default_inference_model_endpoint_reports_cicids2017_model tests/test_api.py::test_sample_inference_endpoint_returns_structured_result -v
```

Expected: PASS.

- [ ] **Step 5: Run backend tests**

Run:

```bash
cd backend
.venv/bin/pytest
```

Expected: all tests pass.

- [ ] **Step 6: Commit Task 2**

Run:

```bash
git add backend/app/main.py backend/tests/test_api.py
git commit -m "feat: expose model inference endpoints"
```

---

### Task 3: Frontend Inference Panel

**Files:**
- Modify: `frontend/src/main.tsx`
- Modify: `frontend/src/styles.css`

- [ ] **Step 1: Add TypeScript types and state**

Modify `frontend/src/main.tsx` near existing type definitions:

```typescript
type InferenceModelInfo = {
  dataset_id: string;
  model_name: string;
  model_path: string;
  available: boolean;
  status: string;
};

type InferenceResult = {
  dataset_id: string;
  model_name: string;
  model_available: boolean;
  prediction: number;
  prediction_label: string;
  confidence: number;
  attack_probability: number | null;
  top_features: string[];
  status: string;
};
```

Add state inside `App`:

```typescript
const [inferenceModel, setInferenceModel] = useState<InferenceModelInfo | null>(null);
const [inferenceResult, setInferenceResult] = useState<InferenceResult | null>(null);
```

- [ ] **Step 2: Fetch inference endpoints with dashboard data**

Modify the `Promise.all` call:

```typescript
const [alertsResponse, evaluationResponse, metricsResponse, inferenceModelResponse, inferenceSampleResponse] = await Promise.all([
  fetch("http://localhost:8000/alerts"),
  fetch("http://localhost:8000/ml/evaluate"),
  fetch("http://localhost:8000/ml/metrics"),
  fetch("http://localhost:8000/ml/inference/default-model"),
  fetch("http://localhost:8000/ml/inference/sample"),
]);
```

Parse and set state:

```typescript
const nextInferenceModel = (await inferenceModelResponse.json()) as InferenceModelInfo;
const nextInferenceResult = (await inferenceSampleResponse.json()) as InferenceResult;
setInferenceModel(nextInferenceModel);
setInferenceResult(nextInferenceResult);
```

Add fallback values in the `catch` block:

```typescript
setInferenceModel({
  dataset_id: "cicids2017-full",
  model_name: "random_forest",
  model_path: "reports/pipeline/cicids2017-full/models/cicids2017-full-random_forest.joblib",
  available: false,
  status: "backend unavailable",
});
setInferenceResult({
  dataset_id: "cicids2017-full",
  model_name: "random_forest",
  model_available: false,
  prediction: 0,
  prediction_label: "unavailable",
  confidence: 0,
  attack_probability: null,
  top_features: [],
  status: "backend unavailable",
});
```

- [ ] **Step 3: Render the inference panel**

Add this section after the `Model Comparison` section:

```tsx
<section className="panel inference-panel">
  <h2>Model Inference</h2>
  <div className="inference-grid">
    <article>
      <span>Default Model</span>
      <strong>{inferenceModel?.dataset_id ?? "cicids2017-full"} / {inferenceModel?.model_name ?? "random_forest"}</strong>
      <p>{inferenceModel?.status ?? "not loaded"}</p>
    </article>
    <article>
      <span>Sample Prediction</span>
      <strong>{inferenceResult?.prediction_label ?? "unavailable"}</strong>
      <p>Confidence: {formatPercent(inferenceResult?.confidence ?? 0)}</p>
    </article>
    <article>
      <span>Attack Probability</span>
      <strong>{inferenceResult?.attack_probability === null || inferenceResult?.attack_probability === undefined ? "n/a" : formatPercent(inferenceResult.attack_probability)}</strong>
      <p>{inferenceResult?.model_available ? "CICIDS2017 artifact loaded" : inferenceResult?.status ?? "model unavailable"}</p>
    </article>
  </div>
  <div className="feature-list">
    <span>Model features</span>
    {(inferenceResult?.top_features.length ? inferenceResult.top_features : ["artifact unavailable"]).map((feature) => <code key={feature}>{feature}</code>)}
  </div>
</section>
```

- [ ] **Step 4: Add panel styles**

Append to `frontend/src/styles.css`:

```css
.inference-panel { margin-top: 18px; }
.inference-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.inference-grid article { border: 1px solid #1f3b57; border-radius: 16px; padding: 16px; background: #071827; }
.inference-grid span { color: #67e8f9; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }
.inference-grid strong { display: block; margin: 8px 0; }
.inference-grid p { color: #b8d7e8; line-height: 1.55; }
@media (max-width: 820px) { .inference-grid { grid-template-columns: 1fr; } }
```

- [ ] **Step 5: Build frontend**

Run:

```bash
cd frontend
npm run build
```

Expected: TypeScript and Vite build pass.

- [ ] **Step 6: Commit Task 3**

Run:

```bash
git add frontend/src/main.tsx frontend/src/styles.css
git commit -m "feat: show model inference on dashboard"
```

---

### Task 4: Final Verification

**Files:**
- Verify all changed files.

- [ ] **Step 1: Run backend test suite**

Run:

```bash
cd backend
.venv/bin/pytest
```

Expected: all tests pass.

- [ ] **Step 2: Run frontend build**

Run:

```bash
cd frontend
npm run build
```

Expected: build passes.

- [ ] **Step 3: Check git status**

Run:

```bash
git status --short
```

Expected: clean working tree after commits, except ignored local artifacts.
