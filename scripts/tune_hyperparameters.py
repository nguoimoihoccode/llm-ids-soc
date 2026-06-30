import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.hyperparameter_tuning import tune_and_save  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Tune hyperparameters for IDS baseline models.")
    parser.add_argument("--processed-train-path", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--models", default="xgboost,random_forest,decision_tree,logistic_regression_scaled")
    parser.add_argument("--n-iter", type=int, default=40)
    parser.add_argument("--cv", type=int, default=3)
    args = parser.parse_args()

    model_names = [name.strip() for name in args.models.split(",") if name.strip()]
    results = {}
    for model_name in model_names:
        result = tune_and_save(
            model_name=model_name,
            processed_train_path=args.processed_train_path,
            output_dir=args.output_dir,
            n_iter=args.n_iter,
            cv=args.cv,
        )
        results[model_name] = result
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
