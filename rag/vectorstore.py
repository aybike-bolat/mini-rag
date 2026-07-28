"""
ChromaDB uzerinde embedding olusturma, kayit ve benzerlik aramasi islemlerini yonetir.
"""
from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document

import config
from rag.pdf_processor import Chunk


def get_embedding_function():
    """Secilen LLM saglayicisina gore embedding fonksiyonunu dondurur."""
    if config.LLM_PROVIDER == "ollama":
        from langchain_community.embeddings import OllamaEmbeddings
        return OllamaEmbeddings(
            model=config.OLLAMA_EMBED_MODEL, base_url=config.OLLAMA_BASE_URL
        )
    else:
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model=config.OPENAI_EMBED_MODEL, api_key=config.OPENAI_API_KEY
        )


def get_vectorstore() -> Chroma:
    """Diskteki (persist edilmis) Chroma veritabanini acar / olusturur."""
    return Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        persist_directory=config.CHROMA_DIR,
    )


def add_chunks(chunks: List[Chunk]) -> int:
    """Chunk listesini embedding'e cevirip veritabanina ekler."""
    if not chunks:
        return 0

    documents = [
        Document(
            page_content=c.text,
            metadata={"source": c.source, "page": c.page, "chunk_id": c.chunk_id},
        )
        for c in chunks
    ]
    ids = [c.chunk_id for c in chunks]

    store = get_vectorstore()
    store.add_documents(documents=documents, ids=ids)
    return len(documents)


def similarity_search(query: str, k: int = None):
    """Soruya en benzer k adet parcayi getirir."""
    store = get_vectorstore()
    k = k or config.TOP_K
    return store.similarity_search(query, k=k)


def list_indexed_sources() -> List[str]:
    """Veritabanina eklenmis benzersiz dosya adlarini dondurur."""
    store = get_vectorstore()
    data = store.get()
    sources = {meta.get("source") for meta in data.get("metadatas", []) if meta}
    return sorted(sources)


def clear_all():
    """Veritabanindaki tum kayitlari siler (yeniden basla)."""
    store = get_vectorstore()
    data = store.get()
    ids = data.get("ids", [])
    if ids:
        store.delete(ids=ids)
