# Caveman activation cost
> What does keeping caveman mode on cost per session, and does the compression it buys pay for it?

Open by Lucas's ruling (2026-08-15): **keep it on, and record the tradeoff to be assessed in depth
later.** It is filed here rather than in a ROADMAP because it is a measurement question, and the
measurement that would settle it has not been run.

## Method

The injected cost is measurable today:

```bash
node core/skills/caveman/hooks/activate.js < /dev/null | wc -c   # the SessionStart block
core/tools/wos/session/context                                   # its share of turn 1
```

The *saving* is not measured and that is the whole gap. What would settle it is an arm — the same
task run with `CAVEMAN_DEFAULT_MODE=off` and with `full`, comparing output tokens per turn on
comparable work. That needs the feature-toggle registry ([/ROADMAP.md](../../ROADMAP.md) Frente
10.4) to make the arm switchable cleanly, which is why this sits open rather than half-answered.

## Results

| Date | SessionStart block | share of turn 1 | per-turn reminder | output saved | Verdict |
|---|---|---|---|---|---|
| 2026-08-15 | 2,485 chars / ~654 tok | 2.4% | 121 chars | — | **Cost known, benefit unmeasured.** Kept on. |

The 2,485 chars are already a filtered subset, not the whole skill: `activate.js` strips `## Routing`,
filters the intensity table to the one active level, and cuts `modes.md` to the matching `- full:`
example — 271 chars survive of 2,359. Unfiltered it would be ~5,200. The four sub-command files
(`commit`, `review`, `compress`, `cavecrew` — 12.7 KB) are never injected.

`{"defaultMode": "off"}` in `~/.config/caveman/config.json` cuts it to 2 bytes; `activate.js:21`
already handles it. That is the arm, and it is one line.

## What changed

Nothing yet — deliberately. Lucas's call is that the register is worth 2.4% of turn 1 until someone
shows otherwise, and the honest position is that **nobody has measured the other side of the trade**.

## Limitations

- **The benefit side is unmeasured and cannot be inferred.** Output tokens per turn are visible in
  `usage`, but sessions differ so much in task shape that a before/after across sessions proves
  nothing without an arm.
- **The cost is not only the 654 tok.** It is re-read on every turn for the life of the session,
  which is cheap per token (cache reads are 0.1x) but not free.
- **Turning it off has a second cost nobody has priced**: `/caveman` must then be invoked by hand,
  and a mode that has to be remembered is a mode that will be forgotten.
