#!/usr/bin/env python3
"""Cut story-ready 9:16 clips from the raw shoot, driven by plan/selects.json.

  python tools/cut.py            # all selects
  python tools/cut.py W1-Mo-2    # only these slots

selects.json (Claude writes it after reading the contact sheets):
  {
    "W1-Mo-2": {"clip": "footage/2026-12/IMG_0412.MOV", "in": 3.2, "out": 9.5,
                "x": 0.5, "speed": 0.5, "note": "cross-section, best angle"}
  }
  x      horizontal crop centre for landscape footage (0 = left, 1 = right)
  speed  0.5 = half-speed slow motion (only looks smooth on 50/60 fps clips)
Output: assets/selects/<slot>.mp4, 1080x1920, 30 fps, CRF 22 (small enough to
commit, so the daily cloud job finds them; the story render re-encodes anyway), no audio (music is
added in Instagram; keep_audio: true keeps the original sound, e.g. sizzling).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def cut(sid, s):
    src = os.path.join(ROOT, s["clip"])
    out = os.path.join(ROOT, "assets", "selects", sid + ".mp4")
    speed = float(s.get("speed", 1.0))
    x = float(s.get("x", 0.5))
    t_in, t_out = float(s["in"]), float(s["out"])
    # Fill 1080x1920: scale so the short side fits, then crop a 9:16 window
    # whose centre sits at x (landscape) or in the middle (portrait).
    vf = ("scale='if(gt(iw/ih,9/16),-2,1080)':'if(gt(iw/ih,9/16),1920,-2)',"
          f"crop=1080:1920:'max(0,min(iw-1080,iw*{x}-540))':'(ih-1920)/2',"
          f"setpts=PTS/{speed},fps=30,format=yuv420p")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t_in), "-to", str(t_out), "-i", src, "-vf", vf,
           "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-movflags", "+faststart"]
    if s.get("keep_audio") and speed == 1.0:
        cmd += ["-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-an"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(cmd + [out], check=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                         capture_output=True, text=True).stdout.strip()
    print(f"{sid}: {os.path.basename(src)} {t_in}-{t_out}s x={x} speed={speed} -> {float(dur):.1f}s")


def main():
    path = os.path.join(ROOT, "plan", "selects.json")
    selects = json.load(open(path, encoding="utf-8"))
    only = set(sys.argv[1:])
    for sid, s in selects.items():
        if sid.startswith("_") or (only and sid not in only):
            continue
        cut(sid, s)


if __name__ == "__main__":
    main()
