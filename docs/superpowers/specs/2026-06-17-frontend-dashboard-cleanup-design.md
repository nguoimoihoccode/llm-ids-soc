# Frontend Dashboard Cleanup Design

## Objective

Clean the frontend dashboard source by splitting `frontend/src/main.tsx` into small files with clear responsibilities while preserving the current UI and behavior.

The cleanup should make future dashboard work easier without changing API contracts, displayed text, or fallback behavior.

## Scope

In scope:

- Move shared TypeScript types out of `main.tsx`.
- Move backend fetch logic into a small API module.
- Move sample and fallback dashboard data into a data module.
- Move the dashboard component into `App.tsx`.
- Keep `main.tsx` focused on React root rendering.
- Keep existing CSS as-is unless imports need adjustment.

Out of scope:

- Redesigning the dashboard UI.
- Splitting every visual block into its own component.
- Adding custom hooks.
- Changing backend endpoints.
- Changing model inference, LLM, or alert behavior.
- Refactoring CSS architecture.

## Target File Structure

```text
frontend/src/
  App.tsx
  api.ts
  main.tsx
  sampleData.ts
  styles.css
  types.ts
  vite-env.d.ts
```

## Components And Responsibilities

### `types.ts`

Owns dashboard DTO and view types:

- `Alert`
- `Evaluation`
- `Explanation`
- `ExplanationComparisonItem`
- `ExplanationComparison`
- `ModelMetric`
- `InferenceModelInfo`
- `InferenceResult`

### `sampleData.ts`

Owns deterministic fallback data used when the backend is unavailable:

- `sampleAlerts`
- `fallbackEvaluation`
- `fallbackModelMetrics`
- `fallbackInferenceModel`
- `fallbackInferenceResult`

### `api.ts`

Owns HTTP calls and API base URL:

- `API_BASE_URL`
- `loadDashboardData()`
- `loadAlertExplanation(alertId)`
- `loadAlertExplanationComparison(alertId)`

`loadDashboardData()` should fetch alerts, ML evaluation, saved metrics, default inference model metadata, and sample inference in parallel.

### `App.tsx`

Owns dashboard state and JSX layout. It imports types, fallback data, and API helpers instead of defining everything inline.

### `main.tsx`

Only imports React root, `App`, and `styles.css`, then renders the application.

## Error Handling

Keep the existing behavior: if backend calls fail, the dashboard renders fallback alerts, fixture metrics, and unavailable CICIDS2017 inference status.

## Testing

Verification is frontend build:

```bash
cd frontend
npm run build
```

Full repo verification can also run:

```bash
cd backend
.venv/bin/pytest
```

No backend behavior should change.
