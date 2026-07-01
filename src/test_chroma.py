from docx import Document
from sentence_transformers import SentenceTransformer
import chromadb

# 1. Load document
file_path = "data/company_bronze/data/content/policies/leave_policy_en.docx"

doc = Document(file_path)

text = "\n".join(
    p.text for p in doc.paragraphs if p.text.strip()
)

chunks = [text[i:i+500] for i in range(0, len(text), 400)]

# 2. Embedding model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# 3. Chroma DB (in-memory first)
client = chromadb.Client()

collection = client.create_collection(name="hr_policies")

# 4. Add chunks + embeddings
embeddings = model.encode(chunks).tolist()

for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk],
        embeddings=[embeddings[i]],
        ids=[f"chunk_{i}"]
    )

# 5. Query
# query = "How many days of leave do employees get?"
query = "Can I carry forward unused vacation days?"

query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

print("\nTOP MATCHES:\n")

for doc in results["documents"][0]:
    print(doc)
    print("-" * 80)