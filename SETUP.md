# Workspace Setup
> How to make this environment work on a new machine: toolchain install and per-machine config.

What the workspace *is* and what each feature buys you: [`README.md`](README.md). What the gates
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
| `> feature:` | which feature the step installs. Skip the step, lose exactly that feature |
| `> substrate: yes` | installs no feature — it installs what every feature *runs on*. Skip it and nothing works, so there is nothing to ablate and no registry row |
| **Precondition** | a command that says whether the step is *already done*. Run it first, always |
| **Install** | idempotent. Running it twice must be a no-op, never a second copy |
| **Verify** | a command proving the thing works. **A step is done when its probe passes, never when its config looks right** |

`agent: no` marks the short list an agent cannot finish alone — an API key, a consent screen, a
device pairing. Each says exactly what to ask for. Everything else, run without asking.

**Two steps are `substrate`, and the distinction is the ablation's, not bookkeeping** (2026-08-17):
the venv and the absolute `#!` line every `core/tools/` CLI carries. Both were registry rows until
they were read properly — switching off the interpreter that the switch itself runs on produces no
signal, and a shebang a clone rewrites once is repair, not a toggle. Third-party machine state this
workspace does not author is a step here plus a `core/tools/deps.txt` line, never a feature.

**Sections are named, never numbered** — a number is a pointer that goes stale the first time a
step is added, and two of them already had.

Everything below is per-machine state that git cannot carry. Everything else is versioned, and the
design principle behind that is the workspace's own: the file system is the source of truth, so no
config lives only in machine state.

---

## Already wired — nothing to do

These are versioned and activate on their own after a clone. They are listed so a newcomer knows
not to go looking for an install step. They are not steps and have no probes of their own.

| Feature | Why nothing is needed |
|---|---|
| Claude Code hooks | `.claude/settings.json` is in the repo; Claude Code reads it when the workspace is opened, and `core/hooks/` activates immediately |
| ZCode hooks | `.zcode/config.json` is in the repo and ZCode reads it at every session start — but project-scope hooks stay **inert until the workspace is trusted in the client** (one-time, per machine; `agent: no` — open the workspace in ZCode and accept the trust prompt / Settings → trust). Until then zcode enforces nothing at edit time; the git gates still fire. Measured: ISSUES.md B6 |
| opencode policy plugin | `.opencode/plugins/workspace-policy.js` is a project-level plugin, auto-loaded on startup from the workspace root. Helpers live in `.opencode/wp-helpers.js`, outside `plugins/` so opencode does not load them as a second plugin |
| Copilot hook registration | `.github/hooks/workspace-policy.json` and `.github/hooks/rtk-rewrite.json` are inert config files until Copilot itself is installed |
| The feature registry | `core/features.txt` and `core/profile.txt` are both versioned, and `core/hooks/feature_law.py` reads them where they sit. Nothing to install |

The one exception is rtk for Claude Code: its code is versioned but its registration is not, which
is why § RTK is a step.

**Before running the steps below, read your profile** — it decides which of them you need:

```bash
core/tools/wos/features                 # every feature, grouped, with your answer
core/tools/wos/features --off <slug>    # one you do not want; its install step is then moot
```

`core/features.txt` declares what each feature is for and what it buys you, so a step you are
about to run can be judged before it is run rather than after. That is the general/Lucas-specific
line made executable: the `scope` column says which rows are personal.

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

<!-- routing:start -->
## Routing

| Shard | Description | Feature |
|-------|-------------|---------|
| [`SETUP-accounts.md`](SETUP-accounts.md) | Everything needing a credential: web search, Exa, Google, the Telegram bot. | web-search, exa, google-auth, forms, telegram-capture |
| [`SETUP-caveman.md`](SETUP-caveman.md) | The compression mode and the shell helper that switches it per session. | caveman |
| [`SETUP-rtk.md`](SETUP-rtk.md) | Tool-output compaction, and registering it with each agent runtime that hooks. | rtk-compaction |
| [`SETUP-toolchain.md`](SETUP-toolchain.md) | Interface generators and linters: stubgen, tsc, ESLint/Prettier, LaTeX. | interface-stubs, lint-typescript, latex |
| [`SETUP-workspace.md`](SETUP-workspace.md) | The path, the venv, the declared deps, the git hook and the executable bits. | substrate — nothing else runs until these do |
<!-- routing:end -->
