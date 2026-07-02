from pathlib import Path
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_policy(file_path: Path) -> str:
    """Read a DOCX policy into a single string."""

    doc = Document(file_path)

    return "\n".join(
        p.text
        for p in doc.paragraphs
        if p.text.strip()
    )


def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=150
    )

    return splitter.split_text(text)