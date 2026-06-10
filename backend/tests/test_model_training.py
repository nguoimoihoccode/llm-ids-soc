import json
import subprocess
import sys
from pathlib import Path

from app.services.model_training import train_models_from_csv, train_models_from_split_csv


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


def test_train_models_script_accepts_train_and_test_inputs(tmp_path: Path) -> None:
    # Kiem tra CLI moi chap nhan train-input/test-input va ghi artifact dung.
    project_root = Path(__file__).resolve().parents[2]
    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    metrics_dir = tmp_path / "metrics"
    models_dir = tmp_path / "trained"
    train_path.write_text(
        "feature,label\n"
        "0,0\n"
        "1,0\n"
        "10,1\n"
        "11,1\n",
        encoding="utf-8",
    )
    test_path.write_text("feature,label\n2,0\n12,1\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "train_models.py"),
            "--dataset-id",
            "split-fixture",
            "--train-input",
            str(train_path),
            "--test-input",
            str(test_path),
            "--metrics-dir",
            str(metrics_dir),
            "--models-dir",
            str(models_dir),
            "--models",
            "decision_tree",
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload[0]["sample_count"] == 2
    assert (metrics_dir / "split-fixture-decision_tree.json").exists()
    assert (models_dir / "split-fixture-decision_tree.joblib").exists()


def test_train_models_from_split_csv_evaluates_on_test_file(tmp_path: Path) -> None:
    # Kiem tra service train tren train.csv nhung sample_count metric lay tu test.csv.
    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    metrics_dir = tmp_path / "metrics"
    models_dir = tmp_path / "trained"
    train_path.write_text(
        "feature,label\n"
        "0,0\n"
        "1,0\n"
        "10,1\n"
        "11,1\n",
        encoding="utf-8",
    )
    test_path.write_text(
        "feature,label\n"
        "2,0\n"
        "12,1\n",
        encoding="utf-8",
    )

    results = train_models_from_split_csv(
        dataset_id="split-fixture",
        train_path=train_path,
        test_path=test_path,
        metrics_dir=metrics_dir,
        models_dir=models_dir,
        model_names=["decision_tree"],
    )

    assert len(results) == 1
    assert results[0]["sample_count"] == 2
    assert (metrics_dir / "split-fixture-decision_tree.json").exists()
    assert (models_dir / "split-fixture-decision_tree.joblib").exists()
