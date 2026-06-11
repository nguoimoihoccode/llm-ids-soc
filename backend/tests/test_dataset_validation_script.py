import json
import subprocess
import sys
from pathlib import Path


def test_validate_dataset_script_writes_validation_json(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    raw_path = tmp_path / "valid.csv"
    output_path = tmp_path / "validation.json"
    raw_path.write_text(
        "proto,service,state,dur,label,attack_cat\n"
        "tcp,http,FIN,0.1,0,Normal\n"
        "udp,dns,CON,0.2,1,DoS\n",
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "validate_dataset.py"),
            "--input",
            str(raw_path),
            "--output",
            str(output_path),
            "--min-rows",
            "2",
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["valid"] is True
    assert payload["missing_required_columns"] == []


def test_validate_dataset_script_exits_nonzero_for_invalid_dataset(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    raw_path = tmp_path / "invalid.csv"
    output_path = tmp_path / "validation.json"
    raw_path.write_text("proto,dur\ntcp,0.1\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "validate_dataset.py"),
            "--input",
            str(raw_path),
            "--output",
            str(output_path),
            "--min-rows",
            "2",
        ],
        cwd=project_root / "backend",
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["valid"] is False
