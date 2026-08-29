# gogit v0.0.9 — Release Notes

Repos are now namespaced: `/{owner}/{repo}` instead of the flat `/repo` 
layout. Every repo lives under a user directory on disk 
(`data/{owner}/{repo}.git`) and on the web. Users can browse an index 
of all users, then click through to each user's repo list.

## Major: Repo namespacing

Every repo now has a required owner (username) set at creation time. 
The git URLs, web URLs, and storage layout all reflect this:

- **URLs:** `/alice/myproject` instead of `/myproject`
- **Storage:** `data/alice/myproject.git` instead of `data/myproject.git`
- **API:** `-init-repo myproject -owner alice` (owner is now required)

Existing repos can be upgraded with `-migrate-to-namespaced` (see below).

## Major: Per-user pages

Clicking a repo from the homepage now goes to `/{username}`, a page listing 
all of that user's repos, rather than directly to the repo. The homepage 
itself is now a user index (`/`) - an index of every user who owns at least 
one repo, each linked to their per-user page.

In other words:
- Flat list of all repos → index of users → click a user → list of that user's repos
- Each repo now lives at `/{owner}/{repo}/` rather than `/{repo}/`

## Major: One-time migration command

Repos created before v0.0.9 live flat (`data/myproject.git`) with no owner 
namespace. Migrating them:

    gogit -repos ./data -migrate-to-namespaced

This command:
- Backs up the entire repos directory first (timestamped sibling 
  directory, deletable once you've verified the migration)
- Moves each flat repo to `{owner}/{repo}.git` based on its `gogit.owner` 
  git config (or to `_unowned/` if no owner was set)
- Is safe to run again if interrupted - already-migrated repos are skipped
- Prints a summary at the end

After migration, the old flat URLs like `/myproject/tree/` will 404; repos 
are addressed at `/{owner}/myproject/tree/` from then on.

## Fixed bugs

Found and fixed while implementing namespacing:

- **Tree page broke on actual files:** `.LinkPath` and `.ParentPath` fields 
  were missing, and the "up a directory" link was missing its `{ref}` 
  segment. Fixed: both now work correctly; navigating into subdirectories 
  and back up to the root works as expected.
- **Commit list page broke on actual commits:** `.ShortHash` field was 
  missing from the template. Fixed: commit hashes now display.
- **Route mux panics on startup:** Adding the bare `/{username}` route 
  created ambiguity with unprefixed `/login`, `/register`, etc. Go's mux 
  panics on such conflicts at startup. Fixed: gave those routes explicit 
  `GET`/`POST` method prefixes.

## Command-line changes

- `-init-repo NAME` now requires `-owner USERNAME` (it was optional before, 
  defaulting to unowned)
- `-add-collaborator` and `-install-ci-hook` now require both `-owner` and 
  `-repo-name` (they took only `-repo-name` before)
- New flag: `-migrate-to-namespaced` runs the one-time migration for 
  upgrading a pre-v0.0.9 reposRoot

## Internals

All handlers now receive both `{owner}` and `{repo}` URL segments instead 
of just `{repo}`. The storage and permission model is unchanged: repo 
ownership is still stored in `git config gogit.owner` and checked via 
`internal/server.RepoOwner()` and `internal/auth.CanPush()`. This migration 
is purely about addressing repos hierarchically rather than in a flat pool.

## Known issues carried over

- Basic-Auth vs. session cookie inconsistency (web UI uses sessions; git 
  protocol uses Basic Auth; not unified)
- No rate limiting on login attempts
- No cancel/re-run button for CI runs; bad runs need a new push to retry
- No locking around concurrent CI runs on the same repo - fast pushes run 
  in parallel
- The CI temp checkout has no `.git` directory, so `act`'s built-in 
  `GITHUB_SHA`/`GITHUB_REF` resolution from git doesn't work (act injects 
  these from the workflow context instead; confirmed harmless)

## How to upgrade

1. Backup your `data/` directory manually if you want extra safety.
2. Run `gogit -repos ./data -migrate-to-namespaced`
3. Verify the migrated repos by browsing the homepage or running `git clone`.
4. Update any git remotes in your local clones from 
   `http://host/myproject.git` to `http://host/{owner}/myproject.git`
5. Optionally delete the `data-backup-*` directory once you're confident.

Going forward, all new repos must be created with `-owner`:

    gogit -init-repo myproject -owner alice
