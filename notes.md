# Implementation Notes

### Main Design Decisions
I refactored the original monolithic `main.py` into a modular layered architecture to satisfy the **Separation of Concerns** principle. The logic is now divided into:
- **Repository Layer (`repository.py`)**: Handles data persistence and Qdrant/In-memory logic.
- **Service Layer (`services.py`)**: Manages the LangGraph workflow and embedding logic.
- **API Layer (`main.py`)**: Handles HTTP requests and dependency orchestration.
- **Models (`models.py`)**: Defines Pydantic schemas for data validation.

### Trade-offs Considered
**1. Memory vs. Availability (Dual-Storage Strategy)**
I implemented a dual-storage approach where data is kept in an in-memory list (`_docs_memory`) as a fallback, even when Qdrant is active. 
- **The Trade-off:** This slightly increases RAM usage. However, for this scale, 1,000 documents only consume approximately 2-5 MB of RAM, which is negligible for modern servers.
- **The Benefit:** It provides a robust failover mechanism. If the Qdrant connection is lost, the system maintains high availability by serving requests from memory, preventing service downtime.

**2. Latency vs. Consistency**
By using an in-memory fallback, retrieval latency is extremely low (sub-millisecond). While Qdrant provides advanced vector search, having a local cache-like structure ensures that the system is responsive even under high-load scenarios or network fluctuations.

**3. Scalability Considerations**
The current design is optimized for Small-to-Medium Enterprises (SME) or prototype scales. If the dataset grows to millions of records, the in-memory fallback can be easily disabled or replaced with a Redis-based cache by modifying only the `Repository` layer, thanks to the modular "Separation of Concerns" architecture.

### Maintainability Improvements
This version significantly improves maintainability through **Explicit Dependency Injection**. By passing the `DocumentStore` instance into the `RAGService` constructor, the components are decoupled. This makes it easy to swap the embedding model or the database provider in the future, and allows for straightforward unit testing by injecting mock objects.