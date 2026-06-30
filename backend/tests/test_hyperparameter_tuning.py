import json
from pathlib import Path

import pandas as pd

from app.services.hyperparameter_tuning import (
    tune_and_save,
    load_best_params,
)


def test_tune_and_save_saves_best_params_file(tmp_path: Path) -> None:
    processed_path = tmp_path / "train.csv"
    frame = pd.DataFrame(
        [
            {"Flow Duration": 1.0, "Total Fwd Packets": 1.0, "Flow Bytes/s": 10.0, "label": 0},
            {"Flow Duration": 1000.0, "Total Fwd Packets": 500.0, "Flow Bytes/s": 50000.0, "label": 1},
            {"Flow Duration": 50.0, "Total Fwd Packets": 30.0, "Flow Bytes/s": 3000.0, "label": 0},
            {"Flow Duration": 900.0, "Total Fwd Packets": 400.0, "Flow Bytes/s": 45000.0, "label": 1},
            {"Flow Duration": 10.0, "Total Fwd Packets": 5.0, "Flow Bytes/s": 500.0, "label": 0},
            {"Flow Duration": 1200.0, "Total Fwd Packets": 700.0, "Flow Bytes/s": 80000.0, "label": 1},
            {"Flow Duration": 2.0, "Total Fwd Packets": 1.0, "Flow Bytes/s": 12.0, "label": 0},
            {"Flow Duration": 1100.0, "Total Fwd Packets": 600.0, "Flow Bytes/s": 70000.0, "label": 1},
        ]
    )
    processed_path.write_text(frame.to_csv(index=False), encoding="utf-8")
    output_dir = tmp_path / "tuning"

    result = tune_and_save("decision_tree", processed_path, output_dir, n_iter=10, cv=2)

    assert result["model_name"] == "decision_tree"
    assert 0.0 <= result["best_score"] <= 1.0
    assert result["scoring"] == "f1"
    assert isinstance(result["best_params"], dict)

    params_path = output_dir / "decision_tree-best-params.json"
    assert params_path.exists()
    loaded = json.loads(params_path.read_text(encoding="utf-8"))
    assert loaded["best_score"] == result["best_score"]


def test_load_best_params_returns_none_when_missing(tmp_path: Path) -> None:
    assert load_best_params(tmp_path / "nonexistent", "xgboost") is None


def test_load_best_params_returns_params_when_file_exists(tmp_path: Path) -> None:
    tuning_dir = tmp_path / "tuning"
    tuning_dir.mkdir()
    data = {"model_name": "xgboost", "best_score": 0.85, "scoring": "f1", "best_params": {"n_estimators": 200, "max_depth": 6}}
    (tuning_dir / "xgboost-best-params.json").write_text(json.dumps(data), encoding="utf-8")

    params = load_best_params(tuning_dir, "xgboost")
    assert params == {"n_estimators": 200, "max_depth": 6}
