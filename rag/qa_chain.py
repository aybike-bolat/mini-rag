"""
Retrieval-Augmented Generation (RAG) mantigini yurutur:
1) Soruya benzer parcalari vektor veritabanindan cek (retrieval)
2) Bu parcalari baglam (context) olarak LLM'e ver
3) LLM SADECE bu baglama dayanarak cevap uretsin, disariya cikmasin
"""
from dataclasses import dataclass
from typing import List

import config
from rag import vectorstore

SYSTEM_PROMPT = """Sen, kullanicinin yukledigi dokumanlara dayanarak soru cevaplayan bir asistansin.

KURALLAR:
- SADECE asagida sana verilen "BAGLAM" icindeki bilgileri kullanarak cevap ver.
- Eger cevap baglamda yoksa, kesinlikle uydurma. Bunun yerine acikca soyle:
  "Bu soru yuklenen dokumanlarin kapsami disindadir, dokumanlarda bu bilgi bulunmuyor."
- Cevabini Turkce, net ve anlasilir sekilde ver.
- Mumkunse hangi kaynaktan/sayfadan geldigini belirt.
"""

USER_PROMPT_TEMPLATE = """BAGLAM:
{context}

SORU:
{question}

Yukaridaki BAGLAM'a dayanarak SORU'yu cevapla. Baglamda yoksa bunu acikca belirt.
"""


@dataclass
class Source:
    source: str
    page: int
    snippet: str


@dataclass
class QAResult:
    answer: str
    sources: List[Source]


def _get_llm():
    if config.LLM_PROVIDER == "ollama":
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(model=config.OLLAMA_MODEL, base_url=config.OLLAMA_BASE_URL, temperature=0)
    else:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=config.OPENAI_MODEL, api_key=config.OPENAI_API_KEY, temperature=0)


def answer_question(question: str) -> QAResult:
    """Kullanicinin sorusunu RAG akisiyla cevaplar."""
    docs = vectorstore.similarity_search(question)

    if not docs:
        return QAResult(
            answer="Henuz hicbir dokuman yuklenmemis ya da ilgili bilgi bulunamadi. "
                   "Lutfen once bir PDF yukleyin.",
            sources=[],
        )

    context = "\n\n---\n\n".join(
        f"[Kaynak: {d.metadata.get('source')}, Sayfa: {d.metadata.get('page')}]\n{d.page_content}"
        for d in docs
    )

    llm = _get_llm()
    messages = [
        ("system", SYSTEM_PROMPT),
        ("user", USER_PROMPT_TEMPLATE.format(context=context, question=question)),
    ]
    response = llm.invoke(messages)

    sources = [
        Source(
            source=d.metadata.get("source", "bilinmiyor"),
            page=d.metadata.get("page", -1),
            snippet=d.page_content[:200].replace("\n", " ") + "...",
        )
        for d in docs
    ]

    return QAResult(answer=response.content, sources=sources)
