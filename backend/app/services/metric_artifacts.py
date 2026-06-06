import json
from pathlib import Path


DEFAULT_METRICS_DIR = Path(__file__).resolve().parents[3] / "models" / "metrics"


def list_metric_artifacts(metrics_dir: Path = DEFAULT_METRICS_DIR) -> list[dict[str, object]]:
    if not metrics_dir.exists():
        return []

    metrics: list[dict[str, object]] = []
    for path in sorted(metrics_dir.glob("*.json")):
        metrics.append(json.loads(path.read_text(encoding="utf-8")))
    return metrics
