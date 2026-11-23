# CLAUDE.md – Burger Vibes Studio

Content studio of the agency **1618 Digital** for the restaurant **Burger Vibes**
(@burgervibes.berlin, Tempelhofer Damm 134, 12099 Berlin; premium beef,
100 % halal, 90s neon look). This folder turns one monthly shoot into a month
of stories and reels.

- Chat with the user in **Turkish**. Text on stories/reels in **German**
  (audience), Gemini/Flow prompts in **English**, code comments in English.
- The user films once a month and drops the raw files into `footage/<YYYY-MM>/`.
  You plan, select, cut, animate and render. The user posts.

## Folder map

| Path | What |
| --- | --- |
| `footage/<YYYY-MM>/` | Raw monthly shoot. **Never modify or delete.** `_index/` is generated. |
| `assets/selects/` | Cut 9:16 clips, named by slot id (`W1-Mo-2.mp4`) |
| `assets/ai/` | Gemini images, named by slot id (`W1-Mo-1.png`) |
| `assets/fonts/` | Anton, Bebas Neue, Pacifico (local, no CDN) |
| `tools/plan.py` → `tools/plan.json` | The 4-week story plan (84 slots). Edit `plan.py`, then run it. |
| `plan/story-plan.html` | Same plan as a page (published copy: claude.ai/artifact/RHo2kgo4V7Kj1vXdVDFwi5) |
| `plan/selects.json` | Your edit decisions: slot → clip, in/out, crop, speed |
| `plan/reels/*.json` | Reel edit decisions (clips, hook, captions, CTA) |
| `plan/overrides.json` | Refined Gemini scenes after art-director rejects |
| `SHOTLIST.md` | What the user must film on shoot day, grouped by setup |
| `tools/` | Python pipeline (ffmpeg + Pillow) |
| `remotion/` | Remotion project: compositions `Story` and `Reel` |
| `output/` | Finished files. `stories/` (ffmpeg), `remotion/` (Remotion), `review/` |

## Monthly workflow

1. **Before the shoot:** update `SHOTLIST.md` for next month's plan (new week
   themes in `tools/plan.py`, never reuse a headline – `plan.py` asserts it).
2. **After upload:** `python tools/ingest.py footage/2026-12`
   Read every `footage/2026-12/_index/sheet-*.jpg` and `index.json`.
3. **Select:** write `plan/selects.json` – for every ECHT slot pick the best
   take, `in`/`out` seconds, crop centre `x`, `speed` (0.5 only on ≥50 fps).
   Prefer: product in frame within 0.5 s, steady, sharp, no strangers' faces.
   Missing shots → list them for the user instead of forcing a bad clip.
4. **Cut:** `python tools/cut.py` → `assets/selects/`
5. **AI images:** `python tools/generate.py --week 1` (needs `GEMINI_API_KEY`),
   then `python tools/check.py --week 1`, review `output/review/W1-*.jpg`
   against `tools/ART_DIRECTOR.md`, write `output/review/W1-verdicts.json`,
   `python tools/pipeline.py regen --week 1`.
6. **Render stories:** Remotion for the final look
   `cd remotion && node scripts/render-plan.mjs --week 1`
   (fast fallback without Node: `python tools/render.py --week 1`).
7. **Reels:** 3–4 per week. Write `plan/reels/<name>.json`, render with
   `node scripts/render-plan.mjs --reel plan/reels/<name>.json`.
8. **Check before handing over:** open frames at 0.3 s, 2 s, end. Headline
   readable, nothing in the top 250 / bottom 340 px, no typo, umlauts render.
9. **Hand over:** a short list per day: file, post time, sticker, music mood.

## Daily automation (cloud, every morning)

A scheduled task starts a fresh cloud session every morning (Berlin time) that runs
`python tools/today.py`. It maps the date onto the plan via `plan/schedule.json`,
generates today's Gemini images, renders what it can into
`output/daily/<date>/` and sends the files plus `brief.md` to the user's phone.
Slots whose real clip is missing are listed as "film today"; when the user
uploads the clip into that session, cut it to 9:16 (`tools/cut.py` logic) and render
it with `tools/story.py` using the slot's text. Exit code 2 means the 4-week plan
is used up: tell the user a new month must be planned (new themes in `tools/plan.py`,
no repeated headline, new `start_monday`).

**Posting rhythm:** one posting moment per day, 2–3 frames posted back to back
(`POST_TIME` in `tools/plan.py`: Mon–Thu 12:00, Fri–Sat 17:00, Sun 13:00, all
inside the opening hours Mon–Thu 12–24, Fri–Sun 12–01). Each day is one mini
story: hook → process → interaction. Never put a poll's result or a question's
answers in the same set as the poll itself; share them the next day.

## Rules (non-negotiable)

- **Product is always real footage.** No AI burger, patty or fries as a hero
  shot (German UWG: misleading advertising). AI only for mood, props, scenes.
  AI images get Instagram's "AI info" label.
- **People:** only with consent. Guests' faces never without permission.
  Reposts only from stories that tagged us.
- **Music** is never baked in. Business accounts use Instagram's commercial
  library in the app; no external tracks (GEMA). Exception: original sound
  from the shoot (`keep_audio: true`, e.g. sizzling).
- **Claims:** "100 % Halal", prices, opening hours, weights only as confirmed
  by the user. Never invent numbers for quizzes.
- **Instagram via the Chrome connection:** reading and drafting are fine.
  Changing the profile needs an explicit OK (show before → after). Never
  post, delete, send DMs/comments, start ads or spend money.
- **Impressum:** a German business account needs one reachable from the
  profile (§5 DDG). Flag it if it is missing.
- **Keys:** `GEMINI_API_KEY` lives in the user's environment, never in a file.
- **Footage is the source of truth.** Never overwrite `footage/`.

## Brand

Pink `#ff2d95`, cyan `#00e5ff`, ink `#0d0717`, cream `#fff4e6`. Headlines
Anton (uppercase), secondary Bebas Neue, accent script Pacifico (sparingly).
One accent per frame. Voice: German "du", warm Berlin, cheeky not cheap.
Motion: neon ignite / punch / ask presets; springs, no endless loops.

## Commands

```bash
python tools/ingest.py footage/<YYYY-MM>
python tools/cut.py [SLOT ...]
python tools/generate.py --week N [--model nano|imagen] [--dry-run]
python tools/check.py --week N
python tools/pipeline.py regen --week N
python tools/render.py --week N [--placeholder]
cd remotion && npm run studio            # live preview in the browser
cd remotion && node scripts/render-plan.mjs --week N [--day Mo] [--ids ...] [--placeholder]
cd remotion && node scripts/render-plan.mjs --reel plan/reels/<name>.json
python tools/plan.py                     # rebuild plan.json after editing plan.py
```
