import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Goi service backend de gom cac metric JSON thanh bang so sanh model.
from app.services.report_export import export_model_comparison_csv  # noqa: E402


def main() -> None:
    # CLI nhan thu muc metrics va duong dan CSV dau ra.
    parser = argparse.ArgumentParser(description="Export model comparison CSV from saved metric artifacts.")
    parser.add_argument("--metrics-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    row_count = export_model_comparison_csv(args.metrics_dir, args.output)
    print(json.dumps({"rows_exported": row_count, "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
