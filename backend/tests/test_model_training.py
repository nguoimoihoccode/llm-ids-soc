import json
import subprocess
import sys
from pathlib import Path

from app.services.model_training import train_models_from_csv


def test_train_models_from_csv_writes_metrics_and_models(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    data_path = project_root / "data" / "processed" / "unsw_nb15_fixture_processed.csv"
    metrics_dir = tmp_path / "metrics"
    models_dir = tmp_path / "trained"

    results = train_models_from_csv(
        dataset_id="fixture",
        processed_path=data_path,
        metrics_dir=metrics_dir,
        models_dir=models_dir,
        model_names=["logistic_regression", "decision_tree", "random_forest"],
    )

    assert [result["model_name"] for result in results] == ["logistic_regression", "decision_tree", "random_forest"]
    assert (metrics_dir / "fixture-logistic_regression.json").exists()
    assert (metrics_dir / "fixture-decision_tree.json").exists()
    assert (metrics_dir / "fixture-random_forest.json").exists()
    assert (models_dir / "fixture-logistic_regression.joblib").exists()
    assert (models_dir / "fixture-decision_tree.joblib").exists()
    assert (models_dir / "fixture-random_forest.joblib").exists()


def test_train_models_script_writes_metrics_and_models(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    data_path = project_root / "data" / "processed" / "unsw_nb15_fixture_processed.csv"
    metrics_dir = tmp_path / "metrics"
    models_dir = tmp_path / "trained"

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "train_models.py"),
            "--dataset-id",
            "fixture",
            "--input",
            str(data_path),
            "--metrics-dir",
            str(metrics_dir),
            "--models-dir",
            str(models_dir),
            "--models",
            "logistic_regression,decision_tree,random_forest",
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert len(payload) == 3
    assert (metrics_dir / "fixture-logistic_regression.json").exists()
    assert (metrics_dir / "fixture-decision_tree.json").exists()
    assert (models_dir / "fixture-random_forest.joblib").exists()
