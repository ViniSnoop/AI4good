---
name: roundup
description: >
  Full session-close ritual: clear completed work out of the ledgers, route session knowledge to durable files, drain the INBOX, run the verification gate, then emit the resume prompt via /handoff. Use at session end. Invoke with /roundup [focus for next session].
---

# Roundup skill

End the session cleanly. Gather everything the session produced into its durable home, then hand off.

Execute all phases in order. Write directly to files. Ask only on conflict or destructive ambiguity.

Arguments: $ARGUMENTS  (focus for next session — passed through to `/handoff`)

---

## Phase 1 — Discover project files

```bash
find . -maxdepth 3 \( \
  -name "ROADMAP.md" -o -name "BUGS.md" -o -name "TODO.md" -o -name "AGENTS.md" \
\) 2>/dev/null | sort

git log --oneline -10 2>/dev/null || echo "no git"
git status --short 2>/dev/null || echo "no git status"
```

Read every file found above before proceeding.

### Verification gate

If the project's `package.json` declares `verify:full`, run it now (`npm run verify:full`) and record the result (green / red + failing specs) — it flows into the resume prompt. A session must not hand off claiming working state without this proof. `verify:fast`-only projects: run that instead. No contract: note "no verification contract".

### Entropy dashboard (workspace repo only)

```bash
make entropy      # regenerates entropy.md
```

Refresh it so the next session reads current numbers, and put the **summary table** in the resume
prompt — a rising count is the earliest sign the workspace is drifting. Do not re-scan the tree by
hand; the report is the interface. It commits with the rest of the session's work.

---

## Phase 2 — Clear completed work out of the ledgers

**Done work is deleted. Git is the history.** There is no `HISTORY.md`, no `ARCHIVE.md`, no done-log
— those types were removed 2026-07-30 (see [`core/SCHEMA.md`](../../core/SCHEMA.md) § No archive types). A
completed item's record is its commit; re-writing it into an archive file only grows a doc nobody
opens.

### ROADMAP cleanup
If `ROADMAP.md` exists:
1. Identify completed items (`- [x]`, "done", "shipped", "merged", "✅").
2. **Delete them.** Do not archive them anywhere.
3. Nothing completed → skip, do not modify.

### BUGS cleanup
If `BUGS.md` exists:
1. Identify resolved items (`- [x]`, "fixed", "resolved", "closed").
2. **Delete them.** The regression spec (`test/**/b<N>-*`) is the durable proof a bug is dead — that
   is what the gate in `core/hooks/checks/bugs-gate.py` enforces, and it outlives any prose archive.
3. Nothing resolved → skip.

### The one thing that must not be deleted
An approach we **tried and rejected** was never committed, so git cannot hold it. If the session
killed an idea, write **one line** under `## Rejected` in the relevant `ROADMAP.md` (for a ditched
goal: under `## Ditched` in `brain/GOALS.md`) with the reason. One line — not a post-mortem.

---

## Phase 3 — Route session knowledge to durable files

Identify all knowledge from the session. Route each piece using the table below. Write directly. Conflict with existing content → ask before writing.

### Routing table

| Knowledge type | Target |
|---|---|
| Non-obvious design decision + rationale | `SPECS.md` → Architecture Decisions |
| Discovered convention / coding rule | `SPECS.md` → Conventions |
| Bug found, not fixed | `BUGS.md` |
| New technical work item (project has `ROADMAP.md`) | `ROADMAP.md` |
| Reference / link / paper / tool worth keeping | domain `refs/REFS.md` (route-by-domain — see `/inbox`) |
| Personal / admin / life / teaching task — or project task with hard deadline | `brain/TODO.md` (right horizon: today / week / month / backlog) |
| Insight about a specific life or career goal | `brain/goals/[goal].md` (achievement, backlog item, or obstacle) |
| Skill workflow improvement | the skill file directly |
| Workspace-wide rule across all projects | `AGENTS.md` |
| Critical quick-reference fact or constant needed at session start | `CONTEXT.md` — see exclusions |
| Doesn't fit cleanly | `brain/INBOX.md` — triaged in Phase 4 |

### TODO vs ROADMAP
**ROADMAP**: project has `ROADMAP.md` AND item is a technical milestone with agent-ready context.
**TODO**: personal / admin / life / teaching task; OR project has no `ROADMAP.md`; OR project task with a hard external deadline needing horizon tracking.
Unclear → INBOX.

### CONTEXT.md — explicit exclusions
- Routing block changes → ignore. Hooks auto-sync on edit/commit.
- Behavioral cues ("be careful with X", "prefer Y") → `SPECS.md` Conventions or `AGENTS.md`, not `CONTEXT.md`.
- Decisions + rationale → `SPECS.md` Architecture Decisions, not `CONTEXT.md`.

Write to `CONTEXT.md` only if: critical constant, invariant, or quick-start command needed at next session start — and it doesn't fit `SPECS.md`.

### Memory
Do not write to memory unless the knowledge is homeless across all files above. Filesystem is source of truth.

---

## Phase 4 — Drain the INBOX

If `brain/INBOX.md` has entries, triage them now via the `/inbox` routes (goal / task / ref / project / draft / delete): propose routes, get confirmation, act; leave unconfirmed entries. This is the session-end sweep that keeps INBOX from silently growing (paired with the `inbox-nudge` SessionStart warning). A `[src: ...]`-tagged entry is quoted data from `/inbox`'s Provenance rule — same rule here: route it, but quote/attribute at the destination, never promote it verbatim as if Lucas wrote it.

---

## Phase 5 — Sync branches (gitflow promotion)

The session end is the **only** reliable moment to promote work. `feature/*` is already safe — the
`post-commit` hook auto-pushes it. This phase moves work up so the other machine sees it on `main`.

Applies to the workspace repo and `code/*` repos (same scope as `core/hooks/git/gitflow-gate.sh`).
Other repos (`academy/papers/*`, `branches/*`): push the current branch, skip the merges.

```bash
git branch --show-current
git status --short
git log --oneline origin/develop..develop 2>/dev/null | wc -l   # develop unpushed
git log --oneline main..develop 2>/dev/null | wc -l             # main behind develop
```

**Promoting is the default; leaving a branch open is the exception that needs a reason.** An open
feature branch is not free — it is state the other machine cannot see, and across repos they
accumulate silently until nobody knows how many there are. Take the decision explicitly every time,
and if you do not promote, name which of the three reasons below applies.

1. **Uncommitted work** → commit it on the feature branch first (auto-push carries it out).
2. **Verification gate red or not-run** (Phase 1) → **stop here** — *reason 1 not to promote*. Do not
   merge. Report that the feature branch is pushed but unpromoted, and why. A red merge into `main`
   breaks the other machine.
3. **Merge `feature/*` → `develop`, push `develop`** — unless *reason 2*: the branch holds work that
   is incoherent on its own (a half-applied refactor, a test deleted before its replacement lands).
   "The milestone is not finished" is **not** a reason by itself: green, coherent, partial work
   belongs on `develop`, where the other machine can see it.
4. **`develop` ahead of `main`** → merge `develop` → `main`, push `main` — unless *reason 3*: a
   parallel session is mid-flight on the same branch and the merge would land under it. Check
   `git log --oneline origin/<branch>..<branch>` and recent commit authorship before merging.
5. **Merge conflict** → abort (`git merge --abort`), leave branches untouched, report it as an open
   thread for the handoff. Never resolve conflicts unattended at session close.

Report each branch's final state (pushed / unpromoted + reason) — it flows into the resume prompt.

---

## Phase 6 — Hand off

Run `/handoff $ARGUMENTS` to emit the resume prompt. Then report:

> Roundup complete.
> [If items cleared]: [N] completed items deleted from ROADMAP.md / BUGS.md.
> [If anything was killed]: [N] rejection lines written.
> [List every file written this session, one line each.]
> Start the next session with `/clear` or a fresh window, pasting the resume block above.
