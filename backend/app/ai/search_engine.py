from app.ai.embedding import generate_embedding
from app.ai.vector_db.index_manager import faiss_store

def semantic_search(query: str, k: int = 10):
    query_embedding = generate_embedding(query)

    results = faiss_store.search(query_embedding, k=k)

    return results
