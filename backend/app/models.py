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


class ModelEvaluation(BaseModel):
    model_name: str
    sample_count: int
    accuracy: float
    attack_recall: float
    benign_recall: float


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
