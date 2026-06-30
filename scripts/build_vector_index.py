import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.vector_rag import build_index  # noqa: E402
from app.paths import PLAYBOOKS_ROOT, KNOWLEDGE_BASE_ROOT  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Build vector index from playbook markdown files.")
    parser.add_argument("--playbook-dir", type=Path, default=PLAYBOOKS_ROOT)
    parser.add_argument("--output-dir", type=Path, default=KNOWLEDGE_BASE_ROOT / "vector_index")
    args = parser.parse_args()

    output = build_index(playbook_dir=args.playbook_dir, output_dir=args.output_dir)
    print(f"Vector index built at: {output}")


if __name__ == "__main__":
    main()
