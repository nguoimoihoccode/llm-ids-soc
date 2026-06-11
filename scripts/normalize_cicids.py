import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.cicids_preprocessing import normalize_cicids_csv_files  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize CICIDS2017/CSE-CIC-IDS CSV files to the project IDS schema.")
    parser.add_argument("--input", required=True, action="append", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    summary = normalize_cicids_csv_files(args.input, args.output)
    print(json.dumps(summary.model_dump(), indent=2))


if __name__ == "__main__":
    main()
