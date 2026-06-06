import subprocess
import sys
from pathlib import Path

from app.services.llm_rubric_summary import build_rag_summary_markdown


def test_build_rag_summary_markdown_aggregates_scores(tmp_path: Path) -> None:
    scores_path = tmp_path / "llm-rubric-scores.csv"
    scores_path.write_text(
        "alert_id,mode,correctness,completeness,groundedness,actionability,hallucination_safety,latency\n"
        "a1,template,3,2,2,2,5,5\n"
        "a1,llm_without_rag,5,4,3,2,5,5\n"
        "a1,llm_with_rag,5,5,5,5,5,5\n",
        encoding="utf-8",
    )

    markdown = build_rag_summary_markdown(scores_path)

    assert "# RAG vs No-RAG Summary" in markdown
    assert "| llm_with_rag | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |" in markdown
    assert "RAG-backed explanations achieved the highest groundedness score." in markdown


def test_export_rag_summary_script_writes_markdown(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    output_path = tmp_path / "rag-vs-no-rag-summary.md"

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "export_rag_summary.py"),
            "--scores",
            str(project_root / "reports" / "evaluation" / "llm-rubric-scores.csv"),
            "--output",
            str(output_path),
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    assert "summary_written" in result.stdout
    assert output_path.exists()
    assert "llm_with_rag" in output_path.read_text(encoding="utf-8")
