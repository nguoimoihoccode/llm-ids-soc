from app.models import Alert
from app.services.llm_rubric import evaluate_comparison_with_rubric
from app.services.llm_service import compare_explanation_modes, explain_alert


def build_incident_case_studies_markdown(alerts: list[Alert]) -> str:
    lines = ["# Incident Case Studies", ""]
    for index, alert in enumerate(alerts, start=1):
        explanation = explain_alert(alert)
        comparison = compare_explanation_modes(alert)
        rubric_rows = evaluate_comparison_with_rubric(comparison.model_dump())

        lines.extend(
            [
                f"## Case {index}: {alert.attack_type}",
                "",
                f"Alert ID: `{alert.alert_id}`",
                f"Source: `{alert.src_ip}` -> Destination: `{alert.dst_ip}`",
                f"Severity: {alert.severity} | Priority: {alert.triage_priority} | Confidence: {alert.confidence:.0%}",
                f"MITRE: {alert.mitre_technique}",
                f"Evidence features: {', '.join(alert.top_features)}",
                "",
                "### Grounded Explanation",
                "",
                explanation.summary,
                "",
                f"Why suspicious: {explanation.why_suspicious}",
                "",
                "Recommended response:",
            ]
        )
        lines.extend(f"- {item}" for item in explanation.recommended_response)
        lines.extend(["", "### Explanation Comparison", ""])
        for item in comparison.comparisons:
            rag_label = "RAG" if item.uses_rag else "No RAG"
            lines.extend([f"- **{item.mode}** ({rag_label}): {item.summary}"])

        lines.extend(["", "### Rubric Scores", "", "| Mode | Correctness | Completeness | Groundedness | Actionability | Hallucination Safety | Latency |", "|---|---:|---:|---:|---:|---:|---:|"])
        for row in rubric_rows:
            lines.append(
                f"| {row['mode']} | {row['correctness']} | {row['completeness']} | {row['groundedness']} | "
                f"{row['actionability']} | {row['hallucination_safety']} | {row['latency']} |"
            )
        lines.append("")
    return "\n".join(lines)
