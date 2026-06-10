from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from app.models import DatasetSplitSummary


def _label_counts(frame: pd.DataFrame, label_column: str) -> dict[str, int]:
    # Dem phan bo label trong tung tap train/test.
    counts = frame[label_column].astype(str).value_counts().sort_index()
    return {label: int(count) for label, count in counts.items()}


def split_dataset_csv(
    raw_path: Path,
    train_path: Path,
    test_path: Path,
    test_size: float = 0.2,
    random_state: int = 42,
    label_column: str = "label",
) -> DatasetSplitSummary:
    # Tach dataset thanh train/test; uu tien stratified de giu ty le label.
    frame = pd.read_csv(raw_path)
    stratify = frame[label_column] if label_column in frame.columns else None
    stratified = stratify is not None
    split_strategy = "stratified"
    try:
        train_frame, test_frame = train_test_split(
            frame,
            test_size=test_size,
            random_state=random_state,
            stratify=stratify,
        )
    except ValueError:
        # Dataset qua nho/le lop qua nang co the khong stratify duoc -> fallback.
        stratified = False
        split_strategy = "fallback_non_stratified"
        train_frame, test_frame = train_test_split(
            frame,
            test_size=test_size,
            random_state=random_state,
            stratify=None,
        )

    train_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.parent.mkdir(parents=True, exist_ok=True)
    # Luu 2 file dau ra de buoc train co the dung tap train va danh gia tren test.
    train_frame.to_csv(train_path, index=False)
    test_frame.to_csv(test_path, index=False)

    return DatasetSplitSummary(
        total_rows=len(frame),
        train_rows=len(train_frame),
        test_rows=len(test_frame),
        label_column=label_column,
        test_size=test_size,
        random_state=random_state,
        stratified=stratified,
        split_strategy=split_strategy,
        train_label_distribution=_label_counts(train_frame, label_column),
        test_label_distribution=_label_counts(test_frame, label_column),
    )
