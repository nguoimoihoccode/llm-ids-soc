import json
import subprocess
import sys
from pathlib import Path


def test_preprocess_unsw_script_writes_output(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    raw_path = project_root / "data" / "samples" / "unsw_nb15_fixture.csv"
    processed_path = tmp_path / "processed.csv"

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "preprocess_unsw_nb15.py"),
            "--input",
            str(raw_path),
            "--output",
            str(processed_path),
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads(result.stdout)
    assert summary["row_count"] == 3
    assert summary["label_column"] == "label"
    assert processed_path.exists()
