# Backend Domain Cleanup Design

## Objective

Clean the backend by splitting the shared schema file into domain-focused modules and centralizing project path resolution in one helper module.

This cleanup must preserve all current endpoints, response payloads, and tests.

## Scope

In scope:

- Split `backend/app/models.py` into smaller domain files.
- Keep existing imports working through `backend/app/models/__init__.py`.
- Add a shared path helper for project/data/reports roots.
- Replace `Path(__file__).resolve().parents[3]` style access in services with the shared helper.
- Keep the current FastAPI routes and service behavior unchanged.

Out of scope:

- Splitting `main.py` into routers.
- Changing any API payloads or route paths.
- Changing model training, dataset handling, or frontend code.
- Renaming existing endpoints.
- Adding new features.

## Target File Structure

```text
backend/app/
  config.py
  main.py
  models/
    __init__.py
    alerts.py
    datasets.py
    ml.py
  paths.py
  services/
    ...
```

## Components And Responsibilities

### `backend/app/models/alerts.py`

Owns alert and explanation schema:

- `NetworkEvent`
- `Alert`
- `Explanation`
- `ExplanationComparisonItem`
- `ExplanationComparison`

### `backend/app/models/datasets.py`

Owns dataset and preprocessing schema:

- `DatasetInfo`
- `PreprocessingSummary`
- `DatasetProfile`
- `DatasetSplitSummary`
- `DatasetValidationResult`

### `backend/app/models/ml.py`

Owns ML and inference schema:

- `ModelEvaluation`
- `InferenceModelInfo`
- `InferenceResult`

### `backend/app/models/__init__.py`

Re-exports the public schema types so existing imports like `from app.models import Alert` continue to work.

### `backend/app/paths.py`

Provides shared repository path constants:

- `PROJECT_ROOT`
- `DATA_ROOT`
- `RAW_DATA_ROOT`
- `PROCESSED_DATA_ROOT`
- `MODELS_ROOT`
- `REPORTS_ROOT`
- `KNOWLEDGE_BASE_ROOT`
- `PLAYBOOKS_ROOT`

Services should import these constants instead of computing `parents[3]` locally.

## Error Handling

The cleanup must not change runtime behavior.

- Missing artifact behavior stays the same.
- Existing route responses stay the same.
- Existing tests should continue to pass without changes to their expectations.

## Testing

Verification is the backend test suite:

```bash
cd backend
.venv/bin/pytest
```

The suite should still pass after the import and path cleanup.
