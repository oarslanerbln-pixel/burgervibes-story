# Burger Vibes Studio – Kurulum (Windows)

Aylık çekimden 4 haftalık story + Reel üreten stüdyo klasörü (1618 Digital).

## 1. Bir kez kur
PowerShell'i aç:
```powershell
winget install Gyan.FFmpeg
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
```
PowerShell'i kapat-aç, sonra bu klasörde:
```powershell
pip install pillow
cd remotion
npm install
```

## 2. Gemini anahtarı (görsel üretimi için)
Anahtarı aistudio.google.com/apikey adresinden al. Dosyaya yazma, ortam değişkeni yap:
```powershell
setx GEMINI_API_KEY "BURAYA_ANAHTAR"
```
(PowerShell'i yeniden aç.)

## 3. Claude ile aç
Claude uygulaması → **Code** → klasör olarak bu klasörü seç. Chrome bağlantısını
aç. Claude `CLAUDE.md` dosyasını okur ve tüm iş akışını bilir.

İlk mesaj önerisi: *„SHOTLIST.md'yi kontrol et, sonra 1. hafta için Gemini görsellerini üret."*

## Her ay
1. `SHOTLIST.md` ile çekime git.
2. Dosyaları `footage/2026-12/` (ayın adıyla) klasörüne kopyala.
3. Claude'a yaz: *„Aralık çekimleri yüklendi, ayı hazırla."*
4. Claude seçer, keser, animasyon ekler; `output/` klasöründe günlük dosyalar hazır olur.
5. Telefona aktar, Instagram'da müzik + sticker ekle, plandaki saatte paylaş.

## Not
- Remotion; birey ve en fazla 3 çalışanlı şirketler için ücretsiz, daha büyük
  ekiplerde şirket lisansı gerekir (remotion.dev/license).
- `footage/` ve `output/` büyük dosyalardır; yedeklemeyi harici diske ya da buluta yap.
