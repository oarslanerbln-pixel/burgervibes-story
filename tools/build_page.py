#!/usr/bin/env python3
"""Refresh the client plan page (plan/story-plan.html) from tools/plan.json.

The page itself (German, client-facing, published at
claude.ai/artifact/RHo2kgo4V7Kj1vXdVDFwi5) is the template: only its embedded
plan JSON is replaced, so design and text edits made on the page survive.
Run after every `python tools/plan.py`, then republish the page.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGE = os.path.join(ROOT, "plan", "story-plan.html")

# The repo plan keeps Turkish team notes; the client sees German labels.
FORMATS_DE = {"Mo": ["MENÜ-MONTAG", "Produkt im Fokus: mit Appetit in die Woche"],
              "Di": ["HINTER DEM GRILL", "Küche und Abläufe: Vertrauen und Qualität"],
              "Mi": ["MITTWOCH-VOTING", "Interaktion: Umfrage, Quiz, Emoji-Slider"],
              "Do": ["CREW", "Team und Gesichter: Die Marke wird nahbar"],
              "Fr": ["NEON-FREITAG", "Abend- und Wochenendstimmung"],
              "Sa": ["EURE VIBES", "Gäste und Reposts (UGC)"],
              "So": ["SONNTAG CHILL", "Mitnehmen und Gemütlichkeit"]}
WEEKS_DE = {"1": ["Hallo Tempelhof", "Kennenlernen: Wer wir sind, was wir machen und wo ihr uns findet."],
            "2": ["Handwerk", "Handwerk: Zutaten, Zubereitung und Halal-Qualität."],
            "3": ["Community", "Gemeinschaft: Gäste, Feedback und Nachbarschaft."],
            "4": ["Specials & Spaß", "Burger der Woche, Spiele und Monatsabschluss."],
            "5": ["Advent-Finale", "Die letzten vier Türchen bis Heiligabend."]}


def main():
    plan = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf-8"))
    for s in plan["slots"]:
        if s["src"] == "ECHT" and re.match(r"C\d{3}:", s["shot"]):
            s["shot"] = "Dreh vom 01.11., Clip " + s["shot"]
    plan["formats"], plan["weeks"] = FORMATS_DE, WEEKS_DE
    data = json.dumps(plan, ensure_ascii=False).replace("</", "<\\/")
    page = open(PAGE, encoding="utf-8").read()
    page, n = re.subn(r'(<script id="plan" type="application/json">).*?(</script>)',
                      lambda m: m.group(1) + data + m.group(2), page, count=1, flags=re.S)
    assert n == 1, "plan JSON block not found in the page"
    open(PAGE, "w", encoding="utf-8").write(page)
    print("updated", PAGE)


if __name__ == "__main__":
    main()
