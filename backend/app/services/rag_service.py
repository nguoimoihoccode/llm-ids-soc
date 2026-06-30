from app.paths import PLAYBOOKS_ROOT


def retrieve_context(attack_type: str, query: str = "") -> str:
    """Return relevant playbook context for an alert.

    Attempts vector retrieval first (FAISS + embeddings), then falls back
    to exact playbook file lookup.
    """
    context = _vector_retrieve(attack_type, query)
    if context:
        return context
    return _exact_file_lookup(attack_type)


def _vector_retrieve(attack_type: str, query: str) -> str:
    try:
        from app.services.vector_rag import retrieve_top_k
        search_query = query or f"{attack_type} attack detection response playbook"
        results = retrieve_top_k(search_query, top_k=3)
        if not results:
            return ""
        lines = ["## Retrieved Security Context\n"]
        for r in results:
            lines.append(f"- [{r['source']}] (score={r['score']:.3f}): {r['text'][:300]}")
        return "\n".join(lines)
    except FileNotFoundError:
        return ""
    except Exception:
        return ""


def _exact_file_lookup(attack_type: str) -> str:
    filename = attack_type.lower().replace(" ", "-") + ".md"
    path = PLAYBOOKS_ROOT / filename
    if not path.exists():
        return "No local playbook found. Use only the alert fields."
    return path.read_text(encoding="utf-8")
