import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.confusion_matrix_export import export_confusion_matrix_svgs  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Export confusion matrix SVG figures from saved metric artifacts.")
    parser.add_argument("--metrics-dir", required=True, type=Path)
    parser.add_argument("--figures-dir", required=True, type=Path)
    args = parser.parse_args()

    outputs = export_confusion_matrix_svgs(args.metrics_dir, args.figures_dir)
    print(json.dumps({"figures_exported": len(outputs), "outputs": [str(path) for path in outputs]}, indent=2))


if __name__ == "__main__":
    main()
