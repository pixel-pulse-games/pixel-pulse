# PyCity v1.0.0-rc.1

First release candidate. Skipping a separate beta phase — this build folds
together everything from v0.0.7 through v0.0.9, plus a round of bug fixes
and cleanup done specifically for this RC.

## What's new since v0.0.9

- **Distinct resource chains.** Farms, factories, and houses are each
  randomly assigned to one of two independent economy chains — Grain/Bread
  or Timber/Furniture — when placed (small gold/teal corner dot shows
  which, legend in the top bar). Trucks only move cargo within the same
  chain, so a healthy city needs a mix of both, not just "more farms."
- **Camera zoom.** Mouse wheel or `+`/`-`, 0.5x–2.0x, zoomed toward screen
  center.
- **Crime & police.** Houses outside a police station's coverage slowly
  build up crime; high crime risks periodic theft events that drain money.
  Build police stations to keep it in check.
- **Road congestion.** Heavily-trafficked road tiles slow trucks down and
  show a red tint — a second parallel road relieves a choke point.
- **Balance pass.** House tax, crime growth/theft frequency, and
  congestion decay were retuned from the original placeholder values.

## Fixed for this RC

- **Building placement no longer charges for nothing past the building
  cap.** Placing a house/factory/farm/police station now checks the
  internal building limit *before* taking your money — previously, once
  you hit the cap, the tile would still get painted and charged for, but
  silently never join the economy (no demand, no meters, no trucks).
- Broken "Source" link on the download page.
- The "latest version" box on the download page was pulling from the
  wrong GitHub repo entirely — fixed.
- Beta download page updated to point at the current build.
- Removed a stray compiled build artifact that had been accidentally
  committed to the repo, and tightened `.gitignore` so it can't happen
  again.

## Known limitations / feedback welcome

This is a release candidate, not a beta — the tradeoff is that a couple
of things haven't been stress-tested by outside players yet:

- **Balance numbers** (house tax rate, crime growth/theft odds, congestion
  decay) were tuned from math, not from real multi-player sessions. If
  something feels too punishing or too easy, say so — these are very
  likely to get a follow-up tuning pass based on actual feedback.
- **Resource chains are assigned randomly** with no way to see or choose
  a building's chain before placing it. If this reads as frustrating
  rather than as an interesting constraint once more people are playing,
  a toolbar preview/toggle is the natural follow-up.
- Zoom range and camera pan speed were picked by feel, not tested widely.

Bug reports and balance feedback are genuinely welcome — this build is
functional and playable, but real-world play is still the fastest way to
find what needs adjusting next.

## Saves

Save format is `PCI3`, unchanged since v0.0.9. If you're updating from a
build older than v0.0.9, your save won't load — convert it first:
[Update Your Saves](https://pycity.pages.dev/save_convert.html)
(runs entirely in your browser, nothing is uploaded).

## Requirements

- Windows 10 or newer
- Under 200 MB free space