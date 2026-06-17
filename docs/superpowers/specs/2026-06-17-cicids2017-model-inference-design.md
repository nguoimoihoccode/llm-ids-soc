# CICIDS2017 Model Inference Design

## Objective

Connect the existing trained ML artifacts to the FastAPI and React demo so the project can show real model inference instead of only rule-based sample alerts.

The default inference target is the local CICIDS2017 full Random Forest model:

```text
reports/pipeline/cicids2017-full/models/cicids2017-full-random_forest.joblib
```

Because CICIDS2017 artifacts are large and ignored by git, the API must report missing artifacts clearly and avoid crashing when the model is unavailable.

## Scope

In scope:

- Add backend model-inference schemas and service code.
- Expose default model metadata through the API.
- Expose sample inference through the API for dashboard demos.
- Prefer CICIDS2017 full Random Forest by default.
- Fall back gracefully when the CICIDS2017 artifact is absent.
- Add focused backend tests for available and missing model behavior.
- Add a small frontend panel that displays default model inference status and sample prediction.

Out of scope:

- Realtime packet capture.
- Training models from the web app.
- Uploading arbitrary CSV files through the UI.
- Full model registry UI.
- SHAP/LIME explainability.
- Real LLM provider integration.

## Architecture

```text
React Dashboard
  -> GET /ml/inference/default-model
  -> GET /ml/inference/sample
       -> model_inference service
          -> load configured joblib model if present
          -> build or load a sample feature row
          -> align row to trained feature columns
          -> predict class and optional probability
          -> return structured inference result
```

The backend owns all model-path and fallback logic. The frontend only renders the API result.

## Backend Components

### Models

Add Pydantic models in `backend/app/models.py`:

- `InferenceModelInfo`
  - `dataset_id`
  - `model_name`
  - `model_path`
  - `available`
  - `status`
- `InferenceResult`
  - `dataset_id`
  - `model_name`
  - `model_available`
  - `prediction`
  - `prediction_label`
  - `confidence`
  - `attack_probability`
  - `top_features`
  - `status`

The response should remain useful even when the model is missing. In that case, prediction values can be neutral and `status` explains the missing artifact.

### Service

Add `backend/app/services/model_inference.py`.

Responsibilities:

- Define the default model config for `cicids2017-full` and `random_forest`.
- Check whether the model artifact exists.
- Load the model with `joblib`.
- Use a deterministic sample feature row for demo inference.
- Align the feature row with `feature_names_in_` when available.
- Return prediction and probability if the model supports `predict_proba`.
- Return a non-crashing unavailable result when the artifact is absent.

The deterministic sample should be small and code-defined, not loaded from the 924 MB processed CICIDS2017 CSV. This keeps API startup and tests fast.

## API

Add endpoints in `backend/app/main.py`:

- `GET /ml/inference/default-model`
  - Returns default model metadata and availability.
- `GET /ml/inference/sample`
  - Runs inference on the deterministic sample row if the model exists.
  - Returns unavailable status if the default model artifact is missing.

The endpoint names are intentionally narrow. A broader `POST /ml/inference` can be added later after deciding the public request schema for arbitrary rows.

## Frontend

Add a `Model Inference` panel to `frontend/src/main.tsx`.

The panel should show:

- Default dataset and model name.
- Availability/status.
- Prediction label.
- Confidence or attack probability when present.
- Top feature names returned by the backend.

If the backend or model is unavailable, the UI should show a readable fallback message instead of hiding the section.

## Error Handling

- Missing CICIDS2017 model artifact returns HTTP 200 with `model_available: false`.
- Corrupt model load may return an unavailable-style result with an explanatory status.
- Unexpected API errors should still be caught by the frontend's existing dashboard fallback path.

This behavior supports both thesis demo machines with local artifacts and fresh clones without large generated files.

## Testing

Backend tests:

- Default model metadata reports CICIDS2017 Random Forest.
- Missing default model returns an unavailable inference result, not an exception.
- A temporary trained fixture model can be loaded and used for prediction.
- API endpoints return the expected schema.

Frontend verification:

- `npm run build` must pass after adding the panel.

Full verification:

```bash
cd backend
.venv/bin/pytest

cd ../frontend
npm run build
```

## Future Work

- Add a full model registry for fixture, UNSW-NB15, and CICIDS2017 artifacts.
- Add `POST /ml/inference` for arbitrary feature rows.
- Convert predictions into alert objects for dashboard triage.
- Add SHAP or LIME to explain individual predictions.
