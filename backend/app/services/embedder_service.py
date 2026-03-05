from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def generate_embeddings(texts):
    return model.encode(texts)