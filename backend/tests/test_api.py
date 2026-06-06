from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_alerts_returns_attack_alerts() -> None:
    response = client.get("/alerts")
    assert response.status_code == 200
    alerts = response.json()
    assert len(alerts) == 3
    assert alerts[0]["attack_type"] == "Brute Force"
    assert alerts[0]["top_features"] == ["failed_login_count", "dst_port", "flow_packets_s"]
    assert alerts[0]["mitre_technique"] == "T1110 - Brute Force"
    assert alerts[0]["triage_priority"] == "P1"


def test_explanation_includes_rag_context() -> None:
    response = client.get("/alerts/alert-evt-002/explanation")
    assert response.status_code == 200
    body = response.json()
    assert body["alert_id"] == "alert-evt-002"
    assert "Brute Force Playbook" in body["knowledge_context"]
    assert body["provider"] == "local-template"
    assert body["evidence_features"] == ["failed_login_count", "dst_port", "flow_packets_s"]
    assert "T1110 - Brute Force" in body["summary"]
    assert "P1" in body["summary"]


def test_explanation_comparison_returns_three_modes() -> None:
    response = client.get("/alerts/alert-evt-002/explanation/comparison")
    assert response.status_code == 200
    body = response.json()
    assert body["alert_id"] == "alert-evt-002"
    assert [item["mode"] for item in body["comparisons"]] == ["template", "llm_without_rag", "llm_with_rag"]
    assert body["comparisons"][0]["uses_rag"] is False
    assert body["comparisons"][1]["uses_rag"] is False
    assert body["comparisons"][2]["uses_rag"] is True
    assert "Brute Force Playbook" in body["comparisons"][2]["knowledge_context"]


def test_ml_evaluation_returns_model_metrics() -> None:
    response = client.get("/ml/evaluate")
    assert response.status_code == 200
    body = response.json()
    assert body["model_name"] == "RuleBasedBaseline"
    assert body["sample_count"] == 5
    assert body["accuracy"] == 1.0
    assert body["attack_recall"] == 1.0
    assert body["benign_recall"] == 1.0


def test_ml_metrics_endpoint_returns_saved_artifacts() -> None:
    response = client.get("/ml/metrics")
    assert response.status_code == 200
    body = response.json()
    model_names = {metric["model_name"] for metric in body}
    assert "logistic_regression" in model_names
    assert "decision_tree" in model_names
    assert "random_forest" in model_names


def test_datasets_endpoint_returns_registry() -> None:
    response = client.get("/datasets")
    assert response.status_code == 200
    body = response.json()
    assert [dataset["dataset_id"] for dataset in body] == ["sample", "unsw-nb15", "cicids2017"]
    assert body[0]["source_url"] == "local sample data"
