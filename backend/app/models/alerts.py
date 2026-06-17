from pydantic import BaseModel


class NetworkEvent(BaseModel):
    # Mot luong mang dau vao duoc mo ta bang cac truong luong va chi so hanh vi.
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
    # Alert la san pham sau khi detector suy ra muc do nghiem trong va huong xu ly.
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
    # Giai thich de dashboard hien thi cho analyst doc nhanh.
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
    # Moi cach giai thich duoc luu rieng de so sanh template, no-RAG, va RAG.
    mode: str
    uses_rag: bool
    summary: str
    knowledge_context: str


class ExplanationComparison(BaseModel):
    alert_id: str
    comparisons: list[ExplanationComparisonItem]
