# Test Senaryoları — Akıllı Doküman Soru-Cevap Sistemi

> En az 10 test senaryosu. PDF'ler: `data/` klasörü (bkz. `data/README.md`).
> Her senaryonun ekran görüntüsü `test_kanitlari/` klasöründe saklanır.

| # | Senaryo | Adımlar | Beklenen Sonuç | Gerçekleşen | Ekran Görüntüsü | Durum |
|---|---------|---------|----------------|-------------|------------------|-------|
| 1 | Tek PDF yükleme | `wiki_ataturk.pdf` yükle, işle | Chunk > 0, başarı mesajı | Beklenen gibi chunk eklendi | `test_kanitlari/senaryo_01_tek_pdf_yukleme.png` | ✅ |
| 2 | Çoklu PDF yükleme | En az 5 farklı PDF yükle | Sidebar'da 5+ kaynak listelenir | 5+ PDF listelendi | `test_kanitlari/senaryo_02_coklu_pdf.png` | ✅ |
| 3 | Doğrudan soru | "İstanbul ne zaman fethedildi?" | 1453 / fetih bilgisi + kaynak | Dokümana dayalı cevap + kaynak | `test_kanitlari/senaryo_03_dogrudan_soru.png` | ✅ |
| 4 | Dolaylı soru | "Atatürk'ün cumhurbaşkanlığı dönemi hakkında ne söylenebilir?" | Dokümana dayalı özet + kaynak | Özet + kaynak gösterildi | `test_kanitlari/senaryo_04_dolayli_soru.png` | ✅ |
| 5 | Doküman dışı soru | "Bugün hava nasıl?" | Kapsam dışı uyarısı | Kapsam dışı uyarı döndü | `test_kanitlari/senaryo_05_dokuman_disi_soru.png` | ✅ |
| 6 | Boş veritabanı | PDF yokken soru sor | PDF yükleyin mesajı | Yükleme uyarısı verildi | `test_kanitlari/senaryo_06_bos_veritabani.png` | ✅ |
| 7 | Kaynak sayfa | "Osmanlı ne zaman kuruldu?" | Sayfa bilgisi doğru | Kaynak dosya + sayfa göründü | `test_kanitlari/senaryo_07_kaynak_sayfa.png` | ✅ |
| 8 | Taranmış PDF | OCR gerektiren PDF yükle | Metin çıkarılamadı hatası | Anlaşılır hata mesajı | `test_kanitlari/senaryo_08_taranmis_pdf.png` | ✅ |
| 9 | Büyük PDF | `kvkk_...pdf` veya `iyi-kahve-rehberi.pdf` (50+ sayfa) | Makul sürede işlenir | İşlem tamamlandı | — | ✅ |
| 10 | Veritabanını temizle | Temizle butonu | Liste ve sohbet sıfırlanır | Liste/sohbet sıfırlandı | — | ✅ |
| 11 | Tekrar yükleme | Aynı PDF'i iki kez ekle | Veri bozulmaz | Sistem bozulmadan çalıştı | — | ✅ |
| 12 | Ürün kılavuzu | "Xiaomi robot süpürge nasıl kullanılır?" | Kılavuzdan cevap + kaynak | Kılavuzdan cevap + kaynak | `test_kanitlari/senaryo_12_urun_kilavuzu.png` | ✅ |

**Durum:** ✅ Başarılı / ❌ Başarısız / ⬜ Henüz test edilmedi

