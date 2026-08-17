# Workspace Setup
> How to make this environment work on a new machine: toolchain install and per-machine config.

What the workspace *is* and what each capability buys you: [`README.md`](README.md). What the gates
enforce and what a new agent's shim must satisfy: [`core/hooks/SPECS.md`](core/hooks/SPECS.md).
This file is only the install.

**This file is a procedure an agent executes, not prose a human reads and improvises from.** You
cloned the repo and opened your own coding agent; *that agent* is the installer. There is no
`curl | sh` and there is not going to be one — an installer would have to be ported to every
harness, while a procedure works on whichever one you already opened. `/install` is a doorway into
this file for agents that support skills; it adds nothing, and this file never depends on it.

**Every step below has the same four parts, and an agent runs them in this order:**

| Part | Contract |
|---|---|
| `> feature:` | which capability the step installs. Skip the step, lose exactly that capability |
| **Precondition** | a command that says whether the step is *already done*. Run it first, always |
| **Install** | idempotent. Running it twice must be a no-op, never a second copy |
| **Verify** | a command proving the thing works. **A step is done when its probe passes, never when its config looks right** |

`agent: no` marks the short list an agent cannot finish alone — an API key, a consent screen, a
device pairing. Each says exactly what to ask for. Everything else, run without asking.

**Sections are named, never numbered** — a number is a pointer that goes stale the first time a
step is added, and two of them already had.

Everything below is per-machine state that git cannot carry. Everything else is versioned, and the
design principle behind that is the workspace's own: the file system is the source of truth, so no
config lives only in machine state.

---

## Already wired — nothing to do

These are versioned and activate on their own after a clone. They are listed so a newcomer knows
not to go looking for an install step. They are not steps and have no probes of their own.

| Capability | Why nothing is needed |
|---|---|
| Claude Code hooks | `.claude/settings.json` is in the repo; Claude Code reads it when the workspace is opened, and `core/hooks/` activates immediately |
| opencode policy plugin | `.opencode/plugins/workspace-policy.js` is a project-level plugin, auto-loaded on startup from the workspace root. Helpers live in `.opencode/wp-helpers.js`, outside `plugins/` so opencode does not load them as a second plugin |
| Copilot hook registration | `.github/hooks/workspace-policy.json` and `.github/hooks/rtk-rewrite.json` are inert config files until Copilot itself is installed |
| The feature registry | `core/features.txt` and `core/profile.txt` are both versioned, and `core/hooks/feature_law.py` reads them where they sit. Nothing to install |

The one exception is rtk for Claude Code: its code is versioned but its registration is not, which
is why § RTK is a step.

**Before running the steps below, read your profile** — it decides which of them you need:

```bash
core/tools/wos/features                 # every capability, grouped, with your answer
core/tools/wos/features --off <slug>    # one you do not want; its install step is then moot
```

`core/features.txt` declares what each capability is for and what it buys you, so a step you are
about to run can be judged before it is run rather than after. That is the general/Lucas-specific
line made executable: the `scope` column says which rows are personal.

---

<!-- steps:start -->

## Workspace path
> feature: `tool-shebangs` · agent: yes

Every tool under `core/tools/` runs on `#!/mnt/workspace/.venv/bin/python3`, because the venv holds
the declared dependencies and the system interpreter holds none of them. A shebang cannot resolve a
relative path, so that prefix is absolute — and a clone living anywhere else must rewrite it. **Run
this step first**: every later Verify probe calls a tool.

**Precondition** — if the workspace is at `/mnt/workspace`, this step is already done, permanently:
```bash
test "$PWD" = /mnt/workspace && echo "already correct"
```

**Install** — rewrite the shebangs to this clone's own path. Idempotent: re-running rewrites the
same line to the same value.
```bash
grep -rl '^#!.*/\.venv/bin/python3$' core/tools | \
  xargs sed -i "1s|^#!.*/\.venv/bin/python3$|#!$PWD/.venv/bin/python3|"
```

**Verify** — no tool points anywhere but this clone:
```bash
for f in $(find core/tools -type f ! -name "*.*"); do head -1 "$f"; done | sort -u
# Expected: only "#!/usr/bin/env bash" and "#!$PWD/.venv/bin/python3"
```

Substitute your real path for `/mnt/workspace` in every command below, too.

## The venv
> feature: `python-runtime` · agent: yes

One virtualenv at the workspace root, shared by every tool and the test suite. Nothing here is
per-project — `code/*` repos own their own environments.

**Precondition**
```bash
.venv/bin/python3 --version        # a version line means the venv exists
```

**Install**
```bash
python3 -m venv .venv              # no-op if .venv already exists
.venv/bin/pip install --upgrade pip
```

**Verify**
```bash
.venv/bin/python3 -c "import sys; print(sys.prefix)"
# Expected: the workspace's own .venv path, not /usr
```

## Declared dependencies
> feature: `declared-deps` · agent: yes

Every external dependency the tool surface needs is declared in
[`core/tools/deps.txt`](core/tools/deps.txt) with its install command, its probe, and **what its
absence looks like**. That last column exists because these were found the expensive way: four
were installed by hand into `.venv` and never written down, so a fresh clone lost the capability
*silently* — the tool returned a worse answer instead of an error. One cost a full session.

**Precondition** — this is the whole step's precondition, install plan, and probe in one command:
```bash
core/tools/wos/deps            # every dep, ok/MISSING, with the install line for each miss
```

**Install** — run what it printed. Rows marked `apt` need `sudo`; if you cannot get it, that is the
one part to hand to Lucas, naming the package and the `breaks` line the tool printed beside it.

**Verify**
```bash
core/tools/wos/deps --check    # exit 0 = nothing missing
```

Adding a tool with a new third-party import fails `make verify-fast` until it is declared here.
The rule and its stated limit: [`core/tools/SPECS.md`](core/tools/SPECS.md) § Declared dependencies.

## Git hook
> feature: `git-hooks` · agent: yes

Applies `core/hooks/pre-commit` to **every** git repo on the machine — that global reach is the
point, since projects under `code/` are their own repos.

**Precondition**
```bash
git config --global core.hooksPath        # already-set means done; expected: <workspace>/core/hooks
```

**Install**
```bash
git config --global core.hooksPath "$PWD/core/hooks"
```

**Verify** — the path resolves to a real dispatcher, not just a string:
```bash
test -f "$(git config --global core.hooksPath)/pre-commit" && echo "hook reachable"
```

## Executable bits
> feature: `git-hooks` · agent: yes

Git carries the execute bit, so a normal clone arrives correct. This step exists for the cases that
do not: an archive export, a copy across a filesystem that drops modes, or a `umask` that strips it.

**Precondition**
```bash
test -x core/hooks/pre-commit && test -x core/hooks/post-edit.sh && echo "bits already set"
```

**Install** — idempotent by nature:
```bash
chmod +x core/hooks/post-edit.sh core/hooks/read/pre-read.sh core/hooks/pre-commit \
         core/hooks/checks/check-line-counts.sh core/hooks/copilot/copilot-agent.sh \
         core/hooks/session/start-session.sh core/tools/wos/deps
```

**Verify**
```bash
find core/hooks core/tools -type f \( -name "*.sh" -o ! -name "*.*" \) ! -perm -u+x
# Expected: no output. Any line is a file that will fail to run.
```

The `.py` hooks are invoked through `python3` and need no execute bit.

## Python interfaces — stubgen
> feature: `interface-stubs` · agent: yes

Generates the `.pyi` stubs the read gate hands an agent instead of a source file.

**Precondition**
```bash
.venv/bin/stubgen --version
```

**Install**
```bash
.venv/bin/pip install mypy
```

**Verify** — it must actually produce a stub, not merely answer `--version`:
```bash
.venv/bin/stubgen -o /tmp/stubprobe core/hooks/file_law.py && head -3 /tmp/stubprobe/file_law.pyi
```

## TypeScript interfaces — tsc
> feature: `interface-stubs` · agent: yes

**Precondition**
```bash
tsc --version || ~/.local/bin/tsc --version
```

**Install** — needs Node (`node --version`); install it with `nvm` if absent:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc && nvm install --lts
npm install -g typescript                    # if this needs sudo, use the prefix form:
npm install -g typescript --prefix ~/.local
```

**Verify**
```bash
tsc --version
```
The hook checks `tsc` on `PATH` first, then `~/.local/bin/tsc`, so either install location works.

## ESLint + Prettier for TypeScript projects
> feature: `lint-typescript` · agent: yes

Project-local, in every TS project carrying an `eslint.config.js`. Each imports the shared rules
from `code/eslint.shared.js` and runs from the project root via `node_modules/.bin/eslint` — no
global install.

**Precondition**
```bash
ls code/isoroll-module/node_modules/.bin/eslint code/voti/node_modules/.bin/eslint
```

**Install**
```bash
(cd code/isoroll-module && npm install)
(cd code/voti && npm install)
```

**Verify** — the gate must *bite*, not merely run:
```bash
printf '// test\nconst x = foo(bar());\n' > /tmp/test-lint.ts
(cd code/isoroll-module && node_modules/.bin/eslint /tmp/test-lint.ts)
# Expected: "2 calls in one statement"
```

## Caveman
> feature: `caveman` · agent: yes

Output compression (~65% saving on the agent's own output). **Vendored** into this workspace since
2026-07-23 — source of truth [`core/skills/caveman/`](core/skills/caveman/CONTEXT.md), upstream
credit [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). **Do not run the upstream
installer**: it overwrites the links with copies and re-forks the two installs. Needs Node ≥ 18.

**Precondition**
```bash
core/tools/wos/sync-global-skills --check
```

**Install**
```bash
core/tools/wos/sync-global-skills            # links ~/.agents/skills/caveman + ~/.claude/hooks/caveman-*
mkdir -p ~/.config/caveman && echo '{"defaultMode": "full"}' > ~/.config/caveman/config.json
```
On Windows the config half is:
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\caveman" | Out-Null
'{"defaultMode": "full"}' | Set-Content "$env:USERPROFILE\.config\caveman\config.json"
```

Then, if `~/.claude/settings.json` did not come across from the old machine, add its three entries:
`SessionStart` → `caveman-activate.js`, `UserPromptSubmit` → `caveman-mode-tracker.js`,
`statusLine` → `caveman-statusline.sh`. Values for the default mode: `lite`, `full`, `ultra`, `off`.

**Verify** — open a Claude Code session; the `[CAVEMAN] ⛏` badge appears in the statusline.

**Wiring a new agent.** Two mechanisms, and every agent uses one: **installed**, where session-start
hooks call `caveman-activate.js` (Claude Code), or **induced**, where a session-start shim reads
`~/.config/caveman/config.json` and injects the rules as context (Copilot, via
`core/hooks/copilot/copilot-session-start.py`). Both read the same config file, so one toggle
controls every agent. Follow the induced pattern by hand — upstream's
[INSTALL.md](https://github.com/JuliusBrussee/caveman/blob/main/INSTALL.md) is still the reference
for what a given agent needs, but never let its generator write into this workspace.

## Caveman shell helper
> feature: `caveman` · agent: yes

**Precondition**
```bash
grep -q "caveman-compress()" ~/.bashrc && echo "already appended"
```

**Install** — guarded by the precondition above; appending twice defines the function twice.
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

**Verify**
```bash
type caveman-compress        # Expected: "caveman-compress is a function"
```

## RTK
> feature: `rtk-compaction` · agent: yes

[rtk-ai/rtk](https://github.com/rtk-ai/rtk) — a Rust CLI proxy that filters and compresses dev-command
output (git, test runners, docker) before it reaches an agent's context: 60-90% token savings.
Complementary to caveman, which compresses the agent's *own* output, not tool output. Apache 2.0,
single static binary, no deps.

**Precondition**
```bash
rtk --version && rtk gain --help >/dev/null && echo "rtk present"
```

**Install**
```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh   # → ~/.local/bin/rtk
```

⚠ **Name collision.** If `rtk gain` reports an unknown subcommand, the installed binary is
reachingforthejack/rtk (Rust Type Kit), a different tool with the same name. Check `which rtk`.

**Verify**
```bash
rtk gain            # a savings table, not an error
```

## RTK — Claude Code registration
> feature: `rtk-compaction` · agent: yes

**One registration, and it must be the shim.** Claude Code merges hooks across settings scopes and
runs *all* matches, so a project entry does not replace a global one; it runs beside it. The
workspace registers the shim **globally** and holds no `Bash` compact entry of its own, which also
covers sessions started inside nested `code/*` repos — those have no project settings and would
otherwise get line-1-only compaction.

**Why a shim at all: `rtk hook` reads the first line only.** A multi-line Bash payload gets one shot
at rewriting, and if line 1 is not rewritable — `cd` opens 23.4% of this workspace's Bash calls —
the whole call runs raw. [`core/hooks/compact/`](core/hooks/compact/CONTEXT.md) patches that.

**Precondition**
```bash
python3 -c "import json,pathlib; d=json.loads((pathlib.Path.home()/'.claude/settings.json').read_text()); \
print([h['command'] for e in d.get('hooks',{}).get('PreToolUse',[]) if e.get('matcher')=='Bash' for h in e['hooks']])"
# Expected when done: one entry ending in core/hooks/compact/bash-compact-rewrite.py
```

**Install** — idempotent; replaces any existing `Bash` entry rather than appending:
```bash
python3 - <<'PATCH'
import json, pathlib
p = pathlib.Path.home() / '.claude' / 'settings.json'
d = json.loads(p.read_text())
shim = 'python3 /mnt/workspace/core/hooks/compact/bash-compact-rewrite.py'
pre = d.setdefault('hooks', {}).setdefault('PreToolUse', [])
entry = next((e for e in pre if e.get('matcher') == 'Bash'), None)
if entry is None:
    pre.append({'matcher': 'Bash', 'hooks': [{'type': 'command', 'command': shim}]})
else:
    entry['hooks'] = [{'type': 'command', 'command': shim}]
p.write_text(json.dumps(d, indent=2) + '\n')
PATCH
```

**Verify** — end to end. **Config alone proves nothing, and this is the step that taught the whole
file that rule**: the wiring looked correct for weeks while it was dropping every multi-line call.
```bash
printf '%s' '{"hook_event_name":"PreToolUse","tool_name":"Bash","session_id":"probe",
"tool_input":{"command":"cd core\ngit status\nls -la"}}' \
  | python3 core/hooks/compact/bash-compact-rewrite.py
# expect: cd core / rtk git status / rtk ls -la  — lines 2 and 3 are what raw rtk drops
```

⚠ **Do not run `rtk init --global --auto-patch` on this machine.** It overwrites that `Bash` entry
back to `rtk hook claude`, silently reverting multi-line compaction. `rtk init --show` cannot tell
the two apart either — it reports `settings.json: RTK hook configured` for both, so a green line
there is not evidence the shim is wired. Use the probe above.

## RTK — other agents
> feature: `rtk-compaction` · agent: yes

Skip whichever agents you do not use; each is independent.

**Precondition** — `ls ~/.config/opencode/plugins/rtk.ts ~/.pi/agent/extensions/rtk.ts 2>/dev/null`

**Install** — opencode (global plugin only, no project-scoped variant exists):
```bash
rtk init --global --opencode        # writes ~/.config/opencode/plugins/rtk.ts
```
Coexists with this workspace's own `.opencode/plugins/workspace-policy.js` — separate files, both
auto-load.

Pi needs a manual peer-dependency fix; the generated extension does not work out of the box:
```bash
rtk init --agent pi --global
mkdir -p ~/.pi/agent/extensions && cd ~/.pi/agent/extensions
echo '{"name":"pi-extensions-peer-deps","private":true}' > package.json
npm install @earendil-works/pi-coding-agent
```
Why: the generated `rtk.ts` does `import type { ExtensionAPI } from "@earendil-works/pi-coding-agent"`,
but Pi's loader resolves it as a real `require()` — type erasure does not happen — and Node resolves
`node_modules` relative to the extension file's own directory, not to wherever `pi` is installed.
Without the local `node_modules` it fails with `Cannot find module`, even with the package installed
globally.

[Feynman](https://www.feynman.is/) is not on rtk's supported list but is built directly on Pi, with
its own `PI_CODING_AGENT_DIR` pointing the loader at `~/.feynman/agent`. Wired by parity, same
peer-dep gotcha:
```bash
mkdir -p ~/.feynman/agent/extensions
cp ~/.pi/agent/extensions/rtk.ts ~/.feynman/agent/extensions/rtk.ts
cd ~/.feynman/agent/extensions
echo '{"name":"feynman-extensions-peer-deps","private":true}' > package.json
npm install @earendil-works/pi-coding-agent
```

**Verify**
```bash
pi -e ~/.pi/agent/extensions/rtk.ts --no-session     # silence and exit 0 means loaded
```
Feynman has no `-e`/dry-run flag, so its only signal is the **absence** of `[rtk] rtk binary not
found` or `Failed to load extension` on the first real session's startup. Treat it as unverified.

**Using it.** Everything is rewritten transparently at zero token cost — `git status` becomes
`rtk git status` without anyone asking. Four commands have to be typed: `rtk gain` (savings),
`rtk gain --history`, `rtk discover` (missed opportunities), `rtk proxy <cmd>` (run raw, for
debugging the proxy itself). **Uninstall** (any target):
`rtk init --uninstall [--global] [--copilot|--opencode|--agent pi]`.

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

## LaTeX toolchain
> feature: `latex` · agent: yes

For `academy/papers/`. The procedure lives in [`academy/SETUP.md`](academy/SETUP.md), which answers
a question no workspace-level install covers.

**Precondition**
```bash
pdflatex --version | head -1
```

**Install** — follow [`academy/SETUP.md`](academy/SETUP.md).

**Verify**
```bash
cd academy && make -n 2>/dev/null | head -3 || pdflatex --version | head -1
```

<!-- steps:end -->

---

## Verification

Does the install work? This is the whole-install probe; each step's own Verify is above.

```bash
core/tools/wos/deps --check                           # every declared dependency present
git config --global core.hooksPath                    # the global gate is wired
.venv/bin/stubgen --version && tsc --version          # interface generators are reachable
node --input-type=module -e "import('$PWD/.opencode/plugins/workspace-policy.js').then(m=>console.log(typeof m.WorkspacePolicy))"
# Expected: function
make verify-fast                                      # the workspace's own suite
```

Whether each *gate* then behaves as promised is a different question, answered by
[`core/hooks/SPECS.md`](core/hooks/SPECS.md) § What a working install looks like.

---

## Per-project setup

Each project under `code/` is its own git repo and owns its environment. A project whose setup
cannot be inferred from its code carries its own `SETUP.md`.

- [`code/SETUP.md`](code/SETUP.md) — per-language quick start, facade templates, codegraph
- [`academy/SETUP.md`](academy/SETUP.md) — LaTeX toolchain, paper compilation
- [`core/tools/video/SETUP.md`](core/tools/video/SETUP.md) — the video tool's model and cookie state
