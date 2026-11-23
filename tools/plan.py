"""Burger Vibes - 4-week story plan (28 days x 3 slots, no repeats).

Why this shape: every weekday has a fixed FORMAT (followers learn the rhythm),
every week has its own THEME (so the same weekday never repeats content).
FLOW = AI image from Google Flow, used only for mood, props and scenes.
ECHT = real footage of the real product: food shown in ads must be the food
that is served (German UWG: misleading advertising), so burgers stay real.
"""
import json
import os

STYLE = ("Vertical 9:16 photo, cinematic and moody, lit by 90s retro neon in hot pink "
         "and electric cyan, glossy reflections, shallow depth of field, 35mm lens, high detail. "
         "Keep the top third of the frame calm and dark for a text overlay. "
         "No text, no letters, no logos, no watermarks, no recognizable faces. Scene: ")
MOTION = ("Slow cinematic push-in, subtle neon flicker, light haze drifting, "
          "camera stays steady, 8 seconds, no text.")

FORMATS = {
    "Mo": ("MENÜ-MONTAG", "Ürün vitrini: haftaya iştahla başla"),
    "Di": ("HINTER DEM GRILL", "Mutfak ve süreç: güven ve kalite"),
    "Mi": ("MITTWOCH-VOTING", "Etkileşim: anket, quiz, emoji slider"),
    "Do": ("CREW", "Ekip ve yüzler: marka insanlaşır"),
    "Fr": ("NEON-FREITAG", "Akşam ve hafta sonu havası"),
    "Sa": ("EURE VIBES", "Misafirler ve repost (UGC)"),
    "So": ("SONNTAG CHILL", "Paket servis, rahatlık, gelecek haftaya bakış"),
}
MUSIC = {
    "Mo": ("Funk / Upbeat · 100–115 BPM", "funk, groove, upbeat"),
    "Di": ("Lo-fi Hip-Hop · 70–90 BPM", "lofi, chill beats"),
    "Mi": ("Verspielt / Pop · 110–125 BPM", "playful, quirky, pop"),
    "Do": ("Soul / R&B warm · 80–95 BPM", "soul, rnb, warm"),
    "Fr": ("Synthwave / Retro · 100–120 BPM", "synthwave, retro, 80s"),
    "Sa": ("90s Hip-Hop / Boom-Bap · 85–95 BPM", "boom bap, hip hop, old school"),
    "So": ("Jazzhop / Chill · 70–85 BPM", "jazz hop, chill, sunday"),
}
WEEKS = {
    1: ("Hallo Tempelhof", "Tanışma: kimiz, ne yapıyoruz, neredeyiz"),
    2: ("Handwerk", "Ustalık: malzeme, süreç, Halal kalite"),
    3: ("Community", "Topluluk: misafirler, geri bildirim, mahalle"),
    4: ("Specials & Spaß", "Haftanın burgeri, oyunlar, ay kapanışı"),
    5: ("Advent-Finale", "Advent takviminin son dört kapısı, 21-24 Aralık"),
}

# (week, day, time, src, scene_or_shot, title, sub, preset, accent, sticker)
# The time column is historical: every frame of a day is posted together at
# POST_TIME[day], in the order listed here.
S = [
 # ---------------- WEEK 1 - Hallo Tempelhof
 (1,"Mo","11:30","FLOW","an empty burger restaurant counter at opening time, bar stools, steam rising from the kitchen pass, pink and cyan neon glow","NEUE WOCHE.\nNEUE VIBES.","Wir haben offen","neon","pink","Standort"),
 (1,"Mo","13:00","ECHT","Klassiker-Burger in Zeitlupe durchschneiden, Querschnitt nah","UNSER\nKLASSIKER","100% BEEF · 100% HALAL","punch","cyan","—"),
 (1,"Mo","18:30","FLOW","a glowing menu board on a dark brick wall, completely out of focus, soft bokeh, nothing readable","WAS BESTELLST\nDU ZUERST?","JETZT ABSTIMMEN","ask","pink","Umfrage: Classic / Cheese"),
 # Week 1 v2 (from Tue 24.11): built on the real shoot of 01.11.2026. Each day is
 # one mini story (hook -> process -> payoff -> interaction) instead of three loose frames.
 (1,"Di","11:00","ECHT","C013: Patties kommen gewürzt auf den Grill","WAS PASSIERT\nAUF DEM GRILL?","Bleib dran","punch","pink","—"),
 (1,"Di","13:00","ECHT","C003: Käse schmilzt auf den Patties, Kruste sichtbar","DIE KRUSTE\nHAT EINEN NAMEN.","Maillard-Reaktion","neon","cyan","—"),
 (1,"Di","18:00","ECHT","C024: Burger wird gebaut, Hero-Shot am Ende","VON ROH\nZU WOW.","WIE ISST DU DEINEN BURGER?","ask","pink","Umfrage: Mit den Händen / Messer & Gabel"),
 (1,"Mi","12:00","ECHT","C053: Käsesauce läuft von der Kelle","KÄSE\nODER SAUCE?","JETZT ABSTIMMEN","ask","pink","Umfrage: Käse / Sauce"),
 (1,"Mi","15:00","ECHT","C054: Maiskolben mit Burger-Vibes-Fähnchen","MAIS ODER\nPOMMES?","DEINE SEITE","ask","cyan","Umfrage: Mais / Pommes"),
 (1,"Mi","19:00","ECHT","C006: Burger vor gestapelten Burger-Vibes-Boxen","SCHICK'S\nDEINER CREW.","Wer zahlt die nächste Runde?","neon","cyan","— (Teilen-Pfeil zeigen; am nächsten Tag Umfrage-Ergebnis als Story teilen)"),
 (1,"Do","11:00","ECHT","C012: Crew-Mitglied winkt in die Kamera","SAG HALLO\nZUR CREW.","Die Hände hinter deinem Burger","neon","pink","—"),
 (1,"Do","14:00","ECHT","C037: Crew-Mitglied spricht am Grill in die Kamera (Originalton)","FRAG\nDIE CREW","WAS WILLST DU WISSEN?","ask","cyan","Fragen-Sticker"),
 (1,"Do","19:00","ECHT","C025: Crew packt eine Bestellung","MIT LIEBE\nGEPACKT.","Burger with Love","punch","pink","—"),
 (1,"Fr","12:00","ECHT","C050: Laden von außen bei Nacht, Neon an (Trend: Black Friday 27.11.)","BLACK FRIDAY?\nNEON FRIDAY.","Kein Rabatt. Nur gute Vibes.","neon","pink","—"),
 (1,"Fr","17:00","ECHT","C049: Neon-Wand 90s Burger Vibes","SCHON MAL\nHIER GEGESSEN?","SAG'S UNS","ask","cyan","Umfrage: Stammgast / Noch nicht"),
 (1,"Fr","21:00","ECHT","C046: Neon-Schriftzug an der Wand","WOCHENENDE\nSTARTET HIER","","neon","cyan","Link: Google Maps"),
 (1,"Sa","12:00","ECHT","C011: Box auf, Burger im Papier","DEIN BURGER\nWARTET SCHON.","","punch","pink","Standort"),
 (1,"Sa","15:00","ECHT","C041: Kuchen in der Vitrine","PLATZ FÜR\nNACHTISCH?","","ask","pink","Emoji-Slider 🍰"),
 (1,"Sa","19:00","ECHT","C056: Burger-Vibes-Fähnchen im Essen","MARKIER\nUNS.","Wir reposten eure Stories","neon","cyan","Erwähnung @burgervibes.berlin"),
 (1,"So","13:00","ECHT","C028: Burger-Vibes-Papiertüte (Trend: 1. Advent 29.11.)","ERSTER ADVENT.\nERSTER BURGER?","Zum Mitnehmen","neon","pink","—"),
 (1,"So","16:00","ECHT","C057: Crispy Chicken auf dem Tablett","TEAM BEEF\nODER TEAM CHICKEN?","JETZT ABSTIMMEN","ask","cyan","Umfrage: Beef / Chicken"),
 (1,"So","19:00","ECHT","C051: Burger-Vibes-Leuchtschrift","BIS MORGEN,\nTEMPELHOF.","Neue Woche, neue Vibes","neon","pink","—"),
 # ---------------- WEEK 2 - Handwerk
 (2,"Mo","11:30","FLOW","macro of sesame seeds and flour on a dark wooden board, warm golden light with a pink neon edge, no bread shown whole","ES BEGINNT\nMIT DEM BUN.","","neon","cyan","—"),
 (2,"Mo","13:00","ECHT","Käse schmilzt über das Patty, Cheese-Pull in Zeitlupe","CHEESE\nO'CLOCK","","punch","pink","—"),
 (2,"Mo","18:30","ECHT","Burger von oben, langsam drehend","EXTRA\nKÄSE?","JETZT ABSTIMMEN","ask","pink","Umfrage: Ja / Doppelt"),
 (2,"Di","12:00","ECHT","C047: Neon-Motiv als Adventstürchen","TÜRCHEN\n1","Heute: der Saucen-Check","door","pink","Countdown-Sticker bis 24.12. (einmal anlegen, jeden Tag wiederverwenden)"),
 (2,"Di","14:00","FLOW","slow-motion splash of thick sauces in pink and orange against a dark background, abstract","SAUCEN-\nCHECK","WELCHE IST AM SCHÄRFSTEN?","ask","pink","Quiz: 3 Saucen"),
 (2,"Di","18:00","ECHT","Halal-Nachweis des Lieferanten zeigen (nur echtes Dokument!)","100% HALAL.\n100% BEEF.","KEINE KOMPROMISSE","punch","cyan","—"),
 (2,"Mi","12:00","ECHT","C048: Neon-Motiv als Adventstürchen","TÜRCHEN\n2","Heute: deine Burger-Playlist","door","cyan","—"),
 (2,"Mi","15:00","FLOW","a cassette tape and crumpled burger wrapping paper on a dark table, 90s mood, neon glow","WELCHER SONG\nZUM BURGER?","SCHICK UNS DEINEN","ask","cyan","Musik-Fragen-Sticker"),
 (2,"Mi","19:00","ECHT","C052: Käsesauce von der Kelle (Querformat, Ausschnitt)","FLÜSSIGES\nGOLD.","Käsesauce, frisch","neon","pink","—"),
 (2,"Do","12:00","ECHT","C046: Neon-Motiv als Adventstürchen","TÜRCHEN\n3","Heute: der Tipp der Crew","door","pink","—"),
 (2,"Do","14:00","ECHT","Crew zeigt ihre Lieblings-Kombi auf dem Tablett","CREW-TIPP","Die Lieblings-Kombi der Crew","neon","pink","—"),
 (2,"Do","19:00","FLOW","a neon-lit kitchen pass with blank order tickets fluttering, motion blur, nothing readable","BESTELLUNG\nRAUS!","","neon","cyan","—"),
 (2,"Fr","12:00","ECHT","C049: Neon-Motiv als Adventstürchen","TÜRCHEN\n4","Heute: Feierabend-Burger","door","cyan","—"),
 (2,"Fr","17:00","ECHT","Mehrere Burger gleichzeitig auf dem Pass","FEIERABEND-\nBURGER","","punch","cyan","Standort"),
 (2,"Fr","21:00","ECHT","Neon-Schild draußen bei Nacht","WIR SIND\nNOCH DA.","Bis später","neon","pink","Link: Google Maps"),
 (2,"Sa","12:00","ECHT","C047: Neon-Motiv als Adventstürchen","TÜRCHEN\n5","Heute: ihr seid dran","door","pink","—"),
 (2,"Sa","15:00","ECHT","Gäste-Stories reposten","IHR SEID\nDIE BESTEN","","punch","pink","Repost"),
 (2,"Sa","19:00","ECHT","Erster Biss eines Gastes (vorher fragen)","DER ERSTE\nBISS","Unbezahlbar","neon","pink","Emoji-Slider 🤤"),
 (2,"So","12:00","ECHT","C048: Neon-Motiv als Adventstürchen","TÜRCHEN\n6","Nikolaus! Stiefel raus, Burger rein.","door","cyan","—"),
 (2,"So","16:00","ECHT","Unboxing aus der Takeaway-Tüte, Papier aufklappen","UNBOXING","SONNTAGS-EDITION","punch","cyan","—"),
 (2,"So","19:00","FLOW","a single glowing neon arrow on a dark tiled wall pointing right, light haze","SEID\nGESPANNT","Nächste Woche: Eure Woche","neon","pink","—"),
 # ---------------- WEEK 3 - Community
 (3,"Mo","12:00","ECHT","C046: Neon-Motiv als Adventstürchen","TÜRCHEN\n7","Heute: die Mittagspause","door","pink","—"),
 (3,"Mo","13:00","ECHT","Mittagstablett: Burger, Sides, Drink von oben","MITTAGS-\nPAUSE","","punch","cyan","Standort"),
 (3,"Mo","18:30","ECHT","Übergabe am Tresen, Hände nehmen die Tüte","HEUTE\nNOCH HUNGER?","JETZT ABSTIMMEN","ask","pink","Umfrage: Ja / Sehr"),
 (3,"Di","12:00","ECHT","C049: Neon-Motiv als Adventstürchen","TÜRCHEN\n8","Heute: Qualität braucht Zeit","door","cyan","—"),
 (3,"Di","14:00","FLOW","close-up of glowing grill embers with sparks flying in the dark","QUALITÄT\nBRAUCHT ZEIT","","neon","pink","—"),
 (3,"Di","18:00","ECHT","Burger einpacken für Abholung","FERTIG ZUM\nABHOLEN","","punch","cyan","—"),
 (3,"Mi","12:00","ECHT","C047: Neon-Motiv als Adventstürchen","TÜRCHEN\n9","Heute: das Burger-Quiz","door","pink","—"),
 (3,"Mi","12:00","FLOW","a glowing pink neon question mark on a dark tiled wall","BURGER-\nQUIZ","WIE GUT KENNST DU UNS?","ask","pink","Quiz: Patty-Gewicht (echte Zahl!)"),
 (3,"Mi","19:00","ECHT","Quiz-Auflösung mit dem echten Patty auf der Waage","AUFLÖSUNG!","","punch","pink","—"),
 (3,"Do","12:00","ECHT","C048: Neon-Motiv als Adventstürchen","TÜRCHEN\n10","Heute: der Schärfe-Test","door","cyan","—"),
 (3,"Do","14:00","ECHT","Crew probiert eine Sauce, ehrliche Reaktion","CREW-TEST","WIE SCHARF?","ask","pink","Emoji-Slider 🔥"),
 (3,"Do","19:00","FLOW","staff aprons hanging on wall hooks under pink neon, moody","DANKE,\nCREW.","","neon","pink","—"),
 (3,"Fr","12:00","ECHT","C046: Neon-Motiv als Adventstürchen","TÜRCHEN\n11","Heute: Vibe Check","door","pink","—"),
 (3,"Fr","17:00","ECHT","Musik an, Crew groovt kurz beim Grillen","VIBE\nCHECK","","punch","pink","—"),
 (3,"Fr","21:00","ECHT","Volle Tische, Neon, Stimmung (keine Gesichter ohne Erlaubnis)","SO FÜHLT SICH\nFREITAG AN","","neon","cyan","—"),
 (3,"Sa","12:00","ECHT","C049: Neon-Motiv als Adventstürchen","TÜRCHEN\n12","Heute: eure Meinung zählt","door","cyan","—"),
 (3,"Sa","15:00","ECHT","Gäste-Stories / Feedback reposten","EUER\nFEEDBACK","WIE WAR'S?","ask","cyan","Fragen-Sticker"),
 (3,"Sa","19:00","ECHT","Echte Google-Bewertungen auf dem Handy zeigen","DANKE FÜR\nEURE STERNE","","punch","pink","Link: Google-Bewertung"),
 (3,"So","12:00","ECHT","C047: Neon-Motiv als Adventstürchen","TÜRCHEN\n13","3. Advent: Sonntags-Date","door","pink","—"),
 (3,"So","16:00","ECHT","Zwei Getränke stoßen an, zwei Burger daneben","SONNTAGS-\nDATE","","punch","pink","—"),
 (3,"So","19:00","FLOW","a single glowing neon arrow on a dark wall pointing right, cyan","NÄCHSTE\nRUNDE","Specials & Spaß","neon","cyan","—"),
 # ---------------- WEEK 4 - Specials & Spaß
 (4,"Mo","12:00","ECHT","C048: Neon-Motiv als Adventstürchen","TÜRCHEN\n14","Heute: der Burger der Woche","door","cyan","—"),
 (4,"Mo","13:00","ECHT","Reveal: Burger der Woche dreht sich auf dem Teller","DAS\nIST ER.","","punch","cyan","—"),
 (4,"Mo","18:30","ECHT","Biss in den Burger der Woche, nah","SCHON\nPROBIERT?","","ask","pink","Emoji-Slider 🍔"),
 (4,"Di","12:00","ECHT","C046: Neon-Motiv als Adventstürchen","TÜRCHEN\n15","Heute: Schicht für Schicht","door","pink","—"),
 (4,"Di","14:00","FLOW","floating fresh vegetables (tomato slices, lettuce, onion rings) in an exploded layout, dark neon studio, no bread, no meat","SCHICHT FÜR\nSCHICHT","","neon","pink","—"),
 (4,"Di","18:00","ECHT","Special wird live gebaut","LIVE\nGEBAUT","","punch","pink","—"),
 (4,"Mi","12:00","ECHT","C049: Neon-Motiv als Adventstürchen","TÜRCHEN\n16","Heute: Wie gut kennst du uns?","door","cyan","—"),
 (4,"Mi","15:00","FLOW","abstract neon light streaks forming a tunnel, pink and cyan","WIE GUT\nKENNST DU UNS?","","ask","cyan","Quiz: Seit wann gibt es uns?"),
 (4,"Mi","19:00","ECHT","Auflösung, Crew zeigt die richtige Antwort","RICHTIG\nODER FALSCH?","","punch","pink","—"),
 (4,"Do","12:00","ECHT","C047: Neon-Motiv als Adventstürchen","TÜRCHEN\n17","Heute: die Crew-Challenge","door","pink","—"),
 (4,"Do","11:00","ECHT","Crew-Challenge: wer baut am schnellsten? (Stoppuhr im Bild)","CREW-\nCHALLENGE","","punch","cyan","—"),
 (4,"Do","14:00","ECHT","Zieleinlauf, Stoppuhr nah","NEUER\nREKORD?","","ask","pink","Umfrage: Name A / Name B"),
 (4,"Fr","12:00","ECHT","C048: Neon-Motiv als Adventstürchen","TÜRCHEN\n18","Heute: der Freitags-Ansturm","door","cyan","—"),
 (4,"Fr","17:00","ECHT","Feierabend-Ansturm, Bestellungen fliegen","BUSY.\nLIEBEN WIR.","","punch","pink","Standort"),
 (4,"Fr","21:00","ECHT","Neon-Schild, Crew winkt","DANKE FÜR\nDIESE WOCHE","","neon","cyan","—"),
 (4,"Sa","12:00","ECHT","C046: Neon-Motiv als Adventstürchen","TÜRCHEN\n19","Heute: eure Galerie","door","pink","—"),
 (4,"Sa","15:00","ECHT","Gäste-Fotos der Woche als Collage","GÄSTE-\nGALERIE","","punch","cyan","Repost"),
 (4,"Sa","19:00","ECHT","Burger to go draußen auf dem Tempelhofer Damm, Neon im Hintergrund","WIR SEHEN\nUNS!","","neon","pink","Standort"),
 (4,"So","12:00","ECHT","C049: Neon-Motiv als Adventstürchen","TÜRCHEN\n20","4. Advent: das Best of","door","cyan","—"),
 (4,"So","16:00","ECHT","Best-of: kurze Clips der 4 Wochen (Claude schneidet zusammen)","BEST OF","","punch","pink","—"),
 (4,"So","19:00","FLOW","a single glowing pink neon arrow on a dark tiled wall pointing right","WAS WOLLT\nIHR SEHEN?","SAG ES UNS","ask","pink","Fragen-Sticker"),
 # ---------------- WEEK 5 - Advent-Finale (Mon 21. - Thu 24.12.2026, no slots Fri-Sun)
 (5,"Mo","12:00","ECHT","C048: Neon-Motiv als Adventstürchen","TÜRCHEN\n21","Noch drei Mal schlafen","door","cyan","—"),
 (5,"Mo","12:00","ECHT","C004: Burger in der Hand, dann Hero-Shot","LAST-MINUTE-\nHUNGER?","Wir sind da","punch","pink","Standort"),
 (5,"Di","12:00","ECHT","C046: Neon-Motiv als Adventstürchen","TÜRCHEN\n22","Heute: Berliner Winter","door","pink","—"),
 (5,"Di","12:00","ECHT","C027: Sesam-Bun von oben","SESAM\nSTATT SCHNEE.","Berliner Winter halt","punch","cyan","Emoji-Slider ❄️"),
 (5,"Mi","12:00","ECHT","C049: Neon-Motiv als Adventstürchen","TÜRCHEN\n23","Heute: die große Frage","door","cyan","—"),
 (5,"Mi","12:00","ECHT","C011: Box auf, Burger im Papier","GANS ODER\nBURGER?","DEIN WEIHNACHTSESSEN","ask","pink","Umfrage: Gans / Burger"),
 (5,"Do","12:00","ECHT","C047: Neon-Motiv als Adventstürchen","TÜRCHEN\n24","Das letzte Türchen","door","pink","—"),
 (5,"Do","12:00","ECHT","C012: Crew winkt in die Kamera","FROHE\nWEIHNACHTEN!","Eure Burger-Vibes-Crew","neon","cyan","— (Feiertags-Öffnungszeiten vorher bestätigen)"),
]

DAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
# One posting moment per day, 2-3 frames in a row: a whole mini story costs the
# poster one app session, and the account keeps its story ring every day.
# Lunch on weekdays, early evening Fri/Sat, Sunday lunch; all inside the
# opening hours (Mon-Thu 12-24, Fri-Sun 12-01).
POST_TIME = {"Mo": "12:00", "Di": "12:00", "Mi": "12:00", "Do": "12:00",
             "Fr": "17:00", "Sa": "17:00", "So": "13:00"}


def build():
    slots = []
    counter = {}
    for w, d, t, src, what, title, sub, preset, accent, sticker in S:
        key = (w, d)
        counter[key] = counter.get(key, 0) + 1
        sid = f"W{w}-{d}-{counter[key]}"
        slots.append({
            "id": sid, "week": w, "day": d, "time": POST_TIME[d], "order": counter[key], "src": src,
            "prompt": STYLE + what + "." if src == "FLOW" else "",
            "shot": what if src == "ECHT" else "",
            "title": title, "sub": sub, "script_sub": bool(sub) and not sub.isupper(),  # mixed case = neon script line
            "preset": preset, "accent": accent, "sticker": sticker,
        })
    # Sanity: 28 days x 3 slots, no duplicate headlines across the month.
    assert len(slots) >= 84, len(slots)
    per_day = {}
    for sl in slots:
        per_day[(sl["week"], sl["day"])] = per_day.get((sl["week"], sl["day"]), 0) + 1
    assert max(per_day.values()) <= 3, per_day
    titles = [s["title"] for s in slots]
    dupes = {x for x in titles if titles.count(x) > 1}
    return slots, dupes


if __name__ == "__main__":
    slots, dupes = build()
    out = {"start": "2026-11-23", "post_time": POST_TIME, "style": STYLE, "motion": MOTION, "formats": FORMATS, "music": MUSIC,
           "weeks": {str(k): v for k, v in WEEKS.items()}, "days": DAYS, "slots": slots}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "plan.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("slots:", len(slots), "| duplicate headlines:", dupes or "none")
    print("FLOW:", sum(s["src"] == "FLOW" for s in slots), "ECHT:", sum(s["src"] == "ECHT" for s in slots))
