# Hooks — Specs
> What must be true of the enforcement layer, and why: what each gate blocks, and the contract a new agent's shim must satisfy.

Companion to [`CONTEXT.md`](CONTEXT.md), which says what this directory *is* and routes into it.
This file holds the constraints. Installing the toolchain these gates depend on is a third
question, answered by [`SETUP.md`](../../SETUP.md).

## The law lives in file_law.py / schema_law.py / limits.env, never in a checker

A checker that restates any of these is the drift the checkers exist to catch. This has bitten
twice: five separate definitions of "a code file" existed across different checkers before they
were unified behind `file_law.is_code_file`, guarded now by
`core/tools/test/law/test_file_law.py::test_no_checker_carries_its_own_extension_list`. And
`entropy_corpus.py`'s `_CHECKER` / `_CHECKER_TESTS` constants once spelled out a sibling path by
hand — a hard-coded path stops exempting the retired-token checker (and its own test file) from
itself the moment `core/hooks` moves. The fix derives both from `Path(__file__)` instead, so a
future move cannot break it the same way.

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

## Git pre-commit (`pre-commit`)

Applied globally via `core.hooksPath`, so it fires on every `git commit` in **every** repo under
this workspace.

- Warns on code files ≥ 150 lines, blocks ≥ 200. Thresholds in [`limits.env`](limits.env); which
  extensions count is [`file_law.py`](file_law.py)'s answer, never a checker's.
- Warns when a newly staged code file lacks its first-line description comment.
- Hard-blocks cross-module imports that bypass the facade (`index` / `__init__`), via
  `facade/check-facade-imports.py`.
- Auto-syncs the `CONTEXT.md` routing block for every directory with staged files, and stages it.
- Auto-generates and stages `.pyi` (stubgen), `.d.ts` (tsc), `.dart.api` (`stubgen/dart-api-extract.py`).
- Runs `checks/check-line-counts.sh` over staged files — the same script that also runs standalone
  for a workspace-wide audit.
- `verify:fast` contract: a project declaring that script must be green, or the commit is blocked.
- `checks/check-duplication.py`: jscpd over the committing repo, blocking clones that involve
  staged files (75 tokens / 10 lines).
- Spec-driven module gate: a new `CONTEXT.md` under `code/` must declare `> spec: <file>` or
  `> spec: none`. Ratchet — existing modules are grandfathered.

**No exemptions for vendored third-party code.** Anything brought into the workspace complies with
the same gates as our own code. A `.vendor` marker that switched them off was tried and rejected
(2026-07-23, Lucas: *"even thirdparty solutions, once brought to our w-os should comply with our
rules. opening exceptions is quite dangerous"*). Vendoring means adopting and adapting, not parking
a copy: split what is too big, and record the deviations so a future re-sync knows what it is
merging against — the live example is `core/skills/caveman/CONTEXT.md` § Local adaptations.

## Agent lifecycle gates

Bound by absolute path from `.claude/settings.json`, and by the equivalent registration in each
other provider's shim.

| Script | Trigger | Behaviour |
|--------|---------|-----------|
| `checks/pre-edit.py` | PreToolUse: Edit, Write | **Blocks** an edit pushing a code file past 200 lines; **blocks** Write of a new file with no first-line description comment |
| `facade/facade-scan.py` | PreToolUse: Write (new files in `code/`) | **Informs** — prints the exports the target module's facade already declares, warns if that list is empty |
| `facade/facade-gate.py` | PreToolUse: Edit, Write (`code/` files) | **Blocks** edits to a `code/` module file until the nearest facade was Read this session |
| `facade/facade-tracker.py` | PostToolUse: Read | Records facade reads, consumed by `facade-gate.py` |
| `read/context-gate.py` | PreToolUse: Read, Edit, Write, Grep, NotebookEdit | **Blocks** file access until the target subtree's `CONTEXT.md` chain was Read this session. Session-deduped; `CONTEXT.md`/`AGENTS.md` targets exempt |
| `read/bash-context-gate.py` | PreToolUse: Bash | **Blocks** Bash commands naming workspace files in subtrees whose chain is unread — this is what closes the `cat`/`grep` bypass |
| `compact/bash-compact-rewrite.py` | PreToolUse: Bash | **Rewrites, never blocks** — sends every line of a multi-line command through rtk, which parses line 1 only; delegates any payload it cannot split safely |
| `read/pre-read.sh` | PreToolUse: Read | **Blocks** reading a source file while its interface is current; warns when the interface is stale. Reading the interface unlocks the source for the session |
| `read/context-tracker.py` | PostToolUse: Read | Records `CONTEXT.md` reads and interface reads — the state both gates above consume |
| `read/spec-read-gate.py` | PreToolUse: Edit, Write (`code/` files) | **Blocks** editing a spec-locked module (`CONTEXT.md` `> spec:` + `SPECS.md` `status: locked`) until its `SPECS.md` was Read this session; nudges on new files in spec-less `code/` modules |
| `read/agent-context.py` | PreToolUse: Agent, SubagentStart | **Induces, never blocks** — hands a spawned worker the `>` line of each subtree its prompt names |
| `checks/bugs-gate.py` | PreToolUse: Edit, Write (`BUGS.md`) | **Blocks** flipping a bug to FIXED without a matching `test/**/b<N>-*` regression spec |
| `post-edit.sh` | PostToolUse: Edit, Write | Regenerates interfaces, scaffolds `jsconfig.json`/`tsconfig.json` if missing, reminds about a missing first-line comment, runs the routing sync |
| `session/precompact-wipe.sh` | PreCompact | Wipes the seen-markers, so the `CONTEXT.md` chain is re-read after compaction |
| `session/session-prune.sh` | SessionStart | Prunes session marker files older than 2 days |

Why a subagent is exempt from the context gate, and why the briefing needs two events to work:
[`../SPECS.md`](../SPECS.md) § AD-13.

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

## Generated artifacts

### Interface files

Every save of a supported source file produces its interface unconditionally — universal, no
per-project config.

| Language | Output | Tool | Notes |
|----------|--------|------|-------|
| Python | `.pyi` | `stubgen` | on every edit and every commit |
| JavaScript | `.d.ts` | `tsc --allowJs --emitDeclarationOnly` | `jsconfig.json` auto-scaffolded if missing (IDE use only) |
| TypeScript | `.d.ts` | `tsc --emitDeclarationOnly` | `tsconfig.json` auto-scaffolded if no ancestor config is found |
| Dart | `.dart.api` | `stubgen/dart-api-extract.py` | public class/mixin/method signatures; needs Python 3 only, no Dart SDK |
| LaTeX | `.texif` | `stubgen/tex-interface-gen.py` | structure, full equations, floats, citations, TODOs, section opening sentences. Also regenerates `labels.md` (cross-file label registry + dangling-ref check). A `.bib` edit warns about missing `reviews/<key>.yaml` |

**To bypass the size gate temporarily**, edit `BLOCK_LINES` in [`limits.env`](limits.env), do the
operation, revert. Both `checks/pre-edit.py` and `checks/check-line-counts.sh` read it immediately.

### The `CONTEXT.md` routing block

`routing/context_synchronizer.py` runs on every edit (via `post-edit.sh`, which also re-syncs the
parent directory) and every commit. It keeps each directory's `## Routing` block true without
anyone maintaining it:

- **adds** a new file, taking its description from the first source that answers, in this order:
  the first-line comment (code, below any shebang), a module docstring's first line (`.py`, per
  PEP 257), `description:` frontmatter then the line-2 `> ` blurb (`.md`), or the ` — ` usage
  comment (extensionless scripts)
- **removes** entries for deleted files, and **links** interfaces to their source
- **folds** a leaf directory under `WARN_FILES` into the parent block; **links** one at or above it,
  or one that carries its own `CONTEXT.md`
- **warns** when a directory exceeds `WARN_FILES` direct files

**Never edit inside the `<!-- routing:start/end -->` sentinels** — the next sync overwrites it.
**Renames are not tracked**: the old entry disappears and the new file arrives with a placeholder,
so the description is rewritten by hand after a rename.

**A `← add` marker is a claim about the generator before it is a claim about the file.** Four times
out of four (2026-08-15) the text was already there and this list was not reaching for it: `.sh` and
`.jsx` had no `COMMENT_RE` pattern, `.py` matched only a single-line docstring, `.env`/`.txt` were
outside `CONTENT_EXTS`, and `.md` rows read the H1 instead of the blurb. **Check the extension's
entry in `routing/workspace_meta.py` before writing a description by hand** — and when a whole
extension is undescribable, fix it there, because a sweep re-fills.

**Hoisted text is bounded and rebased; authored text is not.** A `.md` blurb and a subdirectory
blurb were written to sit under their own heading, in their own directory, so
[`routing/hoist.py`](routing/hoist.py) rebases their links and cuts them at `DESC_LIMIT`. A code
file's first-line comment goes in untouched: it was authored as this table's one-liner and cutting
it would lose text nothing else carries.

### First-line descriptions

Every code file begins with a one-line description comment, because `context_synchronizer.py` reads
it as the canonical description and writes it into `CONTEXT.md`. It is enforced three times, each
weaker than the last: **Write** is blocked outright, **Edit** gets an in-session reminder, and
**commit** warns.

## What a working install looks like

Behavioural assertions — these are what the gates promise, and the list a new shim is tested
against. The commands that check the toolchain itself are in [`SETUP.md`](../../SETUP.md) § Verification.

- edit a `.py` / `.js` / `.ts` / `.dart` file → its interface regenerates immediately
- edit a `.tex` file → `.texif` **and** `labels.md` regenerate; a `.bib` edit warns about bib keys
  with no `reviews/<key>.yaml`
- read a source file whose interface is current → blocked, interface first
- grow a code file past 200 lines → the edit is blocked
- create a new file with no first-line comment → the Write is blocked
- edit a file already missing that comment → a reminder prints, the edit stands
- commit a 200+ line code file → the commit is rejected
- commit any staged code file → its `CONTEXT.md` routing block is updated and staged
