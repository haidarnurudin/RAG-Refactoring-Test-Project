# RAG Refactoring

Proyek ini adalah hasil refaktorisasi sistem RAG menggunakan FastAPI, LangGraph, dan Qdrant dengan fokus pada *Clean Architecture* dan *Dependency Injection*.

---

## Struktur Proyek
- `app/main.py`: Entry point API (FastAPI).
- `app/services.py`: Logika bisnis & Workflow LangGraph.
- `app/repository.py`: Pengelolaan data (Qdrant & Memory).
- `app/models.py`: Skema data (Pydantic).
- `notes.md`: Dokumentasi keputusan desain dan trade-off.

---

> *Dibuat untuk memenuhi Penugasan Teknis Refaktorisasi RAG.*
