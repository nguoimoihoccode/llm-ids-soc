from pathlib import Path

import pandas as pd

from app.models import PreprocessingSummary


def preprocess_unsw_nb15_csv(raw_path: Path, processed_path: Path) -> PreprocessingSummary:
    # Nap du lieu thuc, lam sach, roi luu ra file da xu ly de train model.
    frame = pd.read_csv(raw_path)
    attack_categories = sorted(str(value) for value in frame["attack_cat"].dropna().unique())

    # Khong de gia tri vo cuc pha hu cong doan train.
    frame = frame.replace([float("inf"), float("-inf"), "inf", "-inf", "Infinity", "-Infinity"], 0)
    frame = frame.fillna(0)

    # One-hot encode cac cot phan loai neu chung ton tai trong file nguon.
    categorical_columns = [column for column in ["proto", "service", "state", "attack_cat"] if column in frame.columns]
    frame = pd.get_dummies(frame, columns=categorical_columns, dtype=int)
    # Ep toan bo cot ve so de model scikit-learn doc duoc.
    frame = frame.apply(pd.to_numeric, errors="coerce").fillna(0)

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(processed_path, index=False)

    return PreprocessingSummary(
        row_count=len(frame),
        feature_count=len(frame.columns),
        label_column="label",
        attack_categories=attack_categories,
    )
