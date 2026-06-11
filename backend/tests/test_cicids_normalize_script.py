import json
import subprocess
import sys
from pathlib import Path


def test_normalize_cicids_script_writes_normalized_csv(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    raw_path = tmp_path / "cicids.csv"
    output_path = tmp_path / "normalized.csv"
    raw_path.write_text(
        " Flow Duration, Total Fwd Packets, Label\n"
        "10,2,BENIGN\n"
        "20,5,DDoS\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "normalize_cicids.py"),
            "--input",
            str(raw_path),
            "--output",
            str(output_path),
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["row_count"] == 2
    assert payload["label_column"] == "label"
    assert output_path.read_text(encoding="utf-8").splitlines()[0].endswith("attack_cat,label")


def test_normalize_cicids_script_accepts_multiple_inputs(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    first_path = tmp_path / "day1.csv"
    second_path = tmp_path / "day2.csv"
    output_path = tmp_path / "merged.csv"
    first_path.write_text(" Flow Duration, Label\n10,BENIGN\n", encoding="utf-8")
    second_path.write_text(" Flow Duration, Label\n20,DDoS\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "normalize_cicids.py"),
            "--input",
            str(first_path),
            "--input",
            str(second_path),
            "--output",
            str(output_path),
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["row_count"] == 2
    assert output_path.read_text(encoding="utf-8").count("\n") == 3
