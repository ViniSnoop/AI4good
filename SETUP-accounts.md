# Accounts and keys
> Everything needing a credential: web search, Exa, Google, the Telegram bot.
> feature: web-search, exa, google-auth, forms, telegram-capture

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

Shared OAuth for `mail/gmail`, `calendar/gcalendar`, `files/gdrive`, `slides/gslides` and
`forms/gforms`. Tokens live at `~/.config/workspace-<service>/`, dir `700` / file `600`. Drive,
Slides and Forms each keep a separate write token from their read one.

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

## Google Forms API
> feature: `forms` · agent: no

One switch per Google API, inside the GCP project that owns the OAuth client
(`workspace-gmail-499605`). Consent alone is not enough: a disabled API answers every call with
`SERVICE_DISABLED` no matter which scopes the token carries.

**Precondition**
```bash
core/tools/forms/gforms read --account personal <form_id>   # an outline means the API is on
```

**The project has to be one Lucas administers, and `workspace-gmail-499605` is not.** Signing in
as `lsf.cin@gmail.com` or `lsf@cin.ufpe.br` gets `You need additional access ...
resourcemanager.projects.get (Missing)` — the OAuth client works because a client id needs no
console rights, but switching an API on does. So Forms runs on **its own project**, created by
Lucas, and its credential is read from the service directory rather than the gmail one:
`gauth._credentials_file()` looks in `~/.config/workspace-<service>/` **before** falling back to
`~/.config/workspace-gmail/`, so dropping a second `credentials.json` into `workspace-forms/` and
`workspace-forms-write/` leaves mail, calendar, drive and slides untouched.

**Needs Lucas**, in console.cloud.google.com signed in as `lsf.cin@gmail.com`: create a project,
enable **Google Forms API** and **Google Drive API** in it, configure the auth platform (External,
himself as test user), then create an **OAuth client → Desktop app** and download its JSON. The
agent does everything after the download. Live since 2026-08-19: project `workspace-os-506016`,
which also has gmail, calendar, docs, slides and sheets switched on — the successor to
`workspace-gmail-499605` for anything that ever needs a console again.

**One project serves every account.** The project owns the *app*; an account only consents to it.
A second account needs no second project — just a row under *Audience → Test users*, and an
institutional account may still be refused by its own Workspace admin's unverified-app policy.

**Install**
```bash
core/tools/forms/gforms auth personal --write        # prompts the consent flow on first run
```

**Verify**
```bash
core/tools/forms/gforms new --account personal <spec.json>
```

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
