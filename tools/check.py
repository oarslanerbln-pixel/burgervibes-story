#!/usr/bin/env python3
"""Automatic pre-checks before the art-director review.

Catches the machine-checkable failures so the review agent only judges taste:
  - wrong aspect ratio or too small (story needs 9:16, >= 720 px wide)
  - top third too bright or too busy: the headline sits there and must read
Also writes one contact sheet per day (3 images side by side) for the review.
"""
import argparse
import glob
import json
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def analyse(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    issues = []
    ratio = w / h
    if abs(ratio - 9 / 16) > 0.02:
        issues.append(f"Seitenverhältnis {w}x{h} statt 9:16")
    if w < 720:
        issues.append(f"zu klein ({w}px breit)")
    top = im.crop((0, int(h * 0.12), w, int(h * 0.42))).convert("L")
    bright = ImageStat.Stat(top).mean[0]
    busy = ImageStat.Stat(top.filter(ImageFilter.FIND_EDGES)).mean[0]
    if bright > 150:
        issues.append(f"oberes Drittel zu hell ({bright:.0f}/255) - Headline schwer lesbar")
    if busy > 28:
        issues.append(f"oberes Drittel sehr unruhig (Kanten {busy:.0f})")
    return {"size": [w, h], "top_brightness": round(bright), "top_busyness": round(busy), "issues": issues}


def sheet(paths, out, label):
    tiles = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        im = im.resize((360, int(360 * im.height / im.width)))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 360, 34), fill=(0, 0, 0))
        d.text((10, 8), os.path.basename(p), fill=(255, 255, 255), font=ImageFont.load_default(18))
        tiles.append(im)
    if not tiles:
        return
    hgt = max(t.height for t in tiles)
    canvas = Image.new("RGB", (360 * len(tiles) + 10 * (len(tiles) - 1), hgt + 40), (20, 12, 34))
    ImageDraw.Draw(canvas).text((10, 10), label, fill=(255, 45, 149), font=ImageFont.load_default(20))
    for i, t in enumerate(tiles):
        canvas.paste(t, (i * 370, 40))
    canvas.save(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--week", type=int, required=True)
    p.add_argument("--media", default=os.path.join(ROOT, "assets", "ai"))
    p.add_argument("--out", default=os.path.join(ROOT, "output", "review"))
    a = p.parse_args()
    plan = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf-8"))
    os.makedirs(a.out, exist_ok=True)
    report = {}
    for day in plan["days"]:
        paths = []
        for s in plan["slots"]:
            if s["week"] != a.week or s["day"] != day or s["src"] != "FLOW":
                continue
            found = sorted(glob.glob(os.path.join(a.media, s["id"] + ".*")))
            if not found:
                report[s["id"]] = {"issues": ["fehlt"]}
                continue
            report[s["id"]] = analyse(found[0])
            report[s["id"]]["file"] = found[0]
            paths.append(found[0])
        sheet(paths, os.path.join(a.out, f"W{a.week}-{day}.jpg"), f"Woche {a.week} · {day}")
    path = os.path.join(a.out, f"W{a.week}-checks.json")
    json.dump(report, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    flagged = {k: v["issues"] for k, v in report.items() if v["issues"]}
    print(json.dumps({"checked": len(report), "flagged": flagged, "report": path}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
