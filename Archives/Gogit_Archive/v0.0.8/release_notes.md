# gogit v0.0.8 — Release Notes

Something like GitHub Actions, but gogit runs it the way gogit runs
everything else: by shelling out to a real external tool (`act`)
rather than reimplementing a workflow engine, the same way it already
shells out to the real `git` binary instead of reimplementing the git
wire protocol from scratch.

## New: CI, on by default

Every repo `-init-repo` creates now gets a real git `post-receive`
hook installed automatically - git's own standard extension point,
not something gogit's HTTP layer invents. On push, the hook calls
back into the same gogit binary (`-ci-run`), which:

1. Checks out the pushed commit with `git archive | tar -x` into a
   temp directory (no `.git` in the result - see Known issues).
2. Looks for `.github/workflows/*.yml` - if there's none, the run is
   recorded as `skipped`, nothing else happens.
3. Runs `act push` against it, so existing GitHub Actions workflow
   files work as-is, no new syntax to learn.
4. Records status + full log under `<repo>.git/gogit-ci/runs/<id>/`.

New web UI: `/{repo}/actions` (run history) and
`/{repo}/actions/{run-id}` (full log), with an "Actions" tab added
next to Code/Commits.

Retrofit onto a repo created before this feature (or restore a
deleted hook):

    gogit -install-ci-hook -repos <dir> -repo-name <name>

## New: `act` is embedded, not a separate install

`act` itself ships inside `gogit.exe` now - one real binary per
platform, embedded via `go:embed` behind Go build tags so each
cross-compiled `gogit.exe` only carries its own platform's copy, not
all of them. First CI run extracts it to a `Binarys` folder next to
wherever the running `gogit` binary lives.

- Covers 9 of gogit's 10 build targets: windows/{amd64,386,arm64},
  linux/{amd64,386,arm64,arm}, darwin/{amd64,arm64}. Binaries are
  real downloads from nektos/act's own v0.2.89 GitHub release,
  verified against that release's own published checksums.txt before
  being committed here.
- **Known gap: windows/arm (32-bit ARM).** act's own releases don't
  publish a build for this target - confirmed against v0.2.89's
  checksums.txt, nothing to embed. `GOGIT_ACT_PATH` is the manual
  fallback on that one platform.
- `GOGIT_ACT_PATH`, if set, always wins - opts out of the embedded
  copy entirely and uses that binary/PATH lookup instead.
- `GOGIT_BINARYS_DIR` overrides where the embedded binary gets
  extracted to, if "next to gogit.exe" isn't right for a deployment.

Tradeoff worth knowing: cross-compiled `gogit.exe` itself is now
~29-32MB instead of ~10MB (each embedded `act` is ~20-22MB). Worth it
for "no separate act install," not free.

## What `act` still needs, separately

`act` needs a container engine to actually run a workflow's job
containers - Docker, or Podman via its Docker-API-compatible socket
(`GOGIT_CONTAINER_HOST`, passed through as `DOCKER_HOST`). That's a
full container runtime (namespaces, cgroups, and on Windows/macOS a
real Linux VM) - not a single static binary, can't be embedded the
way `act` itself was. Stays a separate install, same as it would for
a real GitHub Actions runner. Neither `act`'s nor Podman's own Go
internals are imported as libraries here either, for the same reason
- both are full projects with large dependency trees that would break
gogit's single-self-contained-binary approach.

## Real bug found and fixed: act's interactive first-run prompt

`act` prompts interactively ("choose a default image size") on its
own first run if it has no `.actrc` yet. Fine at a terminal - but
this always runs from a git hook with no TTY attached, where the
prompt just hangs on stdin forever. Confirmed live: a push blocked
until it hit end-of-input and exited with `EOF`. **Fixed:** gogit
pre-supplies `-P` image mappings for the common `runs-on` values
(ubuntu-latest/24.04/22.04/20.04, using the same `catthehacker`
images "Medium" would have picked), so the prompt is skipped
entirely rather than answered.

## Also fixed along the way (unrelated pre-existing bugs)

Found while touching the same files for the Actions tab, not part of
the CI feature itself:

- **`commits.html` and `tree.html` referenced `.Repo` in the
  template but the Go code passed `.RepoName`.** Confirmed live:
  template execution errored immediately (`can't evaluate field
  Repo`), so both pages were silently broken. Fixed to `.RepoName`.
- **`/{repo}/tree/` (no branch in the URL) 404'd.** This is exactly
  the link the repo list and the tab bar generate - clicking a repo
  from the homepage led straight to a 404. The handler required an
  explicit ref segment; it now resolves the repo's actual default
  branch (`git symbolic-ref --short HEAD`, not a hardcoded
  "main"/"master" guess - this project's own repos use "master")
  when none is given.

## Known issues

- windows/arm has no embedded `act` binary (see above) - install
  `act` separately and set `GOGIT_ACT_PATH` on that one platform.
- A container engine (Docker or Podman) is still a separate install
  - only `act` itself is embedded, not a runtime to run containers
  in.
- The temp checkout used for CI runs has no `.git` directory (it's
  built with `git archive`, not `git clone`), so `act` can't resolve
  `GITHUB_SHA`/`GITHUB_REF` from git itself the way it normally
  would. Confirmed live as a harmless warning in the run log, not a
  failure - but actions that specifically need a real `.git` present
  (rather than the values act injects from the workflow context)
  would be affected. Worth revisiting if that turns out to matter in
  practice.
- No cancel/re-run button - a bad run has to be fixed with a new
  push.
- No locking around concurrent runs on the same repo - two fast
  pushes in a row will run CI twice in parallel rather than queuing.
- The Basic-Auth-vs-session inconsistency (still not yet resolved,
  carried over from before this release).
- No rate limiting or lockout on failed logins (also carried over).

## How to verify this release

    gogit.exe -repos .\data -init-repo myproject
    git push http://localhost:8080/myproject.git main

...against a commit containing `.github/workflows/*.yml` - no
separate `act` install required. Check `/myproject/actions/<run-id>`
for the log; a `Binarys\act.exe` should appear next to gogit.exe
after the first run. With no container engine installed, the run
should end in `failed` with a clean "can't connect to Docker/Podman"
message in the log - that's the correct behavior for a server with
neither installed; a server with Docker or Podman running would
proceed to actually execute the workflow.
