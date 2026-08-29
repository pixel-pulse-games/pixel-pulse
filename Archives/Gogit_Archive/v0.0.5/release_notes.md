# gogit v0.0.5 — Release Notes

Milestones 5 and 6: multi-repo support and push authentication.
`gogit` now hosts more than one repo, and pushes require a real
username/password instead of being wide open to anyone who can reach
the server.

## What's new in this release

- **Multi-repo routing (Milestone 5)**
  - Routes are no longer hardcoded to `testrepo.git` — the repo name
    comes from the URL itself: `/{repo}/info/refs`,
    `/{repo}/git-upload-pack`, `/{repo}/git-receive-pack`
  - Repo names are validated against a strict allowlist
    (`^[A-Za-z0-9_-]+\.git$`), plus a second independent check that
    the resolved filesystem path is still actually inside the repos
    directory — two separate defenses against path traversal, not
    just one
  - **Verified against a real git client:** cloned two different
    repos by name (`testrepo.git` and a brand-new `secondrepo.git`
    created purely via the new CLI flag below) from the same running
    server; a path traversal attempt (`../../../../etc`, and a
    `%2f`-encoded variant) both correctly returned `400 Bad Request`
  - New CLI flag: `-init-repo NAME` creates a new bare repo under
    `-repos` and exits — the minimal repo-creation tool called for in
    the project plan (a proper `gh`-style CLI is a later idea, not
    part of this milestone)
- **Push authentication (Milestone 6)**
  - HTTP Basic Auth, backed by a flat file (`-userfile`, default
    `./users.txt`) — one `username:salt:hash` line per user
  - Reads (clone/fetch) stay open, unauthenticated, per the plan.
    Pushes (`git-receive-pack`, and its ref advertisement) require
    valid credentials
  - No users configured = all pushes denied (secure default, not
    fail-open)
  - New CLI flag: `-create-user NAME -password PASS` adds a user to
    the flat file and exits
  - **Verified against a real HTTP client and git client:**
    unauthenticated push attempts get `401 Unauthorized` with a
    `WWW-Authenticate` header; wrong password also gets `401`; correct
    credentials succeed and the pushed commit shows up on a fresh
    clone

## Known tradeoffs — read before relying on this for anything real

- **Password hashing is salted SHA-256, not bcrypt.** bcrypt
  (`golang.org/x/crypto/bcrypt`) is the standard choice for password
  storage, but building this milestone happened in an environment
  that couldn't fetch external Go modules to build-test against. This
  is a real simplification, not a stylistic choice — worth upgrading
  to bcrypt when convenient.
- **Flat file, not SQLite, for the user store.** Simpler, zero extra
  dependencies, fine at "one server process, a handful of users."
  Worth revisiting if `gogit` ever needs concurrent writes to the user
  store or many more users.

## What's *not* in this release yet

- No web UI (milestones 7-9).
- No bundled `git` — the server still shells out to whatever `git` is
  on `PATH`.
- No rate limiting or lockout on failed login attempts.

## How to run

```
gogit.exe -repos .\data -init-repo myproject
gogit.exe -userfile .\users.txt -create-user alice -password yourpassword
gogit.exe -addr :8080 -repos .\data -userfile .\users.txt
```

## How to verify this release

```
git clone http://localhost:8080/testrepo.git
git clone http://localhost:8080/myproject.git
git push http://localhost:8080/testrepo.git master
```
(third command should fail without credentials)

```
git push http://alice:yourpassword@localhost:8080/testrepo.git master
```
(should succeed)

## Known issues

- `../Go/bin/go`-style relative build scripts are not part of this
  project — build with a standard `go build` (or the released
  cross-compiled `.exe`) rather than any script referencing a relative
  Go toolchain path.

## Next up

- Milestones 7-9: web UI — repo list, file browser
  (`git ls-tree`/`git show`), commit log
- Stretch goals after that: Path B native pack file handling, README
  rendering, syntax highlighting, minimal issues feature