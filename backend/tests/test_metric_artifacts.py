import json
from pathlib import Path

from app.services.metric_artifacts import list_metric_artifacts


def test_list_metric_artifacts_reads_metrics_json(tmp_path: Path) -> None:
    metric_path = tmp_path / "fixture-random_forest.json"
    metric_path.write_text(
        json.dumps(
            {
                "model_name": "random_forest",
                "dataset_id": "fixture",
                "accuracy": 0.9,
                "precision": 0.8,
                "recall": 1.0,
                "f1_score": 0.88,
                "false_positive_rate": 0.1,
                "confusion_matrix": [[8, 1], [0, 9]],
            }
        ),
        encoding="utf-8",
    )

    metrics = list_metric_artifacts(tmp_path)

    assert len(metrics) == 1
    assert metrics[0]["model_name"] == "random_forest"
    assert metrics[0]["dataset_id"] == "fixture"
    assert metrics[0]["f1_score"] == 0.88
