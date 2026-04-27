import sys
import os
import time
import random
import numpy as np

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.ai.vector_db.index_manager import faiss_store

def run_stress_test(num_profiles=1000):
    print(f"--- Starting VectorStore Stress Test ({num_profiles} profiles) ---")
    
    # 1. Generate mock data
    embeddings = [np.random.rand(384).tolist() for _ in range(num_profiles)]
    metadatas = [{"profile_id": i, "name": f"User {i}"} for i in range(num_profiles)]
    
    # 2. Measure insertion time
    start_time = time.time()
    faiss_store.add_vectors(embeddings, metadatas)
    insert_time = time.time() - start_time
    print(f"Insertion Time: {insert_time:.4f}s ({insert_time/num_profiles:.6f}s per vector)")
    
    # 3. Measure search time (100 searches)
    num_searches = 100
    search_queries = [np.random.rand(384).tolist() for _ in range(num_searches)]
    
    start_time = time.time()
    for q in search_queries:
        faiss_store.search(q, k=10)
    search_time = time.time() - start_time
    print(f"Search Time (100 queries): {search_time:.4f}s ({search_time/num_searches:.6f}s per query)")
    
    # 4. Verify persistence
    faiss_store.save("stress_test_backup")
    print(f"Persistence check: Saved to stress_test_backup.index")
    
    print("--- Stress Test Complete ---")

if __name__ == "__main__":
    run_stress_test()
