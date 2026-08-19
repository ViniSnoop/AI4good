# Accounts and keys
> Everything needing a credential: web search, Exa, Google, the Telegram bot.
> feature: web-search, exa, google-auth, telegram-capture

<!-- steps:start -->

## Web search
> feature: `web-search` · agent: yes

[`core/tools/web/search`](core/tools/web/search) is the single entrypoint for every agent — no MCP,
no per-agent wiring. It resolves its own backend, which is the whole point: picking a search CLI is
a maintenance burden that belongs inside one script, not in every agent's prompt. It works with no
key at all through ddgr; the Exa key is a separate, optional upgrade step below.

**Precondition**
```bash
ddgr --version                                     # expected: 2.2 or later
```

**Install**
```bash
sudo apt install -y ddgr                           # or: pipx install ddgr
```

**Verify**
```bash
core/tools/web/search "test query" --backend ddgr --n 3
```

**Quirk — DDG HTTP 202.** DuckDuckGo intermittently answers 202 with an empty body for piped
requests, especially after a burst from one IP. The fallback retries with exponential backoff
(`WEB_RETRIES`, default 5); if both backends fail the script exits non-zero with
`{"error": "all backends failed", ...}` on stderr, which callers can branch on.

## Exa API key
> feature: `web-search` · agent: no

Optional. Upgrades search quality; without it the ddgr backend above serves every call.

**Needs Lucas:** an API key from the [Exa dashboard](https://exa.ai). Ask for the key itself, then
write it yourself — never ask him to run a command.

**Install** — once he pastes the key:
```bash
mkdir -p ~/.feynman
printf '{"exaApiKey": "%s"}\n' "$KEY" > ~/.feynman/web-search.json    # key via env, never argv
```

**Verify**
```bash
core/tools/web/search "test query" --n 3           # auto-picks Exa when the key is present
```

## Google account access
> feature: `google-auth` · agent: no

Shared OAuth for `mail/gmail`, `calendar/gcalendar`, `files/gdrive` and `slides/gslides`. Tokens
live at `~/.config/workspace-<service>/`, dir `700` / file `600`. Drive and Slides each keep a
separate write token from their read one.

**Precondition**
```bash
core/tools/calendar/gcalendar upcoming --days 1    # a listing means auth is live
```

**Needs Lucas:** the OAuth consent screen is a browser interaction with a Google account — nobody
can click it for him. Run the command below, hand him the URL it prints, and ask for the code it
returns. Everything either side of that, do yourself.

**Install**
```bash
core/tools/mail/gmail sync --since 1               # prompts the consent flow on first run
```

**Verify**
```bash
core/tools/mail/gmail sync --since 1 && core/tools/calendar/gcalendar upcoming --days 7
```

An expired token names its own fix — relay that message verbatim rather than paraphrasing it, per
[`core/tools/SPECS.md`](core/tools/SPECS.md) § An auth failure names its own fix.

## Telegram bot — `code/aiwbot`
> feature: `telegram-capture` · agent: no

The workspace Telegram bridge lives in [`code/aiwbot`](code/aiwbot/CONTEXT.md) as the systemd
`--user` service `aiwbot`. It captures text, photo, voice and document into `brain/INBOX.md` and
drives coding agents remotely over the provider-agnostic `AgentBackend` seam.

**Precondition**
```bash
systemctl --user status aiwbot --no-pager | head -3
```

**Needs Lucas:** a bot token from BotFather, and the pairing — he must message the bot once so its
`allowed_chat_id` can be captured. Bot tokens are guessable by username, so that allowlist is the
only thing between a stranger and writes into `brain/INBOX.md`. Ask for the token, then write the
config yourself.

**Install** — the unit lives outside the repo, at `~/.config/systemd/user/aiwbot.service`:
```bash
systemctl --user daemon-reload
systemctl --user enable --now aiwbot
```

**Verify** — send a message from the paired chat and confirm the entry lands in `brain/INBOX.md`:
```bash
systemctl --user status aiwbot --no-pager
journalctl --user -u aiwbot --no-pager -n 50
```

`Restart=on-failure` means a transient crash (a network timeout on boot) self-heals. This is the
pattern for any long-running workspace process. Three conventions it carries, which any new service
inherits: the **chat allowlist** above; **secrets** at `~/.config/workspace-<service>/config.json`,
dir `700` / file `600`, the same convention gmail, calendar and drive use; and **media** into
`brain/attachments/YYYY-MM/` via the shared
[`core/tools/attachments_util.py`](core/tools/attachments_util.py).

<!-- steps:end -->
