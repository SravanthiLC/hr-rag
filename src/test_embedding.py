from sentence_transformers import SentenceTransformer

chunks = [
    "Employees are entitled to 20 days of annual leave.",
    "Remote work is allowed with manager approval.",
    "All employees must follow security policies."
]

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

embeddings = model.encode(chunks)

print("Embedding shape:", embeddings[0].shape)
print("\nFirst embedding vector (truncated):")
print(embeddings[0][:10])