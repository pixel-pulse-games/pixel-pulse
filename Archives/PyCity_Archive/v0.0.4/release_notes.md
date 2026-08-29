## v0.0.4-alpha

### Economy: farms join the chain
Factories no longer make goods out of thin air — they need feeding. The supply chain is now two steps: farms grow food → trucks haul it to hungry factories → factories turn it into goods → trucks haul those to houses. Farm trucks run green, factory trucks stay the original orange.

- New **Farm** tool, key **4** (bulldoze moved to key **5**)
- Factories get a two-part meter now: food need on top, finished goods below
- Farms show a haybale icon once they've got enough grown to send a truck

### Assets reorganized
Tile art is now split by purpose instead of one flat folder:
- `assets/base/` — existing road/house/factory/grass tiles
- `assets/farm/` — farm building + haybale icons (Kenney Tiny Farm)
- `assets/winter/` — winter grass variants + street tile (Kenney Tiny Ski)
- `assets/april_fools/` — drop-in props, any filenames, no code changes needed

### Seasonal fun
- On April 1st (real-world date), the game quietly scatters random cosmetic props on empty tiles — never blocks building or roads
- During Dec/Jan/Feb (real-world date), grass and roads reskin to winter art automatically, with a graceful fallback to normal tiles if the winter assets aren't present yet

### Compatibility
Old savegame.dat files still load — the new farm tile type was appended to the end of the tile enum rather than inserted in the middle, so existing tile values didn't shift.