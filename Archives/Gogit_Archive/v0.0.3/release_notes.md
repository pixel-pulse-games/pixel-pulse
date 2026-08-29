# gogit v0.0.3 — Release Notes

Milestone 3: clone/fetch. First release where a real, unmodified
`git clone` succeeds end-to-end against `gogit`.

## What's new in this release

- **`POST /testrepo.git/git-upload-pack`**
  - Handles the actual data transfer step of a clone or fetch
  - Client's POST body (pkt-line "want" list) is piped straight into
    `git upload-pack --stateless-rpc`'s stdin; its stdout (the
    packfile) is streamed straight back as the HTTP response — no
    protocol parsing done by `gogit` itself, the `git` binary does all
    of it
  - Transparently handles gzip-compressed request bodies
    (`Content-Encoding: gzip`), which some git clients send
  - **Verified against a real git client:**
    `git clone http://localhost:8080/testrepo.git` succeeds, and the
    resulting working directory has the correct `README.md` and the
    exact same commit as the seeded test repo

## What's *not* in this release yet

- `git push` still doesn't work — that's milestone 4
  (`git receive-pack`).
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
git clone http://localhost:8080/testrepo.git some-folder
```

Should print `Cloning into 'some-folder'...` and succeed with no
errors. `git -C some-folder log --oneline` should show the same
commit(s) as the seeded test repo.

## Known issues

- `../Go/bin/go`-style relative build scripts are not part of this
  project — build with a standard `go build` (or the released
  cross-compiled `.exe`) rather than any script referencing a relative
  Go toolchain path.

## Next up

- Milestone 4: real `git push` support via
  `POST .../git-receive-pack` and `git receive-pack --stateless-rpc`
- Milestone 5: multi-repo support (repos under a data directory,
  routed by URL path)
- Frontend work begins after the git protocol milestones (2-6) are
  solid