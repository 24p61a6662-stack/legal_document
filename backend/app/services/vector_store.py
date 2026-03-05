import chromadb
from app.config import CHROMA_DB_PATH

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection("contracts")

def add_to_vectorstore(texts, embeddings, metadata):
    for i, text in enumerate(texts):
        collection.add(
            documents=[text],
            embeddings=[embeddings[i]],
            metadatas=[metadata[i]],
            ids=[f"id_{i}"]
        )