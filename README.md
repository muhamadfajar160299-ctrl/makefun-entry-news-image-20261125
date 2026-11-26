# The World in One Day — Wednesday 25 November 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![make.fun entry](https://img.shields.io/badge/make.fun-news--image--20261125-blue.svg)](https://make.fun/c/news-image-20261125/)
[![Size: 1024×1024](https://img.shields.io/badge/Image-1024%C3%971024-green.svg)](entry.png)

One image summing up the world's news of **Wednesday 25 November 2026**,
built for the [make.fun](https://make.fun/c/news-image-20261125/)
`news-image-20261125` competition.

## What it is

A dense cream broadsheet: 31 stories across 9 regions, 3 lead stories
(Hormuz tanker mines, the Wall Street AI sell-off, Shenzhou-24 docking
with Pakistan's first astronaut), 13 illustrated reports, a "Rest of the
Day" list, a Day in Numbers sidebar, a UTC timeline, a sketch world map,
and Date Check / How Sure boxes. Every dated event was checked against
news reported on 25 November 2026; one-sided claims are marked ◐, and
events from Tuesday 24 November that were first reported on Wednesday
are marked "Tue". Every picture is drawn programmatically — no photographs.

## Files

- `entry.png` — the entry image, 1024×1024, under 1 MiB, deterministic.
- `main.py` — the entry point. Standard library only: it copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`).
- `render.py` — the program that draws `entry.png` with Pillow
  (used at build time only; the grader never runs it).

## Run it

```sh
python3 render.py            # redraw entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy it to out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
