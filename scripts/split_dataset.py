import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Goi service split de tach raw/processed CSV thanh train va test co summary.
from app.services.dataset_split import split_dataset_csv  # noqa: E402


def main() -> None:
    # CLI tach dataset va ghi them summary JSON de kiem tra ty le split/label.
    parser = argparse.ArgumentParser(description="Split an IDS-style CSV dataset into train/test files.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--train-output", required=True, type=Path)
    parser.add_argument("--test-output", required=True, type=Path)
    parser.add_argument("--summary-output", required=True, type=Path)
    parser.add_argument("--test-size", default=0.2, type=float)
    parser.add_argument("--random-state", default=42, type=int)
    parser.add_argument("--label-column", default="label")
    args = parser.parse_args()

    summary = split_dataset_csv(
        raw_path=args.input,
        train_path=args.train_output,
        test_path=args.test_output,
        test_size=args.test_size,
        random_state=args.random_state,
        label_column=args.label_column,
    )
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary.model_dump(), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
