from pathlib import Path

import pandas as pd

from app.services.dataset_split import split_dataset_csv


def test_split_dataset_csv_writes_train_test_files_and_summary(tmp_path: Path) -> None:
    # Kiem tra split stratified giu duoc ty le label trong train/test.
    raw_path = tmp_path / "raw.csv"
    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    raw_path.write_text(
        "feature,label,attack_cat\n"
        "1,0,Normal\n"
        "2,0,Normal\n"
        "3,0,Normal\n"
        "4,1,DoS\n"
        "5,1,DoS\n"
        "6,1,Reconnaissance\n",
        encoding="utf-8",
    )

    summary = split_dataset_csv(
        raw_path=raw_path,
        train_path=train_path,
        test_path=test_path,
        test_size=0.33,
        random_state=7,
    )

    train_frame = pd.read_csv(train_path)
    test_frame = pd.read_csv(test_path)

    assert summary.total_rows == 6
    assert summary.train_rows == 4
    assert summary.test_rows == 2
    assert summary.label_column == "label"
    assert summary.train_label_distribution == {"0": 2, "1": 2}
    assert summary.test_label_distribution == {"0": 1, "1": 1}
    assert len(train_frame) == 4
    assert len(test_frame) == 2


def test_split_dataset_csv_falls_back_when_stratified_split_is_not_possible(tmp_path: Path) -> None:
    # Dataset qua nho co the khong stratify duoc, test dam bao fallback van tao file.
    raw_path = tmp_path / "small.csv"
    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    raw_path.write_text(
        "feature,label,attack_cat\n"
        "1,0,Normal\n"
        "2,1,DoS\n"
        "3,1,Reconnaissance\n",
        encoding="utf-8",
    )

    summary = split_dataset_csv(
        raw_path=raw_path,
        train_path=train_path,
        test_path=test_path,
        test_size=0.33,
        random_state=42,
    )

    assert summary.total_rows == 3
    assert summary.train_rows == 2
    assert summary.test_rows == 1
    assert summary.stratified is False
    assert "fallback" in summary.split_strategy
