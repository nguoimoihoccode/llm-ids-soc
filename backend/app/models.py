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


class ModelEvaluation(BaseModel):
    # Ket qua danh gia mau cho baseline rule-based.
    model_name: str
    sample_count: int
    accuracy: float
    attack_recall: float
    benign_recall: float


class DatasetInfo(BaseModel):
    # Metadata co ban cho dataset trong demo.
    dataset_id: str
    name: str
    status: str
    source_url: str
    purpose: str


class PreprocessingSummary(BaseModel):
    # Tom tat ket qua xu ly du lieu de in ra sau khi preprocess.
    row_count: int
    feature_count: int
    label_column: str
    attack_categories: list[str]


class DatasetProfile(BaseModel):
    # Ho so dataset: kich thuoc, cot, phan bo label va muc lech lop.
    row_count: int
    column_count: int
    columns: list[str]
    label_distribution: dict[str, int]
    label_percentages: dict[str, float]
    label_imbalance_ratio: float
    attack_category_distribution: dict[str, int]
    attack_category_percentages: dict[str, float]
    attack_category_imbalance_ratio: float
    missing_value_count: int


class DatasetSplitSummary(BaseModel):
    # Tom tat sau khi tach train/test de biet so dong va label co can bang khong.
    total_rows: int
    train_rows: int
    test_rows: int
    label_column: str
    test_size: float
    random_state: int
    stratified: bool
    split_strategy: str
    train_label_distribution: dict[str, int]
    test_label_distribution: dict[str, int]
