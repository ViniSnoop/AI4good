# notes
> Pages and note databases, read as navigable text. Provider leaf: `notion` (Notion REST API).

```bash
core/tools/notes/notion auth personal                    # prompts for the secret, stores it 600
core/tools/notes/notion whoami --account personal        # proves the token is alive
core/tools/notes/notion list --account personal --name "Computação"
core/tools/notes/notion read --account personal <page-id-or-pasted-URL>
core/tools/notes/notion search --account personal "aula 3"
```

**`read` prints block ids on purpose** — every write in the Notion API addresses a block by id, so
reading a page hands back the handles for editing it, the same contract as
[`../slides/`](../slides/CONTEXT.md) `read`. It takes a page or a database, since Notion has no
single endpoint for either.

Notion has no headless consent flow — the secret is minted inside Lucas's account at
[my-integrations](https://www.notion.so/my-integrations) and a page is connected to it one at a
time, his only two clicks. Auth recovery, the builtin-pipe storage rule, and the family-wide
protocol: [`../SPECS.md`](../SPECS.md).

**A 404 is a sharing failure until proven otherwise.** Notion returns the same code for "not
connected to this integration" and "no such id," and the first is by far the more common cause:
content stays invisible to an integration it hasn't been shared with. `not_shared_text` leads
with that reading on purpose.

Notion has no read/write token split (AD-11's exception, [`core/SPECS.md`](../../SPECS.md)):
capabilities are chosen when the integration is created, so one secret already carries the
strongest grant.

`VERSION` in `notion_core.py` pins the API contract — Notion breaks by version, not by date, and a
bump can change the shape of a database response.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | Notion API gotchas and the auth mechanics specific to this tool. |
| [`notion`](notion) | — | — | Notion CLI: auth, whoami, list, search, read |
| [`notion_auth.py`](notion_auth.py) | [`notion_auth.pyi`](notion_auth.pyi) | `AuthMissing`, `NotShared`, `config_dir`, `token_path`, `save_token` | notion_auth.py — Notion's integration-token store, and the instructions a failure prints |
| [`notion_core.py`](notion_core.py) | [`notion_core.pyi`](notion_core.pyi) | `ApiRefused`, `normalize_id`, `url`, `request`, `paged` | notion_core.py — Notion REST seam (workspace-agnostic) for Core/tools/notes/notion |
| [`notion_outline.py`](notion_outline.py) | [`notion_outline.pyi`](notion_outline.pyi) | `rich_text`, `block_text`, `marker`, `prop_value`, `title_of` | notion_outline.py — a page as navigable text: block ids, structure, and the words on them |
<!-- routing:end -->
