# Core Library Roadmap
> Making the agent library sound: one enforced frontmatter contract per layer, symmetric within layer/type. Contract in [SCHEMA.md](SCHEMA.md). Completed work archived in [HISTORY.md](HISTORY.md).

Goal: [[spec-driven-development]] — SPEC-v0 pilot on the `core/` agent library.
No flow is privileged — the exemplar is `flows/_template.md`. (The old "reference implementation /
validator's oracle" status of `deepresearch` was retired 2026-07-23; see [SCHEMA.md](SCHEMA.md).)

## Open

- [ ] **`gitignore-self-heal.sh` wrongly stages `code/*` project dirs as bare gitlinks.** Found live
      2026-07-26: 13 dirs (`code/aiwbot`, `dobra`, `flows`, `isoroll-module`, etc.) showed up staged
      as mode-160000 gitlinks with no `.gitmodules`, which `gitflow-gate.sh`'s undeclared-gitlink
      check correctly rejected at commit time. The self-heal hook (Frente 6, shipped 2026-07-25) is
      meant to un-ignore new context-bearing subdirs so their `CONTEXT.md`/structural files get
      tracked — it should never `git add` the nested-repo directory itself, only its own tracked
      files. Fix the hook to skip/exclude paths that are themselves git repos (have `.git`).
      Workaround used: `git rm --cached -f <path>` before commit. Same class as the pointer-
      integrity bug above — anti-entropy tooling (Frente 4 Tier 0) catching its own sibling's bug.
- [ ] **Ad-hoc venv deps have no declared home — three now.** Each was `pip install`ed directly into
      `.venv` to unblock a tool, so a fresh workspace clone silently loses the capability:
      `pypandoc-binary` (`core/tools/parse` on `.docx`, else `FileNotFoundError: pandoc`),
      `secretstorage` (`core/tools/video` reading Brave cookies — without it yt-dlp fails with an
      AES-CBC decrypt error that reads like wrong credentials, cost a session to diagnose), and
      `gallery-dl` (`core/tools/video` image/carousel path). Fix the class, not the instances:
      a declared dep list or a SETUP.md step the whole `core/tools/` surface is checked against.
- [ ] **2b — craft-agent tier source + generator.** Create `core/agents/craft-{low,medium,high}.md`
      carrying `tier:`; extract the craft flow's tier→model map to `core/tier-map.json`; add a
      generator that emits `.claude/agents/craft-*.md` with `model:` resolved. Removes the last
      provider-name-in-source violation (`model: haiku`). Symmetric with the skills mirror.
      *Unblocked 2026-07-23* — the parallel session's work is committed and the agent mirrors were
      renamed `loop-*`→`craft-*` in craft-flows step 1; only the `core/` source + generator is left.
- [ ] **Skill `flow:` field — loops.md.** research.md done (`flow:` comma list, router shape).
      loops.md needs `flow: craft` (or the router slug). *Unblocked 2026-07-23*, same as 2b.

- [ ] **Survey outside skills, decide what to import.** Lucas's ask (INBOX 2026-07-23): take skills
      seriously as a category and study whether any are worth importing into `core/skills/`. Two
      concrete leads, both DM-bait posts that name skills without linking them, so both need a real
      search first: [five general Claude Code skills](https://www.instagram.com/reel/DavN_06t105/)
      (tool discovery, plan-before-code, cross-session project memory, frontend design, self-improvement
      — the first three overlap what `AGENTS.md` + `/loops` + CONTEXT.md already do, so the question is
      overlap vs gap) and the NB-oriented pair captured in `code/isoroll-content/refs/REFS.md`.
      Lucas also asked for a general sweep for **game-asset-generation** skills while doing this.
- [ ] **Audit context building — are we overdoing it?** Lucas's ask (INBOX 2026-07-23): measure what
      actually loads at session start (`AGENTS.md` chain + every `CONTEXT.md` on the path + memory)
      and whether it has grown past its worth. Includes: consider trimming `MEMORY.md`, and inspect
      what is being stored unannounced under the `~/.claude/` folders. Pairs with the session-size
      monitor and context-drift items already in `brain/TODO.md`.
      → **Now Frente 3.2 of [/ROADMAP.md](../ROADMAP.md)** (workspace-os robustness). Reframed by the
      2026-07-23 research: keep CONTEXT.md *local/granular* (it is what makes weak models work, per
      [P] 2607.17598), cap *chain depth* not file count. Do the audit there; this line is the pointer.

- [ ] **`engineering` is exempted by path, not typed — a privileged special case.** `flows/craft/`
      is skipped by `validate_flows` because the `type` enum has no `engineering` value, so the one
      cluster that is not schema-checked is exactly the one that does the most work. Symmetric fix:
      add `engineering` to the enum, give `craft`/`route`/`architect` real frontmatter (`type`,
      `confirm`, `agents`), delete the path exemption in `sync-skills`. Found while executing
      craft-flows step 1 (2026-07-23) and written down rather than taken silently — it is a schema
      change, and the 8 decided steps did not include it. Note the `uses:` DAG check already covers
      the cluster, so only the type layer is unguarded.
- [ ] **Skill name `loops` vs flow name `craft` — the rename stopped at the skill boundary.**
      `/loops` still dispatches to `flows/craft/craft.md`. Step 1 deliberately listed only the flow
      files, so the skill kept its name; the result is one concept with two words at two layers,
      which the location rule (`flows/<skill>/` ⟺ dispatcher skill name) would otherwise make
      `flows/loops/`. Decide: rename the skill to `craft`, or keep `loops` and record why.

- [ ] **Google-services auth CLI surface isn't standardized across drive/gmail/calendar.** Token
      storage is already unified per `(service, alias)` (see `core/tools/CONTEXT.md`), but the
      command/flag surface of `core/tools/drive|gmail|calendar` isn't — audit each tool's `auth`
      subcommand + flags and converge on one shape. (INBOX 2026-07-26)
- [ ] **Routing-sync tool (`context_synchronizer.py`) has two bugs**, found by the Tier-0
      pointer-integrity checker (shipped 2026-07-25) but out of that checker's own scope:
      1. Unrewritten relative links when hoisting — a child CONTEXT.md's line-2 description is
         copied verbatim into the parent's routing-table row, including any relative markdown
         links, which then resolve from the wrong directory one level up. Seen live:
         `branches/casinhas/CONTEXT.md` (burocracia row: `BUROCRACIA.md`, `docs/`) and
         `code/{apptime,dobra,isoroll-content}/CONTEXT.md` (refs row: `REFS.md`). Fix: strip links
         from hoisted descriptions, or rewrite the path prefix on hoist.
      2. Stale rows survive file deletion — the routing block only updates on save of an existing
         file, so deleting a file out-of-band leaves a dangling row. Seen live:
         `core/prompts/CONTEXT.md` (rows for deleted `fable-loop-engineering.md`,
         `fable-multiview.md`) and `academy/papers/2027-CHI-cria/outputs/CONTEXT.md` (row for
         deleted `cria-workflow.md`). Fix: a prune pass, or hook the delete path too.
      (INBOX 2026-07-25, via pointer-integrity build)
- [ ] **`core/tools/video --level full` crashes on image-only posts** (gallery-dl carousel path):
      `assemble()` always tries `media().transcribe(audio)` when an audio path is truthy, but an
      image post has no real audio stream → `IndexError: tuple index out of range` inside
      `faster_whisper`/`av`. Workaround found live: use `--level visual` instead (skips audio
      entirely) — works. Fix: `assemble()` should detect the image-post case (no video stream) and
      skip the transcribe step instead of attempting it. Found triaging INBOX 2026-07-26.
- [ ] **Subagent cost is concentrated — configure cheaper models where the work is mechanical.**
      Measured usage (last 24h, this machine): 59% of usage from subagent-heavy sessions, 55% from
      >150k-context sessions, 25% from `/roundup`, 22% from `/loops` subagents specifically.
      Action: set cheaper models in `/roundup` and `/loops` (craft-flow) subagent frontmatter for
      mechanical steps; re-measure after. (INBOX 2026-07-26)

## craft-flows — the execution item (decided 2026-07-23, not yet built)

All of the below was **decided in discussion with Lucas on 2026-07-23** and needs an execution
session. The reasoning is recorded in [SCHEMA.md](SCHEMA.md) § *Composition and cycles*; read that
first. Nothing here is open for re-litigation — it is build work.

**The decision in one line:** "loop" is retired as the word for connected agents; **flow** is
canonical; flows compose into a DAG; loops live only at execution time, bounded.

- [x] **1. Retire the `loop-*` vocabulary — rename + fold into `flows/craft/`.**
      `loop-engineering`→**`craft`**, `loop-router`→**`route`**, `loop-architecture`→**`architect`**,
      `LOOP-TREE.md`→**`TREE.md`**. Single-word filenames (Lucas's convention: prefer the full word
      over a truncation — this is why `architect` beat `arch` and `literature` beat `lit`). They move
      into `core/flows/craft/` per the ownership rule. Blast radius is cross-domain: ~14 `brain/`
      files reference `loop-engineering` by path (goals, `GOALS.md`, `.log/done.md`, attachments) plus
      the `loop-*` agents and both mirrors — **do this from a session already editing those goal
      files**, per the parallel-session partition rule. Update the `loop-*` exemptions in
      `SCHEMA.md` § Enforcement and in `sync-skills validate_flows` (they match on the `loop-` prefix).

- [x] **2. Rename the goal + concept to `craft-flows`.** `brain/goals/loop-engineering.md` →
      `brain/goals/craft-flows.md`, and the concept "loop engineering" → "craft flows" **wherever it
      appears** (Lucas's call: option (c), applied broadly — not just the flow files). Includes
      `brain/GOALS.md`, `brain/goals/CONTEXT.md`, and the goal cross-refs in `spacemantics.md`,
      `spec-driven-development.md`, `workspace-os.md`. The `[[craft-flows]]` wiki-links must be
      repointed or they dangle.

- [x] **3. `deep` → `sota`, and redefine what it produces.** Not a rename — a **redefinition**, which
      is why it was deliberately *not* done in the 2026-07-23 session (a `sota.md` still holding
      deepresearch content would be worse than leaving it). New contract:
      fill the relevant `refs/REFS.md` **plus per-paper `*.yaml`** files following the existing
      review/tier strategy, and emit a **≤200-line** summary *written to support a decision* — **not**
      a related-work section, not a giant brief. Rationale: the lean human-facing summary and the rich
      machine-facing yaml serve different readers (Lucas reads 200 lines; future flows read the yaml),
      which is the "artifact is the memory" thesis. Note the scope narrows from "deep dive on
      anything" to "map the state of the art of a field" — accepted, it makes a vague flow crisp.
      Name is `sota` (the field-standard acronym) — **not** `soat`, which reads as a typo of it.

- [x] **4. Make `scout` compose `sota` (the first real DAG edge).** `scout` and `sota` share the
      entire gathering half; today `scout.md` only *asks in prose* not to reimplement search. Make it
      a declared edge — `uses: sota` — so `scout = sota + map-to-our-system + write tiered plan into a
      ROADMAP`. Keep **both** entrypoints: `sota` alone when you want the field map and no plan;
      `scout` when you want the plan too. This is the dogfood case for the composition model.

- [x] **5. Consolidate the template; the oracle is already retired.** `SCHEMA.md` no longer anoints a
      reference implementation (retired 2026-07-23 — Lucas: *"sota should not be special… a template
      should be a template"*; the dual role coupled one flow's evolution to the schema). **Remaining
      work:** physically move the canonical discipline wording (tool-discipline, required-artifacts,
      provenance, scale-gate, integrity) out of `flows/research/deep.md` into `flows/_template.md`,
      annotated by which `type` requires each block, then repoint SCHEMA's "copy from there" pointer.
      SCHEMA currently carries an explicit *migration pending* note — delete it when done.

- [x] **6. Build the cycle guard (two mechanisms, do not merge them).**
      (a) **Static DAG check** in `sync-skills validate_flows`: parse `uses:` from flow frontmatter,
      walk the graph, fail with a clear message if any path returns to its start. This is definition
      time, offline, cheap — and `validate_flows` is already recursive, so it is the natural home.
      (b) **Runtime iteration cap** on execution loops (max N retries + an explicit exit condition),
      which is what makes step-level retry edges safe. (a) forbids cycles; (b) *permits* them,
      bounded. Applying (a) to retry edges would wrongly kill the useful loops.

- [x] **7. Decompose the `craft` monolith by load-frequency.** `craft.md` is ~52 KB and
      mixes three levels: general rules that apply to *all* flows, the one specific build flow, and
      heavy reference material (field practice, case studies, prior art). Split by **access pattern**,
      not arbitrarily — this is what resolves the tension with our own finding that blind .md
      fragmentation hurts: (i) general flow rules → up to `SCHEMA.md` / `flows/CONTEXT.md`, since they
      were never specific to one flow; (ii) the always-loaded protocol → a lean `flows/craft/craft.md`;
      (iii) field practice / case studies / prior art → on-demand subfiles in `flows/craft/`, loaded
      only when relevant (the `skills/foundry/` pattern). Always-needed stays one file; rarely-needed
      becomes subfiles. Stratification, not fragmentation. Good technique to apply during the split:
      `/caveman-compress` **plus** an Opus pass that compresses *content* (redundancy, prose→table,
      outright cuts), not just wording.

- [x] **8. Fold multi-mode skills into folders.** `skills/caveman*` (lite/full/ultra/wenyan variants,
      plus `caveman-commit`/`-review`/`-compress`/`-help`/`cavecrew`) → `skills/caveman/` with a
      router on top and one subfile per mode — same `skills/foundry/` pattern, same reasoning as
      item 7. Note these live in `~/.agents/skills/` (global, outside the workspace) and are **not**
      synced by `core/tools/sync-skills` — check that before moving anything.

## ablation-bench (INBOX 2026-07-25)

- [ ] **Promote the ablation-bench pilot out of `tmp/` and run the follow-up.** First pilot lives in
      `tmp/ablation-bench/` (1 trial per arm, with/without the CONTEXT.md chain gate, race-bug toy
      project; opencode+glm-5.2 operated end-to-end). Result in its `REPORT.md`: the original
      hypothesis was **not supported** — both arms read CONTEXT.md voluntarily because the prompt asked
      for it, so the gate added no safety *against that prompt*. Real finding: glm-5.2 completed the
      reduced `/loops` flow with a working `executor:` self-report + commit when budget ≤ 10 min.
      Move the durable REPORT + design somewhere real **before** `tmp/` gets cleaned (it will — see
      workspace-os cleanup). Follow-up changes (from REPORT § "What a follow-up run would change"):
      prompt that does *not* mention a "documented contract", no marker flag in the seeder, n ≥ 4,
      equal wall-clock budget per arm, and a **third arm** (gate-off + prompt-off) to isolate the effect.

## Notes

- `.claude/` + `.opencode/` are generated mirrors (tracked). Never hand-edit; run `sync-skills`.
- `sync-skills` prunes orphans on every `sync` now — renaming/removing a skill no longer dangles.
