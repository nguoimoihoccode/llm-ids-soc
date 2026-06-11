from pathlib import Path
from typing import Optional

import pandas as pd

from app.models import DatasetValidationResult


REQUIRED_IDS_COLUMNS = ["attack_cat", "label"]


def validate_ids_dataset_csv(
    csv_path: Path,
    min_rows: int = 2,
    required_columns: Optional[list[str]] = None,
) -> DatasetValidationResult:
    columns_to_check = sorted(required_columns or REQUIRED_IDS_COLUMNS)
    frame = pd.read_csv(csv_path)
    missing_columns = [column for column in columns_to_check if column not in frame.columns]
    errors: list[str] = []
    if missing_columns:
        errors.append(f"Dataset is missing required columns: {', '.join(missing_columns)}.")
    if len(frame) < min_rows:
        errors.append(f"Dataset does not meet minimum row count: {len(frame)} < {min_rows}.")

    return DatasetValidationResult(
        valid=not errors,
        row_count=len(frame),
        column_count=len(frame.columns),
        required_columns=columns_to_check,
        missing_required_columns=missing_columns,
        errors=errors,
    )
