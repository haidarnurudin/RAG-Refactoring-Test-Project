import random
from langgraph.graph import StateGraph, END
from .repository import DocumentStore  # Mengimpor kelas dari Step 1

class RAGService:
    def __init__(self, doc_store: DocumentStore):
        """
        Dependency Injection: Kita memasukkan DocumentStore ke sini.
        Ini membuat RAGService mudah di-test tanpa harus mengubah kodenya.
        """
        self.doc_store = doc_store
        self.workflow = self._build_graph()

    def fake_embed(self, text: str):
        """Logika embedding tiruan yang dipindahkan ke dalam service."""
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(128)]

    def _build_graph(self):
        """Membangun alur kerja LangGraph dalam sebuah metode kelas (Encapsulation)."""
        graph = StateGraph(dict)

        # Node 1: Retrieval
        def retrieve_node(state):
            query = state["question"]
            emb = self.fake_embed(query)
            # Menggunakan method dari repository yang kita buat di Step 1
            results = self.doc_store.search_documents(query_vector=emb, query_text=query)
            state["context"] = results
            return state

        # Node 2: Answering
        def answer_node(state):
            ctx = state["context"]
            state["answer"] = f"I found this: '{ctx[0][:100]}...'" if ctx else "Sorry, I don't know."
            return state

        # Menyusun graf
        graph.add_node("retrieve", retrieve_node)
        graph.add_node("answer", answer_node)
        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "answer")
        graph.add_edge("answer", END)
        
        return graph.compile()

    def ask(self, question: str):
        """Metode publik untuk menjalankan alur RAG."""
        return self.workflow.invoke({"question": question})