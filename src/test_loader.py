from docx import Document

file_path = "data/company_bronze/data/content/policies/leave_policy_en.docx"

doc = Document(file_path)

for para in doc.paragraphs[:10]:
    print(para.text)

