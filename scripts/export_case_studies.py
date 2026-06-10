import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.case_studies import build_incident_case_studies_markdown  # noqa: E402
from app.services.data_loader import load_sample_events  # noqa: E402
from app.services.detector import generate_alerts  # noqa: E402


def main() -> None:
    # Tao case study markdown tu alert mau de dung cho phan evaluation/thesis.
    parser = argparse.ArgumentParser(description="Export incident case studies markdown report.")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    alerts = generate_alerts(load_sample_events())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_incident_case_studies_markdown(alerts), encoding="utf-8")
    print(json.dumps({"cases_exported": len(alerts), "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
