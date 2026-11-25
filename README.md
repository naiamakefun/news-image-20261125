# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/naiamakefun/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/naiamakefun/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

**THE WEDNESDAY EDITION** — the whole of Wednesday 25 November 2026 on one broadsheet page.

Fifty stories that happened, or were first reported, on that single Wednesday, drawn as a
newspaper front page. Fourteen numbered panels carry the day's biggest stories, each with
its own drawn scene (no photographs, no icons): Shenzhou-24 carrying Pakistan's first
astronaut to China's Tiangong station, Asia's chip shares sliding as the AI rebound
stumbles, Washington readying new tariffs on China, the EU and 14 more economies, Iran
saying two tankers hit mines in Hormuz, Israel killing a second Hamas security chief in
a day, Russia's own figures implying almost 500,000 war dead in Ukraine, Xi's purge
taking a Politburo star, Puigdemont announcing the end of his nine-year exile,
the Solomon Islands signing with Australia and barring foreign bases, an Iowa town
emptied for the Army's detonation of five tons of rotting lead azide, ESA's Hera probe
sharing the first close-ups of the asteroid humankind moved, hostages freed as Colombian
forces stormed the Cartagena supermarket, RSF drone strikes killing 19 civilians in
Sudan's Blue Nile, and Gukesh taking White in game two of the world chess title match.

A further 36 stories run in the "Also on Wednesday" columns, a pinned world map shows
where the 14 numbered stories happened, and a DATE CHECK box names the big stories
deliberately left out because they belong to other days (Senegal's Cup title came back
on Tuesday; Sarkozy's trial order was Tuesday; the turkey pardon was Tuesday). Every
panel is tagged CONFIRMED or REPORTED with its source outlet, so nothing on the page
claims more than the reporting supports.

The image is generated entirely in code: `build_image.py` draws every panel, vignette,
map pin and column with Pillow and writes `entry.png` (1024 × 1024). `main.ts` is the
runtime entrypoint — it copies the committed `entry.png` into `$MAKEFUN_OUTPUT_DIR`
(default `output/` next to the script), creating the directory if needed, and verifies
the copy's PNG signature and byte length.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To rebuild the picture itself: `python3 build_image.py` (requires Pillow).

---
<sub>Entered on [make.fun](https://make.fun/?ref=naia&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
