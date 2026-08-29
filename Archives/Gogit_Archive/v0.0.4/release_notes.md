# gogit v0.0.4 — Release Notes

Milestone 4: push. First release where a real, unmodified `git push`
succeeds end-to-end against `gogit` — the server now writes data, not
just serves it.

## What's new in this release

- **`GET /testrepo.git/info/refs?service=git-receive-pack`**
  - Ref advertisement for push, mirroring milestone 2's fetch-side
    advertisement but via `git receive-pack --advertise-refs`
    (different capabilities: `report-status`, `delete-refs`, etc.)
- **`POST /testrepo.git/git-receive-pack`**
  - Handles the actual push data transfer: client's packfile + ref
    update instructions piped into
    `git receive-pack --stateless-rpc`'s stdin, its report-status
    response streamed straight back
  - `handleInfoRefs` generalized to serve either service
    (`git-upload-pack` or `git-receive-pack`) instead of only fetch
  - **Verified against a real git client, full round trip:**
    cloned, committed a real change, `git push`ed it, then did a
    completely fresh `git clone` from scratch and confirmed the
    pushed commit and file content were actually there — not just
    that the push command exited cleanly

## What's *not* in this release yet

- **No auth — push is currently wide open.** Anyone who can reach the
  server can write to it. This matches the plan (auth is milestone 6)
  but means this build should only run somewhere trusted/local, never
  exposed publicly as-is.
- Still hardcoded to a single repo (`testrepo.git`) at a fixed URL
  path — multi-repo routing is milestone 5.
- No web UI (milestones 7-9).
- No bundled `git` — the server still shells out to whatever `git` is
  on `PATH`.

## How to run

```
gogit.exe -addr :8080 -repos .\data
```

or from source:

```
go run ./cmd/gogit -addr :8080 -repos ./data
```

Requires a real bare repo at `<repos>/testrepo.git` (not
`testrepo.git.disabled` — rename or copy it to the exact name).

## How to verify this release

```
git clone http://localhost:8080/testrepo.git test1
cd test1
echo "hello" >> README.md
git add README.md && git commit -m "test push"
git push origin master
```

Should succeed with output like `<old-hash>..<new-hash>  master ->
master`. Then, to confirm it's real:

```
git clone http://localhost:8080/testrepo.git test2
```

`test2` should show your pushed commit and file change.

## Known issues

- `../Go/bin/go`-style relative build scripts are not part of this
  project — build with a standard `go build` (or the released
  cross-compiled `.exe`) rather than any script referencing a relative
  Go toolchain path.
- No auth on push (see above) — do not expose this build publicly.

## Next up

- Milestone 5: multi-repo support — repos under a data directory,
  routed by URL path, instead of hardcoded to `testrepo.git`
- Milestone 6: HTTP Basic Auth, at minimum required for pushes
- Frontend work begins after milestones 4-6 are solid