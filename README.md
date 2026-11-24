# 24 November 2026 — The World in One Image

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/yudhisutawan77/news-image-24nov/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/yudhisutawan77/news-image-24nov/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the [make.fun bounty "Sum up 24 November's world news in one image"](https://make.fun/bounty/news-image-20261124) — a $100 prize pool shared by the 50 best-ranked entries.

## The image

A newspaper front page summing up Tuesday **24 November 2026** in five stories, all events that happened or were first reported that day:

1. **Tragedy — Indonesia:** a factory fire kills at least 24 people, with around 30 missing.
2. **War at sea:** a Russian cargo ship is left ablaze after a drone strike off Finland.
3. **Climate — COP31:** the climate talks end with no fossil-fuel phase-out deal.
4. **Sport — Turin:** Carlos Alcaraz wins his first ATP Finals title.
5. **Markets:** Nvidia soars by roughly $1 trillion as Jensen Huang returns and tech rallies.

## How it runs

`main.py` (Python 3.13, standard library only, no network) copies `entry.png` — the 1024×1024 front page drawn for this entry — to `/output/entry.png`. The output is byte-identical on every run.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the entrypoint
- `entry.png` — the news image (1024×1024 PNG, ~114 KB)
- `draw.py` — the script that drew `entry.png` (kept for transparency; the entry itself only needs `main.py` + `entry.png`)

## License

MIT — see [LICENSE](LICENSE).
