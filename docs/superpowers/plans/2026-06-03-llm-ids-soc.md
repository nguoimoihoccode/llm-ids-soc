# LLM IDS SOC Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a scaffolded MVP for an ML IDS + LLM/RAG SOC dashboard thesis prototype.

**Architecture:** FastAPI serves structured alerts, summaries, and explanation endpoints. React/Vite displays SOC overview and alert details. Sample data and markdown playbooks make the MVP runnable before full dataset ingestion.

**Tech Stack:** Python, FastAPI, pytest, React, TypeScript, Vite, CSS, CSV sample data.

---

## File Structure

- `backend/app/main.py`: FastAPI app and routes.
- `backend/app/models.py`: Pydantic models for events, alerts, explanations.
- `backend/app/services/data_loader.py`: CSV sample data loader.
- `backend/app/services/detector.py`: rule-based MVP detection interface.
- `backend/app/services/llm_service.py`: deterministic LLM-style explanation stub with RAG context.
- `backend/app/services/rag_service.py`: markdown playbook retrieval.
- `backend/tests/test_api.py`: API smoke tests.
- `data/samples/network_events.csv`: demo network events.
- `knowledge_base/playbooks/*.md`: attack response context.
- `frontend/src/*`: dashboard skeleton.

## Tasks

- [x] Create repository folder and documentation.
- [x] Add sample data and playbooks.
- [x] Implement FastAPI MVP endpoints.
- [x] Add backend smoke tests.
- [x] Scaffold React dashboard files.
- [x] Install dependencies and run tests/build.
- [x] Add rule-based ML evaluation endpoint.
- [x] Add LLM provider metadata scaffold.
- [x] Connect frontend dashboard to backend APIs with fallback data.
- [ ] Add real UNSW-NB15 preprocessing notebook/script.
- [ ] Add train/evaluate scripts for Random Forest baseline.
- [ ] Replace deterministic LLM stub with provider adapter.
- [ ] Add RAG vector store if needed.
