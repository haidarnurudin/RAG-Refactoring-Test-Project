from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

class DocumentStore:
    def __init__(self, collection_name="demo_collection"):
        """
        Inisialisasi penyimpanan dokumen. 
        Menggunakan Qdrant jika tersedia, jika tidak akan fallback ke memori.
        """
        self.collection_name = collection_name
        self._docs_memory = []  # Private variable (Encapsulation)
        self.client = None
        self.using_qdrant = False
        
        self._setup_qdrant()

    def _setup_qdrant(self):
        """Mencoba koneksi ke Qdrant dan memperbaiki DeprecationWarning."""
        try:
            self.client = QdrantClient("http://localhost:6333")
            # Memperbaiki peringatan kode usang: Cek dulu sebelum buat
            if not self.client.collection_exists(self.collection_name):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=128, distance=Distance.COSINE)
                )
            self.using_qdrant = True
        except Exception:
            print("⚠️  Qdrant not available. Falling back to in-memory list.")
            self.using_qdrant = False

    def add_document(self, text: str, vector: list, doc_id: int):
        """Menyimpan dokumen ke storage yang tersedia."""
        if self.using_qdrant:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[PointStruct(id=doc_id, vector=vector, payload={"text": text})]
            )
        
        # Selalu simpan di memori sebagai backup sederhana
        self._docs_memory.append(text)

    def search_documents(self, query_vector: list, query_text: str, limit: int = 2):
        """Mencari dokumen berdasarkan vektor (Qdrant) atau teks (Memory)."""
        if self.using_qdrant:
            hits = self.client.search(
                collection_name=self.collection_name, 
                query_vector=query_vector, 
                limit=limit
            )
            return [hit.payload["text"] for hit in hits]
        
        # Fallback: Pencarian teks sederhana di memori
        results = [doc for doc in self._docs_memory if query_text.lower() in doc.lower()]
        if not results and self._docs_memory:
            return [self._docs_memory[0]]
        return results[:limit]

    def get_count(self):
        """Mengembalikan jumlah dokumen di memori."""
        return len(self._docs_memory)