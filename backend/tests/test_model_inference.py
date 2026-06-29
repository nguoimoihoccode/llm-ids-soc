from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier

from app.services.model_inference import (
    InferenceModelConfig,
    get_default_model_info,
    run_sample_inference,
)


def test_default_model_info_reports_cicids2017_random_forest() -> None:
    info = get_default_model_info()

    assert info.dataset_id == "cicids2017-full"
    assert info.model_name == "random_forest"
    assert "cicids2017-full-random_forest.joblib" in info.model_path
    assert info.status in {"available", "missing model artifact"}


def test_sample_inference_returns_unavailable_when_model_is_missing(tmp_path: Path) -> None:
    config = InferenceModelConfig(
        dataset_id="cicids2017-full",
        model_name="random_forest",
        model_path=tmp_path / "missing.joblib",
    )

    result = run_sample_inference(config)

    assert result.dataset_id == "cicids2017-full"
    assert result.model_name == "random_forest"
    assert result.model_available is False
    assert result.prediction == 0
    assert result.prediction_label == "unavailable"
    assert result.confidence == 0.0
    assert result.attack_probability is None
    assert result.top_features == []
    assert result.status == "missing model artifact"


def test_sample_inference_loads_model_and_predicts(tmp_path: Path) -> None:
    model_path = tmp_path / "demo-random_forest.joblib"
    frame = pd.DataFrame(
        [
            {"Flow Duration": 1.0, "Total Fwd Packets": 1.0, "Flow Bytes/s": 10.0},
            {"Flow Duration": 1000.0, "Total Fwd Packets": 500.0, "Flow Bytes/s": 50000.0},
            {"Flow Duration": 1200.0, "Total Fwd Packets": 700.0, "Flow Bytes/s": 80000.0},
            {"Flow Duration": 2.0, "Total Fwd Packets": 1.0, "Flow Bytes/s": 12.0},
        ]
    )
    labels = [0, 1, 1, 0]
    model = RandomForestClassifier(n_estimators=5, random_state=42)
    model.fit(frame, labels)
    dump(model, model_path)
    config = InferenceModelConfig(
        dataset_id="demo",
        model_name="random_forest",
        model_path=model_path,
    )

    result = run_sample_inference(config)

    assert result.dataset_id == "demo"
    assert result.model_name == "random_forest"
    assert result.model_available is True
    assert result.prediction in {0, 1}
    assert result.prediction_label in {"benign", "attack"}
    assert 0.0 <= result.confidence <= 1.0
    assert result.attack_probability is not None
    assert 0.0 <= result.attack_probability <= 1.0
    assert len(result.top_features) > 0
    feature_names = [fi.feature for fi in result.top_features]
    assert feature_names[:3] == ["Flow Duration", "Total Fwd Packets", "Flow Bytes/s"]
    for fi in result.top_features:
        assert isinstance(fi.importance, float)
    assert result.status == "ok"
