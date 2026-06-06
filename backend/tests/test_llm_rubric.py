import subprocess
import sys
from pathlib import Path

from app.services.llm_rubric import evaluate_comparison_with_rubric, export_rubric_scores_csv


def test_evaluate_comparison_with_rubric_scores_rag_highest() -> None:
    comparison = {
        "alert_id": "alert-evt-002",
        "comparisons": [
            {"mode": "template", "uses_rag": False, "summary": "Brute Force alert with High severity.", "knowledge_context": ""},
            {"mode": "llm_without_rag", "uses_rag": False, "summary": "Brute Force with evidence features and MITRE T1110.", "knowledge_context": ""},
            {"mode": "llm_with_rag", "uses_rag": True, "summary": "Brute Force with evidence features, MITRE T1110, and response guidance.", "knowledge_context": "Brute Force Playbook"},
        ],
    }

    rows = evaluate_comparison_with_rubric(comparison)

    assert [row["mode"] for row in rows] == ["template", "llm_without_rag", "llm_with_rag"]
    assert rows[0]["groundedness"] < rows[2]["groundedness"]
    assert rows[2]["correctness"] == 5
    assert rows[2]["actionability"] == 5


def test_export_rubric_scores_csv_writes_rows(tmp_path: Path) -> None:
    output_path = tmp_path / "llm-rubric-scores.csv"
    rows = [
        {"alert_id": "a1", "mode": "template", "correctness": 3, "completeness": 2, "groundedness": 2, "actionability": 2, "hallucination_safety": 5, "latency": 5},
    ]

    export_rubric_scores_csv(rows, output_path)

    assert output_path.read_text(encoding="utf-8").splitlines() == [
        "alert_id,mode,correctness,completeness,groundedness,actionability,hallucination_safety,latency",
        "a1,template,3,2,2,2,5,5",
    ]


def test_evaluate_llm_script_writes_rubric_scores(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    output_path = tmp_path / "llm-rubric-scores.csv"

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "evaluate_llm.py"),
            "--output",
            str(output_path),
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    assert "rows_exported" in result.stdout
    assert output_path.exists()
    assert "llm_with_rag" in output_path.read_text(encoding="utf-8")
