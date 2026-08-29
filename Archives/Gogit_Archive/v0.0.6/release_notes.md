# gogit v0.0.6 — Release Notes

Milestones 7 and 8, combined: the first web UI. `gogit` now has a
browsable interface, not just a protocol endpoint — you can see your
repos and their files in a browser, no `git` client required.

## What's new in this release

- **Milestone 7 — repo list**
  - `GET /` lists every bare repo (any directory ending in `.git`)
    found under `-repos`
- **Milestone 8 — file browser**
  - `GET /{repo}/tree/{path...}` — directory listing at any path,
    default branch (`HEAD`), with a `..` link back up
  - `GET /{repo}/blob/{path...}` — file contents at any path
  - Both shell out to `git ls-tree` / `git show` — consistent with
    the project's Path A approach, no manual git object parsing
  - **Verified against a real repo with real nested structure:**
    navigated from repo root into a subfolder, into a file, and back
    up via the `..` link, all by clicking through actual rendered
    pages
- **Styling** — a real embedded CSS file
  (`internal/server/static/style.css`), baked directly into the
  binary via Go's `embed` package. No external file needed at
  runtime — `gogit.exe` is still a single self-contained file.

## A real bug hit and fixed during this milestone

Initially tried serving the CSS via a `/static/` wildcard subtree
route. This **crashed the server at startup** — Go's router refuses
to register a `/static/` subtree alongside `{repo}` wildcard routes,
since it can't prove one pattern is strictly more specific than the
other (`{repo}` could theoretically equal `"static"`). Fixed by
serving the one CSS file at an exact literal route
(`GET /static/style.css`) instead of a wildcard subtree. Worth
remembering if more static files get added later — each currently
needs its own exact route, or the routing scheme needs a rework.

## Path safety note

File browser paths aren't real filesystem paths (they become
arguments to `git ls-tree`/`git show`, so `..` can't actually escape
anywhere) — but a path segment starting with `-` could be misread as
a `git` command-line flag. `validateBrowsePath` rejects that
explicitly. Verified: a crafted path like `/-status` correctly
returns `400 Bad Request` instead of reaching the `git` subprocess.

## What's *not* in this release yet

- No commit log page (milestone 9).
- No account creation UI (milestone 9.5) — users are still added via
  the `-create-user` CLI flag only.
- No public/private repo distinction — every repo is readable by
  anyone who can reach the server, same as milestones 5-6.
- No syntax highlighting, no README rendering on the repo page —
  stretch goals, not started.

## How to run

```
gogit.exe -addr :8080 -repos .\data -userfile .\users.txt
```

## How to verify this release

Open `http://localhost:8080/` in a browser. Should see a styled
(dark-themed) page listing your repos. Click into one, click into a
folder, click a file — should all render correctly with working
navigation, no manually-typed URLs required.

## Known issues

- `../Go/bin/go`-style relative build scripts are not part of this
  project — build with a standard `go build` (or the released
  cross-compiled `.exe`).
- Push is unauthenticated by repo — any registered user can push to
  any repo, no per-repo permissions yet.

## Next up

- Milestone 9: commit log
- Milestone 9.5: account creation UI (planned to stay gated behind
  existing auth, not open public signup — see project notes on why)
- Public/private repo visibility