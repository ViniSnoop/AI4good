# notes
> Pages and note databases, read as navigable text. Provider leaf: `notion` (Notion REST API).

```bash
core/tools/notes/notion auth personal                    # prompts for the secret, stores it 600
core/tools/notes/notion whoami --account personal        # proves the token is alive
core/tools/notes/notion list --account personal --name "Computação"
core/tools/notes/notion read --account personal <page-id-or-pasted-URL>
core/tools/notes/notion search --account personal "aula 3"
```

**`read` prints block ids on purpose.** Every write in the Notion API addresses a block by id, so
reading a page hands back the handles for editing it — the same contract as
[`../slides/`](../slides/CONTEXT.md) `read`. Paste a page URL instead of an id if that is what is
at hand: the id is parsed out of it.

**`read` takes a page or a database.** Notion has no endpoint that accepts either, so the tool
tries `/pages` and falls back to `/databases`. A database prints its rows, each with the id that
reads it. Sub-pages are *not* followed — a `child_page` is its own read, and recursing into one
would drag in a second document unasked.

## The token is Lucas's click, and the CLI says so

Notion has no headless consent flow: an internal integration secret is minted inside his account
at [my-integrations](https://www.notion.so/my-integrations), and pages are then connected to that
integration one parent at a time. Both failure modes print the whole instruction —
**relay it unchanged**, the same rule as [`../CONTEXT.md`](../CONTEXT.md) § *An auth failure names
its own fix*.

**His half is the two clicks inside Notion; every command is the agent's.** Google's flow differs
only in which half is which — there the agent runs the consent command and Lucas picks an account
on the screen it opens. Here he mints the secret, pastes it into the conversation, and connects
the page; the agent stores it through a builtin pipe (`printf … | notion auth <alias>`) so the
value never reaches argv. Handing him the storing command to type is the chore this note exists
to prevent, and a test enforces it: no CLI path may appear above the `AGENT:` line.

**A 404 is a sharing failure until proven otherwise.** Notion returns the same code for "not
connected to this integration" and "no such id", and the first is far more common — content is
invisible to an integration, not forbidden. `not_shared_text` says that in that order on purpose.

Read/write is not a token split here (AD-11's case): capabilities are chosen when the integration
is created, so one secret with *Read + Update + Insert* is the whole grant, and the read path is
already using the strongest consent by construction.

Auth sits beside the tool rather than in [`../auth/`](../auth/gauth.py) because exactly one family
imports it — the rule in [`../CONTEXT.md`](../CONTEXT.md) § *Adding a tool*. It moves the day a
second family needs a Notion token, not before.

`VERSION` in `notion_core.py` pins the API contract. Notion breaks by version, not by date: the
header is mandatory and a bump can change the shape of a database response.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`notion`](notion) | — | — | Notion CLI: auth, whoami, list, search, read |
| [`notion_auth.py`](notion_auth.py) | [`notion_auth.pyi`](notion_auth.pyi) | `AuthMissing`, `NotShared`, `config_dir`, `token_path`, `save_token` | notion_auth.py — Notion's integration-token store, and the instructions a failure prints |
| [`notion_core.py`](notion_core.py) | [`notion_core.pyi`](notion_core.pyi) | `ApiRefused`, `normalize_id`, `url`, `request`, `paged` | notion_core.py — Notion REST seam (workspace-agnostic) for Core/tools/notes/notion |
| [`notion_outline.py`](notion_outline.py) | [`notion_outline.pyi`](notion_outline.pyi) | `rich_text`, `block_text`, `marker`, `prop_value`, `title_of` | notion_outline.py — a page as navigable text: block ids, structure, and the words on them |
<!-- routing:end -->
