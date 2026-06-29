import type { Alert, Evaluation, FeatureImportance, InferenceModelInfo, InferenceResult, ModelMetric } from "./types";

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
  {
    model_name: "logistic_regression",
    dataset_id: "fixture",
    accuracy: 1,
    precision: 1,
    recall: 1,
    f1_score: 1,
    false_positive_rate: 0,
  },
  {
    model_name: "decision_tree",
    dataset_id: "fixture",
    accuracy: 1,
    precision: 1,
    recall: 1,
    f1_score: 1,
    false_positive_rate: 0,
  },
  {
    model_name: "random_forest",
    dataset_id: "fixture",
    accuracy: 1,
    precision: 1,
    recall: 1,
    f1_score: 1,
    false_positive_rate: 0,
  },
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
