import subprocess
import sys
from pathlib import Path

from app.services.feature_importance_export import export_feature_importance_csvs


def test_export_feature_importance_csvs_writes_tree_model_importances(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    processed_path = project_root / "data" / "processed" / "unsw_nb15_fixture_processed.csv"
    models_dir = project_root / "models" / "trained"
    output_dir = tmp_path / "feature-importance"

    outputs = export_feature_importance_csvs(
        dataset_id="fixture",
        processed_path=processed_path,
        models_dir=models_dir,
        output_dir=output_dir,
    )

    output_names = {path.name for path in outputs}
    assert "fixture-decision_tree-feature-importance.csv" in output_names
    assert "fixture-random_forest-feature-importance.csv" in output_names
    assert "fixture-logistic_regression-feature-importance.csv" not in output_names
    csv_text = (output_dir / "fixture-random_forest-feature-importance.csv").read_text(encoding="utf-8")
    assert csv_text.startswith("feature,importance")


def test_export_feature_importance_script_writes_csvs(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    output_dir = tmp_path / "feature-importance"

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "export_feature_importance.py"),
            "--dataset-id",
            "fixture",
            "--input",
            str(project_root / "data" / "processed" / "unsw_nb15_fixture_processed.csv"),
            "--models-dir",
            str(project_root / "models" / "trained"),
            "--output-dir",
            str(output_dir),
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    assert "files_exported" in result.stdout
    assert (output_dir / "fixture-random_forest-feature-importance.csv").exists()
