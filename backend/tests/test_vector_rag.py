import json
from pathlib import Path

import numpy as np

from app.services.vector_rag import (
    _chunk_playbooks,
    _build_tfidf_embeddings,
    build_index,
    retrieve_top_k,
)


def _write_playbook(dir: Path, name: str, content: str) -> Path:
    path = dir / name
    path.write_text(content, encoding="utf-8")
    return path


def test_chunk_playbooks_splits_files(tmp_path: Path) -> None:
    words = "alert traffic source ip destination port attack suspicious " * 60
    _write_playbook(tmp_path, "brute-force.md", f"# Brute Force\n\n{words}\n")

    chunks = _chunk_playbooks(tmp_path, chunk_size=50)

    assert len(chunks) >= 1
    for c in chunks:
        assert c["source"] == "brute-force.md"
        assert c["attack_type"] == "Brute Force"
        assert len(c["text"]) > 0


def test_build_tfidf_embeddings_normalizes_vectors(tmp_path: Path) -> None:
    _write_playbook(tmp_path, "ddos.md", "DDoS attacks flood network bandwidth with malicious traffic.")
    _write_playbook(tmp_path, "port-scan.md", "Port scanning probes open ports for reconnaissance.")

    chunks = _chunk_playbooks(tmp_path, chunk_size=200)
    embeddings = _build_tfidf_embeddings(chunks)

    assert embeddings.shape[0] == len(chunks)
    assert embeddings.dtype == np.float32
    norms = np.linalg.norm(embeddings, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-5)


def test_build_index_and_retrieve(tmp_path: Path) -> None:
    _write_playbook(tmp_path, "brute-force.md",
        "## Brute Force Attack\n\nA brute force attack repeatedly attempts login credentials.\n"
        "Response: block source IP, enable MFA, review password policy.\n")
    _write_playbook(tmp_path, "ddos.md",
        "## DDoS Attack\n\nA DDoS attack overwhelms services with traffic from many sources.\n"
        "Response: rate limiting, upstream filtering, traffic analysis.\n")
    _write_playbook(tmp_path, "port-scan.md",
        "## Port Scan\n\nPort scanning probes hosts for open ports to identify vulnerable services.\n"
        "Response: block scanner IPs, review exposed services.\n")

    index_dir = tmp_path / "index"
    build_index(playbook_dir=tmp_path, output_dir=index_dir)

    assert (index_dir / "chunks.json").exists()
    assert (index_dir / "embeddings.npy").exists()
    assert (index_dir / "index_meta.json").exists()

    meta = json.loads((index_dir / "index_meta.json").read_text())
    assert meta["num_chunks"] > 0
    assert meta["embedding_dim"] > 0

    results = retrieve_top_k("brute force login attempt", top_k=2, index_dir=index_dir)
    assert len(results) >= 1
    assert any("brute" in r["text"].lower() or "brute" in r["source"] for r in results)


def test_retrieve_top_k_falls_back_when_index_missing(tmp_path: Path) -> None:
    _write_playbook(tmp_path, "brute-force.md", "Login brute force detection and response guide.")
    results = retrieve_top_k("login brute force", top_k=2, index_dir=tmp_path / "missing")

    assert isinstance(results, list)
