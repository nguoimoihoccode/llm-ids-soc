from pathlib import Path

import pandas as pd

from app.services.cicids_preprocessing import normalize_cicids_csv


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
