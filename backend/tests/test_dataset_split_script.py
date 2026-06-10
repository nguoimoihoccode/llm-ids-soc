import json
import subprocess
import sys
from pathlib import Path

import pandas as pd


def test_split_dataset_script_writes_train_test_and_summary(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    raw_path = tmp_path / "raw.csv"
    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    summary_path = tmp_path / "split-summary.json"
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

    subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "split_dataset.py"),
            "--input",
            str(raw_path),
            "--train-output",
            str(train_path),
            "--test-output",
            str(test_path),
            "--summary-output",
            str(summary_path),
            "--test-size",
            "0.33",
            "--random-state",
            "7",
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["train_rows"] == 4
    assert summary["test_rows"] == 2
    assert summary["stratified"] is True
    assert summary["split_strategy"] == "stratified"
    assert summary["train_label_distribution"] == {"0": 2, "1": 2}
    assert summary["test_label_distribution"] == {"0": 1, "1": 1}
    assert len(pd.read_csv(train_path)) == 4
    assert len(pd.read_csv(test_path)) == 2
