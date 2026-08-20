# Provider shims
> One canonical behaviour, and what a new agent runtime must do to get it.
> governs: core/hooks/copilot/, core/hooks/hook_input.py, .opencode/plugins/

## Canonical behaviour, provider shims

Canonical behaviour lives in neutral files under `core/hooks/` and [`AGENTS.md`](../../AGENTS.md).
Provider-specific files are shims, discovery points, or startup wiring — never a second copy of a
rule. Three words classify any of them:

| Word | Means |
|------|-------|
| **ENFORCED** | the hook can block a read, an edit, or a commit |
| **INDUCED** | the file only injects guidance; the agent may ignore it |
| **SKIPPED** | present for compatibility, no enforcement effect |

| File | Why it exists | Behaviour |
|------|---------------|-----------|
| `AGENTS.md` | canonical workspace policy + startup anchor for every agent | **INDUCED** |
| `.github/copilot-instructions.md` | one-line Copilot shim pointing to `AGENTS.md` | **INDUCED** |
| `.github/hooks/workspace-policy.json` | VS Code hook registration for Copilot lifecycle events | **ENFORCED** |
| `.vscode/settings.json` | limits hook discovery to the workspace path, not user-level `.claude` hooks | **INDUCED** |

## The contract a new agent's shim must satisfy

Three hook points cover the whole surface:

```
PreTool (Read)  → bash    core/hooks/read/pre-read.sh
PreTool (Edit)  → python3 core/hooks/checks/pre-edit.py
                  python3 core/hooks/facade/facade-scan.py   (write/create only)
                  python3 core/hooks/facade/facade-gate.py
PostTool (Edit) → bash    core/hooks/post-edit.sh
PostTool (Read) → python3 core/hooks/facade/facade-tracker.py
```

Every canonical hook expects:

- `file_path` — absolute path to the file being read or edited
- `CLAUDE_TOOL_NAME` env var — `"Read"`, `"Edit"`, or `"Write"`
- pre-hooks: the JSON payload on **stdin**
- post-hooks: the JSON payload in **`CLAUDE_TOOL_INPUT`**
- exit code **2** = hard block; stdout = the message shown to the agent

**A shim must pass a session-stable id** or the markers never dedupe and every gate fires on every
call. Claude Code takes `session_id` from the stdin JSON; the Copilot shims derive `copilot<host-pid>`.
`facade-gate` and `facade-tracker` additionally key on Claude Code's process PID to isolate parallel
sessions — a new agent adapts `get_session_id()` in those two scripts to its own identifier.

Existing shims, as worked examples: `copilot/copilot-pre-tool.py` and `copilot/copilot-post-tool.py`
(Copilot events → the stdin-JSON + env schema above), and `.opencode/plugins/workspace-policy.js`
(opencode's `tool.execute.before`/`after`, mapping exit-2 onto opencode's `throw` convention).

### Coverage across agents

| Hook | Git | Claude Code | Copilot | opencode |
|------|-----|-------------|---------|----------|
| Pre-read (interface redirect) | — | ✅ | ✅ | ✅ |
| Pre-edit (size / description) | — | ✅ | ✅ | ✅ |
| Pre-edit facade-scan (new files) | — | ✅ | ✅ | ✅ |
| Pre-edit facade-gate (`code/` edits) | — | ✅ | ✅ | ✅ |
| Post-edit (stubs / context sync) | — | ✅ | ✅ | ✅ |
| Post-read facade-tracker | — | ✅ | ✅ | ✅ |
| Context-gate (`CONTEXT.md` chain) | — | ✅ | ✅ | ✅ |
| Bash context-gate (cat/grep bypass) | — | ✅ | ✅ (terminal hints) | ✅ (bash tool) |
| Context / interface read tracker | — | ✅ | ✅ | ✅ |
| BUGS gate (FIXED needs a spec) | — | ✅ | ✅ | ✅ |
| Spec-read-gate (spec-locked modules) | — | ✅ | ✅ | ✅ |
| Size / facade import / stub gen / context sync | ✅ | — | — | automatic (git) |
| Spec-driven new-module gate | ✅ block | — | — | automatic (git) |
| Duplication gate (jscpd) | ✅ block | — | — | automatic (git) |
| `verify:fast` contract gate | ✅ block | — | — | automatic (git) |
| ESLint R1-R6 (TS under `code/`) | ✅ block | ✅ warn | ❌ gap | ❌ gap |
| Prettier auto-format (TS under `code/`) | — | ✅ | ❌ gap | ❌ gap |

The four ❌ are the live gaps: Copilot and opencode get no lint enforcement at all, so a TS
violation authored there is caught only at commit, by git.

## A ✅ in that table is a claim, and until 2026-08-19 nothing checked it

**Every path a shim spawns must resolve, and `test_shim_paths.py` asserts it.** The 2026-07-31
split moved scripts into `read/`, `checks/` and `facade/`; all eleven of opencode's spawns kept
pointing at `core/hooks/<script>` and were dead for weeks with every row above still reading ✅.
Repointed 2026-08-18. Writing the test on 2026-08-19 immediately found **three more, in the
Copilot shim, from the same split** — `read/facade-{tracker,gate,scan}.py`, which is to say the
facade-scan, facade-gate and post-read facade-tracker rows were ✅ for a runtime that could not
reach any of them.

**Two shims, one cause, found a day apart is the argument for the check rather than for another
careful reading.** What the check buys is bounded and the test says so in its own first lines: it
proves a path *resolves*, never that the gate *fires*. A shim whose paths all resolve can still
translate a payload wrongly, and that is a behavioural question this does not answer.

**So a new runtime's shim owes two things**, not one: the contract above, and an entry in
`SHIMS` in `core/tools/test/workspace/gates/test_shim_paths.py` naming its files and how a spawn
names a script. A shim with no entry is unchecked, which is the state opencode and Copilot were
both in.
