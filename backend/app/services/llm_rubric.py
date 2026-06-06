import csv
from pathlib import Path


RUBRIC_FIELDS = [
    "alert_id",
    "mode",
    "correctness",
    "completeness",
    "groundedness",
    "actionability",
    "hallucination_safety",
    "latency",
]


def evaluate_comparison_with_rubric(comparison: dict[str, object]) -> list[dict[str, object]]:
    alert_id = str(comparison["alert_id"])
    rows: list[dict[str, object]] = []
    for item in comparison["comparisons"]:  # type: ignore[index]
        mode = str(item["mode"])
        uses_rag = bool(item["uses_rag"])
        summary = str(item["summary"])
        knowledge_context = str(item["knowledge_context"])
        rows.append(
            {
                "alert_id": alert_id,
                "mode": mode,
                "correctness": _score_correctness(summary),
                "completeness": _score_completeness(summary, uses_rag),
                "groundedness": _score_groundedness(summary, knowledge_context, uses_rag),
                "actionability": _score_actionability(summary, knowledge_context, uses_rag),
                "hallucination_safety": _score_hallucination_safety(summary),
                "latency": 5,
            }
        )
    return rows


def export_rubric_scores_csv(rows: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=RUBRIC_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _score_correctness(summary: str) -> int:
    return 5 if any(term in summary for term in ["Brute Force", "DDoS", "Port Scan"]) else 3


def _score_completeness(summary: str, uses_rag: bool) -> int:
    score = 3
    if "evidence" in summary.lower() or "MITRE" in summary:
        score += 1
    if uses_rag:
        score += 1
    return min(score, 5)


def _score_groundedness(summary: str, knowledge_context: str, uses_rag: bool) -> int:
    score = 2
    if "evidence" in summary.lower() or "MITRE" in summary:
        score += 1
    if uses_rag and knowledge_context:
        score += 2
    return min(score, 5)


def _score_actionability(summary: str, knowledge_context: str, uses_rag: bool) -> int:
    if uses_rag and knowledge_context:
        return 5
    return 4 if "response" in summary.lower() or "guidance" in summary.lower() else 2


def _score_hallucination_safety(summary: str) -> int:
    risky_terms = ["CVE-", "guaranteed", "certainly compromised"]
    return 3 if any(term in summary for term in risky_terms) else 5
