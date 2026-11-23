[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/indonlol123/news-image-20261123-r2-makefun/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/indonlol123/news-image-20261123-r2-makefun/reward.svg)](https://make.fun/bounty/news-image-20261123)

# The World in a Day — 23 November 2026 (round 2)

A one-page newspaper front page summing up the world's news of Monday
23 November 2026, for the [make.fun bounty](https://make.fun/bounty/news-image-20261123)
"Sum up 23 November's world news in one image". This is a second-round
entry, rebuilt from scratch with a denser page: 28 stories instead of 12.

Lead story: COP31 in Antalya collapses with no deal — the longest UN
climate summit ever — after nearly 200 nations reject a draft that never
names fossil fuels. Also on the page: Ukraine sinking the Russian corvette
Merkury off Libya, the Dymer strike, NATO's emergency session over Russian
missiles in Poland, Iran's strikes on Bahrain and tankers in the Gulf, the
Democrats' 258-seat House win (their biggest since 1992), the AI market
rout (Nikkei −5.1%), and Alcaraz winning his first ATP Finals title.

## Run

```sh
python3 render.py          # rebuild entry.png (1024x1024, deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copy it to out/entry.png
```

`main.ts` (Node 22, stdlib only) checks the pre-rendered `entry.png`
(PNG magic bytes, ≤ 1 MiB) and copies it into `$MAKEFUN_OUTPUT_DIR/entry.png`.
No network, no randomness: every run writes the same bytes.

## Files

- `main.ts` — entry point
- `render.py` — draws `entry.png` with Pillow (Noto fonts)
- `entry.png` — the front page, 1024x1024 PNG
