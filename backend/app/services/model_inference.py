from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd

from app.models import InferenceModelInfo, InferenceResult
from app.paths import REPORTS_ROOT


DEFAULT_MODEL_PATH = REPORTS_ROOT / "pipeline" / "cicids2017-full" / "models" / "cicids2017-full-random_forest.joblib"


@dataclass(frozen=True)
class InferenceModelConfig:
    dataset_id: str
    model_name: str
    model_path: Path


DEFAULT_MODEL_CONFIG = InferenceModelConfig(
    dataset_id="cicids2017-full",
    model_name="random_forest",
    model_path=DEFAULT_MODEL_PATH,
)


def get_default_model_info(config: InferenceModelConfig = DEFAULT_MODEL_CONFIG) -> InferenceModelInfo:
    available = config.model_path.exists()
    return InferenceModelInfo(
        dataset_id=config.dataset_id,
        model_name=config.model_name,
        model_path=str(config.model_path),
        available=available,
        status="available" if available else "missing model artifact",
    )


def run_sample_inference(config: InferenceModelConfig = DEFAULT_MODEL_CONFIG) -> InferenceResult:
    if not config.model_path.exists():
        return _unavailable_result(config, "missing model artifact")

    try:
        model = joblib.load(config.model_path)
    except Exception as exc:
        return _unavailable_result(config, f"failed to load model: {exc}")

    sample = _sample_frame_for_model(model)
    prediction = int(model.predict(sample)[0])
    attack_probability = _attack_probability(model, sample, prediction)
    confidence = attack_probability if prediction == 1 and attack_probability is not None else None
    if confidence is None and attack_probability is not None:
        confidence = 1.0 - attack_probability
    if confidence is None:
        confidence = 1.0

    return InferenceResult(
        dataset_id=config.dataset_id,
        model_name=config.model_name,
        model_available=True,
        prediction=prediction,
        prediction_label="attack" if prediction == 1 else "benign",
        confidence=float(confidence),
        attack_probability=attack_probability,
        top_features=list(sample.columns[:5]),
        status="ok",
    )


def _sample_frame_for_model(model) -> pd.DataFrame:
    feature_names = list(getattr(model, "feature_names_in_", []))
    if not feature_names:
        feature_names = ["Flow Duration", "Total Fwd Packets", "Flow Bytes/s"]

    row = {feature: 0.0 for feature in feature_names}
    defaults = {
        "Flow Duration": 1200.0,
        "Total Fwd Packets": 700.0,
        "Total Backward Packets": 5.0,
        "Flow Bytes/s": 80000.0,
        "Flow Packets/s": 3000.0,
        "SYN Flag Count": 1.0,
    }
    for feature, value in defaults.items():
        if feature in row:
            row[feature] = value
    return pd.DataFrame([row], columns=feature_names)


def _attack_probability(model, sample: pd.DataFrame, prediction: int) -> Optional[float]:
    if not hasattr(model, "predict_proba"):
        return None
    probabilities = model.predict_proba(sample)[0]
    classes = list(getattr(model, "classes_", []))
    if 1 in classes:
        return float(probabilities[classes.index(1)])
    return float(probabilities[prediction]) if prediction < len(probabilities) else None


def _unavailable_result(config: InferenceModelConfig, status: str) -> InferenceResult:
    return InferenceResult(
        dataset_id=config.dataset_id,
        model_name=config.model_name,
        model_available=False,
        prediction=0,
        prediction_label="unavailable",
        confidence=0.0,
        attack_probability=None,
        top_features=[],
        status=status,
    )
