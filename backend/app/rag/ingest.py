import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ✅ Correct absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "chroma_db")


def load_documents():
    documents = []

    if not os.path.exists(DATA_PATH):
        print(f"❌ Data folder not found at {DATA_PATH}")
        return documents

    for file in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file)

        if file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())

        elif file.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())

    return documents


def main():
    print("Loading documents...")
    documents = load_documents()

    if not documents:
        print("❌ No documents found in data folder.")
        return

    print("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)

    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Creating vector database...")
    db = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory=DB_PATH
    )

    db.persist()
    print("✅ Ingestion Complete!")


if __name__ == "__main__":
    main()