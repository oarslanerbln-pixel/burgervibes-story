#!/usr/bin/env python3
"""Batch-render stories from plan.json.

Media files are matched by slot id in their filename, e.g. W1-Mo-1.png,
W1-Mo-2.mp4 (case-insensitive, any image/video extension). Slots without
media are skipped unless --placeholder is given (then a neon gradient stands
in, useful to preview texts before the Flow images exist).
"""
import argparse
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXT = (".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov", ".m4v", ".webm")


def find_media(media_dirs, sid):
    for media_dir in media_dirs:
        for path in sorted(glob.glob(os.path.join(media_dir, "*"))):
            name = os.path.basename(path).lower()
            # "W1-Mo-2.mp4" or "W1-Mo-2_take3.mp4", but never "W1-Mo-21..."
            if name.endswith(EXT) and (name.startswith(sid.lower() + ".") or name.startswith(sid.lower() + "_")):
                return path
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--media", nargs="*", default=[os.path.join(ROOT, "assets", "selects"), os.path.join(ROOT, "assets", "ai")])
    p.add_argument("--out", default=os.path.join(ROOT, "output", "stories"))
    p.add_argument("--week", type=int)
    p.add_argument("--day")
    p.add_argument("--ids", nargs="*")
    p.add_argument("--placeholder", action="store_true")
    p.add_argument("--keep-audio", action="store_true")
    a = p.parse_args()

    plan = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf-8"))
    os.makedirs(a.out, exist_ok=True)
    done, skipped = [], []
    for s in plan["slots"]:
        if a.week and s["week"] != a.week:
            continue
        if a.day and s["day"] != a.day:
            continue
        if a.ids and s["id"] not in a.ids:
            continue
        media = find_media(a.media, s["id"])
        if not media and not a.placeholder:
            skipped.append(s["id"])
            continue
        cmd = [sys.executable, os.path.join(HERE, "story.py"), "--preset", s["preset"],
               "--accent", s["accent"], "--title", s["title"], "--out",
               os.path.join(a.out, s["id"] + ".mp4")]
        if s["sub"]:
            cmd += ["--sub", s["sub"]]
        if s["script_sub"]:
            cmd += ["--script-sub"]
        if media:
            cmd += ["--bg", media]
        if a.keep_audio or (media and "selects" in media):
            cmd += ["--keep-audio"]
        subprocess.run(cmd, check=True)
        done.append(s["id"])
    print("rendered:", " ".join(done) or "-")
    print("no media yet:", " ".join(skipped) or "-")


if __name__ == "__main__":
    main()
