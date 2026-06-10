from collections.abc import Sequence


def calculate_binary_metrics(
    model_name: str,
    dataset_id: str,
    y_true: Sequence[int],
    y_pred: Sequence[int],
) -> dict[str, object]:
    tn = fp = fn = tp = 0
    for actual, predicted in zip(y_true, y_pred):
        if actual == 0 and predicted == 0:
            tn += 1
        elif actual == 0 and predicted == 1:
            fp += 1
        elif actual == 1 and predicted == 0:
            fn += 1
        elif actual == 1 and predicted == 1:
            tp += 1

    total = tn + fp + fn + tp
    accuracy = (tp + tn) / total if total else 0.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1_score = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    false_positive_rate = fp / (fp + tn) if fp + tn else 0.0

    return {
        "model_name": model_name,
        "dataset_id": dataset_id,
        "sample_count": total,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "false_positive_rate": false_positive_rate,
        "confusion_matrix": [[tn, fp], [fn, tp]],
    }
