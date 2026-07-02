from docx import Document
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import ollama

# Load document

file_path = "data/company_bronze/data/content/policies/leave_policy_en.docx"

doc = Document(file_path)

text = "\n".join(
    p.text
    for p in doc.paragraphs
    if p.text.strip()
)

# Chunk document

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_text(text)

print(f"Created {len(chunks)} chunks")

# Load embedding model

embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

embeddings = embedding_model.encode(chunks).tolist()

# Create Chroma collection

client = chromadb.Client()

collection = client.create_collection("leave_policy")

for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
    collection.add(
        ids=[f"chunk_{i}"],
        documents=[chunk],
        embeddings=[embedding],
    )

# User Question

question = input("\nAsk a question: ")

query_embedding = embedding_model.encode([question]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3,
)

retrieved_chunks = results["documents"][0]

context = "\n\n".join(retrieved_chunks)

# Prompt

prompt = f"""
You are an HR policy assistant.

Answer ONLY using the information provided in the context below.

If the answer is not present in the context, reply exactly:

I could not find that information in the policy.

Keep your answer concise.

Context:
--------------------
{context}
--------------------

Question:
{question}
"""

# Send to Qwen

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# Output

print("\n" + "=" * 80)
print("ANSWER")
print("=" * 80)
print(response["message"]["content"])

print("\n" + "=" * 80)
print("RETRIEVED CHUNKS")
print("=" * 80)

for i, chunk in enumerate(retrieved_chunks, start=1):
    print(f"\nChunk {i}\n")
    print(chunk)