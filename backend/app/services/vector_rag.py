import json
import logging
from pathlib import Path
from typing import Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from app.paths import KNOWLEDGE_BASE_ROOT, PLAYBOOKS_ROOT

logger = logging.getLogger(__name__)

VECTOR_INDEX_PATH = KNOWLEDGE_BASE_ROOT / "vector_index"

EMBEDDING_DIM = 384
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def _chunk_playbooks(playbook_dir: Path, chunk_size: int = 200) -> list[dict]:
    chunks = []
    for md_path in sorted(playbook_dir.glob("*.md")):
        text = md_path.read_text(encoding="utf-8")
        attack_type = md_path.stem.replace("-", " ").title()
        words = text.split()
        for i in range(0, len(words), chunk_size):
            chunk_text = " ".join(words[i:i + chunk_size])
            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "source": md_path.name,
                    "attack_type": attack_type,
                })
    return chunks


def _build_tfidf_embeddings(chunks: list[dict]) -> np.ndarray:
    vectorizer = TfidfVectorizer(max_features=EMBEDDING_DIM)
    texts = [c["text"] for c in chunks]
    embeddings = vectorizer.fit_transform(texts).toarray().astype(np.float32)
    # Normalize for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return embeddings / norms


def _build_sentence_transformer_embeddings(chunks: list[dict]) -> Optional[np.ndarray]:
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        texts = [c["text"] for c in chunks]
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return embeddings / norms
    except ImportError:
        logger.info("sentence-transformers not installed, using TF-IDF fallback")
        return None
    except Exception as exc:
        logger.warning("sentence-transformers failed (%s), using TF-IDF fallback", exc)
        return None


def build_index(playbook_dir: Path = PLAYBOOKS_ROOT, output_dir: Path = VECTOR_INDEX_PATH) -> Path:
    chunks = _chunk_playbooks(playbook_dir)
    if not chunks:
        raise ValueError("No playbook chunks found")

    embeddings = _build_sentence_transformer_embeddings(chunks)
    embedding_method = "sentence-transformers" if embeddings is not None else "tfidf"
    if embeddings is None:
        embeddings = _build_tfidf_embeddings(chunks)

    output_dir.mkdir(parents=True, exist_ok=True)
    chunks_path = output_dir / "chunks.json"
    chunks_path.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    embeddings_path = output_dir / "embeddings.npy"
    np.save(embeddings_path, embeddings)

    meta_path = output_dir / "index_meta.json"
    meta_path.write_text(json.dumps({
        "num_chunks": len(chunks),
        "embedding_dim": int(embeddings.shape[1]),
        "embedding_method": embedding_method,
    }, indent=2), encoding="utf-8")

    logger.info("Vector index built: %d chunks, method=%s", len(chunks), embedding_method)
    return output_dir


def _load_index(index_dir: Path = VECTOR_INDEX_PATH) -> tuple[list[dict], np.ndarray]:
    chunks_path = index_dir / "chunks.json"
    embeddings_path = index_dir / "embeddings.npy"
    if not chunks_path.exists() or not embeddings_path.exists():
        raise FileNotFoundError(f"Vector index not found at {index_dir}. Run build_index first.")
    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    embeddings = np.load(embeddings_path)
    return chunks, embeddings


def retrieve_top_k(query: str, top_k: int = 3, index_dir: Path = VECTOR_INDEX_PATH) -> list[dict]:
    try:
        chunks, embeddings = _load_index(index_dir)
    except FileNotFoundError:
        logger.warning("Vector index missing, falling back to keyword match")
        return _keyword_fallback(query, top_k)

    try:
        query_vec = _embed_query(query)
    except Exception:
        query_vec = _embed_query_tfidf(query, [c["text"] for c in chunks])

    similarities = np.dot(embeddings, query_vec)
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        score = float(similarities[idx])
        if score > 0.01:
            results.append({
                **chunks[idx],
                "score": round(score, 4),
            })
    return results


def _embed_query(query: str) -> np.ndarray:
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        vec = model.encode([query], convert_to_numpy=True, show_progress_bar=False)[0]
        return vec / np.linalg.norm(vec)
    except ImportError:
        raise


def _embed_query_tfidf(query: str, corpus: list[str]) -> np.ndarray:
    vectorizer = TfidfVectorizer(max_features=EMBEDDING_DIM)
    vectorizer.fit(corpus)
    vec = vectorizer.transform([query]).toarray()[0].astype(np.float32)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


def _keyword_fallback(query: str, top_k: int) -> list[dict]:
    chunks = _chunk_playbooks(PLAYBOOKS_ROOT)
    query_lower = query.lower()
    scored = []
    for chunk in chunks:
        score = sum(1 for word in query_lower.split() if word in chunk["text"].lower())
        if score > 0:
            scored.append({**chunk, "score": float(score)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
