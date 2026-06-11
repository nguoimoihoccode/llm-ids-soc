from pathlib import Path

import pandas as pd

from app.services.cicids_preprocessing import normalize_cicids_csv
from app.services.cicids_preprocessing import normalize_cicids_csv_files


def test_normalize_cicids_csv_maps_label_to_binary_and_attack_category(tmp_path: Path) -> None:
    raw_path = tmp_path / "cicids.csv"
    output_path = tmp_path / "normalized.csv"
    raw_path.write_text(
        " Flow Duration, Total Fwd Packets,Flow Bytes/s, Label\n"
        "10,2,100.0,BENIGN\n"
        "20,5,200.0,DDoS\n"
        "30,7,Infinity,PortScan\n",
        encoding="utf-8",
    )

    summary = normalize_cicids_csv(raw_path, output_path)

    frame = pd.read_csv(output_path)
    assert summary.row_count == 3
    assert summary.attack_categories == ["BENIGN", "DDoS", "PortScan"]
    assert frame["label"].tolist() == [0, 1, 1]
    assert frame["attack_cat"].tolist() == ["BENIGN", "DDoS", "PortScan"]
    assert "Label" not in frame.columns
    assert "Flow Duration" in frame.columns
    assert frame["Flow Bytes/s"].tolist() == [100.0, 200.0, 0.0]


def test_normalize_cicids_csv_files_merges_multiple_days(tmp_path: Path) -> None:
    first_path = tmp_path / "day1.csv"
    second_path = tmp_path / "day2.csv"
    output_path = tmp_path / "merged.csv"
    first_path.write_text(
        " Flow Duration, Total Fwd Packets, Label\n"
        "10,2,BENIGN\n"
        "20,5,DDoS\n",
        encoding="utf-8",
    )
    second_path.write_text(
        " Flow Duration, Total Backward Packets, Label\n"
        "30,7,BENIGN\n"
        "40,9,PortScan\n",
        encoding="utf-8",
    )

    summary = normalize_cicids_csv_files([first_path, second_path], output_path)

    frame = pd.read_csv(output_path)
    assert summary.row_count == 4
    assert summary.attack_categories == ["BENIGN", "DDoS", "PortScan"]
    assert frame["label"].tolist() == [0, 1, 0, 1]
    assert "Total Fwd Packets" in frame.columns
    assert "Total Backward Packets" in frame.columns
    assert frame["Total Fwd Packets"].tolist() == [2.0, 5.0, 0.0, 0.0]
    assert frame["Total Backward Packets"].tolist() == [0.0, 0.0, 7.0, 9.0]
