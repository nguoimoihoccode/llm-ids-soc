import json
import logging
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from app.services.hyperparameter_tuning import load_best_params
from app.services.model_metrics import calculate_binary_metrics

logger = logging.getLogger(__name__)


def train_models_from_csv(
    dataset_id: str,
    processed_path: Path,
    metrics_dir: Path,
    models_dir: Path,
    model_names: list[str],
    tuning_dir: Optional[Path] = None,
) -> list[dict[str, object]]:
    # Doc dataset da xu ly va train tung baseline model tren cung bo feature.
    frame = pd.read_csv(processed_path)
    if "label" not in frame.columns:
        raise ValueError("Processed dataset must include a label column.")

    x = frame.drop(columns=["label"])
    y = frame["label"].astype(int)
    return _train_and_evaluate_models(dataset_id, x, y, x, y, metrics_dir, models_dir, model_names, tuning_dir)


def train_models_from_split_csv(
    dataset_id: str,
    train_path: Path,
    test_path: Path,
    metrics_dir: Path,
    models_dir: Path,
    model_names: list[str],
    tuning_dir: Optional[Path] = None,
) -> list[dict[str, object]]:
    # Che do nghiem tuc hon: train bang train CSV, tinh metric bang test CSV.
    train_frame = pd.read_csv(train_path)
    test_frame = pd.read_csv(test_path)
    if "label" not in train_frame.columns or "label" not in test_frame.columns:
        raise ValueError("Train and test datasets must include a label column.")

    x_train = train_frame.drop(columns=["label"])
    y_train = train_frame["label"].astype(int)
    x_test = test_frame.drop(columns=["label"])
    y_test = test_frame["label"].astype(int)
    # Neu train/test sau one-hot co cot khac nhau thi align de model nhan cung feature set.
    x_train, x_test = x_train.align(x_test, join="outer", axis=1, fill_value=0)
    return _train_and_evaluate_models(dataset_id, x_train, y_train, x_test, y_test, metrics_dir, models_dir, model_names, tuning_dir)


def _train_and_evaluate_models(
    dataset_id: str,
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_eval: pd.DataFrame,
    y_eval: pd.Series,
    metrics_dir: Path,
    models_dir: Path,
    model_names: list[str],
    tuning_dir: Optional[Path] = None,
) -> list[dict[str, object]]:
    # Ham dung chung cho ca 2 che do: same-file demo va train/test split.
    metrics_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, object]] = []
    for model_name in model_names:
        # Moi model duoc train, tinh metric va luu artifact rieng.
        model = _build_model(model_name, tuning_dir)
        model.fit(x_train, y_train)
        predictions = model.predict(x_eval).astype(int).tolist()
        metrics = calculate_binary_metrics(model_name, dataset_id, y_eval.astype(int).tolist(), predictions)

        metrics_path = metrics_dir / f"{dataset_id}-{model_name}.json"
        metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        joblib.dump(model, models_dir / f"{dataset_id}-{model_name}.joblib")
        results.append(metrics)

    return results


def _build_model(model_name: str, tuning_dir: Optional[Path] = None):
    # Map ten model sang classifier cu the dung trong demo.
    if model_name == "logistic_regression":
        return LogisticRegression(max_iter=1000, random_state=42)
    if model_name == "logistic_regression_scaled":
        return _build_logistic_regression_scaled(tuning_dir)
    if model_name == "decision_tree":
        return _build_decision_tree(tuning_dir)
    if model_name == "random_forest":
        return _build_random_forest(tuning_dir)
    if model_name == "xgboost":
        return _build_xgboost_default()
    if model_name == "xgboost_tuned":
        return _build_xgboost_tuned(tuning_dir)
    raise ValueError(f"Unsupported model: {model_name}")


def _build_logistic_regression_scaled(tuning_dir: Optional[Path] = None):
    params = load_best_params(tuning_dir, "logistic_regression_scaled") if tuning_dir else None
    C = params.get("model__C", 1.0) if params else 1.0
    solver = params.get("model__solver", "lbfgs") if params else "lbfgs"
    return Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(C=C, solver=solver, max_iter=2000, random_state=42)),
    ])


def _build_decision_tree(tuning_dir: Optional[Path] = None):
    params = load_best_params(tuning_dir, "decision_tree") if tuning_dir else None
    kwargs = {k: v for k, v in (params or {}).items()}
    kwargs.setdefault("random_state", 42)
    return DecisionTreeClassifier(**kwargs)


def _build_random_forest(tuning_dir: Optional[Path] = None):
    params = load_best_params(tuning_dir, "random_forest") if tuning_dir else None
    kwargs = {k: v for k, v in (params or {}).items()}
    kwargs.setdefault("random_state", 42)
    return RandomForestClassifier(**kwargs)


def _build_xgboost_default():
    return XGBClassifier(
        n_estimators=50,
        max_depth=4,
        learning_rate=0.1,
        eval_metric="logloss",
        random_state=42,
    )


def _build_xgboost_tuned(tuning_dir: Optional[Path] = None):
    params = load_best_params(tuning_dir, "xgboost") if tuning_dir else None
    if params is None:
        logger.warning("No tuned params found for xgboost, using factory defaults.")
        params = {
            "n_estimators": 120,
            "max_depth": 3,
            "learning_rate": 0.05,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "min_child_weight": 3,
            "reg_lambda": 2.0,
        }
    return XGBClassifier(
        **{k: v for k, v in params.items()},
        eval_metric="logloss",
        random_state=42,
    )
