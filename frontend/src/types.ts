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
