#!/usr/bin/env python3
"""Index a monthly shoot so Claude can "see" the footage before editing.

  python tools/ingest.py footage/2026-12

For every video (recursively): duration, resolution, orientation, fps, audio,
plus a 4-frame strip at 10/35/60/85 %. Strips are combined into contact
sheets of 8 clips each. Claude reads the sheets and index.json, then writes
plan/selects.json (which clip, which seconds, for which story slot).

Nothing in footage/ is ever modified; results go to footage/<month>/_index/.
"""
import argparse
import json
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

VIDEO = (".mp4", ".mov", ".m4v", ".mts", ".avi", ".mkv", ".webm")
THUMB_W = 240


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    info = json.loads(out)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    if not v:
        return None
    w, h = int(v["width"]), int(v["height"])
    rot = 0
    for sd in v.get("side_data_list", []):
        if "rotation" in sd:
            rot = abs(int(sd["rotation"]))
    if rot in (90, 270):
        w, h = h, w
    num, den = (v.get("avg_frame_rate") or "0/1").split("/")
    fps = round(float(num) / float(den), 2) if float(den) else 0
    return {
        "duration": round(float(info["format"].get("duration", 0)), 2),
        "width": w, "height": h,
        "orientation": "vertical" if h > w else "horizontal" if w > h else "square",
        "fps": fps,
        "slowmo_capable": fps >= 50,
        "audio": any(s["codec_type"] == "audio" for s in info["streams"]),
    }


def strip(path, duration, out_png):
    frames = []
    for i, pct in enumerate((0.10, 0.35, 0.60, 0.85)):
        tmp = out_png + f".{i}.jpg"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{duration * pct:.2f}", "-i", path,
                        "-frames:v", "1", "-vf", f"scale={THUMB_W}:-2", tmp], check=True)
        frames.append(Image.open(tmp).convert("RGB"))
        os.remove(tmp)
    h = max(f.height for f in frames)
    canvas = Image.new("RGB", (THUMB_W * 4 + 30, h), (16, 10, 28))
    for i, f in enumerate(frames):
        canvas.paste(f, (i * (THUMB_W + 10), 0))
    canvas.save(out_png)
    return canvas


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("month_dir", help="e.g. footage/2026-12")
    a = p.parse_args()
    src = os.path.abspath(a.month_dir)
    idx_dir = os.path.join(src, "_index")
    os.makedirs(idx_dir, exist_ok=True)

    clips = []
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        for name in sorted(files):
            if name.lower().endswith(VIDEO):
                clips.append(os.path.join(root, name))

    index, rows = [], []
    font = ImageFont.load_default(18)
    for n, path in enumerate(clips, 1):
        meta = probe(path)
        if not meta:
            continue
        cid = f"C{n:03d}"
        rel = os.path.relpath(path, os.path.dirname(os.path.dirname(src)))
        png = os.path.join(idx_dir, cid + ".jpg")
        img = strip(path, meta["duration"], png)
        index.append({"id": cid, "file": rel.replace(os.sep, "/"), **meta})
        label = Image.new("RGB", (img.width, 30), (0, 0, 0))
        ImageDraw.Draw(label).text((8, 5), f"{cid}  {os.path.basename(path)}  {meta['duration']}s  "
                                   f"{meta['width']}x{meta['height']}  {meta['fps']}fps",
                                   fill=(255, 45, 149), font=font)
        rows.append((label, img))
        print(cid, os.path.basename(path), meta["duration"], "s", meta["orientation"], flush=True)

    for s in range(0, len(rows), 8):
        chunk = rows[s:s + 8]
        H = sum(l.height + i.height + 12 for l, i in chunk)
        sheet = Image.new("RGB", (chunk[0][1].width, H), (16, 10, 28))
        y = 0
        for l, i in chunk:
            sheet.paste(l, (0, y)); y += l.height
            sheet.paste(i, (0, y)); y += i.height + 12
        sheet.save(os.path.join(idx_dir, f"sheet-{s // 8 + 1:02d}.jpg"), quality=85)

    with open(os.path.join(idx_dir, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    total = sum(c["duration"] for c in index)
    print(json.dumps({"clips": len(index), "minutes": round(total / 60, 1), "index": idx_dir}, indent=1))


if __name__ == "__main__":
    main()
