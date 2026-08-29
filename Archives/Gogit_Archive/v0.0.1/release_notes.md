# gogit v0.0.1 — Release Notes

First working build of `gogit`: a Git-over-HTTP server written in Go,
built as a learning project to understand the git wire protocol from the
ground up. This release covers Milestone 1 — project scaffold — plus a
Windows build of the binary.

## What's in this release

- **Project scaffold**
  - Go module (`gogit`) with a clean `cmd/` + `internal/` layout
  - `cmd/gogit/main.go` — entrypoint with configurable flags:
    - `-addr` — address to listen on (default `:8080`)
    - `-repos` — directory containing bare repos (default `./data`)
  - `internal/server/server.go` — HTTP server setup and routing
- **HTTP server**
  - `GET /healthz` — health check endpoint, returns `ok`
  - Request logging middleware — logs method + path for every incoming
    request (groundwork for inspecting real git client traffic in later
    milestones)
- **Test data**
  - `data/testrepo.git` — a bare repo seeded with one commit (`README.md`),
    so there's something real to work with once clone/push support lands
- **Windows build**
  - `dist/gogit.exe` — cross-compiled Windows binary (`GOOS=windows
    GOARCH=amd64`), no local Go install required to run it

## What's *not* in this release yet

- No actual git protocol support — `git clone` / `git push` against the
  server don't work yet. That's the next chunk of milestones (ref
  advertisement, upload-pack, receive-pack).
- No web UI. A frontend (repo list, file browser, commit log) is planned
  after the git protocol milestones land.
- No auth.
- The server currently doesn't bundle a copy of `git` — later milestones
  that shell out to `git upload-pack` / `git receive-pack` will need git
  available on whatever machine runs the server (bundling a portable copy
  is on the list, not done yet).

## How to run

```
gogit.exe -addr :8080 -repos .\data
```

or from source:

```
go run ./cmd/gogit -addr :8080 -repos ./data
```

Verify it's up:

```
curl -i http://localhost:8080/healthz
```

Should return `HTTP/1.1 200 OK` with body `ok`.

## Known issues

- `../Go/bin/go`-style relative build scripts are not part of this
  project — build with a standard `go build` (or the provided
  cross-compiled `.exe`) rather than any script referencing a relative
  Go toolchain path.

## Next up

- Milestone 2: serve `GET /testrepo.git/info/refs?service=git-upload-pack`
  (pkt-line ref advertisement)
- Milestone 3: real `git clone` support via `git upload-pack
  --stateless-rpc`
- Frontend work begins after the git protocol milestones are solid