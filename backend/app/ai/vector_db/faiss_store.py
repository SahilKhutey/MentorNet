import faiss
import numpy as np
import os
import pickle

# Ensure data directory is in the backend root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "faiss_meta.pkl")

import threading

class FaissStore:
    def __init__(self, dim=384):
        self.dim = dim
        self.last_loaded = 0
        self._lock = threading.Lock()
        
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        self._load_if_needed()

    def _load_if_needed(self):
        with self._lock:
            if not os.path.exists(INDEX_PATH):
                if not hasattr(self, 'index'):
                    self.index = faiss.IndexFlatL2(self.dim)
                    self.id_map = []
                return

            mtime = os.path.getmtime(INDEX_PATH)
            if mtime > self.last_loaded:
                try:
                    print(f"Reloading FAISS index (disk version changed)...")
                    self.index = faiss.read_index(INDEX_PATH)
                    with open(META_PATH, "rb") as f:
                        self.id_map = pickle.load(f)
                    self.last_loaded = mtime
                except Exception as e:
                    print(f"Error loading FAISS index: {e}")
                    # Fallback initialization
                    if not hasattr(self, 'index'):
                        self.index = faiss.IndexFlatL2(self.dim)
                        self.id_map = []

    def save(self):
        # Already inside lock when called from add()
        try:
            faiss.write_index(self.index, INDEX_PATH)
            with open(META_PATH, "wb") as f:
                pickle.dump(self.id_map, f)
            self.last_loaded = os.path.getmtime(INDEX_PATH)
        except Exception as e:
            print(f"Failed to save FAISS index: {e}")

    def add(self, profile_id: int, embedding):
        with self._lock:
            self._load_if_needed()
            vector = np.array([embedding]).astype("float32")
            self.index.add(vector)
            self.id_map.append(profile_id)
            self.save()

    def search(self, embedding, k=10):
        try:
            self._load_if_needed()
            vector = np.array([embedding]).astype("float32")
            distances, indices = self.index.search(vector, k)
            
            results = []
            for idx, dist in zip(indices[0], distances[0]):
                if idx != -1 and idx < len(self.id_map):
                    results.append({
                        "profile_id": self.id_map[idx],
                        "score": float(dist)
                    })
            return results
        except Exception as e:
            print(f"FAISS Search Failure: {e}")
            return [] # Empty list triggers fallback in service layer
