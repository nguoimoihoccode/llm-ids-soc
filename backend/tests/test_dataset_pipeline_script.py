import json
import subprocess
import sys
from pathlib import Path


def test_dataset_pipeline_script_runs_profile_split_preprocess_and_train(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = tmp_path / "raw.csv"
    output_dir = tmp_path / "pipeline"
    input_path.write_text(
        "proto,service,state,dur,sbytes,rate,label,attack_cat\n"
        "tcp,http,FIN,0.1,100,50.5,0,Normal\n"
        "tcp,http,FIN,0.2,120,45.5,0,Normal\n"
        "udp,dns,CON,0.3,250,10.5,1,DoS\n"
        "udp,dns,CON,0.4,260,11.5,1,DoS\n"
        "tcp,ftp,FIN,0.5,500,20.0,1,Reconnaissance\n"
        "tcp,ftp,FIN,0.6,520,22.0,1,Reconnaissance\n",
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "run_dataset_pipeline.py"),
            "--dataset-id",
            "pipeline-fixture",
            "--input",
            str(input_path),
            "--output-dir",
            str(output_dir),
            "--models",
            "decision_tree",
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

    summary = json.loads((output_dir / "pipeline-summary.json").read_text(encoding="utf-8"))
    assert summary["dataset_id"] == "pipeline-fixture"
    assert summary["profile_path"].endswith("dataset-profile.json")
    assert summary["split_summary_path"].endswith("dataset-split-summary.json")
    assert (output_dir / "processed" / "train.csv").exists()
    assert (output_dir / "processed" / "test.csv").exists()
    assert (output_dir / "metrics" / "pipeline-fixture-decision_tree.json").exists()
    assert (output_dir / "models" / "pipeline-fixture-decision_tree.joblib").exists()
    comparison = (output_dir / "reports" / "model-comparison.csv").read_text(encoding="utf-8")
    assert "dataset_id,model_name,accuracy,precision,recall,f1_score,false_positive_rate" in comparison
    assert "pipeline-fixture,decision_tree" in comparison
    assert (output_dir / "figures" / "pipeline-fixture-decision_tree-confusion-matrix.svg").exists()
    assert (output_dir / "reports" / "feature-importance" / "pipeline-fixture-decision_tree-feature-importance.csv").exists()
    report = (output_dir / "pipeline-report.md").read_text(encoding="utf-8")
    assert "# Dataset Pipeline Report" in report
    assert "pipeline-fixture" in report
    assert "| Model | Accuracy | Precision | Recall | F1-score | FPR | Sample Count |" in report
    assert "## Generated Artifacts" in report
    assert "dataset-profile.json" in report
    assert "model-comparison.csv" in report
    assert "confusion-matrix.svg" in report
    assert "feature-importance.csv" in report


def test_dataset_pipeline_script_accepts_explicit_train_test_inputs(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    output_dir = tmp_path / "pipeline"
    train_path.write_text(
        "proto,service,state,dur,sbytes,rate,label,attack_cat\n"
        "tcp,http,FIN,0.1,100,50.5,0,Normal\n"
        "tcp,http,FIN,0.2,120,45.5,0,Normal\n"
        "udp,dns,CON,0.3,250,10.5,1,DoS\n"
        "udp,dns,CON,0.4,260,11.5,1,DoS\n",
        encoding="utf-8",
    )
    test_path.write_text(
        "proto,service,state,dur,sbytes,rate,label,attack_cat\n"
        "tcp,http,FIN,0.5,150,40.5,0,Normal\n"
        "udp,dns,CON,0.6,280,12.5,1,DoS\n",
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "run_dataset_pipeline.py"),
            "--dataset-id",
            "pipeline-explicit",
            "--train-input",
            str(train_path),
            "--test-input",
            str(test_path),
            "--output-dir",
            str(output_dir),
            "--models",
            "decision_tree",
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads((output_dir / "pipeline-summary.json").read_text(encoding="utf-8"))
    assert summary["split_mode"] == "explicit"
    assert summary["split_summary_path"].endswith("dataset-split-summary.json")
    split_summary = json.loads((output_dir / "reports" / "dataset-split-summary.json").read_text(encoding="utf-8"))
    assert split_summary["train_rows"] == 4
    assert split_summary["test_rows"] == 2
    assert split_summary["split_strategy"] == "explicit_train_test"
    assert split_summary["stratified"] is False
    assert (output_dir / "processed" / "train.csv").exists()
    assert (output_dir / "processed" / "test.csv").exists()
    assert (output_dir / "metrics" / "pipeline-explicit-decision_tree.json").exists()
