PyCity v0.0.6 

No game changes in this release — same game as v0.0.5.

Patcher fixes only:
- Auto-updater now verifies a SHA256 checksum before installing any
  update.
- Fixed Patcher.exe wrongly triggering a Windows admin (UAC) prompt.

If you're on v0.0.5, see EMERGENCY_README.txt — one manual step is
needed since the patcher can't update itself.

Assets in this release:
  pycity-win64.zip / pycity-win32.zip   game files with Patcher.new
  Patcher.zip                           contains Patcher.exe
  checksums.txt                         required by the auto-updater