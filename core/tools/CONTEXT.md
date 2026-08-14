# Tools
> CLI tools callable via bash, one directory per family; routing block auto-synced on save.

Split into families 2026-07-31 at 37 files in one directory. **The path changed for every
tool** — `core/tools/search` is now `core/tools/web/search`. Only the two helpers shared
across families stay at the root: `google_auth.py` (google + slides) and
`attachments_util.py` (gmail + video).

Call any tool via bash:
```
core/tools/web/search "relativistic raytracing GPU"
core/tools/paper/papers "Schwarzschild geodesics" --cat gr-qc --n 15
core/tools/web/fetch "https://arxiv.org/abs/1601.02063"
core/tools/paper/parse paper.pdf --pages 1-5
core/tools/web/hf dataset allenai/c4
```

## An auth failure names its own fix — relay it verbatim

A dead token makes `google_auth.auth()` raise `AuthExpired`, and every CLI entrypoint prints
it through `google_auth.run()` instead of a traceback. That message is written **for Lucas**
and already carries the exact command *and* the address to sign in as. **Show it to him
unchanged — do not paraphrase it, and never say "you need to re-auth" on its own.**

Why the address is in the message and not in this file: Lucas has four Google accounts, so
"re-authenticate" without one is an instruction he cannot act on, and a wrong account is worse
than a failure — it authenticates fine and then reads the wrong mailbox or drive. The address
is read at runtime from `accounts.json`, so it cannot go stale here.

Re-consent opens a browser, so it is **always Lucas's step, never an agent's**. Tokens are per
`(service, alias)` at `~/.config/workspace-<service>/<alias>.token.json`; Drive writes
(`mkdir`, `put`) use a separate `drive-write` token from the read one.

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

1. Create an executable script in the family directory it belongs to — a new family is a new
   directory with its own `CONTEXT.md`, never a file at this root.
2. Add `# Usage: core/tools/<family>/<name> <args> — <description>` as the first comment line
   (after the shebang).
3. Save — the routing block below regenerates automatically.

A module imported by more than one family belongs at this root; a module imported by exactly
one belongs beside it. That rule is why only two files are left here.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`assets/`](assets/CONTEXT.md) | Interface stubs for non-code assets (.imgif / .csvif), one file or a whole paper |
| [`google/`](google/CONTEXT.md) | Google service CLIs — calendar, drive, gmail. Auth is shared: google_auth.py at  |
| [`paper/`](paper/CONTEXT.md) | Academic sources and text: search papers, extract text, annotate, check terminol |
| [`slides/`](slides/CONTEXT.md) | Slidev presentations: auth, scaffold, serve, build, and port from Google Slides. |
| [`test/`](test/CONTEXT.md) | The verify-fast suite: every Tier 0 check plus the tool unit tests. Zero-token,  |
| [`verify/`](verify/CONTEXT.md) | Verification contract + patterns for all code projects: tiers T0-T3, script name |
| [`video/`](video/CONTEXT.md) | Link to navigable text — metadata, captions, transcript, OCR, VLM caption. |
| [`web/`](web/CONTEXT.md) | Reach the open web: search, fetch a page as text, browse and search code hosts. |
| [`wos/`](wos/CONTEXT.md) | Tools that act on the workspace itself: spec ledger, contract check, skill mirro |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | Slides Pipeline — Specs & Architecture Decisions |
| [`attachments_util.py`](attachments_util.py) | [`attachments_util.pyi`](attachments_util.pyi) | `safe_name`, `month_dir`, `unique_path` | attachments_util.py — shared filename/dir helpers for Core/tools attachment downloaders (gmail, telegram) |
| [`google_auth.py`](google_auth.py) | [`google_auth.pyi`](google_auth.pyi) | `config_dir`, `get_accounts`, `primary_aliases`, `resolve_alias`, `AuthExpired` | google_auth.py — Shared OAuth2 auth for workspace Google services (drive, calendar, gmail) |
<!-- routing:end -->
