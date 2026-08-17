# Core Library Roadmap
> Making the agent library sound: one enforced frontmatter contract per layer, symmetric within
> layer/type. Contract in [SCHEMA.md](SCHEMA.md). Completed work is deleted -- git is the history.
>
> **Scope: agent-library internals only** — skills, agents, flows, tools, and their schema. Workspace
> scaffold work (hooks, gitignore, anti-entropy, cost, portability) lives in the single wos ledger,
> [/ROADMAP.md](../ROADMAP.md). An item belongs to exactly one of the two.

Goal: [[spec-driven-development]] — SPEC-v0 pilot on the `core/` agent library.
No flow is privileged — the exemplar is `flows/_template.md` (see [SCHEMA.md](SCHEMA.md)).

## Open

- [ ] **The `video/` family name now describes less than the family delivers.** It gained a page
      fallback — a link with no media goes to `web/fetch` — so what it actually offers is *link →
      navigable text*, and the directory name still says one medium. Captured by Lucas
      (INBOX 2026-08-16) and routed here 2026-08-16; the asymmetry was written down deliberately
      rather than renamed, because [`tools/SPECS.md`](tools/SPECS.md) § Naming records that two path
      sweeps have already happened and a third is not free. **The item is the trigger, not the
      decision**: settle it the next time something else opens `core/tools/` for a path change, and
      pay one sweep instead of two. A rename with no other reason to touch those paths is the case
      SPECS already rejected.
      → **model: sonnet**.
- [ ] **`parse_owns` swallows prose as declared paths.** In
      [`hooks/brain/brain_attention.py`](hooks/brain/brain_attention.py), the `>**owns**` block ends
      only at the next `>**field**` or a `##` heading, so a blank line followed by an ordinary
      blockquote stays inside it and every sentence becomes a candidate path. Visible on **every
      commit** as `[Brain] ⚠ <goal>: owns '<prose>' ... which resolves to no repo` — at least
      `craft-flows`, `burocracia-academica`, `ecovila`. The noise is the real cost: it trains the
      reader to skip post-commit output, which is where the gates also speak. Likely fix: end the
      block at the first blank line. Add a case to the brain tests with a goal file whose `owns`
      block is followed by prose.
      → **model: sonnet**.
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
- [ ] **Rename the skill `loops` → `craft` — ruled 2026-08-14 (Lucas).** `/loops` dispatches to
      `flows/craft/craft.md`: one concept, two words at two layers. Renaming the skill restores the
      location rule (`flows/<skill>/` ⟺ dispatcher skill name) instead of dragging the flow pool
      backwards to `flows/loops/`. **Ship it inside the Front 4.2 sweep in
      [/ROADMAP.md](../ROADMAP.md), not separately** — that sweep already renames `.loop/` → `.craft/`
      and `.loop-skills/` → `.craft-skills/` across 14 live state dirs and 74 doc mentions, and this
      skill is the generator-side half that made the rename keep coming back. Keep **"Loop 0..6"** as
      step names: an iterative step really is a loop, and that word is correct English, not the
      retired label. Add `loops` to `core/SCHEMA.md` § Retired tokens the moment it lands, so the
      check proves the rename complete.
- [ ] **The other three accounts have no `slides-write` grant.** `personal` was consented on
      2026-08-14 to prove remote editing works; `cin` and `ufrpe` still hold read-only slides
      tokens (and `personal`'s read token is dead, which no longer matters — a read now uses the
      write grant when the alias has one). Run `core/tools/slides/gslides auth <alias> --write`
      for the other two **when a deck on that account actually needs editing**, not before: each
      one costs Lucas a consent screen, and the account it must be is in the message.
- [ ] **Slides motion — the capability question is answered; what is left is a `frames` command.**
      Measured 2026-08-14: per-object motion tweens are **not** in the API surface, but the fallback
      Lucas named *is* — `duplicateObject` (with an `objectIds` map) plus
      `updatePageElementTransform` in one `batchUpdate` authors a frame sequence, proven live with a
      constant-acceleration run. It is PDF-safe by construction, since the motion is carried by the
      slides themselves and not by a player feature.
      What remains is ergonomics, not discovery: a `gslides frames` command taking an element, a
      start and end position, a frame count and an easing (constant velocity / constant
      acceleration), emitting the batch. Two knowns to build against — object ids must be ≥5 chars,
      and duplicates land right after their source so the run comes out reversed unless
      `updateSlidesPosition` is in the same batch. Both are in
      [`../core/tools/slides/SPECS.md`](tools/slides/SPECS.md). (INBOX 2026-08-13)
- [ ] **Notion — the read CLI is built and blocked on one paste; writing is unstarted.**
      [`core/tools/notes/notion`](tools/notes/CONTEXT.md) ships `auth`/`whoami`/`list`/`search`/`read`
      over the official REST API (no MCP — its connector needs an interactive OAuth flow this
      workspace cannot run headless). Verified 2026-08-14 against the live API with a deliberately
      bogus secret: endpoint, pinned `Notion-Version` header and the 401 → instruction mapping all
      answer correctly, so **a valid secret is the only untested link.**
      1. **The secret is minted and stored** (2026-08-14): integration `WOS` on workspace *Lucas
         Silva Figueiredo's Notion*, token at `~/.config/workspace-notion/personal.token.json`.
         `whoami` answers. **`list` returns nothing** — content is invisible to an integration until
         it is connected, so the one open step is Lucas opening the class page → ⋯ → Connections →
         add `WOS` (a parent connection covers everything under it). Until then `[notion-read]` in
         [`brain/goals/teaching-materials.md`](../brain/goals/teaching-materials.md) cannot close and
         nothing here can be smoke-tested against real content.
      2. **Then `[notion-write]`** — append/update blocks. The read path already returns block ids
         because that is what the write path addresses; the missing piece is a request seam shaped
         like `gslides apply`, taking Notion's own request format rather than a DSL.
      **This line owns only the build**; the goal file owns the intent and the ordering, so neither
      restates the other.
- [ ] **Audit our own skills — effective, or verbose and making work?** Lucas (INBOX 2026-08-13): check
      every `core/skills/*.md` for verbosity, redundancy, ambiguity, and steps that cost more than they
      save. Distinct from the survey bullet below — that one imports from outside, this one prunes what we
      already run. Sequence it after the six-practices assessment in [/ROADMAP.md](../ROADMAP.md) Front 3,
      which decides the *shape* to prune toward (rules → interfaces).
- [ ] **`/caveman compress` — two bugs that outlive the rejection.** The measured rejection of compressing
      workspace docs is recorded in [/ROADMAP.md](../ROADMAP.md) Front 3.2; these two survive it because
      the tool still runs on demand: (a) it strips the file's trailing newline
      (`skills/caveman/scripts/compress.py`, `write_text(compressed)`); (b) `compress.py:34` defaults
      `CAVEMAN_MODEL` to `claude-sonnet-4-5`, a stale model id. (INBOX 2026-07-30)
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

## ablation-bench

**Rescued 2026-08-15 — the pilot's durable half now lives in
[`core/experiments/subagent-context-chain.md`](experiments/subagent-context-chain.md)**, beside the
2026-08-15 subagent probe that reframes it, with the follow-up design (n ≥ 4, equal budgets, a third
gate-off *and* prompt-off arm) preserved verbatim. The metrics schema and honest-reporting rules the
pilot froze became the ledger's format, in
[`core/experiments/CONTEXT.md`](experiments/CONTEXT.md).

Still in `tmp/ablation-bench/`, gitignored and never in git: the raw run data (`arms/`, `runners/`,
`toy-project/`, `metrics-all.json`). Delete it with `tmp/` — the durable content is out.

## Notes

- `.claude/` + `.opencode/` are generated mirrors (tracked). Never hand-edit; run `sync-skills`.
- `sync-skills` prunes orphans on every `sync` now — renaming/removing a skill no longer dangles.
