import os
import json
import zipfile
import json_repair
from docxtpl import DocxTemplate
from openai import OpenAI
from datetime import datetime
import chromadb
from sentence_transformers import SentenceTransformer
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
TEMPLATES_DIR = "tagged_templates"
DOWNLOADS_DIR = "downloads"
REGISTRY_FILE = "templates_registry.json"
TAGS_DB_FILE = "tags_db.json"
DB_PATH = "./legal_db"
ZIP_PATH = "./legal_db.zip"
PROMPTS = {
    "router": """
You are a Legal Document Dispatcher. Your goal is to identify the most suitable document template from the list below based on the user's request.
AVAILABLE TEMPLATES:
{docs_list}

INSTRUCTION:
Return ONLY a JSON object: {{"filename": "exact_name.docx"}}
If no suitable template is found, return: {{"filename": null}}
""",

    "ner_extractor": """
You are a Legal Data Extraction specialist. Your task is to extract entity information from the user's query into a structured JSON format.
DATE FORMAT: dd.mm.yyyy
REQUIRED SCHEMA:
{schema}
""",

    "consultant": """
You are LexGuard AI, a professional legal assistant specializing in EU Law and GDPR. 
Provide accurate, structured, and formal legal advice based on the provided context.

GUIDELINES:
1. CITATIONS: Always mention specific GDPR Articles or Recitals if they are present in the context.
2. LIMITATIONS: If the context doesn't contain the answer, use your general knowledge of EU Law but clearly state it is general information.
3. STRUCTURE: Use Markdown (bolding, bullet points) for clarity.
4. TONE: Professional, objective, and helpful.

GDPR DATABASE CONTEXT:
{context}
"""
}
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
collection = None
encoder = None

# Extract database if needed
if not os.path.exists(DB_PATH) and os.path.exists(ZIP_PATH):
    try:
        with zipfile.ZipFile(ZIP_PATH, 'r') as z:
            z.extractall(".")
    except Exception as e:
        print(f"⚠️ Zip extraction failed: {e}")
try:
    encoder = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    collection = chroma_client.get_collection(name="laws")
    print("✅ ChromaDB and Encoder initialized")
except Exception as e:
    print(f"⚠️ RAG initialization error: {e}")
try:
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
    with open(TAGS_DB_FILE, "r", encoding="utf-8") as f:
        tags_db = json.load(f)
    clean_tags_db = {k: v for k, v in tags_db.items() if not k.startswith("_")}
except Exception as e:
    print(f"⚠️ Config files loading error: {e}")
    registry, clean_tags_db = [], {}


async def select_best_template(user_query):
    """Identifies the best document template using LLM reasoning."""
    docs_list = "\n".join([f"- {item['filename']} ({item.get('description', '')})" for item in registry])

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": PROMPTS["router"].format(docs_list=docs_list)},
                {"role": "user", "content": user_query}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        result = json_repair.loads(response.choices[0].message.content)
        return result.get("filename")
    except Exception as e:
        print(f"⚠️ Router Error: {e}")
        return None


async def extract_data_from_chat(user_query, filename):
    """Extracts required data fields for the document."""
    schema = "\n".join([f"- {v['tag']}: {v['description']}" for k, v in clean_tags_db.items()])

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": PROMPTS["ner_extractor"].format(schema=schema)},
                {"role": "user", "content": user_query}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json_repair.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"⚠️ Extraction Error: {e}")
        return {}


async def consult_logic(user_text):
    """Core RAG consultation logic."""
    context = "No specific articles found in the database."

    # RAG: Retrieve context from ChromaDB
    if collection and encoder:
        try:
            vec = encoder.encode(user_text).tolist()
            res = collection.query(query_embeddings=[vec], n_results=3)
            if res['documents'] and res['documents'][0]:
                context = "\n---\n".join(res['documents'][0])
        except Exception as e:
            print(f"⚠️ Vector Search Error: {e}")

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": PROMPTS["consultant"].format(context=context)},
                {"role": "user", "content": f"User Question: {user_text}"}
            ],
            temperature=0.3
        )
        return {"type": "text", "content": response.choices[0].message.content}
    except Exception as e:
        return {"type": "text", "content": f"⚠️ Connection Error: {str(e)}"}


async def generate_doc_logic(user_text):
    """Handles the document generation pipeline (Currently in development)."""
    best_filename = await select_best_template(user_text)

    if not best_filename:
        fallback = await consult_logic(f"Draft a response for: {user_text}")
        fallback["content"] = "⚠️ **No matching template found.** Here is a manual draft:\n\n" + fallback["content"]
        return fallback

    template_path = os.path.join(TEMPLATES_DIR, best_filename)
    if not os.path.exists(template_path):
        return {"type": "text", "content": f"⚠️ Template file '{best_filename}' not found on server."}

    data = await extract_data_from_chat(user_text, best_filename)
    if "doc_date" not in data: data["doc_date"] = datetime.now().strftime("%d.%m.%Y")

    try:
        doc = DocxTemplate(template_path)
        doc.render(data)
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_name = f"LexGuard_{ts}_{best_filename}"
        out_path = os.path.join(DOWNLOADS_DIR, out_name)
        doc.save(out_path)

        return {
            "type": "file",
            "content": f"✅ Document successfully generated using template: **{best_filename}**",
            "file_url": out_path
        }
    except Exception as e:
        return {"type": "text", "content": f"⚠️ Generation error: {e}"}