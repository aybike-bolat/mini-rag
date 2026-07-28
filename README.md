# Akıllı Doküman Soru-Cevap Sistemi (Mini RAG)

Kullanıcının yüklediği PDF dokümanlara dayanarak soru cevaplayan bir **RAG (Retrieval-Augmented Generation)** uygulamasıdır.

Sistem yalnızca yüklenen dokümanlardan cevap üretir; kaynak dosya ve sayfa bilgisini gösterir. Doküman kapsamı dışındaki sorularda uyarı verir.

Demo ve testler **Ollama** (yerel LLM) ile yapılmıştır. İstenirse OpenAI da kullanılabilir.

## Mimari Akış

```
PDF Yükle → Metin Çıkar (PyMuPDF) → Parçala (Chunk) → Embedding Üret
        → ChromaDB'ye Kaydet → Soru Sor → Benzer Parçaları Bul
        → LLM'e Bağlam Olarak Ver → Kaynak Sayfa ile Cevap Üret
```

## Klasör Yapısı

```
mini-rag/
├── app.py                 # Streamlit arayüzü (giriş noktası)
├── config.py              # Ayarlar (.env okur)
├── requirements.txt       # Python bağımlılıkları
├── .env.example           # Ortam değişkeni şablonu (gerçek anahtar yok)
├── .gitignore
├── calistir.bat           # Windows: tek tıkla kurulum + çalıştırma
├── rag/
│   ├── __init__.py        # Python paketi
│   ├── pdf_processor.py   # PDF → metin → chunk
│   ├── vectorstore.py     # ChromaDB embedding / kayıt / arama
│   └── qa_chain.py        # RAG prompt + LLM cevap üretimi
├── data/                  # Türkçe örnek PDF'ler + README
├── reports/
│   ├── teknik_rapor.docx  # Teknik rapor
│   └── sunum.pptx         # Proje sunumu
├── test_senaryolari.md    # Test senaryoları / test raporu
└── test_kanitlari/        # Test ekran görüntüleri
```

> `venv/`, `.env` ve `chroma_db/` yerelde oluşur; depoya eklenmez.

## Teknolojiler

- Python 3.12
- Streamlit
- LangChain
- PyMuPDF
- ChromaDB
- Ollama (varsayılan) veya OpenAI

## Örnek PDF'ler

`data/` klasöründe Türkçe örnek PDF’ler vardır (Wikipedia maddeleri, KVKK rehberi, kahve rehberi, ürün kılavuzu).  
Liste ve demo soruları: `data/README.md`.

## Kurulum

### En kolay yol (Windows)

1. [Ollama](https://ollama.com) kurun.
2. Terminalde modelleri çekin:
   ```bash
   ollama pull llama3
   ollama pull nomic-embed-text
   ```
3. `.env.example` dosyasını `.env` olarak kopyalayın.
4. `.env` içinde `LLM_PROVIDER=ollama` olduğundan emin olun.
5. `calistir.bat` dosyasına çift tıklayın.  
   Bat dosyası gerekirse `venv` oluşturur, paketleri kurar ve uygulamayı açar.

Tarayıcıda genelde `http://localhost:8501` açılır.

### Manuel kurulum

```bash
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env         # macOS/Linux: cp .env.example .env
streamlit run app.py
```

### OpenAI kullanmak isterseniz

`.env` dosyasında:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

## Kullanım

1. Sol menüden bir veya birden fazla PDF yükleyin.
2. "PDF'leri İşle ve Veritabanına Ekle" butonuna basın.
3. Sohbet kutusuna dokümanla ilgili bir soru yazın.
4. Cevabın altındaki "Kaynaklar" bölümünden hangi dosya/sayfadan geldiğini görebilirsiniz.
5. Doküman dışı bir soru sorarsanız sistem bunu size açıkça belirtecektir.
6. İsterseniz **Veritabanını Temizle** ile indeksi sıfırlayın.

## Teslim Dosyaları

| Dosya | Açıklama |
|-------|----------|
| `reports/teknik_rapor.docx` | Teknik rapor |
| `reports/sunum.pptx` | Proje sunumu |
| `test_senaryolari.md` | Test senaryoları / test raporu |
| `test_kanitlari/` | Test ekran görüntüleri |
| `README.md` | Kurulum ve kullanım dokümanı |

## Notlar / Sınırlamalar

- Taranmış (görüntü tabanlı) PDF'ler için OCR desteği yoktur; PDF içinde seçilebilir metin olmalıdır.
- Vektör veritabanı `chroma_db/` klasöründe kalıcı olarak saklanır; silmek için arayüzdeki "Veritabanını Temizle" butonunu kullanabilirsiniz.
- `config.py` üzerinden chunk boyutu (`CHUNK_SIZE`), örtüşme (`CHUNK_OVERLAP`) ve getirilecek parça sayısı (`TOP_K`) ayarlanabilir.

## Sonraki Adımlar (Genişletme Fikirleri)

- Taranmış PDF’ler için OCR desteği eklemek
- Kullanıcı bazlı doküman koleksiyonları (multi-tenant)
- Sohbet geçmişini dosyaya kaydetme
- Streaming (kelime kelime) cevap gösterimi
- Farklı dosya formatları (docx, txt) desteği
