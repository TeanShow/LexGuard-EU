\# LexGuard EU ⚖️🤖

\*\*High-Efficiency GDPR Compliance Assistant \& RAG-Powered Legal Engine\*\*



LexGuard EU is a modular AI-powered assistant designed to navigate complex legal frameworks like the GDPR. Unlike generic LLM wrappers, LexGuard uses a specialized RAG (Retrieval-Augmented Generation) pipeline to provide verifiable, context-aware legal analysis with extreme cost efficiency.



\---



\## 🚀 Key Features



\* \*\*Verifiable RAG Engine:\*\* Utilizes `ChromaDB` and `paraphrase-multilingual-mpnet-base-v2` embeddings to perform semantic searches across all 99 Articles of the GDPR.

\* \*\*Model-Agnostic Architecture:\*\* Swappable "LLM Brains". Easily switch between \*\*DeepSeek-R1\*\*, \*\*Qwen-2.5-Audio\*\*, or local \*\*Llama-3\*\* with just two lines of code.

\* \*\*Dynamic Document Ingestion:\*\* Includes a `live\_parser.py` utility to instantly expand the knowledge base with new HTML/Legal documents.

\* \*\*Cost-Optimized:\*\* Engineered for production. Performance metrics show \~70k tokens processed for as little as \*\*$0.02 USD\*\*.

\* \*\*Security First:\*\* Strictly follows environment variable standards for API key management; zero-leakage design.



\---



\## 🛠 Tech Stack



\* \*\*Language:\*\* Python 3.10+

\* \*\*LLM Core:\*\* DeepSeek-R1 / Qwen-2.5 (via OpenAI-compatible API)

\* \*\*Vector Database:\*\* ChromaDB (Persistent local storage)

\* \*\*Frontend:\*\* Gradio (Modern Dark Theme UI)

\* \*\*Document Processing:\*\* BeautifulSoup4 \& DocxTemplate (for automated document generation)



\---



\## 📊 The "2-Cent" Benchmark



One of the core objectives of this project is to prove that high-tier legal AI doesn't require "Enterprise" budgets. 



| Metric | LexGuard (DeepSeek RAG) | Standard SOTA (Claude Opus) |

| :--- | :--- | :--- |

| \*\*Input Cost (1M Tokens)\*\* | \~$0.27 | \~$15.00 - $18.00 |

| \*\*Accuracy\*\* | High (Context-Anchored) | Variable (Hallucination risk) |

| \*\*Scalability\*\* | High (Pay-as-you-go) | Low (Fixed/High subscriptions) |



\---



\## ⚙️ Quick Start



\### 1. Clone \& Install

```bash

git clone \[https://github.com/your-username/lexguard-eu.git](https://github.com/your-username/lexguard-eu.git)

cd lexguard-eu

pip install -r requirements.txt

