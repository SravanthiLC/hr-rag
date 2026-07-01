from docx import Document

# text splitter that breaks down large text based on character counts
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Define the file path where the Word document is located
file_path = (
    "data/company_bronze/data/content/policies/leave_policy_en.docx"
)

doc = Document(file_path)

# Extract text: loop through all paragraphs, skip empty ones, and join them with newlines
text = "\n".join(
    p.text
    for p in doc.paragraphs
    if p.text.strip()
)

# Initialize the splitter: target 500 characters per chunk, with a 100-character overlap to maintain context between consecutive chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# Process the single large string and divide it into a list of smaller text chunks
chunks = splitter.split_text(text)

# Print the total number of text segments generated
print(f"Total chunks: {len(chunks)}")

# Loop through the list of chunks to print them out cleanly
for i, chunk in enumerate(chunks):
    print("\n" + "=" * 80)
    print(f"Chunk {i+1}")
    print("=" * 80)
    print(chunk)