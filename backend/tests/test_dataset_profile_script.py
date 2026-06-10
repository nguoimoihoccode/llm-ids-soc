import json
import subprocess
import sys
from pathlib import Path


def test_profile_dataset_script_writes_summary_json(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    raw_path = project_root / "data" / "samples" / "unsw_nb15_fixture.csv"
    output_path = tmp_path / "dataset-summary.json"

    subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "profile_dataset.py"),
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

    summary = json.loads(output_path.read_text(encoding="utf-8"))
    assert summary["row_count"] == 3
    assert summary["column_count"] == 11
    assert summary["label_distribution"] == {"0": 1, "1": 2}
    assert summary["label_percentages"] == {"0": 33.33, "1": 66.67}
    assert summary["label_imbalance_ratio"] == 2.0
    assert summary["attack_category_distribution"] == {
        "DoS": 1,
        "Normal": 1,
        "Reconnaissance": 1,
    }
    assert summary["attack_category_imbalance_ratio"] == 1.0
