from pydantic import BaseModel

class QuestionRequest(BaseModel):
    """Skema untuk request pertanyaan dari user."""
    question: str

class DocumentRequest(BaseModel):
    """Skema untuk request penambahan dokumen baru."""
    text: str