from pathlib import Path

from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# folder path containing the HR policy documents
POLICY_DIR = Path("data/company_bronze/data/content/policies")

# Initialize the embedding model to convert text chunks into numerical vectors
print("Loading embedding model...")
embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# Set up the text splitter to break large documents into manageable pieces
splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150
)

# Initialize a persistent local Vector Database to store data across script runs
client = chromadb.PersistentClient(path="chroma_db")

# Delete old collection if it exists
try:
    client.delete_collection("hr_policies")
except Exception:
    pass

# Create a new vector database collection for the HR policies
collection = client.create_collection("hr_policies")

chunk_count = 0

for file in sorted(POLICY_DIR.glob("*_en.docx")):

    print(f"Indexing {file.name}")

    doc = Document(file)

    # Extract and merge all text paragraphs, ignoring blank lines
    text = "\n".join(
        p.text
        for p in doc.paragraphs
        if p.text.strip()
    )

    # Split the long document text into smaller, overlapping chunks
    chunks = splitter.split_text(text)

    # Convert all text chunks into numerical embeddings using the AI model
    embeddings = embedding_model.encode(chunks).tolist()

    # Save each chunk and its corresponding vector into the database
    for chunk, embedding in zip(chunks, embeddings):

        collection.add(
            ids=[f"chunk_{chunk_count}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "source": file.name,
                    "policy": file.stem.replace("_en", "")
                }
            ]
        )

        chunk_count += 1

print(f"\nDone! Indexed {chunk_count} chunks.")