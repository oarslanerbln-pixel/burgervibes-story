# Trend-Radar – Burger Vibes

Weekly check (Sunday evening) that adapts next week's stories to what is
happening. Trends serve the brand, never the other way round: a trend frame
still needs the neon look, real product footage and a true statement.

## Three layers

| Layer | Sources | Typical use |
| --- | --- | --- |
| 1. Calendar moments | the calendar below, German holidays, Berlin events | swap a hook frame, add a series |
| 2. Local situation | Berlin weather forecast (web search), football fixtures (Union, Hertha), school holidays | comfort food on rain/cold days, match-day hooks, takeaway |
| 3. Platform formats | web search for current Instagram/TikTok story and reel formats in Germany; Instagram's in-app "trending" audio (↗ arrow) | reuse a *format* (question, POV, "rate my …"), never someone else's footage |

## Rules

- **At most 3 changes per week**, and at most one trend frame per day. The weekday
  formats and the week theme stay; trends change the hook, not the plan.
- **Only footage we own** (assets/selects, footage/) and our own AI mood images.
  No memes made from film/TV stills, no other brands' logos, no celebrity faces.
- **No invented offers.** A discount, giveaway or "free fries" only when the user
  confirms it in writing. Giveaways need conditions of participation and Meta's
  promotion rules (see the agency prompt).
- **True facts only** (dates checked against a calendar, no guessed numbers).
- **Sensitive moments** (religious holidays, tragedies, politics): respectful tone or
  skip. Ramadan content is about iftar timing and community, never jokes.
- **Trending audio** is chosen by the user in the app (business-account library);
  the brief only names the mood or the trend to look for.
- Headlines stay unique across the month (`tools/plan.py` asserts it).

## Process

1. Read next week's slots from `tools/plan.json` (date mapping: `plan/schedule.json`).
2. Check the calendar below and search the web for: Berlin weather for the week,
   Berlin events/markets, Union/Hertha home games, current Instagram/TikTok
   trends in Germany (food and restaurants).
3. Propose up to 3 changes as a table: date, slot, current → proposed title/sub,
   clip, why (which signal). Write it to `plan/trends/<YYYY-MM-DD>.md` and send it.
4. Apply nothing until the user replies "onay" (or picks single changes). Then edit
   `tools/plan.py`, run it, commit and push.

## Calendar (verify dates each year)

| Date | Moment | Idea |
| --- | --- | --- |
| Fri 27.11.2026 | Black Friday | "BLACK FRIDAY? NEON FRIDAY." – no fake discount (in plan) |
| Sun 29.11.2026 | 1st Advent | "ERSTER ADVENT. ERSTER BURGER?" (in plan) |
| 01.–24.12. | Advent season | optional series "Burger-Adventskalender": one door per day (poll, fact, crew) |
| late Nov – 23.12. | Berlin Christmas markets | "Erst Glühwein, dann Burger." (only if open late enough) |
| Sun 06.12.2026 | Nikolaus | "Stiefel? Wir füllen lieber Bäuche." |
| 24.–26.12. | Christmas | opening hours story (ask the user) |
| 31.12. | Silvester | "Letzter Burger 2026?" + opening hours |
| 14.02.2027 | Valentine's Day | "Teilen? Nur mit Liebe." two-burger shot |
| ~08.02.2027 (expected, moon sighting) | Ramadan begins | iftar times, late opening if true, community tone |
| ~10.03.2027 (expected) | Eid al-Fitr | greeting story, family tables |
