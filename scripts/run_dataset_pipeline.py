import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.dataset_profile import profile_dataset_csv  # noqa: E402
from app.services.dataset_split import split_dataset_csv  # noqa: E402
from app.models import DatasetSplitSummary  # noqa: E402
from app.services.confusion_matrix_export import export_confusion_matrix_svgs  # noqa: E402
from app.services.feature_importance_export import export_feature_importance_csvs  # noqa: E402
from app.services.model_training import train_models_from_split_csv  # noqa: E402
from app.services.preprocessing import preprocess_unsw_nb15_csv  # noqa: E402
from app.services.report_export import export_model_comparison_csv  # noqa: E402
from app.services.shap_export import export_shap_summary_plots, export_shap_instance_values  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run profile, split, preprocess, and train workflow for IDS CSV data.")
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--train-input", type=Path)
    parser.add_argument("--test-input", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--models", default="logistic_regression,decision_tree,random_forest")
    parser.add_argument("--test-size", default=0.2, type=float)
    parser.add_argument("--random-state", default=42, type=int)
    args = parser.parse_args()

    output_dir = args.output_dir
    figures_dir = output_dir / "figures"
    raw_dir = output_dir / "raw"
    processed_dir = output_dir / "processed"
    metrics_dir = output_dir / "metrics"
    models_dir = output_dir / "models"
    reports_dir = output_dir / "reports"
    for directory in [figures_dir, raw_dir, processed_dir, metrics_dir, models_dir, reports_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    shap_plots_dir = output_dir / "shap" / "plots"
    shap_instances_dir = output_dir / "shap" / "instances"
    shap_plots_dir.mkdir(parents=True, exist_ok=True)
    shap_instances_dir.mkdir(parents=True, exist_ok=True)

    profile_path = reports_dir / "dataset-profile.json"
    split_summary_path = reports_dir / "dataset-split-summary.json"
    raw_train_path = raw_dir / "train.csv"
    raw_test_path = raw_dir / "test.csv"
    processed_train_path = processed_dir / "train.csv"
    processed_test_path = processed_dir / "test.csv"

    if args.train_input and args.test_input:
        split_mode = "explicit"
        profile = profile_dataset_csv(args.train_input)
        train_profile = profile_dataset_csv(args.train_input)
        test_profile = profile_dataset_csv(args.test_input)
        split_summary = DatasetSplitSummary(
            total_rows=train_profile.row_count + test_profile.row_count,
            train_rows=train_profile.row_count,
            test_rows=test_profile.row_count,
            label_column="label",
            test_size=test_profile.row_count / (train_profile.row_count + test_profile.row_count),
            random_state=args.random_state,
            stratified=False,
            split_strategy="explicit_train_test",
            train_label_distribution=train_profile.label_distribution,
            test_label_distribution=test_profile.label_distribution,
        )
        raw_train_path.write_text(args.train_input.read_text(encoding="utf-8"), encoding="utf-8")
        raw_test_path.write_text(args.test_input.read_text(encoding="utf-8"), encoding="utf-8")
    elif args.input:
        split_mode = "generated"
        profile = profile_dataset_csv(args.input)
        split_summary = split_dataset_csv(
            raw_path=args.input,
            train_path=raw_train_path,
            test_path=raw_test_path,
            test_size=args.test_size,
            random_state=args.random_state,
        )
    else:
        parser.error("Provide either --input or both --train-input and --test-input.")

    profile_path.write_text(json.dumps(profile.model_dump(), indent=2), encoding="utf-8")
    split_summary_path.write_text(json.dumps(split_summary.model_dump(), indent=2), encoding="utf-8")

    preprocess_unsw_nb15_csv(raw_train_path, processed_train_path)
    preprocess_unsw_nb15_csv(raw_test_path, processed_test_path)

    model_names = [name.strip() for name in args.models.split(",") if name.strip()]
    metrics = train_models_from_split_csv(
        dataset_id=args.dataset_id,
        train_path=processed_train_path,
        test_path=processed_test_path,
        metrics_dir=metrics_dir,
        models_dir=models_dir,
        model_names=model_names,
    )

    report_path = output_dir / "pipeline-report.md"
    comparison_path = reports_dir / "model-comparison.csv"
    export_model_comparison_csv(metrics_dir, comparison_path)
    confusion_matrix_paths = export_confusion_matrix_svgs(metrics_dir, figures_dir)
    feature_importance_paths = export_feature_importance_csvs(
        args.dataset_id,
        processed_train_path,
        models_dir,
        reports_dir / "feature-importance",
    )

    shap_plot_paths = export_shap_summary_plots(
        args.dataset_id,
        processed_test_path,
        models_dir,
        shap_plots_dir,
    )
    shap_instance_paths = export_shap_instance_values(
        args.dataset_id,
        processed_test_path,
        models_dir,
        shap_instances_dir,
    )

    summary = {
        "dataset_id": args.dataset_id,
        "split_mode": split_mode,
        "profile_path": str(profile_path),
        "split_summary_path": str(split_summary_path),
        "report_path": str(report_path),
        "model_comparison_path": str(comparison_path),
        "confusion_matrix_paths": [str(path) for path in confusion_matrix_paths],
        "feature_importance_paths": [str(path) for path in feature_importance_paths],
        "shap_plot_paths": [str(path) for path in shap_plot_paths],
        "shap_instance_paths": [str(path) for path in shap_instance_paths],
        "processed_train_path": str(processed_train_path),
        "processed_test_path": str(processed_test_path),
        "metrics_dir": str(metrics_dir),
        "models_dir": str(models_dir),
        "models": model_names,
        "metrics": metrics,
    }
    summary_path = output_dir / "pipeline-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    artifact_paths = {
        "Dataset profile": str(profile_path),
        "Split summary": str(split_summary_path),
        "Model comparison": str(comparison_path),
        "Confusion matrices": [str(path) for path in confusion_matrix_paths],
        "Feature importance": [str(path) for path in feature_importance_paths],
        "SHAP summary plots": [str(path) for path in shap_plot_paths],
        "SHAP instance explanations": [str(path) for path in shap_instance_paths],
        "Metrics directory": str(metrics_dir),
        "Models directory": str(models_dir),
    }
    report_path.write_text(
        _build_markdown_report(args.dataset_id, profile.model_dump(), split_summary.model_dump(), metrics, artifact_paths),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


def _build_markdown_report(
    dataset_id: str,
    profile: dict[str, object],
    split_summary: dict[str, object],
    metrics: list[dict[str, object]],
    artifact_paths: dict[str, object],
) -> str:
    lines = [
        "# Dataset Pipeline Report",
        "",
        f"## Dataset: `{dataset_id}`",
        "",
        "## Dataset Profile",
        "",
        f"- Rows: {profile['row_count']}",
        f"- Columns: {profile['column_count']}",
        f"- Missing values: {profile['missing_value_count']}",
        f"- Label distribution: `{profile['label_distribution']}`",
        f"- Attack category distribution: `{profile['attack_category_distribution']}`",
        "",
        "## Train/Test Split",
        "",
        f"- Train rows: {split_summary['train_rows']}",
        f"- Test rows: {split_summary['test_rows']}",
        f"- Strategy: `{split_summary['split_strategy']}`",
        f"- Stratified: `{split_summary['stratified']}`",
        f"- Train label distribution: `{split_summary['train_label_distribution']}`",
        f"- Test label distribution: `{split_summary['test_label_distribution']}`",
        "",
        "## Model Metrics",
        "",
        "| Model | Accuracy | Precision | Recall | F1-score | FPR | Sample Count |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in metrics:
        lines.append(
            "| {model} | {accuracy:.4f} | {precision:.4f} | {recall:.4f} | {f1:.4f} | {fpr:.4f} | {count} |".format(
                model=row["model_name"],
                accuracy=float(row["accuracy"]),
                precision=float(row["precision"]),
                recall=float(row["recall"]),
                f1=float(row["f1_score"]),
                fpr=float(row["false_positive_rate"]),
                count=row["sample_count"],
            )
        )
    lines.extend(["", "## Generated Artifacts", ""])
    for label, value in artifact_paths.items():
        if isinstance(value, list):
            lines.append(f"- {label}:")
            for path in value:
                lines.append(f"  - `{path}`")
        else:
            lines.append(f"- {label}: `{value}`")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "Fixture or small-dataset results are for pipeline validation only. Full thesis claims require benchmark datasets such as UNSW-NB15 and CICIDS2017/CSE-CIC-IDS2018.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
