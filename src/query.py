import chromadb
import ollama
from sentence_transformers import SentenceTransformer

from prompts import PROMPT_TEMPLATE

# Name of the ChromaDB collection
COLLECTION_NAME = "hr_policies"


def main():
    print("Loading embedding model...")

    embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    # Connect to the existing ChromaDB
    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_collection(COLLECTION_NAME)

    print("Connected to vector database.")

    while True:

        question = input("\nAsk a question (or type 'exit'): ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Convert the user's question into an embedding
        query_embedding = embedding_model.encode([question]).tolist()

        # Retrieve the most relevant chunks
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=5
        )

        retrieved_chunks = results["documents"][0]
        retrieved_metadata = results["metadatas"][0]

        # Uncomment this block if you want to inspect retrieval quality
        """
        print("\nRetrieved Chunks:\n")

        for i, chunk in enumerate(retrieved_chunks, start=1):
            print(f"\n----- Chunk {i} -----\n")
            print(chunk)
        """

        context = "\n\n".join(retrieved_chunks)

        # Build the prompt
        prompt = PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )

        # Generate answer using Qwen
        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        print("\n" + "=" * 80)
        print("ANSWER")
        print("=" * 80)
        print(response["message"]["content"])

        print("\nSources:")

        # Print unique source documents
        seen = set()

        for metadata in retrieved_metadata:

            source = metadata["source"]

            if source not in seen:
                print(f"- {source}")
                seen.add(source)


if __name__ == "__main__":
    main()