import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Goi service lay feature importance tu model artifact da train.
from app.services.feature_importance_export import export_feature_importance_csvs  # noqa: E402


def main() -> None:
    # CLI can dataset id de tim dung cac file model trong models-dir.
    parser = argparse.ArgumentParser(description="Export tree-model feature importance CSV files.")
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--models-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    outputs = export_feature_importance_csvs(args.dataset_id, args.input, args.models_dir, args.output_dir)
    print(json.dumps({"files_exported": len(outputs), "outputs": [str(path) for path in outputs]}, indent=2))


if __name__ == "__main__":
    main()
