# Measure it yourself

Do not take the claims on trust. Trikeel is a pattern; whether it helps **you** is an empirical question. Here is a small, honest protocol.

## Protocol

1. **Pick 3 comparable slices** of work (similar size and difficulty), for example three small features or three bug fixes.
2. **Run each under both setups** if you can: once with your current prompt style (baseline) and once with Trikeel. If the work cannot be repeated, alternate: slice A baseline, slice B Trikeel, slice C baseline, and so on.
3. **Log the same metrics** every time (below).
4. **Compare medians**, not single runs. Agent variance is large.

## Metrics

| Metric | How to get it |
|---|---|
| Input + output tokens | Your tool's usage readout |
| Turns to "done" | Count of human messages |
| Gate or test failures before green | Count of red runs |
| Rework | Lines changed *after* you first declared it done |
| Wall-clock time | Stopwatch |
| Out-of-scope edits | Files touched that the slice did not need |
| Secret exposure | Any value printed or committed (should be zero) |

## Log template

Copy into a spreadsheet:

| Slice | Setup (baseline / Trikeel) | Tokens in | Tokens out | Turns | Red runs | Rework (lines) | Minutes | Out-of-scope files | Notes |
|---|---|---|---|---|---|---|---|---|---|
| A | baseline | | | | | | | | |
| B | Trikeel | | | | | | | | |
| C | baseline | | | | | | | | |

## Caveats

- Tiny samples are noisy. Treat 3 slices as a sanity check, not proof.
- Learning effects: you improve at specifying work over time. Alternate setups to reduce this bias.
- Model and tool versions matter. Record them.
- If Trikeel does **not** help on your work, that is useful information. Open an issue.
