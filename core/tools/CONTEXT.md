# Tools
> CLI tools callable via bash, one directory per family; routing block auto-synced on save.

**A family directory is a capability; the tool inside it is the provider.** `mail/gmail`,
`calendar/gcalendar`, `files/gdrive` — swapping a provider changes a leaf, never a family.

Naming rules, the auth-failure protocol, and how to add a tool: [`SPECS.md`](SPECS.md).

Call any tool via bash:
```
core/tools/web/search "relativistic raytracing GPU"
core/tools/paper/papers "Schwarzschild geodesics" --cat gr-qc --n 15
core/tools/mail/gmail sync --since 7
core/tools/calendar/gcalendar upcoming --days 7
core/tools/files/gdrive search --account personal "aula"
```

## Subagent tool

The `subagent` capability is runtime-specific and has no CLI wrapper:

| Runtime | How to spawn a worker agent |
|---------|----------------------------|
| Claude Code | Agent tool — pass `core/agents/<name>.md` content as system prompt |
| Feynman / Pi | Native `subagent` tool with JSON task spec |

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`assets/`](assets/CONTEXT.md) | Interface stubs for non-code assets (.imgif / .csvif), one file or a whole… |
| [`calendar/`](calendar/CONTEXT.md) | Read what is scheduled. Provider leaf: `gcalendar`. Auth… |
| [`files/`](files/CONTEXT.md) | Remote file storage: list, search, download, upload. Provider leaf: `gdrive`. |
| [`mail/`](mail/CONTEXT.md) | Read a mailbox and triage it. Provider leaf: `gmail`. Auth… |
| [`notes/`](notes/CONTEXT.md) | Pages and note databases, read as navigable text. Provider leaf: `notion`… |
| [`paper/`](paper/CONTEXT.md) | Academic sources and text: search papers, extract text, annotate, check… |
| [`slides/`](slides/CONTEXT.md) | Presentations, read and edited in place. Provider leaf: `gslides` (Google Slides… |
| [`test/`](test/CONTEXT.md) | The verify-fast suite: every Tier 0 check plus the tool unit tests. Zero-token… |
| [`verify/`](verify/CONTEXT.md) | Verification contract + patterns for all code projects: tiers T0-T3, script… |
| [`video/`](video/CONTEXT.md) | Link to navigable text — metadata, captions, transcript, OCR, VLM caption. |
| [`web/`](web/CONTEXT.md) | Reach the open web: search, fetch a page as text, browse and search code hosts. |
| [`wos/`](wos/CONTEXT.md) | Tools that act on the workspace itself: spec ledger, contract check, skill… |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | What must be true of a `core/tools/` capability, and why: how a family is named… |
| [`attachments_util.py`](attachments_util.py) | [`attachments_util.pyi`](attachments_util.pyi) | `safe_name`, `month_dir`, `unique_path` | attachments_util.py — shared filename/dir helpers for Core/tools attachment downloaders (gmail, telegram) |
| [`auth/gauth.py`](auth/gauth.py) | [`auth/gauth.pyi`](auth/gauth.pyi) | `config_dir`, `get_accounts`, `primary_aliases`, `resolve_alias`, `AuthExpired` | gauth.py — Google's leaf of the auth family: shared OAuth2 for every Google-backed tool |
<!-- routing:end -->
