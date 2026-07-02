import chromadb
import ollama

from sentence_transformers import SentenceTransformer

# Load embedding model

print("Loading embedding model...")

embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# Connect to ChromaDB

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("hr_policies")

print("Connected to vector database.")

# Interactive loop

while True:

    question = input("\nAsk a question (or type 'exit'): ")

    if question.lower() == "exit":
        break

    # Embed question
    query_embedding = embedding_model.encode([question]).tolist()

    # Retrieve
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )

    retrieved_chunks = results["documents"][0]

    retrieved_metadata = results["metadatas"][0]

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
        You are an HR policy assistant.

        Use ONLY the information provided in the context.

        If the context contains enough information to answer the question, answer it naturally.

        If the context does NOT contain enough information, respond ONLY with:

        "I could not find that information in the provided HR policies."

        Do not use outside knowledge.
        Do not guess.
        Do not mention what is or isn't in the context.
        Do not add disclaimers.

        Context:
        ----------------
        {context}
        ----------------

        Question:
        {question}
        """

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

    # Remove duplicate source names while preserving order
    seen = set()
    for metadata in retrieved_metadata:
        source = metadata["source"]
        if source not in seen:
            print(f"- {source}")
            seen.add(source)