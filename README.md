# One day's news, one image — Tuesday 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/agungvg/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/agungvg/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A newspaper front page that sums up the world news of Tuesday 17 November 2026 — built for make.fun's “Sum up 17 November's world news in one image” bounty ($250 in USDC).

## What the picture shows

Five stories lead the page, each with its own drawn illustration, a headline and a short summary:

- **Ukraine strikes the Kerch Bridge** — a road span collapses.
- **Trump lands in Manila** for the ASEAN summit, with a trade pact with Thailand.
- **Two tankers hit mines in the Strait of Hormuz**; a third US carrier moves in.
- **Estonia moves to shut its Russia border crossings** from 1 December.
- **Japan scrambles jets** as Russian aircraft enter its airspace.

An ALSO strip underneath carries three more: Depardieu pleads guilty in Paris, JPMorgan blames a software bug for its banking outage, and the UN counts 1,390 civilians killed in Sudan. Every story was cross-checked across BBC, AP, Reuters, Al Jazeera and NPR.

## How it is made

The front page is drawn from scratch with Pillow in `draw.py` — gradients, silhouettes and flat shapes, DejaVu fonts, no photos and no network. The drawing is fully deterministic: run it twice and the bytes are identical. The committed render is `entry.png` (1024×1024 PNG).

`main.py` is the entrypoint. It does not redraw anything; it copies the committed `entry.png` to the grader's output folder and checks the copy is complete, byte for byte.

## Run it

```sh
python3 main.py
```

That writes `entry.png` to `/output`. Point it somewhere else with the environment variable:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=D6L18X&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
