# LexGuard EU ⚖️🤖

**Efficiency-driven RAG engine for GDPR Compliance.**

LexGuard EU is a modular assistant designed to navigate the complexity of European legal frameworks. Instead of relying on a model's "memory", it uses a specialized RAG (Retrieval-Augmented Generation) pipeline to ground every answer in official law.

---

### 🚀 Key Principles

**Verifiable Accuracy**
The system performs semantic searches across all 99 Articles of the GDPR using `ChromaDB` and multilingual embeddings. No guessing, just citations.

**Extreme Cost Efficiency**
Engineered for production. While legacy systems cost dollars per query, LexGuard processed **70,000 tokens for just $0.02** during stress tests.

**Architectural Flexibility**
The "LLM Brain" is swappable. Switch between **DeepSeek-R1**, **Qwen-2.5**, or local **Llama-3** by modifying only 5 lines of code.

---

### 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Logic** | Python 3.10+ / OpenAI-compatible API |
| **Vector DB** | ChromaDB (Persistent storage) |
| **Embeddings** | paraphrase-multilingual-mpnet-base-v2 |
| **Interface** | Gradio (Clean Dark Mode) |

---

### 📂 Project Structure

* `app.py` — The UI and orchestration layer.
* `api.py` — Core RAG logic and LLM management.
* `adderparser.py` — Tool for real-time document ingestion into the database.
* `parserEU.py` — Initial parser for the GDPR framework.
* `requirements.txt` — List of dependencies.
* `.env.example` — Configuration template for API keys.

---

### ⚙️ Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
