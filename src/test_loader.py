from pathlib import Path
from docx import Document

policy_dir = Path(
    "data/company_bronze/data/content/policies"
)

# Loop through all files in the directory that end with "_en.docx" (English policies)
for file in policy_dir.glob("*_en.docx"):
    doc = Document(file)
    
    # Extract text: loop through paragraphs, skip empty ones, and join with newlines
    text = "\n".join(
        p.text
        for p in doc.paragraphs
        if p.text.strip()
    )

    print("=" * 80)

    # Print the specific file name currently being read
    print(file.name)

    print("=" * 80)

    # Print only the first 500 characters of the extracted text as a preview
    print(text[:500])
    print()
