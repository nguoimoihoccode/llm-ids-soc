# Frontend Dashboard Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split the React dashboard source into focused frontend modules without changing UI behavior.

**Architecture:** Keep the existing dashboard component and CSS behavior, but move DTO types, fallback data, and API calls out of `main.tsx`. `main.tsx` becomes the React root only, `App.tsx` owns dashboard state/layout, and helper modules provide typed data boundaries.

**Tech Stack:** React, TypeScript, Vite.

---

## File Structure

- Create `frontend/src/types.ts`: shared dashboard DTO types.
- Create `frontend/src/sampleData.ts`: deterministic fallback data used when backend calls fail.
- Create `frontend/src/api.ts`: backend API base URL and typed fetch helpers.
- Create `frontend/src/App.tsx`: dashboard component currently embedded in `main.tsx`.
- Modify `frontend/src/main.tsx`: render `<App />` and import CSS.
- Keep `frontend/src/styles.css`: no CSS architecture refactor in this cleanup.

---

### Task 1: Extract Frontend Types

**Files:**
- Create: `frontend/src/types.ts`
- Modify: `frontend/src/main.tsx`
- Test: `frontend` build after Task 3

- [ ] **Step 1: Create `frontend/src/types.ts`**

Create `frontend/src/types.ts` with:

```typescript
export type Alert = {
  alert_id: string;
  timestamp: string;
  src_ip: string;
  dst_ip: string;
  attack_type: string;
  severity: string;
  confidence: number;
  reason: string;
  top_features: string[];
  mitre_technique: string;
  triage_priority: string;
};

export type Evaluation = {
  model_name: string;
  sample_count: number;
  accuracy: number;
  attack_recall: number;
  benign_recall: number;
};

export type Explanation = {
  alert_id: string;
  provider: string;
  summary: string;
  why_suspicious: string;
  evidence_features: string[];
  mitre_technique: string;
  triage_priority: string;
  recommended_response: string[];
};

export type ExplanationComparisonItem = {
  mode: string;
  uses_rag: boolean;
  summary: string;
  knowledge_context: string;
};

export type ExplanationComparison = {
  alert_id: string;
  comparisons: ExplanationComparisonItem[];
};

export type ModelMetric = {
  model_name: string;
  dataset_id: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  false_positive_rate: number;
};

export type InferenceModelInfo = {
  dataset_id: string;
  model_name: string;
  model_path: string;
  available: boolean;
  status: string;
};

export type InferenceResult = {
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

- [ ] **Step 2: Leave `main.tsx` unchanged for now**

Do not modify `frontend/src/main.tsx` until Tasks 2 and 3 are ready. This keeps the app buildable while helper files are introduced.

- [ ] **Step 3: Commit Task 1**

Run:

```bash
git add frontend/src/types.ts
git commit -m "refactor: extract frontend dashboard types"
```

---

### Task 2: Extract Fallback Data

**Files:**
- Create: `frontend/src/sampleData.ts`
- Test: `frontend` build after Task 3

- [ ] **Step 1: Create `frontend/src/sampleData.ts`**

Create `frontend/src/sampleData.ts` with:

```typescript
import type { Alert, Evaluation, InferenceModelInfo, InferenceResult, ModelMetric } from "./types";

export const sampleAlerts: Alert[] = [
  {
    alert_id: "alert-evt-002",
    timestamp: "2026-06-03T09:02:05Z",
    src_ip: "192.168.1.45",
    dst_ip: "10.0.0.8",
    attack_type: "Brute Force",
    severity: "High",
    confidence: 0.94,
    reason: "80 failed login attempts against port 22.",
    top_features: ["failed_login_count", "dst_port", "flow_packets_s"],
    mitre_technique: "T1110 - Brute Force",
    triage_priority: "P1",
  },
  {
    alert_id: "alert-evt-003",
    timestamp: "2026-06-03T09:04:31Z",
    src_ip: "172.16.4.20",
    dst_ip: "10.0.0.12",
    attack_type: "DDoS",
    severity: "High",
    confidence: 0.92,
    reason: "High packet rate targeting web service.",
    top_features: ["flow_packets_s", "total_fwd_packets", "flow_bytes_s"],
    mitre_technique: "T1498 - Network Denial of Service",
    triage_priority: "P1",
  },
];

export const fallbackEvaluation: Evaluation = {
  model_name: "RuleBasedBaseline",
  sample_count: 5,
  accuracy: 1,
  attack_recall: 1,
  benign_recall: 1,
};

export const fallbackModelMetrics: ModelMetric[] = [
  { model_name: "logistic_regression", dataset_id: "fixture", accuracy: 1, precision: 1, recall: 1, f1_score: 1, false_positive_rate: 0 },
  { model_name: "decision_tree", dataset_id: "fixture", accuracy: 1, precision: 1, recall: 1, f1_score: 1, false_positive_rate: 0 },
  { model_name: "random_forest", dataset_id: "fixture", accuracy: 1, precision: 1, recall: 1, f1_score: 1, false_positive_rate: 0 },
];

export const fallbackInferenceModel: InferenceModelInfo = {
  dataset_id: "cicids2017-full",
  model_name: "random_forest",
  model_path: "reports/pipeline/cicids2017-full/models/cicids2017-full-random_forest.joblib",
  available: false,
  status: "backend unavailable",
};

export const fallbackInferenceResult: InferenceResult = {
  dataset_id: "cicids2017-full",
  model_name: "random_forest",
  model_available: false,
  prediction: 0,
  prediction_label: "unavailable",
  confidence: 0,
  attack_probability: null,
  top_features: [],
  status: "backend unavailable",
};
```

- [ ] **Step 2: Commit Task 2**

Run:

```bash
git add frontend/src/sampleData.ts
git commit -m "refactor: extract frontend fallback data"
```

---

### Task 3: Extract API Helpers

**Files:**
- Create: `frontend/src/api.ts`
- Test: `frontend` build after Task 4

- [ ] **Step 1: Create `frontend/src/api.ts`**

Create `frontend/src/api.ts` with:

```typescript
import type {
  Alert,
  Evaluation,
  Explanation,
  ExplanationComparison,
  InferenceModelInfo,
  InferenceResult,
  ModelMetric,
} from "./types";

export const API_BASE_URL = "http://localhost:8000";

export type DashboardData = {
  alerts: Alert[];
  evaluation: Evaluation;
  modelMetrics: ModelMetric[];
  inferenceModel: InferenceModelInfo;
  inferenceResult: InferenceResult;
};

export async function loadDashboardData(): Promise<DashboardData> {
  const [alertsResponse, evaluationResponse, metricsResponse, inferenceModelResponse, inferenceSampleResponse] = await Promise.all([
    fetch(`${API_BASE_URL}/alerts`),
    fetch(`${API_BASE_URL}/ml/evaluate`),
    fetch(`${API_BASE_URL}/ml/metrics`),
    fetch(`${API_BASE_URL}/ml/inference/default-model`),
    fetch(`${API_BASE_URL}/ml/inference/sample`),
  ]);

  return {
    alerts: (await alertsResponse.json()) as Alert[],
    evaluation: (await evaluationResponse.json()) as Evaluation,
    modelMetrics: (await metricsResponse.json()) as ModelMetric[],
    inferenceModel: (await inferenceModelResponse.json()) as InferenceModelInfo,
    inferenceResult: (await inferenceSampleResponse.json()) as InferenceResult,
  };
}

export async function loadAlertExplanation(alertId: string): Promise<Explanation> {
  const response = await fetch(`${API_BASE_URL}/alerts/${alertId}/explanation`);
  return (await response.json()) as Explanation;
}

export async function loadAlertExplanationComparison(alertId: string): Promise<ExplanationComparison> {
  const response = await fetch(`${API_BASE_URL}/alerts/${alertId}/explanation/comparison`);
  return (await response.json()) as ExplanationComparison;
}
```

- [ ] **Step 2: Commit Task 3**

Run:

```bash
git add frontend/src/api.ts
git commit -m "refactor: extract frontend api helpers"
```

---

### Task 4: Move Dashboard Component To App

**Files:**
- Create: `frontend/src/App.tsx`
- Modify: `frontend/src/main.tsx`
- Test: `frontend` build

- [ ] **Step 1: Move current dashboard implementation into `App.tsx`**

Create `frontend/src/App.tsx` by moving the current `App` component and `formatPercent` helper out of `frontend/src/main.tsx`.

At the top of `frontend/src/App.tsx`, use these imports:

```typescript
import { useEffect, useState } from "react";
import { loadAlertExplanation, loadAlertExplanationComparison, loadDashboardData } from "./api";
import {
  fallbackEvaluation,
  fallbackInferenceModel,
  fallbackInferenceResult,
  fallbackModelMetrics,
  sampleAlerts,
} from "./sampleData";
import type { Evaluation, Explanation, ExplanationComparison, InferenceModelInfo, InferenceResult, ModelMetric } from "./types";
```

Inside `App`, keep the same state shape:

```typescript
const [alerts, setAlerts] = useState(sampleAlerts);
const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
const [explanation, setExplanation] = useState<Explanation | null>(null);
const [comparison, setComparison] = useState<ExplanationComparison | null>(null);
const [modelMetrics, setModelMetrics] = useState<ModelMetric[]>([]);
const [inferenceModel, setInferenceModel] = useState<InferenceModelInfo | null>(null);
const [inferenceResult, setInferenceResult] = useState<InferenceResult | null>(null);
const selected = alerts[0];
```

Replace the inline fetch block in `loadDashboard()` with:

```typescript
const dashboardData = await loadDashboardData();
setAlerts(dashboardData.alerts);
setEvaluation(dashboardData.evaluation);
setModelMetrics(dashboardData.modelMetrics);
setInferenceModel(dashboardData.inferenceModel);
setInferenceResult(dashboardData.inferenceResult);

if (dashboardData.alerts[0]) {
  setExplanation(await loadAlertExplanation(dashboardData.alerts[0].alert_id));
  setComparison(await loadAlertExplanationComparison(dashboardData.alerts[0].alert_id));
}
```

Replace the catch block body with:

```typescript
setEvaluation(fallbackEvaluation);
setModelMetrics(fallbackModelMetrics);
setInferenceModel(fallbackInferenceModel);
setInferenceResult(fallbackInferenceResult);
```

Export the component:

```typescript
export default App;
```

- [ ] **Step 2: Replace `frontend/src/main.tsx` with root rendering only**

Replace `frontend/src/main.tsx` with:

```typescript
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

- [ ] **Step 3: Run frontend build**

Run:

```bash
cd frontend
npm run build
```

Expected: TypeScript and Vite build pass.

- [ ] **Step 4: Commit Task 4**

Run:

```bash
git add frontend/src/App.tsx frontend/src/main.tsx
git commit -m "refactor: move dashboard app component"
```

---

### Task 5: Final Verification

**Files:**
- Verify all frontend refactor files.

- [ ] **Step 1: Run frontend build**

Run:

```bash
cd frontend
npm run build
```

Expected: build passes.

- [ ] **Step 2: Run backend tests**

Run:

```bash
cd backend
.venv/bin/pytest
```

Expected: all tests pass. This confirms no frontend refactor accidentally changed backend-tracked files or repo assumptions.

- [ ] **Step 3: Check git status**

Run:

```bash
git status --short
```

Expected: only ignored build/cache artifacts remain, or clean tracked state after commits.
