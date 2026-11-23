# Reel-Fikirleri: Aralık 2026 – Şubat 2027

Burger Vibes için 12 Reel. Her biri bir **hikaye** anlatıyor (başlangıç → gerilim →
ödül), takvime ya da gündeme bağlı ve 1618 Digital'in marka kurallarına uyuyor
(ürün hep gerçek, bilgi hep doğru, müzik sadece Instagram'dan ya da orijinal ses).
Ekrandaki yazılar Almanca. **Önce çekilecekler** işaretli; hepsi `SHOTLIST.md`'de sahne
sahne var.

Algoritma notları (her Reel için):
- **İlk 1 saniye:** hareket + yazılı kanca. Logo ya da yavaş açılış yok.
- **7–20 sn** ideal; hikaye Reel'leri en fazla 45 sn.
- **Altyazı her zaman** (çoğu kişi sessiz izliyor).
- Sonda tek bir CTA: kaydet, paylaş ya da gel. Üçü birden değil.
- Açıklamada 1 soru (yorum toplar) + konum etiketi + 3–5 hashtag.

| # | Kanca (ekranda) | Hikaye | Süre / ses | Ne zaman | Gerekli bilgi |
|---|---|---|---|---|---|
| 1 ⭐ | „Warum eröffnet man einen 90s-Burgerladen in Tempelhof?" | Kurucu 3 cümlede anlatıyor: neden 90'lar, neden Tempelhof, Premium Beef ve Halal ne demek. Arada neon, ızgara, ilk ısırık. Profilde **sabitlenecek** Reel. | 30–40 sn · kurucunun sesi + altyazı | 1. Aralık haftası | Kurucu kameraya konuşmayı kabul ediyor mu? |
| 2 ⭐ | „POV: Du kommst vom Weihnachtsmarkt und hast immer noch Hunger" | Soğuk sokak, nefes buharı → kapı açılır, neon sıcaklığı → peynir sosu dökülür → ilk ısırık → „Willkommen im Warmen." | 12–15 sn · trend ses (app) | Weihnachtsmarkt dönemi | — |
| 3 ⭐ | „Burger Vibes Wrapped 2026" | Spotify-Wrapped formatı: neon kartlarda en çok satan burger, en sevilen sos, en yoğun saat, açılıştan beri satılan burger. | 15–20 sn · upbeat trend ses | 2.–6. Aralık (Wrapped haftası) | **Gerçek rakamlar** kasa sisteminden |
| 4 | „Ich bin ein Patty. Heute ist mein großer Tag." | Köftenin ağzından mini film: soğuk dolap → ızgaranın cızırtısı („heiß hier!") → peynir („endlich Gesellschaft") → ekmek → ısırık („es war schön"). | 20 sn · ekipten biri seslendirir | Aralık ortası | — |
| 5 | „Crew-Wichteln: Wer hat wen gezogen?" | Ekip gizli Noel Baba yapıyor: hediyeler küçük ve burger temalı, tepkiler gerçek. Ekibi insanlaştırır. | 30 sn · orijinal ses | 18.–22.12 | Ekip katılıyor mu? (izin formu) |
| 6 | „Nur Sound. Kein Wort." | ASMR: cızırtı, sos, çıtır patates, kağıt hışırtısı, ısırık. Müzik yok. | 15 sn · **sadece orijinal ses** | Her zaman (Aralık 2. yarısı) | Harici mikrofon |
| 7 | „Halal – was heißt das eigentlich?" | Kurucu ya da ekip 3 cümlede ve saygılı bir dille anlatıyor: kesim kuralı, tedarikçi, sertifika. Bilgiye dayalı, güven veren bir Reel. | 25–30 sn · ses + altyazı | Ocak (Ramazan'dan önce) | Metni kurucu onaylasın + sertifika |
| 8 ⭐ | „Der letzte Burger 2026" | 10'dan 0'a geri sayım, her saniye bir kesit (ızgara, sos, ekip, neon), sonunda „Frohes 2027 – Danke, Tempelhof!" | 12 sn · trend ses | 31.12 sabahı | 31.12 açılış saati |
| 9 | „Vorsatz 2027: mehr Gemüse." | Kamera marula zoom yapıyor… burgerin içinde. „Hat doch geklappt." | 7 sn · komik trend ses | 1.–5. Ocak | — |
| 10 | „Berliner Winter-Survival-Guide" | Adım 1: bere. Adım 2: atkı. Adım 3: cheeseburger. Soğuk sokak → sıcak neon. | 10 sn · trend ses | Ocak, ilk soğuk ya da karlı gün | — |
| 11 | „POV: Es ist 0:59 und du stehst vor der Tür" | Cuma gecesi, kapanıştan 1 dakika önce. Ekip kapıyı açar: „Einer geht noch." | 10 sn · orijinal ses | Ocak'ta bir cuma | Son sipariş saati gerçekten 1:00 mı? |
| 12 | „Teilen ist Liebe. Außer bei Burgern." | Çift, tek burger: biri burgeri çekip alıyor. Sevgililer Günü. | 8 sn · trend ses | 14.02 öncesi | — |

**Ramazan (tahminen 8 Şubat 2027'den itibaren):** iftar saatlerine göre açılış ya da
özel menü varsa Ocak sonunda ayrı bir plan. Şakaya değil topluluğa ve saygıya dayanmalı.

**Reel'lerin kurgusu:** çekimler `footage/<YYYY-MM>/` klasörüne gelince Claude her Reel için
`plan/reels/<isim>.json` yazar (klipler, kanca, altyazı, CTA) ve Remotion ile render eder:
`node scripts/render-plan.mjs --reel plan/reels/<isim>.json`.
