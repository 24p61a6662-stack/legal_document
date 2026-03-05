from app.services.vector_store import collection
from app.config import TOP_K

def retrieve(query_embedding):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )