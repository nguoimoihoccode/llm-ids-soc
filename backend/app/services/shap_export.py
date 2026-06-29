import csv
import json
import logging
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)


def _select_explainer(model, X_background: pd.DataFrame):
    if _has_feature_importances(model):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            explainer = shap.TreeExplainer(model)
        return explainer, "TreeExplainer"

    if isinstance(model, Pipeline):
        final = model.steps[-1][1]
        if isinstance(final, LogisticRegression):
            explainer = shap.LinearExplainer(final, X_background)
            return explainer, "LinearExplainer"

    if isinstance(model, LogisticRegression):
        explainer = shap.LinearExplainer(model, X_background)
        return explainer, "LinearExplainer"

    logger.warning("No exact SHAP explainer for %s, falling back to KernelExplainer", type(model).__name__)
    explainer = shap.KernelExplainer(model.predict_proba, X_background)
    return explainer, "KernelExplainer"


def _has_feature_importances(model) -> bool:
    if isinstance(model, Pipeline):
        return hasattr(model.steps[-1][1], "feature_importances_")
    return hasattr(model, "feature_importances_")


def _align_features(X: pd.DataFrame, model) -> pd.DataFrame:
    expected = list(getattr(model, "feature_names_in_", []))
    if not expected:
        return X
    missing = [col for col in expected if col not in X.columns]
    for col in missing:
        X[col] = 0.0
    return X[expected]


def export_shap_summary_plots(
    dataset_id: str,
    processed_path: Path,
    models_dir: Path,
    output_dir: Path,
    background_size: int = 100,
    eval_sample_size: int = 500,
) -> list[Path]:
    frame = pd.read_csv(processed_path)
    feature_names = [col for col in frame.columns if col != "label"]
    X = frame[feature_names]
    if len(X) > eval_sample_size:
        X = X.sample(n=eval_sample_size, random_state=42)
    X_background = X.sample(n=min(background_size, len(X)), random_state=42)

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    for model_path in sorted(models_dir.glob(f"{dataset_id}-*.joblib")):
        model = joblib.load(model_path)
        model_name = model_path.stem.replace(f"{dataset_id}-", "")
        X_aligned = _align_features(X, model)
        explainer, explainer_type = _select_explainer(model, X_background)

        shap_values = explainer.shap_values(X_aligned)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        figure = plt.figure()
        shap.summary_plot(shap_values, X_aligned, feature_names=np.array(X_aligned.columns.tolist()), show=False)
        output_path = output_dir / f"{dataset_id}-{model_name}-shap-summary.svg"
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close(figure)

        outputs.append(output_path)
        logger.info("SHAP summary exported: %s (%s)", output_path.name, explainer_type)

    return outputs


def export_shap_instance_values(
    dataset_id: str,
    processed_path: Path,
    models_dir: Path,
    output_dir: Path,
    background_size: int = 100,
    eval_sample_size: int = 500,
    top_k: int = 10,
) -> list[Path]:
    frame = pd.read_csv(processed_path)
    feature_names = [col for col in frame.columns if col != "label"]
    label_col = frame["label"]
    X = frame[feature_names]
    y = label_col

    if len(X) > eval_sample_size:
        indices = X.sample(n=eval_sample_size, random_state=42).index
        X = X.loc[indices]
        y = y.loc[indices]
    X_background = X.sample(n=min(background_size, len(X)), random_state=42)

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    for model_path in sorted(models_dir.glob(f"{dataset_id}-*.joblib")):
        model = joblib.load(model_path)
        model_name = model_path.stem.replace(f"{dataset_id}-", "")
        X_aligned = _align_features(X, model)
        model_feature_names = X_aligned.columns.tolist()
        explainer, _ = _select_explainer(model, X_background)

        shap_values = explainer.shap_values(X_aligned)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        if len(shap_values.shape) > 2:
            shap_values = shap_values.reshape(shap_values.shape[0], -1)

        predictions = model.predict(X_aligned)
        instances = []
        for idx in range(len(X_aligned)):
            row_shap = np.asarray(shap_values[idx]).flatten()
            feature_scores = sorted(
                zip(model_feature_names, [float(v) for v in row_shap]),
                key=lambda item: abs(item[1]),
                reverse=True,
            )[:top_k]
            instances.append({
                "instance_index": int(idx),
                "true_label": int(y.iloc[idx]),
                "predicted": int(predictions[idx]),
                "top_features": [
                    {
                        "feature": name,
                        "shap_value": value,
                        "direction": "attack" if value > 0 else "benign",
                    }
                    for name, value in feature_scores
                ],
            })

        output_path = output_dir / f"{dataset_id}-{model_name}-shap-instances.json"
        output_path.write_text(json.dumps(instances, indent=2), encoding="utf-8")
        outputs.append(output_path)
        logger.info("SHAP instances exported: %s (%d instances)", output_path.name, len(instances))

    return outputs


def compute_single_instance_shap(
    model,
    instance: pd.DataFrame,
    top_k: int = 10,
) -> list[dict]:
    feature_names = list(getattr(model, "feature_names_in_", instance.columns))

    if len(instance) < 10:
        background = pd.concat([instance] * max(2, min(10, 100 // len(instance))), ignore_index=True)
    else:
        background = instance.head(min(100, len(instance)))

    explainer, _ = _select_explainer(model, background)
    shap_values = explainer.shap_values(instance)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    feature_scores = sorted(
        zip(feature_names, [float(v) for v in shap_values[0]]),
        key=lambda item: abs(item[1]),
        reverse=True,
    )[:top_k]

    return [{"feature": name, "importance": value} for name, value in feature_scores]
