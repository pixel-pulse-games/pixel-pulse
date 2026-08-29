# gogit v0.0.7c — Release Notes

This release covers the application itself. A lot happened since the
last app-focused notes (v0.0.7): a serious regression was found and
fixed, several real bugs were caught and corrected, and real per-repo
permissions were added - the missing piece that makes open account
registration actually safe.

## The big fix: `git clone` / `git push` are back

The web UI (login, register, repo list) had been rewritten in
`cmd/gogit/` as its own self-contained server, but never wired in
`internal/server` - the package containing the entire git protocol
implementation. Confirmed with a real test: `git clone` returned
`404`. The actual point of this project had silently stopped working.
**Fixed:** both halves now share one mux and one auth store
(`server.RegisterGitAndBrowseRoutes`). Verified again with a real
`git clone` - works.

## Security fixes

- **Passwords were being stored in plain text.** Replaced with real
  bcrypt, vendored by hand from `golang.org/x/crypto` (see
  `internal/vendored/README.md`). **Breaking change:** old plaintext
  entries in `users.txt` aren't valid bcrypt hashes - recreate
  accounts after upgrading.
- **"Private" repos were only private by name** (a `strings.Contains`
  check on the repo name, trivially defeated by renaming). **Fixed:**
  real `git config gogit.private` check, shared by the web UI and the
  git protocol layer.
- **Registering an existing username silently overwrote that user's
  password.** **Fixed:** `auth.AddUser` now rejects duplicates.
- **A stale-cache bug**: the git protocol layer cached a snapshot of
  the user store at server startup, so a newly-registered account
  couldn't push until the server restarted. **Fixed:** both sides now
  reload the (small, cheap) user file fresh on every check.

## New: per-repo permissions

The real prerequisite for safely opening registration. Each repo can
now have an **owner** and a list of **collaborators**, stored as git
config inside the bare repo itself:

- `-init-repo NAME -owner USERNAME` — sets the owner at creation
- `-add-collaborator USERNAME -repo-name NAME` — grants push access to
  an existing repo without changing who owns it
- A repo with **no** owner set stays open to any authenticated user
  (the same behavior every repo had before this feature existed - no
  breaking change for repos made before now)
- Push attempts by anyone else get `403 you don't have push access to
  this repo`, both at the ref-advertisement stage and the actual push

**Verified with a real permission matrix**: owner can push; a random
authenticated user cannot; adding that user as a collaborator makes it
work; a third user still cannot, even after the second was granted
access; legacy unowned repos remain open to anyone authenticated, as
before.

## Registration is now open

`/register` no longer requires being logged in - anyone reaching the
server can create an account (auto-logs in after signup, same flow as
typical public git hosts). This is safe **now** specifically because
of per-repo permissions above: a self-registered stranger can push to
repos they own or were added to, not to everything on the server.
Repos without an explicit owner are still the exception - those stay
open to any authenticated user regardless of who registered.

## Other bug fixed along the way

Repo list filter was `entry.IsDir() || strings.HasSuffix(name,
".git")` - an OR, meaning any directory at all (not just real bare
repos) showed up in the repo list. Fixed to `&&`.

## Known inconsistency, not yet resolved

The file browser and commit log for private repos still use HTTP
Basic Auth (a browser popup) rather than the session cookie the login
page sets, so browsing a private repo prompts a separate login even
when already signed in. Both paths are genuinely gated - this is UX
polish, not a security gap.

## How to verify this release

```
gogit.exe -repos .\data -init-repo myproject -owner alice
gogit.exe -userfile .\users.txt -create-user alice -password yourpassword
gogit.exe -addr :8080 -repos .\data -userfile .\users.txt
```

```
git push http://alice:yourpassword@localhost:8080/myproject.git master   # works
git push http://someoneelse:pw@localhost:8080/myproject.git master        # 403
```

Visit `/register` while logged out - should show a signup form
directly (not redirect to login).

## Known issues

- No rate limiting or lockout on failed logins.
- The Basic-Auth-vs-session inconsistency noted above.