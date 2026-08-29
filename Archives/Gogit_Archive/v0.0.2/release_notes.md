# gogit v0.0.2 — Release Notes

Milestone 2: ref advertisement. First release where `gogit` actually
speaks part of the git protocol — a real `git` client can now ask the
server what it has.

## What's new in this release

- **`GET /testrepo.git/info/refs?service=git-upload-pack`**
  - Serves the ref advertisement a git client requests before any
    clone or fetch
  - Response is proper pkt-line format: a `# service=git-upload-pack`
    line, a flush-pkt, then the repo's refs (via
    `git upload-pack --stateless-rpc --advertise-refs`), then a final
    flush-pkt
  - **Verified against a real git client:** `git ls-remote
    http://localhost:8080/testrepo.git` correctly lists `HEAD` and
    `refs/heads/master` against the seeded test repo
- **Internal restructure:** handlers now have access to server state
  (`reposRoot`) via a small `server` struct, replacing the previous
  stateless handler functions — needed since routes now have to know
  where repos live on disk

## What's *not* in this release yet

- `git clone` / `git push` still don't work — ref advertisement only
  tells a client what exists, not how to fetch it. That's milestones
  3 (clone/fetch) and 4 (push).
- Still hardcoded to a single repo (`testrepo.git`) at a fixed URL
  path — multi-repo routing is milestone 5.
- No web UI, no auth (milestones 6-9).
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
`testrepo.git.disabled` — rename or copy it to the exact name for
this to work).

## How to verify this release

```
git ls-remote http://localhost:8080/testrepo.git
```

Should print two lines — `HEAD` and `refs/heads/master` — both
showing the same commit hash as the seeded test repo.

## Known issues

- `../Go/bin/go`-style relative build scripts are not part of this
  project — build with a standard `go build` (or the released
  cross-compiled `.exe`) rather than any script referencing a relative
  Go toolchain path.

## Next up

- Milestone 3: real `git clone` support via
  `POST .../git-upload-pack` and `git upload-pack --stateless-rpc`
- Milestone 4: real `git push` support via `git receive-pack`
- Frontend work begins after the git protocol milestones (2-6) are
  solid