# news-image-20-nov-2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Gondok18-ui/news-image-20-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Gondok18-ui/news-image-20-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up Friday 20 November 2026's world news: the Shenzhen peace declaration, Russia's barrage on Ukraine, the ICJ's Myanmar genocide ruling, Anthropic's record IPO and the Microsoft 365 outage.

The image is a broadsheet-style front page drawn entirely in code (Pillow
primitives, no photographs): a masthead naming the day, the Shenzhen summit
as the lead story, four panels — Ukraine, the World Court ruling, Anthropic's
record IPO, the Microsoft 365 outage — and a ticker with GTA VI's launch,
the EU–UK Brussels summit, the Haiti raid and the tanker struck in the
Strait of Hormuz. Every story is drawn from that day's reporting.

`main.py` (standard library only) copies the rendered `entry.png` into the
output directory; `draw.py` is the artwork source that renders it.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=d6b9q93n&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
