import csv
from pathlib import Path

import joblib
import pandas as pd


def export_feature_importance_csvs(
    dataset_id: str,
    processed_path: Path,
    models_dir: Path,
    output_dir: Path,
) -> list[Path]:
    frame = pd.read_csv(processed_path)
    feature_names = [column for column in frame.columns if column != "label"]
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs: list[Path] = []
    for model_path in sorted(models_dir.glob(f"{dataset_id}-*.joblib")):
        model = joblib.load(model_path)
        importances = getattr(model, "feature_importances_", None)
        if importances is None:
            continue

        model_name = model_path.stem.replace(f"{dataset_id}-", "")
        output_path = output_dir / f"{dataset_id}-{model_name}-feature-importance.csv"
        _write_importances(output_path, feature_names, importances)
        outputs.append(output_path)

    return outputs


def _write_importances(output_path: Path, feature_names: list[str], importances) -> None:
    rows = sorted(
        zip(feature_names, [float(value) for value in importances]),
        key=lambda item: item[1],
        reverse=True,
    )
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["feature", "importance"])
        writer.writerows(rows)
