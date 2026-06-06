import json
import subprocess
import sys
from pathlib import Path

from app.services.report_export import export_model_comparison_csv


def test_export_model_comparison_csv_writes_sorted_rows(tmp_path: Path) -> None:
    metrics_dir = tmp_path / "metrics"
    metrics_dir.mkdir()
    (metrics_dir / "fixture-random_forest.json").write_text(
        json.dumps({"dataset_id": "fixture", "model_name": "random_forest", "accuracy": 0.9, "precision": 0.8, "recall": 0.7, "f1_score": 0.75, "false_positive_rate": 0.1}),
        encoding="utf-8",
    )
    (metrics_dir / "fixture-decision_tree.json").write_text(
        json.dumps({"dataset_id": "fixture", "model_name": "decision_tree", "accuracy": 1.0, "precision": 1.0, "recall": 1.0, "f1_score": 1.0, "false_positive_rate": 0.0}),
        encoding="utf-8",
    )
    output_path = tmp_path / "model-comparison.csv"

    row_count = export_model_comparison_csv(metrics_dir, output_path)

    assert row_count == 2
    assert output_path.read_text(encoding="utf-8").splitlines() == [
        "dataset_id,model_name,accuracy,precision,recall,f1_score,false_positive_rate",
        "fixture,decision_tree,1.0,1.0,1.0,1.0,0.0",
        "fixture,random_forest,0.9,0.8,0.7,0.75,0.1",
    ]


def test_export_model_comparison_script_writes_csv(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    output_path = tmp_path / "model-comparison.csv"

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "export_model_comparison.py"),
            "--metrics-dir",
            str(project_root / "models" / "metrics"),
            "--output",
            str(output_path),
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    assert "rows_exported" in result.stdout
    assert output_path.exists()
    assert "random_forest" in output_path.read_text(encoding="utf-8")
