import os
import uuid
from bs4 import BeautifulSoup
import chromadb
from sentence_transformers import SentenceTransformer

# --- Configuration ---
DB_PATH = "./legal_db"
COLLECTION_NAME = "laws"
MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'
INPUT_FOLDER = "./ingest_now"


def clean_html(html_content):
    """Remove tags and scripts, return clean text"""
    soup = BeautifulSoup(html_content, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    return soup.get_text(separator=' ', strip=True)


def chunk_text(text, chunk_size=800):
    """Split text into chunks for RAG"""
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def ingest_folder():
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"Folder {INPUT_FOLDER} created. Add HTML files there.")
        return

    print("Loading encoder...")
    encoder = SentenceTransformer(MODEL_NAME)

    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".html")]

    if not files:
        print("No new HTML files found.")
        return

    for filename in files:
        print(f"Ingesting: {filename}...")
        file_path = os.path.join(INPUT_FOLDER, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            raw_html = f.read()

        clean_txt = clean_html(raw_html)
        chunks = chunk_text(clean_txt)

        # Prepare data for ChromaDB
        ids = [str(uuid.uuid4()) for _ in chunks]
        embeddings = encoder.encode(chunks).tolist()
        metadatas = [{"source": filename} for _ in chunks]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )
        print(f"Successfully added {len(chunks)} chunks from {filename}")


if __name__ == "__main__":
    ingest_folder()