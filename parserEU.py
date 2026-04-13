import os
import re
import chromadb
import shutil
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
SOURCE_FOLDER = "to_parse"
DB_PATH = "./legal_db"
COLLECTION_NAME = "laws"
MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'


def process_file(file_path):
    print(f"Parsing file: {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    file_articles = []
    containers = soup.find_all('div', class_='eli-subdivision', id=re.compile(r'^art_\d+'))
    if not containers:
        containers = soup.find_all('p', class_='title-article-norm')

    for container in containers:
        element_id = container.get('id', 'unknown')
        text = container.get_text(separator="\n", strip=True)
        doc_id = f"{os.path.basename(file_path)}_{element_id}"

        file_articles.append({
            "id": doc_id,
            "text": text,
            "metadata": {
                "source": os.path.basename(file_path),
                "article_id": element_id
            }
        })

    return file_articles


def rebuild_database():
    if not os.path.exists(SOURCE_FOLDER):
        os.makedirs(SOURCE_FOLDER)
        print(f"Created '{SOURCE_FOLDER}' folder. Put your HTML files there!")
        return

    all_data = []
    for file in os.listdir(SOURCE_FOLDER):
        if file.endswith(".html"):
            all_data.extend(process_file(os.path.join(SOURCE_FOLDER, file)))

    if not all_data:
        print("No data found to parse.")
        return
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    encoder = SentenceTransformer(MODEL_NAME)
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    collection = chroma_client.create_collection(name=COLLECTION_NAME)

    print(f"Vectorizing {len(all_data)} chunks from all documents...")
    collection.add(
        documents=[d['text'] for d in all_data],
        embeddings=encoder.encode([d['text'] for d in all_data], show_progress_bar=True).tolist(),
        metadatas=[d['metadata'] for d in all_data],
        ids=[d['id'] for d in all_data]
    )
    print(f"Success! Total items in database: {len(all_data)}")


if __name__ == "__main__":
    rebuild_database()