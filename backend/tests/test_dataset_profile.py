from pathlib import Path

from app.services.dataset_profile import profile_dataset_csv


def test_profile_dataset_csv_summarizes_rows_columns_and_labels(tmp_path: Path) -> None:
    # Kiem tra profile dem dung so dong, cot, label va missing value.
    raw_path = tmp_path / "raw.csv"
    raw_path.write_text(
        "proto,service,dur,label,attack_cat\n"
        "tcp,http,0.1,0,Normal\n"
        "udp,dns,,1,DoS\n"
        "tcp,ftp,0.3,1,Reconnaissance\n",
        encoding="utf-8",
    )

    summary = profile_dataset_csv(raw_path)

    assert summary.row_count == 3
    assert summary.column_count == 5
    assert summary.label_distribution == {"0": 1, "1": 2}
    assert summary.attack_category_distribution == {
        "DoS": 1,
        "Normal": 1,
        "Reconnaissance": 1,
    }
    assert summary.missing_value_count == 1
    assert summary.columns == ["proto", "service", "dur", "label", "attack_cat"]


def test_profile_dataset_csv_reports_class_imbalance(tmp_path: Path) -> None:
    # Kiem tra tinh phan tram va ty le lech lop cho dataset mat can bang.
    raw_path = tmp_path / "imbalanced.csv"
    raw_path.write_text(
        "proto,dur,label,attack_cat\n"
        "tcp,0.1,0,Normal\n"
        "udp,0.2,1,DoS\n"
        "tcp,0.3,1,DoS\n"
        "tcp,0.4,1,Reconnaissance\n",
        encoding="utf-8",
    )

    summary = profile_dataset_csv(raw_path)

    assert summary.label_percentages == {"0": 25.0, "1": 75.0}
    assert summary.attack_category_percentages == {
        "DoS": 50.0,
        "Normal": 25.0,
        "Reconnaissance": 25.0,
    }
    assert summary.label_imbalance_ratio == 3.0
    assert summary.attack_category_imbalance_ratio == 2.0
