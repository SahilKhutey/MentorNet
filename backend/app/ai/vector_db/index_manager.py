from app.ai.vector_db.adapters.faiss_adapter import FAISSAdapter
import os

# Configuration
DIMENSION = 384 # Default for many SentenceTransformers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "mentornet_vectors")

# Singleton instance using the adapter
faiss_store = FAISSAdapter(dimension=DIMENSION)
faiss_store._save_path = DATA_PATH # Set path for auto-save

# Load existing index if it exists
if os.path.exists(f"{DATA_PATH}.index"):
    faiss_store.load(DATA_PATH)
