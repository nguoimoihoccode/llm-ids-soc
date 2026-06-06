import subprocess
import sys
from pathlib import Path

from app.services.case_studies import build_incident_case_studies_markdown
from app.services.data_loader import load_sample_events
from app.services.detector import generate_alerts


def test_build_incident_case_studies_markdown_contains_alert_context() -> None:
    alerts = generate_alerts(load_sample_events())

    markdown = build_incident_case_studies_markdown(alerts[:1])

    assert "# Incident Case Studies" in markdown
    assert "## Case 1: Brute Force" in markdown
    assert "MITRE: T1110 - Brute Force" in markdown
    assert "Evidence features: failed_login_count, dst_port, flow_packets_s" in markdown
    assert "### Explanation Comparison" in markdown
    assert "llm_with_rag" in markdown


def test_export_case_studies_script_writes_markdown(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    output_path = tmp_path / "incident-case-studies.md"

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "export_case_studies.py"),
            "--output",
            str(output_path),
        ],
        cwd=project_root / "backend",
        check=True,
        capture_output=True,
        text=True,
    )

    assert "cases_exported" in result.stdout
    assert output_path.exists()
    assert "Incident Case Studies" in output_path.read_text(encoding="utf-8")
