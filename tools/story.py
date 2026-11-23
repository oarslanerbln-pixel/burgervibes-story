#!/usr/bin/env python3
"""Burger Vibes story renderer.

Turns one background (Flow image, Flow/real video, or nothing) plus a headline
into a 1080x1920 Instagram story MP4 with brand-consistent motion:

  neon   - headline glows pink/cyan and "ignites" with a short neon flicker
           (echoes the 90s neon sign inside the restaurant)
  punch  - heavy white headline slams in from the left, ease-out
  ask    - question in the upper third, the middle stays empty for the
           poll/quiz sticker that is added in the Instagram app

Text stays inside the story safe zone (top 250 px and bottom 340 px are
covered by Instagram UI). No music is baked in on purpose: business accounts
should add audio from Instagram's licensed library inside the app.
"""
import argparse
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
F_HEAD = os.path.join(FONTS, "anton-latin.ttf")
F_SUB = os.path.join(FONTS, "bebas-neue-latin.ttf")
F_SCRIPT = os.path.join(FONTS, "pacifico-latin.ttf")

PINK = (255, 45, 149)
CYAN = (0, 229, 255)
CREAM = (255, 244, 230)


def text_size(draw, text, font, spacing):
    box = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align="center")
    return int(box[2] - box[0]), int(box[3] - box[1]), box


def fit_font(path, text, max_w, start, spacing_ratio=0.08):
    size = start
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while size > 30:
        font = ImageFont.truetype(path, size)
        w, _, _ = text_size(probe, text, font, int(size * spacing_ratio))
        if w <= max_w:
            return font, int(size * spacing_ratio)
        size -= 4
    return ImageFont.truetype(path, size), int(size * spacing_ratio)


def render_text(text, path, out, start_size, color, glow=None, shadow=True, max_w=940):
    font, spacing = fit_font(path, text, max_w, start_size)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw, th, box = text_size(probe, text, font, spacing)
    pad = 90
    img = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
    origin = (pad - box[0], pad - box[1])

    def layer(fill):
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).multiline_text(origin, text, font=font, fill=fill,
                                           spacing=spacing, align="center")
        return lay

    if glow:
        # Stacked blurs: wide halo, tube glow, tight edge. Repeated passes make the
        # halo dense enough to read on bright food shots, not only on dark scenes.
        for radius, passes in ((40, 3), (18, 3), (7, 2), (2, 1)):
            g = layer(glow + (255,)).filter(ImageFilter.GaussianBlur(radius))
            for _ in range(passes):
                img = Image.alpha_composite(img, g)
    elif shadow:
        s = layer((0, 0, 0, 200)).filter(ImageFilter.GaussianBlur(14))
        img = Image.alpha_composite(img, s)
    img = Image.alpha_composite(img, layer(color + (255,)))
    img.save(out)
    return img.size


def render_shade(out, strength=0.55):
    """Top and bottom darkening so text reads on any Flow image."""
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = shade.load()
    for y in range(H):
        top = max(0.0, 1 - y / (H * 0.5)) * strength
        bottom = max(0.0, (y - H * 0.72) / (H * 0.28)) * strength * 0.9
        a = int(255 * min(0.85, top + bottom))
        for x in range(W):
            px[x, y] = (8, 4, 18, a)
    shade.save(out)


def render_tag(out, text):
    font = ImageFont.truetype(F_SUB, 46)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw, th, box = text_size(probe, text, font, 0)
    img = Image.new("RGBA", (tw + 120, th + 50), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=img.height // 2,
                        fill=(10, 6, 24, 190), outline=PINK + (255,), width=3)
    d.ellipse((30, img.height // 2 - 9, 48, img.height // 2 + 9), fill=CYAN + (255,))
    d.text((70 - box[0], 25 - box[1]), text, font=font, fill=CREAM + (255,))
    img.save(out)
    return img.size


def render_placeholder_bg(out):
    """Dark neon gradient, only used when no background is given (demos)."""
    bg = Image.new("RGB", (W, H), (12, 6, 26))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.ellipse((-300, 900, 700, 1900), fill=PINK + (150,))
    d.ellipse((500, 200, 1400, 1100), fill=CYAN + (110,))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    bg = Image.alpha_composite(bg.convert("RGBA"), glow)
    bg.convert("RGB").save(out)


def is_video(path):
    return os.path.splitext(path)[1].lower() in (".mp4", ".mov", ".webm", ".m4v")


def build(args):
    tmp = tempfile.mkdtemp(prefix="bv_")
    dur = args.dur
    fps = 30
    shade = os.path.join(tmp, "shade.png")
    render_shade(shade, 0.62 if args.preset != "punch" else 0.5)

    accent = PINK if args.accent == "pink" else CYAN
    title_png = os.path.join(tmp, "title.png")
    if args.preset == "neon":
        tw, th = render_text(args.title, F_HEAD, title_png, 190, (255, 240, 250), glow=accent)
    else:
        tw, th = render_text(args.title, F_HEAD, title_png, 170 if args.preset == "punch" else 150, CREAM)

    sub_png = None
    if args.sub:
        sub_png = os.path.join(tmp, "sub.png")
        sw, sh = render_text(args.sub, F_SCRIPT if args.script_sub else F_SUB, sub_png,
                             84 if args.script_sub else 96, accent if args.script_sub else CREAM,
                             glow=None, shadow=True)
    tag_png = os.path.join(tmp, "tag.png")
    gw, gh = render_tag(tag_png, args.tag)

    bg = args.bg
    if not bg:
        bg = os.path.join(tmp, "bg.png")
        render_placeholder_bg(bg)

    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if is_video(bg):
        cmd += ["-stream_loop", "-1", "-t", str(dur), "-i", bg]
        bg_chain = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
                    f"crop={W}:{H},fps={fps},setsar=1[bg]")
    else:
        cmd += ["-loop", "1", "-t", str(dur), "-i", bg]
        frames = int(dur * fps)
        # Upscale first: zoompan on a 2x canvas avoids the typical sub-pixel jitter.
        bg_chain = (f"[0:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,"
                    f"crop={W*2}:{H*2},zoompan=z='1+0.07*on/{frames}':"
                    f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={fps},setsar=1[bg]")
    for png in (shade, title_png, tag_png) + ((sub_png,) if sub_png else ()):
        cmd += ["-loop", "1", "-t", str(dur), "-i", png]

    # Headline position: upper third, below the 250 px Instagram header zone.
    pad = 90
    ty = 300 - pad if args.preset == "ask" else 360 - pad
    t0, d0 = 0.25, 0.4
    if args.preset == "punch":
        title_ov = (f"overlay=x='(W-w)/2-1300*pow(max(0,1-(t-{t0})/{d0}),3)':y={ty}")
        title_in = "[2:v]format=rgba[ti]"
    else:
        title_in = f"[2:v]format=rgba,fade=t=in:st={t0}:d={d0}:alpha=1[ti]"
        title_ov = f"overlay=x='(W-w)/2':y='{ty}+70*max(0,1-max(0,t-{t0})/{d0})'"
        if args.preset == "neon":
            title_ov += ":enable='not(between(t,0.48,0.53)+between(t,0.62,0.65)+between(t,0.74,0.76))'"

    chain = [bg_chain, "[bg][1:v]overlay=0:0[b1]", title_in, f"[b1][ti]{title_ov}[b2]"]
    last = "b2"
    if sub_png:
        # Both PNGs carry `pad` of transparent margin for the glow/shadow.
        sub_y = ty + th - 2 * pad + 56
        s0 = 0.95
        chain.append(f"[4:v]format=rgba,fade=t=in:st={s0}:d=0.4:alpha=1[si]")
        chain.append(f"[{last}][si]overlay=x='(W-w)/2':y='{sub_y}+40*max(0,1-max(0,t-{s0})/0.4)'[b3]")
        last = "b3"
    # Footer tag sits just above the bottom UI zone (reply bar).
    chain.append(f"[3:v]format=rgba,fade=t=in:st=1.3:d=0.4:alpha=1[gi]")
    chain.append(f"[{last}][gi]overlay=x='(W-w)/2':y={H - 340 - gh - 30}[b4]")
    chain.append("[b4]format=yuv420p[out]")

    cmd += ["-filter_complex", ";".join(chain), "-map", "[out]"]
    if is_video(args.bg or "") and args.keep_audio:
        cmd += ["-map", "0:a?", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-t", str(dur), "-r", str(fps), "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", args.out]
    subprocess.run(cmd, check=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bg", help="Flow image/video or real footage; empty = neon placeholder")
    p.add_argument("--title", required=True, help="Headline, use \\n for line breaks")
    p.add_argument("--sub", default="", help="Second line")
    p.add_argument("--script-sub", action="store_true", help="Second line in neon script font")
    p.add_argument("--preset", choices=["neon", "punch", "ask"], default="neon")
    p.add_argument("--accent", choices=["pink", "cyan"], default="pink")
    p.add_argument("--tag", default="BURGER VIBES  ·  TEMPELHOFER DAMM 134")
    p.add_argument("--dur", type=float, default=6.0)
    p.add_argument("--keep-audio", action="store_true", help="Keep the audio of a video background")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    a.title = a.title.replace("\\n", "\n")
    a.sub = a.sub.replace("\\n", "\n")
    build(a)


if __name__ == "__main__":
    main()
