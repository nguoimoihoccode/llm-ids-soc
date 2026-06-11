from pathlib import Path

from app.services.dataset_validation import validate_ids_dataset_csv


def test_validate_ids_dataset_csv_accepts_required_columns(tmp_path: Path) -> None:
    raw_path = tmp_path / "valid.csv"
    raw_path.write_text(
        "proto,service,state,dur,label,attack_cat\n"
        "tcp,http,FIN,0.1,0,Normal\n"
        "udp,dns,CON,0.2,1,DoS\n",
        encoding="utf-8",
    )

    result = validate_ids_dataset_csv(raw_path, min_rows=2)

    assert result.valid is True
    assert result.row_count == 2
    assert result.missing_required_columns == []
    assert result.errors == []


def test_validate_ids_dataset_csv_reports_missing_required_columns(tmp_path: Path) -> None:
    raw_path = tmp_path / "invalid.csv"
    raw_path.write_text(
        "proto,service,state,dur\n"
        "tcp,http,FIN,0.1\n",
        encoding="utf-8",
    )

    result = validate_ids_dataset_csv(raw_path, min_rows=2)

    assert result.valid is False
    assert result.missing_required_columns == ["attack_cat", "label"]
    assert "missing required columns" in result.errors[0]
    assert "minimum row count" in result.errors[1]
