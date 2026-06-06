import csv
from collections import defaultdict
from pathlib import Path


SCORE_FIELDS = ["correctness", "completeness", "groundedness", "actionability", "hallucination_safety", "latency"]


def build_rag_summary_markdown(scores_path: Path) -> str:
    rows = _read_scores(scores_path)
    averages = _average_by_mode(rows)
    lines = [
        "# RAG vs No-RAG Summary",
        "",
        "| Mode | Correctness | Completeness | Groundedness | Actionability | Hallucination Safety | Latency |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for mode in sorted(averages):
        values = averages[mode]
        lines.append(
            f"| {mode} | {values['correctness']:.2f} | {values['completeness']:.2f} | "
            f"{values['groundedness']:.2f} | {values['actionability']:.2f} | "
            f"{values['hallucination_safety']:.2f} | {values['latency']:.2f} |"
        )

    best_grounded = max(averages.items(), key=lambda item: item[1]["groundedness"])[0] if averages else "none"
    lines.extend([
        "",
        "## Interpretation",
        "",
        "RAG-backed explanations achieved the highest groundedness score." if best_grounded == "llm_with_rag" else f"Highest groundedness mode: {best_grounded}.",
        "This report is generated from deterministic rubric scores and should be extended with expert review for the final thesis.",
    ])
    return "\n".join(lines) + "\n"


def export_rag_summary_markdown(scores_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_rag_summary_markdown(scores_path), encoding="utf-8")


def _read_scores(scores_path: Path) -> list[dict[str, str]]:
    with scores_path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def _average_by_mode(rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    totals: dict[str, dict[str, float]] = defaultdict(lambda: {field: 0.0 for field in SCORE_FIELDS})
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        mode = row["mode"]
        counts[mode] += 1
        for field in SCORE_FIELDS:
            totals[mode][field] += float(row[field])
    return {
        mode: {field: totals[mode][field] / counts[mode] for field in SCORE_FIELDS}
        for mode in totals
    }
