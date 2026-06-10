from pathlib import Path

import pandas as pd

from app.models import DatasetProfile


def _value_counts(frame: pd.DataFrame, column: str) -> dict[str, int]:
    # Dem so mau theo tung gia tri cua cot; thieu cot thi tra dict rong.
    if column not in frame.columns:
        return {}
    counts = frame[column].fillna("Unknown").astype(str).value_counts().sort_index()
    return {label: int(count) for label, count in counts.items()}


def _percentages(counts: dict[str, int]) -> dict[str, float]:
    # Doi so luong thanh phan tram de nhin phan bo lop nhanh hon.
    total = sum(counts.values())
    if total == 0:
        return {}
    return {label: round((count / total) * 100, 2) for label, count in counts.items()}


def _imbalance_ratio(counts: dict[str, int]) -> float:
    # Ty le lech lop = lop dong nhat / lop it nhat, cang cao cang mat can bang.
    if not counts:
        return 0.0
    non_zero_counts = [count for count in counts.values() if count > 0]
    if not non_zero_counts:
        return 0.0
    return round(max(non_zero_counts) / min(non_zero_counts), 2)


def profile_dataset_csv(csv_path: Path) -> DatasetProfile:
    # Doc CSV raw va tao report tong quan truoc khi preprocess/train.
    frame = pd.read_csv(csv_path)
    label_distribution = _value_counts(frame, "label")
    attack_category_distribution = _value_counts(frame, "attack_cat")

    return DatasetProfile(
        row_count=len(frame),
        column_count=len(frame.columns),
        columns=list(frame.columns),
        label_distribution=label_distribution,
        label_percentages=_percentages(label_distribution),
        label_imbalance_ratio=_imbalance_ratio(label_distribution),
        attack_category_distribution=attack_category_distribution,
        attack_category_percentages=_percentages(attack_category_distribution),
        attack_category_imbalance_ratio=_imbalance_ratio(attack_category_distribution),
        missing_value_count=int(frame.isna().sum().sum()),
    )
