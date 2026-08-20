# Gates
> What each blocking gate rejects, at commit time and at edit time.
> governs: core/hooks/pre-commit, core/hooks/gates/, core/hooks/checks/, core/hooks/read/

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
- `checks/type-gate.py`: a staged `.md` must be a known type or a well-shaped instance, sitting
  where its type is allowed. Ratchet — only what a commit **adds**. Law parsed from
  [`../SCHEMA.md`](../SCHEMA.md), never restated.
- `checks/citation-gate.py`: a roadmap item number (`Front 4.1`, and the bare `Front 9`) may not
  appear outside `ROADMAP.md` / `ROADMAP-<slug>.md`. **Not a ratchet** — the corpus was swept to
  zero on 2026-08-16, so every staged file is checked, not only what a commit adds. Completion is
  deletion here, so a cited number becomes a pointer to nothing the day the item lands; point at
  the `SPECS.md` / `SCHEMA.md` section that owns the rule instead. The gate also owns the
  `Frente`→`Front` rename by matching the citation *shape* rather than the word, because
  `frente` is ordinary Portuguese and a bare-word retired token fired on honest prose.

- `git/gitignore-self-heal.sh`: a new domain subdirectory carrying a `CONTEXT.md` gets its
  `!<domain>/<dir>/` allow line written automatically. **It then stops the commit** if that
  directory holds files git could not see — because staging happened before this hook ran, so
  those files are not in the index and the commit would ship a `CONTEXT.md` without the content it
  describes. It heals, names the directory, and asks for one `git add` and a re-run. A heal that
  hides nothing (the line was missing but the files were already tracked) lets the commit through.
  Ruled 2026-08-19 (Lucas), against the alternative of the hook staging the files itself: **a
  commit hook that stages what the caller did not is worse than the bug it fixes.**

### Branch drift

**HEAD is shared mutable state between parallel sessions, and until this existed nothing said so.**
Observed 2026-08-14: a session began on one branch, a parallel session switched the shared checkout
mid-flight, and the first session's commit landed on *their* branch and was auto-pushed there by
[`post-commit`](post-commit). It was caught only because that hook happens to print the branch it
pushed. **The branch read correct at session start**, which is why no start-of-session check can
catch it.

[`git/branch-marker.sh`](git/branch-marker.sh) records the branch at `SessionStart` and the
pre-commit path warns when HEAD no longer matches. Three properties carry the design:

- **Warn, never block.** A deliberate mid-session switch is legitimate and common.
- **Warn once per divergence.** The check re-records after warning, so the session that switched
  branches on purpose does not eat the same warning on every subsequent commit — a warning that
  repeats after being understood is one people learn to skip.
- **One marker per repo, not per session.** `record` runs where only the repo is known and `check`
  runs inside a git hook, which has no session id to pair with. A repo with no marker is silent,
  so nested repos and non-agent commits are unaffected.

Recovery is non-destructive and the warning prints it: confirm a fast-forward with
`git merge-base --is-ancestor <your-branch> HEAD`, then `git branch -f <your-branch> HEAD` and push
**yours**. Never reset or force-push theirs, and never `git checkout` your branch back — that yanks
HEAD out from under them, which is the same defect pointed the other way.

One worktree per session removes the shared HEAD entirely and is the better end state, but every
session must adopt it before it protects anything, and a checked-out worktree makes `git branch -d`
refuse — which fights the branch sweep in `core/skills/roundup.md` Phase 5. Ruled 2026-08-14
(Lucas): the warning now, worktrees as a later opt-in piloted on one parallel pair.

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
| `checks/heredoc-gate.py` | PreToolUse: Bash | **Warns, never blocks** — a heredoc writing a workspace file (`cat >`/`tee`) meets none of the `Edit|Write` gates. Silent for stdin-to-an-interpreter, which writes nothing |
| `compact/bash-compact-rewrite.py` | PreToolUse: Bash | **Rewrites, never blocks** — sends every line of a multi-line command through rtk, which parses line 1 only; delegates any payload it cannot split safely |
| `read/pre-read.sh` | PreToolUse: Read | **Blocks** reading a source file while its interface is current; warns when the interface is stale. Reading the interface unlocks the source for the session |
| `read/context-tracker.py` | PostToolUse: Read | Records `CONTEXT.md` reads and interface reads — the state both gates above consume |
| `read/spec-read-gate.py` | PreToolUse: Edit, Write (`code/` files) | **Blocks** editing a spec-locked module (`CONTEXT.md` `> spec:` + `SPECS.md` `status: locked`) until its `SPECS.md` was Read this session; nudges on new files in spec-less `code/` modules |
| `read/agent-context.py` | PreToolUse: Agent, SubagentStart | **Induces, never blocks** — hands a spawned worker the `>` line of each subtree its prompt names |
| `checks/issues-gate.py` | PreToolUse: Edit, Write (`ISSUES.md`) | **Blocks** flipping a bug to FIXED without a matching `test/**/b<N>-*` regression spec |
| `post-edit.sh` | PostToolUse: Edit, Write | Regenerates interfaces, scaffolds `jsconfig.json`/`tsconfig.json` if missing, reminds about a missing first-line comment, runs the routing sync |
| `session/precompact-wipe.sh` | PreCompact | Wipes the seen-markers, so the `CONTEXT.md` chain is re-read after compaction |
| `session/session-prune.sh` | SessionStart | Prunes session marker files older than 2 days |

**Why one of them only warns.** A `PreToolUse` hook fires *after* the model has emitted the tool
call, so by the time `heredoc-gate.py` sees a 3,000-character `cat >` payload those tokens are
already billed and already in the thread. Blocking cannot recover them — it makes the turn emit the
same content a second time as a `Write`. So the gate exists to change turn N+1, and its whole cost
is zero until it fires. Any gate whose subject is *what was already sent* has this shape; a gate
whose subject is *what is about to happen on disk* should still block.

**How a hook warns without blocking**, and two harness facts verified by running it (Claude Code
2.1.218, neither in the documentation):

- `PreToolUse` delivers `hookSpecificOutput.additionalContext` **to the model**, on exit 0, with the
  tool still running. That is the only non-blocking channel that reaches the model: exit-0 stdout is
  transcript-only and `systemMessage` addresses Lucas, not the agent. **Every "Informs" hook uses it**
  — `facade-scan.py` printed to stdout until 2026-08-16 and so was read by nobody, which is the
  asymmetry this line used to record. Asserted now by
  `test_an_informing_hook_speaks_on_the_channel_that_reaches_the_model`.
- **A `.claude/settings.json` hook edit is live in the session that made it.** Registration is not
  captured at session start, which was an open question for two sessions. Probed by adding
  `heredoc-gate.py` and running one heredoc write in the same session; the context arrived.

Why a subagent is exempt from the context gate, and why the briefing needs two events to work:
[`../SPECS-session.md`](../SPECS-session.md) § AD-13.
