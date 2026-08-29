Tile art added — roads, houses, and factories now render with actual textures instead of flat colored squares.

- Road, house, and factory tiles now draw from PNG assets
- Fixed a build issue where texture loading conflicted with tile-type definitions
- Falls back to the old flat-color tiles if an asset fails to load, instead of crashing

Requires an `assets/` folder next to the executable (tile_0025.png, tile_0100.png, tile_0073.png).

Still very early alpha — expect bugs and missing features.