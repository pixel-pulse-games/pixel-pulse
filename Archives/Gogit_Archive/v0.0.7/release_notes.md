# gogit v0.0.7 — Release Notes

Milestone 9, milestone 9.5, and public/private repo visibility, all
in one release. `gogit` now has a commit log, a web-based way to add
users, and a real distinction between repos anyone can see and repos
that require credentials.

## What's new in this release

- **Milestone 9 — commit log**
  - `GET /{repo}/commits` — hash, author, date, and message for every
    commit on `HEAD`, via `git log`
  - Uses `\x1f` (unit separator) as the field delimiter when parsing
    `git log` output, not a printable character like `|` — a commit
    message containing a pipe would otherwise silently corrupt the
    parsing
  - Handles empty repos (no commits yet) without erroring
- **Milestone 9.5 — account creation UI**
  - `GET /admin/users/new` — a form to add a new user
  - `POST /admin/users/new` — creates the user and reloads the auth
    store immediately, no server restart needed
  - **Deliberately gated behind existing auth, not open signup.**
    `gogit` doesn't have per-repo permissions yet — any registered
    user can push to any repo — so open signup would mean anyone on
    the internet could register and immediately push to every repo,
    "private" or not. The first account still bootstraps via the
    `-create-user` CLI flag; this page is for adding more after that.
  - **Verified end to end, not just cosmetically:** created a user
    through the web form, then confirmed that exact user could
    successfully push a real commit — proving it writes usable
    credentials into the same store the CLI uses, not a decorative
    form.
- **Public/private repo visibility**
  - Stored as ordinary git config inside the bare repo itself
    (`git config gogit.private true`), not a separate state file
  - Repos with no such config are public by default — existing repos
    from before this feature keep behaving exactly as they did
  - Private repos now require auth for **reads too** (browsing,
    cloning), not just pushes
  - New CLI flag: `-init-repo NAME -private`
  - Repo list page now shows public/private badges, and filters
    private repos out of the anonymous view entirely
  - **Verified with a real, comprehensive test matrix:** anonymous
    dashboard view, authenticated dashboard view, anonymous browse of
    a private repo (401), authenticated browse (200), anonymous clone
    of a private repo (fails), authenticated clone (succeeds) — all
    confirmed against a running server, not assumed from reading the
    code

## Dashboard styling

Repo list page redesigned to look like an actual dashboard rather
than a bare bullet list — header with an "Add user" button (shown
only when authenticated), public/private badges per repo.

## What's *not* in this release yet

- No per-repo permissions — any registered user can push to any repo,
  public or private. This is why signup stays admin-gated (see above).
- No password reset / account deletion.
- No rate limiting or lockout on failed login attempts.
- No syntax highlighting, no README rendering on the repo page.

## How to run

```
gogit.exe -repos .\data -init-repo myproject
gogit.exe -repos .\data -init-repo secret -private
gogit.exe -userfile .\users.txt -create-user alice -password yourpassword
gogit.exe -addr :8080 -repos .\data -userfile .\users.txt
```

## How to verify this release

```
git clone http://localhost:8080/myproject.git         # should succeed, no auth needed
git clone http://localhost:8080/secret.git             # should FAIL, no credentials
git clone http://alice:yourpassword@localhost:8080/secret.git   # should succeed
```

In a browser: `http://localhost:8080/` anonymously should show only
public repos. Log in via `http://alice:yourpassword@localhost:8080/`
and both repos should appear, plus an "Add user" button. Click it,
create a second user, and confirm that new user can push.

## Known issues

- `../Go/bin/go`-style relative build scripts are not part of this
  project — build with a standard `go build` (or the released
  cross-compiled `.exe`).
- No per-repo permissions (see above) — treat this as "some repos are
  hidden from strangers," not "fully access-controlled."

## Next up

- Per-repo permissions (who can push to what) — the real prerequisite
  for ever considering open public signup
- Syntax highlighting, README rendering (stretch goals)
- A proper standalone CLI (parked idea, not started)