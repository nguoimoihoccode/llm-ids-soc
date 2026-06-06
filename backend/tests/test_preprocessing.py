import math
from pathlib import Path

from app.services.preprocessing import preprocess_unsw_nb15_csv


def test_preprocess_unsw_nb15_cleans_values_and_encodes_labels(tmp_path: Path) -> None:
    raw_path = tmp_path / "raw.csv"
    processed_path = tmp_path / "processed.csv"
    raw_path.write_text(
        "proto,service,state,dur,sbytes,rate,label,attack_cat\n"
        "tcp,http,FIN,0.1,100,inf,0,Normal\n"
        "udp,dns,CON,NaN,250,10.5,1,DoS\n",
        encoding="utf-8",
    )

    summary = preprocess_unsw_nb15_csv(raw_path, processed_path)

    assert summary.row_count == 2
    assert summary.feature_count == 12
    assert summary.label_column == "label"
    assert summary.attack_categories == ["DoS", "Normal"]
    output = processed_path.read_text(encoding="utf-8")
    assert "inf" not in output.lower()
    assert "nan" not in output.lower()
    assert "proto_tcp" in output
    assert "attack_cat_DoS" in output


def test_preprocess_unsw_nb15_replaces_non_finite_numbers(tmp_path: Path) -> None:
    raw_path = tmp_path / "raw.csv"
    processed_path = tmp_path / "processed.csv"
    raw_path.write_text(
        "proto,dur,sbytes,label,attack_cat\n"
        "tcp,Infinity,100,1,Reconnaissance\n"
        "tcp,-Infinity,200,0,Normal\n",
        encoding="utf-8",
    )

    preprocess_unsw_nb15_csv(raw_path, processed_path)

    for line in processed_path.read_text(encoding="utf-8").splitlines()[1:]:
        values = [float(value) for value in line.split(",") if value]
        assert all(math.isfinite(value) for value in values)
