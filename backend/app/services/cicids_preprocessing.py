from pathlib import Path

import pandas as pd

from app.models import PreprocessingSummary


def normalize_cicids_csv(raw_path: Path, output_path: Path) -> PreprocessingSummary:
    frame = pd.read_csv(raw_path)
    frame.columns = [column.strip() for column in frame.columns]
    if "Label" not in frame.columns:
        raise ValueError("CICIDS CSV must include a Label column.")

    labels = frame["Label"].astype(str).str.strip()
    attack_categories = sorted(labels.dropna().unique().tolist())
    frame["attack_cat"] = labels
    frame["label"] = labels.str.upper().ne("BENIGN").astype(int)
    frame = frame.drop(columns=["Label"])
    frame = frame.replace([float("inf"), float("-inf"), "inf", "-inf", "Infinity", "-Infinity"], 0)
    frame = frame.fillna(0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    return PreprocessingSummary(
        row_count=len(frame),
        feature_count=len(frame.columns),
        label_column="label",
        attack_categories=attack_categories,
    )
