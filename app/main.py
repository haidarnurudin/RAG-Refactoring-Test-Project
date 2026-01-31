import time
from fastapi import FastAPI, HTTPException

# Mengambil skema, repository, dan service dari file lain di folder yang sama
from .models import QuestionRequest, DocumentRequest
from .repository import DocumentStore
from .services import RAGService

app = FastAPI(title="Refactored RAG API")

# --- Inisialisasi ---
# Sesuai prinsip Explicit Dependencies: menyuntikkan doc_store ke dalam rag_service
doc_store = DocumentStore()
rag_service = RAGService(doc_store=doc_store)

# --- API Endpoints ---

@app.post("/ask")
def ask_question(req: QuestionRequest):
    start_time = time.time()
    try:
        # Menjalankan logika bisnis melalui service layer
        result = rag_service.ask(req.question)
        
        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start_time, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add")
def add_document(req: DocumentRequest):
    try:
        # Menghasilkan embedding lalu menyimpannya ke repository
        emb = rag_service.fake_embed(req.text)
        doc_id = doc_store.get_count() 
        
        doc_store.add_document(text=req.text, vector=emb, doc_id=doc_id)
        
        return {"id": doc_id, "status": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
def get_status():
    return {
        "qdrant_ready": doc_store.using_qdrant,
        "total_documents": doc_store.get_count(),
        "service_initialized": rag_service is not None
    }