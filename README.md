[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/akbare12/news-22-b14-by-field/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/akbare12/news-22-b14-by-field/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — Sunday 22 November 2026

**48 stories · 7 regions · 6 fields.** One image summing up Sunday 22 November 2026,
built to the top-20 pattern of this bounty: hero trio (COP31 NO DEAL, 186 drones
over Ukraine, Iran's claim of 2 US Patriot radars hit in Bahrain), a canonical
number strip (186 / 161 / 720/9 / 98.79% / $120bn / 50 / 258 / 11,613), a BY FIELD
bar, a "THE DAY IN UTC" timeline, 3 illustrated hero scenes, 12 illustrated
cards, a world map with numbered pins, and a DATE CHECK box (wires read up to
23:00 UTC, LEFT OUT with dates, NOT YET).

Every card carries a certainty chip — CONFIRMED (2+ outlets), REPORTED (carried
by the wires), CLAIM (one side, unverified), OFFICIAL (recorded result) — with
definitions in the footer. Scenes are drawn illustrations, not photographs.

## How it is built

`draw.py` (Pillow) draws `entry.png` (1024×1024, < 1 MiB). `main.py` is a
stdlib-only copy program: it copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, verifies the PNG header (1024×1024) and the
sha256, and never writes next to itself.

Run locally:

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources

AP · Reuters · BBC · Al Jazeera · Guardian · France 24 · Yonhap · Anadolu ·
SCMP · WHO · ATP · NBA · SpaceX · Detiknews

## License

MIT — see LICENSE.
