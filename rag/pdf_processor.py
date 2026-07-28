"""
PDF dosyalarindan metin cikarma ve parcalara (chunk) ayirma islemlerini yapar.
PyMuPDF (fitz) kullanarak sayfa numarasi bilgisini korur; boylece
cevap uretilirken "kaynak sayfa" bilgisi gosterilebilir.
"""
from dataclasses import dataclass
from typing import List
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config


@dataclass
class Chunk:
    text: str
    source: str      # dosya adi
    page: int         # sayfa numarasi (1'den baslar)
    chunk_id: str     # benzersiz id


def extract_text_by_page(pdf_path: str) -> List[dict]:
    """PDF'i sayfa sayfa okuyup metinlerini dondurur."""
    pages = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc):
            text = page.get_text("text")
            if text.strip():
                pages.append({"page": i + 1, "text": text})
    return pages


def split_into_chunks(pages: List[dict], source_name: str) -> List[Chunk]:
    """Sayfa metinlerini kucuk parcalara ayirir, sayfa bilgisini korur."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: List[Chunk] = []
    for page_data in pages:
        page_num = page_data["page"]
        page_text = page_data["text"]
        pieces = splitter.split_text(page_text)
        for idx, piece in enumerate(pieces):
            chunk_id = f"{source_name}_p{page_num}_c{idx}"
            chunks.append(
                Chunk(text=piece, source=source_name, page=page_num, chunk_id=chunk_id)
            )
    return chunks


def process_pdf(pdf_path: str, source_name: str) -> List[Chunk]:
    """Tek bir PDF dosyasini uctan uca isler: metin cikar + chunk'la."""
    pages = extract_text_by_page(pdf_path)
    if not pages:
        raise ValueError(
            f"'{source_name}' dosyasindan metin cikarilamadi. "
            "Dosya taranmis (goruntu) bir PDF olabilir; OCR destegi bu projede yoktur."
        )
    return split_into_chunks(pages, source_name)
