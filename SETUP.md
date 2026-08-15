# Workspace Setup
> How to make this environment work on a new machine: toolchain install and per-machine config.

What the workspace *is* and what each capability buys you: [`README.md`](README.md). What the gates
enforce and what a new agent's shim must satisfy: [`core/hooks/SPECS.md`](core/hooks/SPECS.md).
This file is only the install.

**Sections are named, never numbered** — a number is a pointer that goes stale the first time a
step is added, and two of them already had.

Everything below is per-machine state that git cannot carry. Everything else is versioned, and the
design principle behind that is the workspace's own: the file system is the source of truth, so no
config lives only in machine state.

If the workspace is not at `/mnt/workspace`, substitute the real path everywhere in this file.

---

## Already wired — nothing to do

These are versioned and activate on their own after a clone. They are listed so a newcomer knows
not to go looking for an install step.

| Capability | Why nothing is needed |
|---|---|
| Claude Code hooks | `.claude/settings.json` is in the repo; Claude Code reads it when the workspace is opened, and `core/hooks/` activates immediately |
| opencode policy plugin | `.opencode/plugins/workspace-policy.js` is a project-level plugin, auto-loaded on startup from `/mnt/workspace`. Helpers live in `.opencode/wp-helpers.js`, outside `plugins/` so opencode does not load them as a second plugin |
| Copilot hook registration | `.github/hooks/workspace-policy.json` and `.github/hooks/rtk-rewrite.json` are inert config files until Copilot itself is installed |
| rtk for Claude Code in this repo | the `Bash` matcher in `.claude/settings.json` already runs `rtk hook claude`; only the binary itself is per-machine (see § RTK) |

Verify the opencode plugin parses:
```bash
node --input-type=module -e "import('/mnt/workspace/.opencode/plugins/workspace-policy.js').then(m=>console.log(typeof m.WorkspacePolicy))"
# Expected: function
```

---

## Git hook

```bash
git config --global core.hooksPath /mnt/workspace/core/hooks
```

Applies `core/hooks/pre-commit` to **every** git repo on the machine — that global reach is the
point, since projects under `code/` are their own repos.

```bash
git config --global core.hooksPath     # Expected: /mnt/workspace/core/hooks
```

## Executable bits

```bash
chmod +x /mnt/workspace/core/hooks/post-edit.sh
chmod +x /mnt/workspace/core/hooks/read/pre-read.sh
chmod +x /mnt/workspace/core/hooks/pre-commit
chmod +x /mnt/workspace/core/hooks/checks/check-line-counts.sh
chmod +x /mnt/workspace/core/hooks/copilot/copilot-agent.sh
chmod +x /mnt/workspace/core/hooks/session/start-session.sh
```

The `.py` hooks are invoked through `python3` and need no execute bit.

## Python interfaces — stubgen

```bash
pip install mypy                          # or: /mnt/workspace/.venv/bin/pip install mypy
stubgen --version                         # or: /mnt/workspace/.venv/bin/stubgen --version
```

## JavaScript / TypeScript interfaces — tsc

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install --lts
npm install -g typescript
```

If Node is already present but a global install would need sudo:
```bash
npm install -g typescript --prefix ~/.local
```

The hook checks `tsc` on `PATH` first, then `~/.local/bin/tsc`. Verify with `tsc --version`.

## ESLint + Prettier for TypeScript projects

Project-local, in every TS project carrying an `eslint.config.js`. Each imports the shared rules
from `code/eslint.shared.js`, and ESLint runs from the project root via `node_modules/.bin/eslint`
— no global install.

```bash
cd /mnt/workspace/code/isoroll-module && npm install
cd /mnt/workspace/code/voti && npm install
```

Verify:
```bash
ls /mnt/workspace/code/isoroll-module/node_modules/.bin/eslint
cd /mnt/workspace/code/isoroll-module && npm run lint
```

## Caveman

Output compression (~65% saving on the agent's own output). **Vendored** into this workspace since
2026-07-23 — the source of truth is [`core/skills/caveman/`](core/skills/caveman/CONTEXT.md),
upstream credit [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). **Do not run the
upstream installer**: it overwrites the links with copies and re-forks the two installs.

Requires Node ≥ 18. One command wires the suite:

```bash
core/tools/wos/sync-global-skills            # links ~/.agents/skills/caveman + ~/.claude/hooks/caveman-*
core/tools/wos/sync-global-skills --check    # verify
```

Then, if `~/.claude/settings.json` did not come across from the old machine, add its three entries:
`SessionStart` → `caveman-activate.js`, `UserPromptSubmit` → `caveman-mode-tracker.js`,
`statusLine` → `caveman-statusline.sh`.

**Default mode** — optional (caveman's own default is `full`), but a config file makes it explicit
and reproducible. Values: `lite`, `full`, `ultra`, `off`.

```bash
mkdir -p ~/.config/caveman && echo '{"defaultMode": "full"}' > ~/.config/caveman/config.json
```
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\caveman" | Out-Null
'{"defaultMode": "full"}' | Set-Content "$env:USERPROFILE\.config\caveman\config.json"
```

**The `caveman-compress` shell function**, appended to `~/.bashrc` (or `~/.zshrc`):

```bash
cat >> ~/.bashrc << 'EOF'

# caveman-compress shortcut
caveman-compress() {
  local CLAUDE_BIN
  CLAUDE_BIN="$(dirname "$CLAUDE_CODE_EXECPATH")"
  (cd /mnt/workspace/core/skills/caveman && PATH="$CLAUDE_BIN:$PATH" python3 -m scripts "$1")
}
EOF
source ~/.bashrc
```
```powershell
Add-Content $PROFILE @'

# caveman-compress shortcut
function caveman-compress {
    param([string]$File)
    $claudeBin = Split-Path $env:CLAUDE_CODE_EXECPATH
    Push-Location "$env:USERPROFILE\.claude\skills\caveman"
    $env:PATH = "$claudeBin;$env:PATH"
    python3 -m scripts $File
    Pop-Location
}
'@
```

**Verify:** open a Claude Code session — the `[CAVEMAN] ⛏` badge appears in the statusline.

**Wiring a new agent.** Two mechanisms, and every agent uses one: **installed**, where session-start
hooks call `caveman-activate.js` (Claude Code), or **induced**, where a session-start shim reads
`~/.config/caveman/config.json` and injects the rules as context (Copilot, via
`core/hooks/copilot/copilot-session-start.py`). Both read the same config file, so one toggle
controls every agent. Follow the induced pattern by hand — upstream's
[INSTALL.md](https://github.com/JuliusBrussee/caveman/blob/main/INSTALL.md) is still the reference
for what a given agent needs, but never let its generator write into this workspace.

## RTK

[rtk-ai/rtk](https://github.com/rtk-ai/rtk) — a Rust CLI proxy that filters and compresses dev-command
output (git, test runners, docker) before it reaches an agent's context: 60-90% token savings.
Complementary to caveman, which compresses the agent's *own* output, not tool output. Apache 2.0,
single static binary, no deps.

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
rtk --version                     # installs to ~/.local/bin/rtk
```

⚠ **Name collision.** If `rtk gain` reports an unknown subcommand, the installed binary is
reachingforthejack/rtk (Rust Type Kit), a different tool with the same name. Check `which rtk`.

**Claude Code** is dual-wired: the project-scoped hook is already versioned here (see § Already
wired). For sessions *outside* this workspace, patch the global config:
```bash
rtk init --global --auto-patch      # additive; takes a .bak; verify with: rtk init --show
```
It only inserts a `PreToolUse`/`Bash` block into `~/.claude/settings.json` and leaves existing
`SessionStart`/`UserPromptSubmit`/`statusLine` keys (caveman's) untouched.

**opencode** — global plugin only, no project-scoped variant exists:
```bash
rtk init --global --opencode        # writes ~/.config/opencode/plugins/rtk.ts
```
Coexists with this workspace's own `.opencode/plugins/workspace-policy.js` — separate files, both
auto-load.

**Pi** needs a manual peer-dependency fix; the generated extension does not work out of the box:
```bash
rtk init --agent pi --global
mkdir -p ~/.pi/agent/extensions
cd ~/.pi/agent/extensions
echo '{"name":"pi-extensions-peer-deps","private":true}' > package.json
npm install @earendil-works/pi-coding-agent
```
Why: the generated `rtk.ts` does `import type { ExtensionAPI } from "@earendil-works/pi-coding-agent"`,
but Pi's loader resolves it as a real `require()` — type erasure does not happen — and Node resolves
`node_modules` relative to the extension file's own directory, not to wherever `pi` is installed.
Without the local `node_modules` it fails with `Cannot find module`, even with the package installed
globally. Verify: `pi -e ~/.pi/agent/extensions/rtk.ts --no-session` — silence and exit 0 means loaded.

**Feynman** ([feynman.is](https://www.feynman.is/)) is not on rtk's supported list but is built
directly on Pi, with its own `PI_CODING_AGENT_DIR` pointing the loader at `~/.feynman/agent`. Wired
by parity, same peer-dep gotcha:
```bash
mkdir -p ~/.feynman/agent/extensions
cp ~/.pi/agent/extensions/rtk.ts ~/.feynman/agent/extensions/rtk.ts
cd ~/.feynman/agent/extensions
echo '{"name":"feynman-extensions-peer-deps","private":true}' > package.json
npm install @earendil-works/pi-coding-agent
```
**Unverified** — Feynman has no `-e`/dry-run flag, so the confirmation signal is the *absence* of
`[rtk] rtk binary not found` or `Failed to load extension` on the first real session's startup.

**Using it.** Everything is rewritten transparently at zero token cost — `git status` becomes
`rtk git status` without anyone asking. Four commands have to be typed:

```bash
rtk gain              # token savings analytics
rtk gain --history    # command usage history with savings
rtk discover          # analyse session history for missed opportunities
rtk proxy <cmd>       # run a command raw — for debugging the proxy itself
```

**Uninstall** (any target): `rtk init --uninstall [--global] [--copilot|--opencode|--agent pi]`.

## Web search

[`core/tools/web/search`](core/tools/web/search) is the single entrypoint for every agent — no MCP,
no per-agent wiring. It resolves its own backend, which is the whole point: picking a search CLI is
a maintenance burden that belongs inside one script, not in every agent's prompt.

| Backend | When | Setup |
|---|---|---|
| **Exa** | `~/.feynman/web-search.json` holds `exaApiKey` | key from the [Exa dashboard](https://exa.ai), saved as `{"exaApiKey": "..."}` — no system install |
| **ddgr** | Exa key missing, or Exa errors (bad key, quota, network); also on `--backend ddgr` | `sudo apt install -y ddgr` (or `pipx install ddgr`) |

Both return the same normalized JSON: `[{title, url, abstract, score?}]`.

```bash
ddgr --version                                     # expected: 2.2 or later
core/tools/web/search "test query" --n 3           # auto-picks Exa if the key is present
core/tools/web/search "test query" --backend ddgr  # force DDG
```

**Quirk — DDG HTTP 202.** DuckDuckGo intermittently answers 202 with an empty body for piped
requests, especially after a burst from one IP. The fallback retries with exponential backoff
(`WEB_RETRIES`, default 5); if both backends fail the script exits non-zero with
`{"error": "all backends failed", ...}` on stderr, which callers can branch on.

Per-agent wiring: none. Every agent's bash already reaches the system shell.

## Telegram bot — `code/aiwbot`

The workspace Telegram bridge lives in [`code/aiwbot`](code/aiwbot/CONTEXT.md) as the systemd
`--user` service `aiwbot`. It captures text, photo, voice and document into `brain/INBOX.md` and
drives coding agents remotely over the provider-agnostic `AgentBackend` seam.

```bash
# the unit lives outside the repo, at ~/.config/systemd/user/aiwbot.service
systemctl --user daemon-reload
systemctl --user enable --now aiwbot
systemctl --user status aiwbot --no-pager
journalctl --user -u aiwbot --no-pager -n 50
```

`Restart=on-failure` means a transient crash (a network timeout on boot) self-heals. This is the
pattern for any long-running workspace process.

Three conventions it carries, which any new service inherits:

- **Security** — every incoming update is checked against one `allowed_chat_id` captured at pairing.
  Bot tokens are guessable by username, so this allowlist is the only thing between a stranger and
  writes into `brain/INBOX.md`.
- **Secrets** — `~/.config/workspace-<service>/config.json`, dir `700` / file `600`, the same
  convention gmail, calendar and drive use.
- **Media** — attachments to `brain/attachments/YYYY-MM/` via the shared
  [`core/tools/attachments_util.py`](core/tools/attachments_util.py).

**Verify:** send a message from the paired chat, confirm the entry lands in `brain/INBOX.md`.

## Codeburn

Run `codeburn optimize` periodically to audit token waste.

## LaTeX toolchain

For `academy/papers/` — see [`academy/SETUP.md`](academy/SETUP.md).

---

## Verification

Does the install work?

```bash
# git hook is wired
git config --global core.hooksPath                    # Expected: /mnt/workspace/core/hooks

# interface generators are reachable
stubgen --version || /mnt/workspace/.venv/bin/stubgen --version
tsc --version

# agent hooks are configured
grep -c "hooks" /mnt/workspace/.claude/settings.json  # Expected: > 0
node --input-type=module -e "import('/mnt/workspace/.opencode/plugins/workspace-policy.js').then(m=>console.log(typeof m.WorkspacePolicy))"

# hook scripts are executable
ls -la /mnt/workspace/core/hooks/post-edit.sh /mnt/workspace/core/hooks/read/pre-read.sh \
       /mnt/workspace/core/hooks/pre-commit /mnt/workspace/core/hooks/checks/check-line-counts.sh

# the workspace's own suite
python3 -m pytest core/tools/test/ -q
```

An end-to-end check that the lint gate actually bites:
```bash
printf '// test\nconst x = foo(bar());\n' > /tmp/test-lint.ts
cd /mnt/workspace/code/isoroll-module && node_modules/.bin/eslint /tmp/test-lint.ts
# Expected: "2 calls in one statement"
```

Whether each *gate* then behaves as promised is a different question, answered by
[`core/hooks/SPECS.md`](core/hooks/SPECS.md) § What a working install looks like.

---

## Per-project setup

Each project under `code/` is its own git repo and owns its environment. A project whose setup
cannot be inferred from its code carries its own `SETUP.md`.

- [`code/SETUP.md`](code/SETUP.md) — per-language quick start, facade templates, codegraph
- [`academy/SETUP.md`](academy/SETUP.md) — LaTeX toolchain, paper compilation
