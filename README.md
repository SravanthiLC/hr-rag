# HR Policy RAG Assistant

A lightweight Retrieval-Augmented Generation (RAG) application that answers HR policy questions using local AI models.

The project indexes HR policy documents into a vector database, retrieves the most relevant policy sections for a user query, and generates grounded answers using a local Large Language Model (LLM).

The entire pipeline runs locally using free and open-source tools.

---

## Features

- Loads HR policy documents from Microsoft Word (`.docx`) files
- Splits documents into overlapping text chunks
- Generates semantic embeddings using **BAAI/bge-small-en-v1.5**
- Stores embeddings in **ChromaDB**
- Retrieves relevant policy sections using semantic search
- Generates answers using **Qwen2.5** running locally with **Ollama**
- Displays the source document used to answer the question

---

## Tech Stack

| Component       | Tool                                     |
| --------------- | ---------------------------------------- |
| Language        | Python                                   |
| Document Loader | python-docx                              |
| Text Chunking   | LangChain RecursiveCharacterTextSplitter |
| Embeddings      | BAAI/bge-small-en-v1.5                   |
| Vector Database | ChromaDB                                 |
| LLM             | Qwen2.5 (Ollama)                         |

---

## Project Structure

```
hr-rag/
│
├── data/
│   └── company_bronze/
│
├── src/
│   ├── ingest.py
│   ├── query.py
│   ├── prompts.py
│   └── utils.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Architecture

```
                HR Policy Documents (.docx)
                           │
                           ▼
                    Document Loading
                           │
                           ▼
                      Text Chunking
                           │
                           ▼
                  Embedding Generation
              (BAAI/bge-small-en-v1.5)
                           │
                           ▼
                       ChromaDB
                           │
                           ▼
                 Semantic Retrieval
                           │
                           ▼
               Prompt Construction
                           │
                           ▼
             Qwen2.5 (via Ollama)
                           │
                           ▼
                  Grounded Response
```

---

## Setup

Clone the repository

```bash
git clone https://github.com/SravanthiLC/hr-rag.git
cd hr-rag
```

Create a virtual environment

```bash
python -m venv v1
source v1/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Download the Ollama model

```bash
ollama pull qwen2.5:3b
```

---

## Build the Vector Database

```bash
python src/ingest.py
```

This reads all English HR policy documents, chunks them, generates embeddings, and stores them in ChromaDB.

---

## Run the Application

```bash
python src/query.py
```

Example:

```
Ask a question:

Can I work remotely?
```

Output:

```
Employees whose roles do not require a physical presence may be eligible for remote work...

Sources:
- remote_work_policy_en.docx
```

---

## Dataset

This project uses the **HR Corporate Data (Bilingual EN/PL, Bronze Layer)** dataset from Kaggle.

For this implementation, only the English HR policy documents (`.docx`) are indexed.

---

## Future Improvements

- Support PDF, CSV, email, and chat documents
- Hybrid retrieval (keyword + semantic search)
- Retrieval evaluation metrics
- Web interface (Streamlit or FastAPI)
- Conversation memory
- Metadata filtering
- Reranking retrieved documents

---

