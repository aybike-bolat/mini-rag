"""
Mini RAG - Akilli Dokuman Soru-Cevap Sistemi
Streamlit tabanli kullanici arayuzu.

Calistirma: streamlit run app.py
"""
import os
import tempfile

import streamlit as st

import config
from rag.pdf_processor import process_pdf
from rag.vectorstore import add_chunks, list_indexed_sources, clear_all
from rag.qa_chain import answer_question

st.set_page_config(page_title="Akilli Dokuman Soru-Cevap Sistemi", page_icon="📄", layout="wide")

st.title("📄 Akilli Dokuman Soru-Cevap Sistemi (Mini RAG)")
st.caption("PDF yukleyin, dokumanlariniz hakkinda soru sorun. Sistem sadece yukledigi dokumanlara dayanarak cevap verir.")

# ---- Session state ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # [(soru, cevap, kaynaklar)]

# ---- Yan panel: PDF yukleme ----
with st.sidebar:
    st.header("📎 Dokuman Yonetimi")
    st.write(f"**Aktif LLM saglayici:** `{config.LLM_PROVIDER}`")

    uploaded_files = st.file_uploader(
        "PDF dosyalarini yukleyin", type=["pdf"], accept_multiple_files=True
    )

    if st.button("PDF'leri Isle ve Veritabanina Ekle", type="primary", disabled=not uploaded_files):
        with st.spinner("PDF'ler isleniyor: metin cikariliyor, parcalara ayriliyor, embedding olusturuluyor..."):
            toplam_chunk = 0
            for uf in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uf.getvalue())
                    tmp_path = tmp.name
                try:
                    chunks = process_pdf(tmp_path, source_name=uf.name)
                    eklenen = add_chunks(chunks)
                    toplam_chunk += eklenen
                    st.success(f"✅ {uf.name}: {eklenen} parca eklendi.")
                except Exception as e:
                    st.error(f"❌ {uf.name} islenirken hata: {e}")
                finally:
                    os.remove(tmp_path)
            st.info(f"Toplam {toplam_chunk} parca vektor veritabanina eklendi.")

    st.divider()
    st.subheader("Yuklu Dokumanlar")
    try:
        sources = list_indexed_sources()
        if sources:
            for s in sources:
                st.write(f"- {s}")
        else:
            st.write("_Henuz dokuman yuklenmedi._")
    except Exception as e:
        st.write(f"_Veritabani henuz bos ({e})_")

    st.divider()
    if st.button("🗑️ Tum Veritabanini Temizle"):
        clear_all()
        st.session_state.chat_history = []
        st.success("Veritabani temizlendi.")
        st.rerun()

# ---- Ana alan: sohbet ----
st.subheader("💬 Sohbet")

for soru, cevap, kaynaklar in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(soru)
    with st.chat_message("assistant"):
        st.write(cevap)
        if kaynaklar:
            with st.expander("📚 Kaynaklar"):
                for k in kaynaklar:
                    st.markdown(f"**{k.source}** - Sayfa {k.page}")
                    st.caption(k.snippet)

soru = st.chat_input("Dokumanlariniz hakkinda bir soru sorun...")

if soru:
    with st.chat_message("user"):
        st.write(soru)

    with st.chat_message("assistant"):
        with st.spinner("Cevap araniyor..."):
            try:
                sonuc = answer_question(soru)
                st.write(sonuc.answer)
                if sonuc.sources:
                    with st.expander("📚 Kaynaklar"):
                        for k in sonuc.sources:
                            st.markdown(f"**{k.source}** - Sayfa {k.page}")
                            st.caption(k.snippet)
                st.session_state.chat_history.append((soru, sonuc.answer, sonuc.sources))
            except Exception as e:
                st.error(f"Hata olustu: {e}")
