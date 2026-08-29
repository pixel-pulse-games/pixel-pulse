# PyCity v0.0.8

Small update, one thing this time: the patcher can now update itself.

## Patcher self-update

Added `Bootstrap.exe` — a small helper that installs new versions of `Patcher.exe` automatically. Before this, the patcher had no way to update itself (a program can't overwrite itself while it's running), so it needed manual fixes if it ever needed changes. Now it can update on its own, same as it already does for the game.

`Bootstrap.exe` ships inside the main game download — you don't need to grab it separately. It just comes along for the ride next time you update.

Nothing changes for you day-to-day — the game updates the same way it always has. This just means future patcher fixes/updates can go out automatically instead of needing a manual reinstall.

## Upgrading

No save changes this time. Your saves from v0.0.7 work as-is.