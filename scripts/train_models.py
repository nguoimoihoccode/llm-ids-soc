import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.model_training import train_models_from_csv  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Train IDS baseline models from processed CSV data.")
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--metrics-dir", required=True, type=Path)
    parser.add_argument("--models-dir", required=True, type=Path)
    parser.add_argument("--models", default="logistic_regression,decision_tree,random_forest")
    args = parser.parse_args()

    model_names = [name.strip() for name in args.models.split(",") if name.strip()]
    results = train_models_from_csv(args.dataset_id, args.input, args.metrics_dir, args.models_dir, model_names)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
