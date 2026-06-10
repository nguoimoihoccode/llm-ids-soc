import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.data_loader import load_sample_events  # noqa: E402
from app.services.detector import generate_alerts  # noqa: E402
from app.services.llm_rubric import evaluate_comparison_with_rubric, export_rubric_scores_csv  # noqa: E402
from app.services.llm_service import compare_explanation_modes  # noqa: E402


def main() -> None:
    # Tao alert mau, so sanh cac mode giai thich, roi cham diem bang rubric co dinh.
    parser = argparse.ArgumentParser(description="Evaluate LLM explanation modes with a deterministic rubric.")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    rows: list[dict[str, object]] = []
    for alert in generate_alerts(load_sample_events()):
        # model_dump bien Pydantic model thanh dict de rubric doc duoc don gian.
        comparison = compare_explanation_modes(alert).model_dump()
        rows.extend(evaluate_comparison_with_rubric(comparison))
    export_rubric_scores_csv(rows, args.output)
    print(json.dumps({"rows_exported": len(rows), "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
