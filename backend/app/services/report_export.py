import csv
from pathlib import Path

from app.services.metric_artifacts import list_metric_artifacts


MODEL_COMPARISON_FIELDS = [
    "dataset_id",
    "model_name",
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "false_positive_rate",
]


def export_model_comparison_csv(metrics_dir: Path, output_path: Path) -> int:
    metrics = sorted(
        list_metric_artifacts(metrics_dir),
        key=lambda metric: (str(metric.get("dataset_id", "")), str(metric.get("model_name", ""))),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=MODEL_COMPARISON_FIELDS)
        writer.writeheader()
        for metric in metrics:
            writer.writerow({field: metric.get(field, "") for field in MODEL_COMPARISON_FIELDS})
    return len(metrics)
