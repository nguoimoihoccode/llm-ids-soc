from pathlib import Path
from xml.sax.saxutils import escape

from app.services.metric_artifacts import list_metric_artifacts


def export_confusion_matrix_svgs(metrics_dir: Path, figures_dir: Path) -> list[Path]:
    # Moi metric hop le se duoc ve thanh mot hinh SVG confusion matrix.
    figures_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for metric in list_metric_artifacts(metrics_dir):
        matrix = metric.get("confusion_matrix")
        if not _is_binary_matrix(matrix):
            continue

        dataset_id = str(metric.get("dataset_id", "dataset"))
        model_name = str(metric.get("model_name", "model"))
        output_path = figures_dir / f"{dataset_id}-{model_name}-confusion-matrix.svg"
        output_path.write_text(_render_svg(dataset_id, model_name, matrix), encoding="utf-8")
        outputs.append(output_path)
    return outputs


def _is_binary_matrix(matrix: object) -> bool:
    return isinstance(matrix, list) and len(matrix) == 2 and all(isinstance(row, list) and len(row) == 2 for row in matrix)


def _render_svg(dataset_id: str, model_name: str, matrix: list[list[int]]) -> str:
    # Ve 4 o TN/FP/FN/TP bang SVG de xem truc tiep trong bao cao.
    tn, fp = matrix[0]
    fn, tp = matrix[1]
    title = f"Confusion Matrix: {dataset_id} / {model_name}"
    cells = [
        ("TN", tn, 80, 90, "#22c55e"),
        ("FP", fp, 230, 90, "#f97316"),
        ("FN", fn, 80, 220, "#ef4444"),
        ("TP", tp, 230, 220, "#38bdf8"),
    ]
    cell_markup = "\n".join(
        f'<rect x="{x}" y="{y}" width="120" height="90" rx="12" fill="{color}" opacity="0.82" />'
        f'<text x="{x + 60}" y="{y + 43}" text-anchor="middle" font-size="22" fill="#07111f" font-weight="700">{label} {value}</text>'
        for label, value, x, y, color in cells
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="430" height="360" viewBox="0 0 430 360">
  <rect width="430" height="360" rx="22" fill="#07111f" />
  <text x="215" y="42" text-anchor="middle" font-size="18" fill="#d8f3ff" font-family="Arial">{escape(title)}</text>
  <text x="215" y="72" text-anchor="middle" font-size="13" fill="#8fb4ca" font-family="Arial">Predicted label</text>
  <text x="35" y="190" text-anchor="middle" font-size="13" fill="#8fb4ca" font-family="Arial" transform="rotate(-90 35 190)">Actual label</text>
  {cell_markup}
</svg>
'''
