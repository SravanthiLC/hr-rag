from pathlib import Path
from docx import Document

policy_dir = Path(
    "data/company_bronze/data/content/policies"
)

for file in policy_dir.glob("*_en.docx"):
    doc = Document(file)

    text = "\n".join(
        p.text
        for p in doc.paragraphs
        if p.text.strip()
    )

    print("=" * 80)
    print(file.name)
    print("=" * 80)
    print(text[:500])
    print()
