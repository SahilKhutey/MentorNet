from sentence_transformers import SentenceTransformer
print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded!")
embedding = model.encode("Hello world")
print(f"Embedding shape: {embedding.shape}")
