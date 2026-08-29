# v0.0.7

## New
- **Police stations.** New tool (key **5**, $200) that gives nearby houses
  crime protection. Bulldoze moved to key **6**.
- **Crime.** Houses outside every police station's coverage radius slowly
  build up crime; being covered brings it back down. High crime carries a
  small risk of a theft event that drains some money — build stations to
  keep it in check.
- **Road congestion.** Busy roads slow trucks down and show a red tint, so
  a single overloaded route is now visibly a bottleneck — add a second road
  to relieve it.

## Changed
- Save file format updated to support the above. **Old saves (v0.0.6 and
  earlier) will be marked invalid on this build.**

## Updating your save
If you're coming from v0.0.6 or earlier, convert your save first:
**[Converter](https://pycity.pages.dev/save_convert)** — runs entirely in your browser,
nothing is uploaded. Existing crime values default to 0 for everyone.

## Known gaps
- No dedicated art yet for the police station tile — flat color for now,
  same as any other missing asset.
- Crime, theft, and congestion numbers are first-guess placeholders, not
  balance-tested yet.