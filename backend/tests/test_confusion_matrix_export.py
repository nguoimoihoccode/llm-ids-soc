import json
import subprocess
import sys
from pathlib import Path

from app.services.confusion_matrix_export import export_confusion_matrix_svgs


def test_export_confusion_matrix_svgs_writes_one_svg_per_metric(tmp_path: Path) -> None:
    metrics_dir = tmp_path / "metrics"
    figures_dir = tmp_path / "figures"
    metrics_dir.mkdir()
    (metrics_dir / "fixture-random_forest.json").write_text(
        json.dumps(
            {
                "dataset_id": "fixture",
                "model_name": "random_forest",
                "confusion_matrix": [[8, 1], [2, 9]],
            }
        ),
        encoding="utf-8",
    )

    outputs = export_confusion_matrix_svgs(metrics_dir, figures_dir)

    assert outputs == [figures_dir / "fixture-random_forest-confusion-matrix.svg"]
    svg = outputs[0].read_text(encoding="utf-8")
    assert "Confusion Matrix: fixture / random_forest" in svg
    assert "TN 8" in svg
    assert "FP 1" in svg
    assert "FN 2" in svg
    assert "TP 9" in svg


def test_export_confusion_matrix_script_writes_figures(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    figures_dir = tmp_path / "figures"

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "export_confusion_matrices.py"),
            "--metrics-dir",
            str(project_root / "models" / "metrics"),
            "--figures-dir",
            str(figures_dir),
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    assert "figures_exported" in result.stdout
    assert (figures_dir / "fixture-random_forest-confusion-matrix.svg").exists()
