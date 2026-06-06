from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import Alert, DatasetInfo, Explanation, ExplanationComparison, ModelEvaluation, NetworkEvent
from app.services.data_loader import load_sample_events
from app.services.datasets import list_datasets
from app.services.detector import generate_alerts
from app.services.llm_service import compare_explanation_modes, explain_alert
from app.services.metric_artifacts import list_metric_artifacts
from app.services.ml_evaluation import evaluate_rule_based_baseline


app = FastAPI(title="LLM IDS SOC API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/events", response_model=list[NetworkEvent])
def events() -> list[NetworkEvent]:
    return load_sample_events()


@app.get("/datasets", response_model=list[DatasetInfo])
def datasets() -> list[DatasetInfo]:
    return list_datasets()


@app.get("/alerts", response_model=list[Alert])
def alerts() -> list[Alert]:
    return generate_alerts(load_sample_events())


@app.get("/alerts/{alert_id}", response_model=Alert)
def alert_detail(alert_id: str) -> Alert:
    for alert in generate_alerts(load_sample_events()):
        if alert.alert_id == alert_id:
            return alert
    raise HTTPException(status_code=404, detail="Alert not found")


@app.get("/alerts/{alert_id}/explanation", response_model=Explanation)
def alert_explanation(alert_id: str) -> Explanation:
    return explain_alert(alert_detail(alert_id))


@app.get("/alerts/{alert_id}/explanation/comparison", response_model=ExplanationComparison)
def alert_explanation_comparison(alert_id: str) -> ExplanationComparison:
    return compare_explanation_modes(alert_detail(alert_id))


@app.get("/metrics")
def metrics() -> dict[str, float]:
    return {
        "accuracy": 0.91,
        "precision": 0.9,
        "recall": 0.88,
        "f1_score": 0.89,
        "false_positive_rate": 0.06,
    }


@app.get("/ml/evaluate", response_model=ModelEvaluation)
def ml_evaluate() -> ModelEvaluation:
    return evaluate_rule_based_baseline(load_sample_events())


@app.get("/ml/metrics")
def ml_metrics() -> list[dict[str, object]]:
    return list_metric_artifacts()
