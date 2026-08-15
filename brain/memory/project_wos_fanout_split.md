---
name: project_wos_fanout_split
description: core/hooks and core/tools split into families 2026-07-31 (every CLI path changed); a fanout split only counts once each new dir has its own CONTEXT.md
metadata: 
  node_type: memory
  type: project
  originSessionId: bc9d38a2-0e9c-4b0c-bf0a-6f4c93630029
  modified: 2026-08-01T05:40:06.130Z
---

**Every `core/tools/` CLI path changed on 2026-07-31.** The flat 37-file directory became
eight families, and Lucas chose the breaking rename over a named exception when asked.
`core/tools/search` → `core/tools/web/search`, `gmail` → `google/gmail`, `papers` →
`paper/papers`, `video` → `video/video`, `sync-skills` → `wos/sync-skills`. Only
`google_auth.py` and `attachments_util.py` stay at the root, by a rule worth reusing: a
module imported by more than one family lives at the root, a module imported by exactly one
lives beside it. `core/hooks/` split the same day, 50 files → a root of 6 (the two law
modules, `hook_input.py`, and the three entrypoints git and settings.json name) plus 13
responsibility directories. **Check `core/tools/CONTEXT.md` before invoking any tool from
memory — a remembered path from before this date is wrong.**

**The non-obvious part, and the reason this is worth remembering.** The fanout check counts
code files per directory, but `context_synchronizer` folds any directory under `WARN_FILES`
back into its parent's routing table. So moving files satisfies the count while leaving the
reader exactly as much to hold — the first pass on `core/hooks` took its table from 50 rows
to *55*. A fanout split only pays off once **each new directory declares itself with its own
`CONTEXT.md`**; with those, the tables went 50 → 19 and 37 → 12. A split that leaves the
parent table the same size gamed the check rather than answering it.

**Why:** the fanout signal exists to bound what one directory asks a reader to hold. The
count is a proxy for that, and the proxy is satisfiable without the thing it proxies for.

**How to apply:** when draining fanout in any repo — the remaining work is all nested repos
(`isoroll-content/src/pipeline` 55, `aiwbot/tests` 51, `aiwbot/frontend` 38) — split by
responsibility, write a real one-line description into each new `CONTEXT.md`, then check the
parent's row count actually fell. Related: [[project_verify_roadmap]], [[project_core_schema]].
