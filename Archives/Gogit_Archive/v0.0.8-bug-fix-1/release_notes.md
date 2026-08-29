# gogit v0.0.8-bug-fix-1 — Release Notes

Small patch on top of v0.0.8. See that release for the CI feature
itself (act via post-receive hook, embedded per-platform).

## Fixed: /{repo}/commits/ and /{repo}/actions/ 404'd with a trailing slash

Go's `net/http` mux treats a route pattern without a trailing slash
as an exact-path match only. `/{repo}/commits` and `/{repo}/actions`
were registered that way, but every template's own tab bar links to
`/{repo}/commits/` (trailing slash included) - so clicking "Commits"
from anywhere in the UI 404'd. Confirmed live via screenshot before
fixing.

Same underlying cause as the `/{repo}/tree/` 404 fixed in v0.0.8 -
this patch closes the two routes that fix missed. Registered explicit
trailing-slash variants for both, in both places server.go builds a
mux. No handler changes needed - both already trim the path before
parsing it.
