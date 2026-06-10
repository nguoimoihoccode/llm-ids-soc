from app.models import ModelEvaluation, NetworkEvent


def evaluate_rule_based_baseline(events: list[NetworkEvent]) -> ModelEvaluation:
    # Danh gia rule-based baseline tren tap event mau de co so sanh nhanh.
    predictions = [_predict_label(event) for event in events]
    labels = [event.label for event in events]
    sample_count = len(labels)
    correct = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted)

    return ModelEvaluation(
        model_name="RuleBasedBaseline",
        sample_count=sample_count,
        accuracy=correct / sample_count if sample_count else 0.0,
        attack_recall=_recall(labels, predictions, "Attack"),
        benign_recall=_recall(labels, predictions, "Benign"),
    )


def _predict_label(event: NetworkEvent) -> str:
    # Nhom quy tac rat don gian: chi so bat thuong vuot nguong thi gan la Attack.
    if event.failed_login_count >= 20:
        return "Attack"
    if event.flow_packets_s >= 500:
        return "Attack"
    if event.syn_flag_count >= 3 and event.flow_duration_ms <= 200:
        return "Attack"
    return "Benign"


def _recall(labels: list[str], predictions: list[str], target: str) -> float:
    # Tinh recall rieng cho tung lop de biet model bat duoc Attack/Benign den dau.
    positives = [index for index, label in enumerate(labels) if label == target]
    if not positives:
        return 0.0
    hits = sum(1 for index in positives if predictions[index] == target)
    return hits / len(positives)
