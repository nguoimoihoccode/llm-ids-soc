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
  const [alertsResponse, evaluationResponse, metricsResponse, inferenceModelResponse, inferenceSampleResponse] =
    await Promise.all([
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
