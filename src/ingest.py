from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from utils import load_policy, chunk_text

# Folder containing the HR policy documents
POLICY_DIR = Path("data/company_bronze/data/content/policies")

# Name of the ChromaDB collection
COLLECTION_NAME = "hr_policies"

def main():
    print("Loading embedding model...")
    embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    # Create (or connect to) a persistent local ChromaDB instance
    client = chromadb.PersistentClient(path="chroma_db")

    # Recreate the collection every time we ingest
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    chunk_id = 0

    # Index only the English policy documents
    for file in sorted(POLICY_DIR.glob("*_en.docx")):

        print(f"Indexing {file.name}")

        # Read the document
        text = load_policy(file)

        # Split into overlapping chunks
        chunks = chunk_text(text)

        # Generate embeddings for all chunks
        embeddings = embedding_model.encode(chunks).tolist()

        # Store chunks, embeddings and metadata in ChromaDB
        for chunk, embedding in zip(chunks, embeddings):

            collection.add(
                ids=[f"chunk_{chunk_id}"],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[
                    {
                        "source": file.name,
                        "policy": file.stem.replace("_en", "")
                    }
                ]
            )

            chunk_id += 1

    print(f"\nDone! Indexed {chunk_id} chunks.")


if __name__ == "__main__":
    main()