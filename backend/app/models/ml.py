from typing import Optional

from pydantic import BaseModel


class FeatureImportance(BaseModel):
    feature: str
    importance: float


class ModelEvaluation(BaseModel):
    # Ket qua danh gia mau cho baseline rule-based.
    model_name: str
    sample_count: int
    accuracy: float
    attack_recall: float
    benign_recall: float


class InferenceModelInfo(BaseModel):
    dataset_id: str
    model_name: str
    model_path: str
    available: bool
    status: str


class InferenceResult(BaseModel):
    dataset_id: str
    model_name: str
    model_available: bool
    prediction: int
    prediction_label: str
    confidence: float
    attack_probability: Optional[float]
    top_features: list[FeatureImportance]
    status: str
