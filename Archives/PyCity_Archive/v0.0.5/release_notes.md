## v0.0.5

### Money & economy
Building things costs money now, and houses pay you back over time.

- Starting funds: **$500**
- Build costs: road **$10**, house **$50**, factory **$150**, farm **$100**
- Houses pay a flat tax over time, regardless of how well they're currently being served
- No debt — if you can't afford it, placement is just blocked, never goes negative
- Bulldozing refunds **50%** of a tile's build cost (not the full amount, so build-then-bulldoze isn't free money)
- Toolbar now shows each tool's cost and your current balance (turns red when you can't afford even a road)

### Auto-updater
`Patcher.exe` is bundled (not expermental) starting this version — checks the latest GitHub release, downloads the matching 32/64-bit build, and only replaces your install after verifying the download actually worked. Existing installs before this version need one last manual download to get the patcher; every version after this can self-update.

- Detects whether you're running the 32-bit or 64-bit build and grabs the matching update automatically
- Extracts to a staging folder and verifies it before touching your live files — a failed download or bad zip can never leave you with a half-updated game
- New `build.bat` option to build the patcher itself (built 32-bit deliberately, so one binary works on both 32-bit and 64-bit Windows)

### Compatibility
Old savegame.dat files still load — houses/factories/farms without a saved money value just start fresh at $500 instead of reading garbage.