import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.dataset_validation import validate_ids_dataset_csv  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an IDS-style CSV dataset before running the pipeline.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--min-rows", default=2, type=int)
    parser.add_argument("--required-columns", default="attack_cat,label")
    args = parser.parse_args()

    required_columns = [column.strip() for column in args.required_columns.split(",") if column.strip()]
    result = validate_ids_dataset_csv(args.input, min_rows=args.min_rows, required_columns=required_columns)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result.model_dump(), indent=2), encoding="utf-8")
    print(json.dumps(result.model_dump(), indent=2))
    if not result.valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
