import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from app.services.model_metrics import calculate_binary_metrics


def train_models_from_csv(
    dataset_id: str,
    processed_path: Path,
    metrics_dir: Path,
    models_dir: Path,
    model_names: list[str],
) -> list[dict[str, object]]:
    frame = pd.read_csv(processed_path)
    if "label" not in frame.columns:
        raise ValueError("Processed dataset must include a label column.")

    x = frame.drop(columns=["label"])
    y = frame["label"].astype(int)
    metrics_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, object]] = []
    for model_name in model_names:
        model = _build_model(model_name)
        model.fit(x, y)
        predictions = model.predict(x).astype(int).tolist()
        metrics = calculate_binary_metrics(model_name, dataset_id, y.astype(int).tolist(), predictions)

        metrics_path = metrics_dir / f"{dataset_id}-{model_name}.json"
        metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        joblib.dump(model, models_dir / f"{dataset_id}-{model_name}.joblib")
        results.append(metrics)

    return results


def _build_model(model_name: str):
    if model_name == "logistic_regression":
        return LogisticRegression(max_iter=1000, random_state=42)
    if model_name == "decision_tree":
        return DecisionTreeClassifier(random_state=42)
    if model_name == "random_forest":
        return RandomForestClassifier(n_estimators=20, random_state=42)
    raise ValueError(f"Unsupported model: {model_name}")
