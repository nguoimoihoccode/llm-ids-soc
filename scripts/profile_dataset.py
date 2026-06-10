import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Goi service profiling de xuat JSON mo ta dataset truoc khi xu ly.
from app.services.dataset_profile import profile_dataset_csv  # noqa: E402


def main() -> None:
    # CLI nhan file CSV dau vao va ghi summary JSON ra output.
    parser = argparse.ArgumentParser(description="Profile an IDS-style CSV dataset.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    summary = profile_dataset_csv(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary.model_dump(), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
