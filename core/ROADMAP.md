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

- [ ] **stubgen writes stubs into a doubled path when a package gains a subdirectory.** Splitting
      `code/flows/engine/tests/unit` into subject directories made stubgen emit
      `engine/tests/unit/<subject>/unit/<subject>/*.pyi` — a mirror of the path inside itself, one
      per new directory, all untracked. Same shape as the older `engine/tests/benchmarks/benchmarks/`
      debris. It resolves the output root relative to the wrong anchor. Deleted by hand both times;
      the next directory split will recreate it. (Found 2026-08-02 during the flows fanout drain.)
- [ ] **The generated `jsconfig.json` excludes the directory it is meant to include.** Every
      stubgen run over a JS folder printed `error TS18003: No inputs were found in config file
      '.../jsconfig.json'. Specified 'include' paths were '["*.js"]' and 'exclude' paths were
      '["<that same directory>"]'` — so no `.d.ts` is generated for any JS module and the failure is
      only a warning nobody reads. Sibling of the long-known broken `exclude` in
      `.opencode/plugins/jsconfig.json`; likely the same generator line. (Found 2026-08-02.)
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
- [ ] **Google-services CLI surface isn't standardized — two axes, one pass.** Token storage is already
      unified per `(service, alias)` (see [tools/CONTEXT.md](tools/CONTEXT.md)). What isn't:
      (a) **flags** — the command/flag surface of `core/tools/google/drive|gmail|calendar` diverges; audit
      each tool's `auth` subcommand + flags and converge on one shape (INBOX 2026-07-26);
      (b) **names** — Lucas wants `gmail`/`gdrive`/`gslides`/`gsheets` read as one family, but today it is
      `google/{drive,gmail,calendar}` plus a separate `slides/slides`, and no sheets tool exists at all.
      Decide the convention before a fifth tool lands: the `g` prefix is redundant *inside* `google/` and
      load-bearing *outside* it, so this is a directory-vs-name question, not a rename. (INBOX 2026-08-13)
- [ ] **Slides motion animation — is it scriptable at all?** Lucas wants movement authored from the CLI in
      Google Slides: lines and shapes moving, with start/end positions and controlled velocity and
      acceleration. First act is a capability check, not code — the Slides API exposes slide *transitions*
      and static shape geometry, so per-object motion tweens may simply not be in the API surface.
      **Lucas already named the fallback and it is the better-scoped problem:** if real motion is not
      scriptable, work out how far *slide-to-slide transition* can simulate it — the constraint being that
      it must survive export to **PDF**, i.e. the motion is carried by a generated sequence of slides
      (position/velocity/acceleration sampled into frames), not by a player feature. That version is
      squarely in reach of the existing `core/tools/slides/` surface and does not depend on the API
      answer. (INBOX 2026-08-13)
- [ ] **Notion access without MCP.** Lucas: *"será que dá pra acessar o meu notion? sem MCP? gostaria"* —
      a `core/tools/notion/notion` CLI on the official REST API with an internal integration token, shaped
      like `core/tools/google/` (per-alias token under `~/.config/workspace-notion/`). The MCP connector
      needs an interactive OAuth flow this workspace cannot run headless, which is precisely the argument
      for owning the CLI. Scope: list/search/read pages first; writing later. (INBOX 2026-08-13)
- [ ] **Audit our own skills — effective, or verbose and making work?** Lucas (INBOX 2026-08-13): check
      every `core/skills/*.md` for verbosity, redundancy, ambiguity, and steps that cost more than they
      save. Distinct from the survey bullet below — that one imports from outside, this one prunes what we
      already run. Sequence it after the six-practices assessment in [/ROADMAP.md](../ROADMAP.md) Frente 3,
      which decides the *shape* to prune toward (rules → interfaces).
- [ ] **`/caveman compress` — two bugs that outlive the rejection.** The measured rejection of compressing
      workspace docs is recorded in [/ROADMAP.md](../ROADMAP.md) Frente 3.2; these two survive it because
      the tool still runs on demand: (a) it strips the file's trailing newline
      (`skills/caveman/scripts/compress.py`, `write_text(compressed)`); (b) `compress.py:34` defaults
      `CAVEMAN_MODEL` to `claude-sonnet-4-5`, a stale model id. (INBOX 2026-07-30)
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
      A third lead arrived twice (INBOX 2026-08-02, two posts, same list): an **animation/UI skill set** —
      `threejs-skills`, `gsap-skills`, `motion-design-skill` (Lottie), `design-dna` (extract a site's visual
      identity), `genjutsu` (UI system). Same DM-bait shape, names only, no links — ref in
      [refs/REFS.md](refs/REFS.md). Worth a look for `code/isoroll-*` and `code/apptime` if any is real.

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
