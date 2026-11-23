#!/usr/bin/env python3
"""End-to-end weekly pipeline for Burger Vibes stories.

  stage generate : Gemini API fills every missing FLOW image of the week
  stage check    : machine checks + one contact sheet per day (review/)
  [art director] : agents review the sheets against ART_DIRECTOR.md and
                   write rejects with refined scenes into overrides.json
  stage regen    : deletes rejected images, regenerates them from overrides
  stage render   : every slot with media becomes a finished MP4 (out/)
  stage pack     : one ZIP per week + a poster sheet of all rendered frames

Real footage (ECHT) is dropped into media/ with the slot id as filename and
flows through check/render the same way; it is never generated.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable


def run(*args):
    print("$", " ".join(args), flush=True)
    subprocess.run([PY, *args], check=True, cwd=HERE)


def regen(week):
    """Apply art-director verdicts: delete rejects so generate.py redoes them."""
    path = os.path.join(ROOT, "output", "review", f"W{week}-verdicts.json")
    if not os.path.exists(path):
        print("no verdicts yet:", path)
        return []
    verdicts = json.load(open(path, encoding="utf-8"))
    ov_path = os.path.join(ROOT, "plan", "overrides.json")
    overrides = json.load(open(ov_path, encoding="utf-8")) if os.path.exists(ov_path) else {}
    rejects = []
    for sid, v in verdicts.items():
        if v.get("verdict") == "REJECT" and v.get("scene"):
            overrides[sid] = v["scene"].rstrip(".") + "."
            for f in glob.glob(os.path.join(ROOT, "assets", "ai", sid + ".*")):
                os.remove(f)
            rejects.append(sid)
    json.dump(overrides, open(ov_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if rejects:
        run("generate.py", "--ids", *rejects)
    return rejects


def pack(week):
    out = os.path.join(ROOT, "output", "stories")
    files = sorted(glob.glob(os.path.join(out, f"W{week}-*.mp4")))
    frames = []
    for f in files:
        png = f[:-4] + ".jpg"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "2.8", "-i", f,
                        "-frames:v", "1", "-vf", "scale=270:-1", png], check=True)
        frames.append(png)
    if frames:
        cols = 7
        rows = (len(frames) + cols - 1) // cols
        inputs = sum([["-i", p] for p in frames], [])
        layout = "|".join(f"{(i % cols) * 270}_{(i // cols) * 480}" for i in range(len(frames)))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex",
                        f"xstack=inputs={len(frames)}:layout={layout}:fill=black" if len(frames) > 1 else "null",
                        os.path.join(out, f"W{week}-poster.jpg")], check=True)
        for p in frames:
            os.remove(p)
    zpath = os.path.join(out, f"BurgerVibes-Woche{week}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_STORED) as z:
        for f in files:
            z.write(f, os.path.basename(f))
    print(json.dumps({"rendered": len(files), "zip": zpath}, indent=1))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("stage", choices=["generate", "check", "regen", "render", "pack", "all"])
    p.add_argument("--week", type=int, required=True)
    p.add_argument("--model", default="nano", choices=["nano", "imagen"])
    a = p.parse_args()
    w = str(a.week)
    if a.stage in ("generate", "all"):
        run("generate.py", "--week", w, "--model", a.model)
    if a.stage in ("check", "all"):
        run("check.py", "--week", w)
    if a.stage == "regen":
        regen(a.week)
        run("check.py", "--week", w)
    if a.stage in ("render", "all"):
        run("render.py", "--week", w)
    if a.stage in ("pack", "all"):
        pack(a.week)


if __name__ == "__main__":
    main()
