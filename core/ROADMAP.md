# Core Library Roadmap
> Making the agent library sound: one enforced frontmatter contract per layer, symmetric within
> layer/type. Contract in [SCHEMA.md](SCHEMA.md). Completed work is deleted -- git is the history.
>
> **Scope: agent-library internals only** — skills, agents, flows, tools, and their schema. Workspace
> scaffold work (hooks, gitignore, anti-entropy, cost, portability) lives in the single wos ledger,
> [/ROADMAP.md](../ROADMAP.md). An item belongs to exactly one of the two.

Goal: [[spec-driven-development]] — SPEC-v0 pilot on the `core/` agent library.
No flow is privileged — the exemplar is `flows/_template.md`. (The old "reference implementation /
validator's oracle" status of `deepresearch` was retired 2026-07-23; see [SCHEMA.md](SCHEMA.md).)

## Open

- [ ] **2b — craft-agent tier source + generator.** Create `core/agents/craft-{low,medium,high}.md`
      carrying `tier:`; extract the craft flow's tier→model map to `core/tier-map.json`; add a
      generator that emits `.claude/agents/craft-*.md` with `model:` resolved. Removes the last
      provider-name-in-source violation (`model: haiku`). Symmetric with the skills mirror.
- [ ] **Skill `flow:` field — loops.md.** research.md done (`flow:` comma list, router shape).
      loops.md needs `flow: craft` (or the router slug).
- [ ] **`engineering` is exempted by path, not typed — a privileged special case.** `flows/craft/`
      is skipped by `validate_flows` because the `type` enum has no `engineering` value, so the one
      cluster that does the most work is exactly the one that is not schema-checked. Symmetric fix:
      add `engineering` to the enum, give `craft`/`route`/`architect` real frontmatter (`type`,
      `confirm`, `agents`), delete the path exemption in `sync-skills`. The `uses:` DAG check already
      covers the cluster, so only the type layer is unguarded.
- [ ] **Skill name `loops` vs flow name `craft` — the rename stopped at the skill boundary.**
      `/loops` still dispatches to `flows/craft/craft.md`. One concept, two words at two layers; the
      location rule (`flows/<skill>/` ⟺ dispatcher skill name) would otherwise make it `flows/loops/`.
      Decide: rename the skill to `craft`, or keep `loops` and record why.
- [ ] **Google-services auth CLI surface isn't standardized across drive/gmail/calendar.** Token
      storage is already unified per `(service, alias)` (see [tools/CONTEXT.md](tools/CONTEXT.md)), but
      the command/flag surface of `core/tools/google/drive|gmail|calendar` isn't — audit each tool's `auth`
      subcommand + flags and converge on one shape. (INBOX 2026-07-26)
- [ ] **Routing-sync tool (`context_synchronizer.py`) bugs** — found by the Tier-0 pointer-integrity
      checker but out of that checker's scope. Three known: unrewritten relative links when hoisting a
      child's line-2 description; stale rows surviving file deletion; a duplicate routing block appended
      to hand-curated CONTEXT.md files that use a manual `## Routing` without sentinels. Live cases and
      the fix shape are specced in [/ROADMAP.md](../ROADMAP.md) § Batch B item 1 — execute from there,
      this line is the library-side pointer.
- [ ] **Survey outside skills, decide what to import.** Lucas's ask (INBOX 2026-07-23): take skills
      seriously as a category and study whether any are worth importing into `core/skills/`. Two
      concrete leads, both DM-bait posts that name skills without linking them, so both need a real
      search first: [five general Claude Code skills](https://www.instagram.com/reel/DavN_06t105/)
      (tool discovery, plan-before-code, cross-session project memory, frontend design, self-improvement
      — the first three overlap what `AGENTS.md` + `/loops` + CONTEXT.md already do, so the question is
      overlap vs gap) and the NB-oriented pair captured in `code/isoroll-content/refs/REFS.md`.
      Lucas also asked for a general sweep for **game-asset-generation** skills while doing this.

## craft-flows — DONE 2026-07-23/25

All 8 steps shipped: `loop-*` vocabulary retired for **flow** (`craft`/`route`/`architect`, `tree.md`),
the goal renamed `craft-flows`, `deep` redefined as `sota` (tiered `REFS.md` + per-paper yaml + a
≤200-line decision-support summary), `scout` composes `sota` via a declared `uses:` edge (the first
real DAG edge), the template consolidated with the oracle retired, the cycle guard built as two
separate mechanisms (static DAG check in `validate_flows` forbids cycles; a runtime iteration cap
*permits* bounded retry loops), `craft.md` decomposed by access pattern, and multi-mode skills folded
into router folders. Reasoning recorded in [SCHEMA.md](SCHEMA.md) § *Composition and cycles*.

## ablation-bench

- [ ] **Promote the ablation-bench pilot out of `tmp/` and run the follow-up.** First pilot lives in
      `tmp/ablation-bench/` (1 trial per arm, with/without the CONTEXT.md chain gate, race-bug toy
      project; opencode+glm-5.2 operated end-to-end). Result in its `REPORT.md`: the original
      hypothesis was **not supported** — both arms read CONTEXT.md voluntarily because the prompt asked
      for it, so the gate added no safety *against that prompt*. Real finding: glm-5.2 completed the
      reduced `/loops` flow with a working `executor:` self-report + commit when budget ≤ 10 min.
      Move the durable REPORT + design somewhere real **before** `tmp/` gets cleaned (it will — see
      [/ROADMAP.md](../ROADMAP.md) Frente 6.1). Follow-up changes (from REPORT § "What a follow-up run
      would change"): a prompt that does *not* mention a "documented contract", no marker flag in the
      seeder, n ≥ 4, equal wall-clock budget per arm, and a **third arm** (gate-off + prompt-off) to
      isolate the effect.

## Notes

- `.claude/` + `.opencode/` are generated mirrors (tracked). Never hand-edit; run `sync-skills`.
- `sync-skills` prunes orphans on every `sync` now — renaming/removing a skill no longer dangles.
