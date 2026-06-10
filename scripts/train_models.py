import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Reuse ham train trong backend de ket qua train va export artifact dong nhat.
from app.services.model_training import train_models_from_csv, train_models_from_split_csv  # noqa: E402


def main() -> None:
    # Script nay train baseline model tu file CSV da xu ly va luu metric + model.
    parser = argparse.ArgumentParser(description="Train IDS baseline models from processed CSV data.")
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--train-input", type=Path)
    parser.add_argument("--test-input", type=Path)
    parser.add_argument("--metrics-dir", required=True, type=Path)
    parser.add_argument("--models-dir", required=True, type=Path)
    parser.add_argument("--models", default="logistic_regression,decision_tree,random_forest")
    args = parser.parse_args()

    model_names = [name.strip() for name in args.models.split(",") if name.strip()]
    if args.train_input and args.test_input:
        # Neu co train/test rieng, metric se duoc tinh tren test-input.
        results = train_models_from_split_csv(
            args.dataset_id,
            args.train_input,
            args.test_input,
            args.metrics_dir,
            args.models_dir,
            model_names,
        )
    elif args.input:
        # Che do cu: train va evaluate tren cung mot file, phu hop demo nhanh.
        results = train_models_from_csv(args.dataset_id, args.input, args.metrics_dir, args.models_dir, model_names)
    else:
        parser.error("Provide either --input or both --train-input and --test-input.")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
