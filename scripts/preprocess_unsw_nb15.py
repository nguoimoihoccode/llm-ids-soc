import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.preprocessing import preprocess_unsw_nb15_csv  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess UNSW-NB15 CSV data.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    summary = preprocess_unsw_nb15_csv(args.input, args.output)
    print(json.dumps(summary.model_dump(), indent=2))


if __name__ == "__main__":
    main()
