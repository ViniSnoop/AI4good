# Tools
> CLI tools callable via bash, one directory per family; routing block auto-synced on save.

**A family directory is a capability; the tool inside it is the provider.** `mail/gmail`,
`calendar/gcalendar`, `files/gdrive` — swapping a provider changes a leaf, never a family.
This is [CONTEXT.md](../CONTEXT.md)'s provider-agnostic rule applied to the path: function in
the directory, vendor at the file. Ruled 2026-08-14, after one folder (`google/`) spent months
classifying on a different axis from all its siblings and no rename ever felt right.

Two moves have changed every tool path here: the 2026-07-31 fanout split (`core/tools/search`
→ `core/tools/web/search`) and the 2026-08-14 capability move (`core/tools/google/drive` →
`core/tools/files/gdrive`). Both were done as one sweep. **A third is not free** — check
[`ROADMAP.md`](../ROADMAP.md) before proposing one.

Only `attachments_util.py` (mail + video) still sits at this root. Auth is a family of its own,
`auth/gauth.py`, because it is shared across families rather than owned by any.

Call any tool via bash:
```
core/tools/web/search "relativistic raytracing GPU"
core/tools/paper/papers "Schwarzschild geodesics" --cat gr-qc --n 15
core/tools/mail/gmail sync --since 7
core/tools/calendar/gcalendar upcoming --days 7
core/tools/files/gdrive search --account personal "aula"
```

## An auth failure names its own fix — relay it verbatim

A dead token makes `gauth.auth()` raise `AuthExpired`, and every CLI entrypoint prints
it through `gauth.run()` instead of a traceback. That message is written **for Lucas**
and already carries the exact command *and* the address to sign in as. **Show it to him
unchanged — do not paraphrase it, and never say "you need to re-auth" on its own.**

Why the address is in the message and not in this file: Lucas has several Google accounts, so
"re-authenticate" without one is an instruction he cannot act on, and a wrong account is worse
than a failure — it authenticates fine and then reads the wrong mailbox or drive. The address
is read at runtime from `accounts.json`, so it cannot go stale here.

**Run the re-auth command yourself** — backgrounded, since it blocks until consent lands. It
opens a browser on Lucas's machine, so the only part that is his is picking the account on the
consent screen. Handing him the command to type is a chore the agent could have absorbed
(his correction, 2026-08-14). Tokens are per `(service, alias)` at
`~/.config/workspace-<service>/<alias>.token.json`; Drive writes (`mkdir`, `put`) use a separate
`drive-write` token from the read one.

## Subagent tool

The `subagent` capability is runtime-specific and has no CLI wrapper:

| Runtime | How to spawn a worker agent |
|---------|----------------------------|
| Claude Code | Agent tool — pass `core/agents/<name>.md` content as system prompt |
| Feynman / Pi | Native `subagent` tool with JSON task spec |

## Workspace line-limit checker

Not a research tool — lives in `core/hooks/` alongside the commit hooks:

```bash
bash core/hooks/checks/check-line-counts.sh             # scan all code files in cwd
bash core/hooks/checks/check-line-counts.sh file.py     # check one file
find . -name "*.py" | bash core/hooks/checks/check-line-counts.sh --from-stdin
```

Thresholds: `core/hooks/limits.env`. The `pre-commit` hook runs it automatically; `pre-edit.py` enforces per-edit. Both read the same limits file.

## Adding a tool

1. Name the file for its **provider**, and put it in the directory named for the **capability**
   it delivers. Never a file at this root.
2. Create the family directory only when the tool actually lands in it — no empty `sheets/`,
   `docs/`, `maps/` waiting for a someday tool.
3. Give a family its own `CONTEXT.md` only once it holds more than one file. A one-tool family
   folds into the table below: one path hop, zero extra rows. Declaring itself early costs the
   reader a routing table that says nothing (`auth/` is the live example of the cheap side).
4. Add `# Usage: core/tools/<family>/<name> <args> — <description>` as the first comment line
   (after the shebang).
5. Save — the routing block below regenerates automatically.

A module imported by more than one family belongs at this root; a module imported by exactly
one belongs beside its tool. That rule is why one file is left here.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`assets/`](assets/CONTEXT.md) | Interface stubs for non-code assets (.imgif / .csvif), one file or a whole paper |
| [`calendar/`](calendar/CONTEXT.md) | Read what is scheduled. Provider leaf: `gcalendar`. Auth: [`../auth/gauth.py`](. |
| [`files/`](files/CONTEXT.md) | Remote file storage: list, search, download, upload. Provider leaf: `gdrive`. |
| [`mail/`](mail/CONTEXT.md) | Read a mailbox and triage it. Provider leaf: `gmail`. Auth: [`../auth/gauth.py`] |
| [`notes/`](notes/CONTEXT.md) | Pages and note databases, read as navigable text. Provider leaf: `notion` (Notio |
| [`paper/`](paper/CONTEXT.md) | Academic sources and text: search papers, extract text, annotate, check terminol |
| [`slides/`](slides/CONTEXT.md) | Presentations, read and edited in place. Provider leaf: `gslides` (Google Slides |
| [`test/`](test/CONTEXT.md) | The verify-fast suite: every Tier 0 check plus the tool unit tests. Zero-token,  |
| [`verify/`](verify/CONTEXT.md) | Verification contract + patterns for all code projects: tiers T0-T3, script name |
| [`video/`](video/CONTEXT.md) | Link to navigable text — metadata, captions, transcript, OCR, VLM caption. |
| [`web/`](web/CONTEXT.md) | Reach the open web: search, fetch a page as text, browse and search code hosts. |
| [`wos/`](wos/CONTEXT.md) | Tools that act on the workspace itself: spec ledger, contract check, skill mirro |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`attachments_util.py`](attachments_util.py) | [`attachments_util.pyi`](attachments_util.pyi) | `safe_name`, `month_dir`, `unique_path` | attachments_util.py — shared filename/dir helpers for Core/tools attachment downloaders (gmail, telegram) |
| [`auth/gauth.py`](auth/gauth.py) | [`auth/gauth.pyi`](auth/gauth.pyi) | `config_dir`, `get_accounts`, `primary_aliases`, `resolve_alias`, `AuthExpired` | gauth.py — Google's leaf of the auth family: shared OAuth2 for every Google-backed tool |
<!-- routing:end -->
