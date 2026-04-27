import faiss
import numpy as np
import pickle
from typing import List, Dict, Any
from app.ai.vector_db.base import VectorStore

class FAISSAdapter(VectorStore):
    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)
        self.id_map = {} # Maps index ID to metadata

    def add_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, Any]]):
        v_np = np.array(vectors).astype('float32')
        start_id = self.index.ntotal
        self.index.add(v_np)
        
        for i, meta in enumerate(metadata):
            self.id_map[start_id + i] = meta
        
        # In a real system, we might want to defer saving or handle it via a background task.
        # But for this implementation, we ensure locality of persistence.
        if hasattr(self, '_save_path') and self._save_path:
            self.save(self._save_path)

    def add(self, profile_id: int, embedding: List[float]):
        """Backward compatibility for the old FaissStore interface."""
        self.add_vectors([embedding], [{"profile_id": profile_id}])

    def search(self, query_vector: List[float], k: int = 10) -> List[Dict[str, Any]]:
        v_np = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(v_np, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx in self.id_map:
                res = self.id_map[idx].copy()
                res["score"] = float(dist)
                results.append(res)
        return results

    def save(self, path: str):
        self._save_path = path # Remember path for auto-save
        faiss.write_index(self.index, f"{path}.index")
        with open(f"{path}.meta", 'wb') as f:
            pickle.dump(self.id_map, f)

    def load(self, path: str):
        self.index = faiss.read_index(f"{path}.index")
        with open(f"{path}.meta", 'rb') as f:
            self.id_map = pickle.load(f)
