#!/usr/bin/env python3
"""Daily story job: prepare today's Burger Vibes stories.

  python tools/today.py                 # today (Europe/Berlin)
  python tools/today.py --date 2026-11-24

Maps the calendar date onto the 4-week plan (plan/schedule.json holds the
Monday the plan started), then for each of the day's three slots:
  FLOW  -> Gemini image (generate.py) -> render; without a working key the
           neon fallback background is used and the brief says so
  ECHT  -> rendered from assets/selects/<slot>.mp4 when the clip exists,
           otherwise listed as "film today" with the exact shot
Everything for the day lands in output/daily/<date>/ with files named by
post time (1130_W1-Mo-1.mp4) plus brief.md for the phone.
Exit code 2 = plan finished, a new month has to be planned.
"""
import argparse
import datetime as dt
import glob
import json
import os
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable
DAYKEYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
DAYNAMES_TR = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]


def media_for(sid):
    for sub in ("selects", "ai"):
        for path in sorted(glob.glob(os.path.join(ROOT, "assets", sub, sid + ".*"))):
            if not path.endswith(".keep"):
                return path
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--date", help="YYYY-MM-DD, default: today in Berlin")
    p.add_argument("--no-generate", action="store_true", help="Skip Gemini, use existing images or fallback")
    a = p.parse_args()

    sched = json.load(open(os.path.join(ROOT, "plan", "schedule.json"), encoding="utf-8"))
    tz = ZoneInfo(sched.get("timezone", "Europe/Berlin"))
    day = dt.date.fromisoformat(a.date) if a.date else dt.datetime.now(tz).date()
    start = dt.date.fromisoformat(sched["start_monday"])
    offset = (day - start).days
    plan = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf-8"))
    weeks = max(s["week"] for s in plan["slots"])
    if offset < 0:
        print(f"Plan starts on {start}, nothing to do on {day}.")
        return 0
    week = offset // 7 + 1
    if week > weeks:
        print(f"PLAN FINISHED on {start + dt.timedelta(days=7 * weeks - 1)}: a new month must be planned.")
        return 2
    dkey = DAYKEYS[day.weekday()]
    slots = [s for s in plan["slots"] if s["week"] == week and s["day"] == dkey]

    out_dir = os.path.join(ROOT, "output", "daily", day.isoformat())
    os.makedirs(out_dir, exist_ok=True)

    # 1) AI images for today's FLOW slots
    gen_note = ""
    flow_ids = [s["id"] for s in slots if s["src"] == "FLOW" and not media_for(s["id"])]
    if flow_ids and not a.no_generate:
        r = subprocess.run([PY, os.path.join(HERE, "generate.py"), "--ids", *flow_ids],
                           capture_output=True, text=True)
        if r.returncode != 0 or any(not media_for(i) for i in flow_ids):
            log = r.stdout + r.stderr
            why = ("API anahtarı eksik ya da geçersiz" if "API_KEY" in log else
                   "kota/limit doldu" if "429" in log or "RESOURCE_EXHAUSTED" in log else
                   "güvenlik filtresi görseli engelledi" if "safety" in log.lower() else
                   "bağlantı ya da sunucu hatası")
            gen_note = f"Gemini görseli üretilemedi ({why}). Yedek neon arka plan kullanıldı."
    elif flow_ids:
        gen_note = "Gemini atlandı (--no-generate), yedek neon arka plan kullanıldı."

    # 2) render
    rows, todo_shots = [], []
    for s in slots:
        media = media_for(s["id"])
        if s["src"] == "ECHT" and not media:
            todo_shots.append(s)
            continue
        target = os.path.join(out_dir, f"{s['time'].replace(':', '')}_{s['id']}.mp4")
        cmd = [PY, os.path.join(HERE, "story.py"), "--preset", s["preset"], "--accent", s["accent"],
               "--title", s["title"], "--out", target]
        if s["sub"]:
            cmd += ["--sub", s["sub"]]
        if s["script_sub"]:
            cmd += ["--script-sub"]
        if media:
            cmd += ["--bg", media]
        subprocess.run(cmd, check=True)
        rows.append((s, os.path.basename(target), "AI" if s["src"] == "FLOW" and media else
                     "yedek arka plan" if s["src"] == "FLOW" else "gerçek çekim"))

    # 3) brief for the phone
    music = plan["music"][dkey]
    fmt = plan["formats"][dkey]
    lines = [f"# Burger Vibes · {DAYNAMES_TR[day.weekday()]} {day.strftime('%d.%m.%Y')}",
             f"Hafta {week} „{plan['weeks'][str(week)][0]}\" · Format: {fmt[0]}",
             f"Müzik (Instagram'da ara): {music[0]} · {music[1]}", ""]
    if rows:
        lines += ["## Hazır story'ler", "| Saat | Dosya | Sticker | Not |", "|---|---|---|---|"]
        for s, f, kind in rows:
            note = kind + (" · KI-Info etiketini aç" if kind == "AI" else "")
            lines.append(f"| {s['time']} | {f} | {s['sticker']} | {note} |")
        lines.append("")
    if todo_shots:
        lines += ["## Bugün telefonla çek (10–15 sn, dikey, 60 fps)",
                  "Klibi bu oturuma yükle, aynı yazı ve animasyonla render edeyim:"]
        for s in todo_shots:
            lines.append(f"- **{s['time']} · {s['id']}**: {s['shot']} → yazı: „{s['title'].replace(chr(10), ' ')}\" · sticker: {s['sticker']}")
        lines.append("")
    if gen_note:
        lines += ["## Uyarı", gen_note, ""]
    lines += ["Paylaşmadan önce: müzik + sticker uygulamada eklenir, ürün iddiaları (fiyat, saat) güncel mi kontrol et."]
    brief = "\n".join(lines)
    open(os.path.join(out_dir, "brief.md"), "w", encoding="utf-8").write(brief)
    print(brief)
    print("\nOUTPUT:", out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
