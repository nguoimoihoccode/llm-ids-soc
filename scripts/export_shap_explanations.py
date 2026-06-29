import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.shap_export import export_shap_summary_plots, export_shap_instance_values  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export SHAP global summary plots and per-instance explanations."
    )
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--processed-path", required=True, type=Path)
    parser.add_argument("--models-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--background-size", type=int, default=100)
    parser.add_argument("--eval-sample-size", type=int, default=500)
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()

    plot_paths = export_shap_summary_plots(
        dataset_id=args.dataset_id,
        processed_path=args.processed_path,
        models_dir=args.models_dir,
        output_dir=args.output_dir / "plots",
        background_size=args.background_size,
        eval_sample_size=args.eval_sample_size,
    )

    instance_paths = export_shap_instance_values(
        dataset_id=args.dataset_id,
        processed_path=args.processed_path,
        models_dir=args.models_dir,
        output_dir=args.output_dir / "instances",
        background_size=args.background_size,
        eval_sample_size=args.eval_sample_size,
        top_k=args.top_k,
    )

    print(json.dumps({
        "summary_plots": [str(p) for p in plot_paths],
        "instance_exports": [str(p) for p in instance_paths],
    }, indent=2))


if __name__ == "__main__":
    main()
