import json
import logging
from pathlib import Path
from typing import Optional

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

logger = logging.getLogger(__name__)

PARAM_GRIDS = {
    "logistic_regression": {
        "model__C": [0.01, 0.1, 1.0, 10.0, 100.0],
        "model__solver": ["lbfgs", "liblinear"],
    },
    "logistic_regression_scaled": {
        "model__C": [0.01, 0.1, 1.0, 10.0, 100.0],
        "model__solver": ["lbfgs", "liblinear"],
    },
    "decision_tree": {
        "max_depth": [None, 5, 10, 20, 30, 50],
        "min_samples_split": [2, 5, 10, 20],
        "min_samples_leaf": [1, 2, 5, 10],
        "criterion": ["gini", "entropy"],
    },
    "random_forest": {
        "n_estimators": [50, 100, 200, 300],
        "max_depth": [None, 10, 20, 30, 50],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", None],
    },
    "xgboost": {
        "n_estimators": [50, 100, 200, 300],
        "max_depth": [3, 4, 6, 8, 10],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "subsample": [0.6, 0.8, 1.0],
        "colsample_bytree": [0.6, 0.8, 1.0],
        "min_child_weight": [1, 3, 5, 7],
        "reg_lambda": [0.1, 1.0, 2.0, 5.0],
        "reg_alpha": [0.0, 0.1, 0.5, 1.0],
    },
}


def _build_base_estimator(model_name: str):
    if model_name == "logistic_regression":
        return Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=2000, random_state=42)),
        ])
    if model_name == "logistic_regression_scaled":
        return Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=2000, random_state=42)),
        ])
    if model_name == "decision_tree":
        return DecisionTreeClassifier(random_state=42)
    if model_name == "random_forest":
        return RandomForestClassifier(random_state=42)
    if model_name == "xgboost":
        return XGBClassifier(eval_metric="logloss", random_state=42)
    raise ValueError(f"Unsupported model for tuning: {model_name}")


def tune_model(
    model_name: str,
    x_train: pd.DataFrame,
    y_train: pd.Series,
    n_iter: int = 40,
    cv: int = 3,
    random_state: int = 42,
    scoring: str = "f1",
) -> dict:
    grid = PARAM_GRIDS.get(model_name)
    if grid is None:
        raise ValueError(f"No param grid defined for: {model_name}")

    estimator = _build_base_estimator(model_name)
    search = RandomizedSearchCV(
        estimator,
        param_distributions=grid,
        n_iter=n_iter,
        cv=cv,
        scoring=scoring,
        random_state=random_state,
        n_jobs=-1,
        verbose=0,
    )
    search.fit(x_train, y_train)

    return {
        "model_name": model_name,
        "best_score": float(search.best_score_),
        "scoring": scoring,
        "best_params": search.best_params_,
    }


def tune_and_save(
    model_name: str,
    processed_train_path: Path,
    output_dir: Path,
    n_iter: int = 40,
    cv: int = 3,
) -> dict:
    frame = pd.read_csv(processed_train_path)
    if "label" not in frame.columns:
        raise ValueError("Processed dataset must include a label column.")
    x_train = frame.drop(columns=["label"])
    y_train = frame["label"].astype(int)

    logger.info("Tuning %s with %d iterations, %d-fold CV...", model_name, n_iter, cv)
    result = tune_model(model_name, x_train, y_train, n_iter=n_iter, cv=cv)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{model_name}-best-params.json"
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    logger.info("Best %s params saved to %s (score=%.4f)", model_name, output_path.name, result["best_score"])

    return result


def load_best_params(tuning_dir: Path, model_name: str) -> Optional[dict]:
    params_path = tuning_dir / f"{model_name}-best-params.json"
    if not params_path.exists():
        return None
    data = json.loads(params_path.read_text(encoding="utf-8"))
    return data.get("best_params")
