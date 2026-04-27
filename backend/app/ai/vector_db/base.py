from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStore(ABC):
    @abstractmethod
    def add_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, Any]]):
        """Adds vectors and their metadata to the store."""
        pass

    @abstractmethod
    def search(self, query_vector: List[float], k: int = 10) -> List[Dict[str, Any]]:
        """Searches for the nearest neighbors of a query vector."""
        pass

    @abstractmethod
    def save(self, path: str):
        """Persists the store to disk."""
        pass

    @abstractmethod
    def load(self, path: str):
        """Loads the store from disk."""
        pass
