from app.services.model_metrics import calculate_binary_metrics


def test_calculate_binary_metrics_returns_standard_ids_metrics() -> None:
    metrics = calculate_binary_metrics(
        model_name="UnitModel",
        dataset_id="fixture",
        y_true=[0, 0, 1, 1],
        y_pred=[0, 1, 1, 1],
    )

    assert metrics["model_name"] == "UnitModel"
    assert metrics["dataset_id"] == "fixture"
    assert metrics["accuracy"] == 0.75
    assert metrics["precision"] == 2 / 3
    assert metrics["recall"] == 1.0
    assert metrics["f1_score"] == 0.8
    assert metrics["false_positive_rate"] == 0.5
    assert metrics["confusion_matrix"] == [[1, 1], [0, 2]]
