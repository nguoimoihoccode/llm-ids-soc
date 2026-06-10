import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

# Goi service tong hop diem rubric thanh markdown RAG vs no-RAG.
from app.services.llm_rubric_summary import export_rag_summary_markdown  # noqa: E402


def main() -> None:
    # CLI doc CSV diem rubric va xuat bao cao markdown ngan gon.
    parser = argparse.ArgumentParser(description="Export RAG vs no-RAG markdown summary from rubric scores.")
    parser.add_argument("--scores", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    export_rag_summary_markdown(args.scores, args.output)
    print(json.dumps({"summary_written": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
