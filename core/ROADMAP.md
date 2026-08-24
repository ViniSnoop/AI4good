# Core Library Roadmap
> What is still unsound about the agent library itself, and what would make it sound? Holds the
> per-layer frontmatter contract and the migrations that have not landed. Open it for a skill, an
> agent, a flow, a tool or their schema — workspace scaffold work is the wos ledger's, never this
> file's.

**Scope: agent-library internals only** — skills, agents, flows, tools, and their schema. Workspace
scaffold work (hooks, gitignore, anti-entropy, cost, portability) lives in the single wos ledger,
[/ROADMAP.md](../ROADMAP.md). An item belongs to exactly one of the two.

Contract in [SCHEMA.md](SCHEMA.md). Completed work is deleted -- git is the history.

Goal: [[spec-driven-development]] — SPEC-v0 pilot on the `core/` agent library.
No flow is privileged — the exemplar is `flows/_template.md` (see [SCHEMA.md](SCHEMA.md)).

## Open

- [ ] **The craft router has no home for a measurement, and the shortcut it falls back to
      contradicts itself.** Both found by *running* the flow on 2026-08-24 (the trial funded by
      [`ROADMAP-cost.md`](../ROADMAP-cost.md)), not by reading it — which is the point of having
      run it.
      - **No `experiment` subtree.** `route.md` offers padaria · feature/SDD · research ·
        architecture. A controlled experiment on our own harness fits none: every `research/*` flow
        is a source-gathering shape, and `research/explore.md` is an *optimization* loop demanding a
        benchmark command and blocking on user confirmation. The fallback was the padaria gate,
        which **measures the write, not the investigation** — the same task touching three files
        would have routed to contract-first TDD, which is absurd for a measurement. Its step
        sequence is genuinely distinct (hypothesis → arms → control → run → record → decide) and
        [`core/experiments/SPECS.md`](SPECS.md) already defines its output contract with a hook
        enforcing it, which clears `tree.md`'s own bar for a fifth subtree.
      - **Padaria mandates the thing it forbids.** It says to skip Loops 1/3/3.5/4a/5 and then to
        execute Loop 2, which mandates a `feature/<slug>` branch off develop — while `craft.md`'s
        own Field Practice names "two loops, one repo = worktree fight" as the hazard. It needs an
        explicit *reuse the current feature branch, stage explicitly* path. Its verification step
        also assumes an existing test suite, and offers no route for "the check is a linter."
      → **tier: medium**, and the first half is Lucas's call because it adds a subtree.

- [ ] **The flow front-loads its most expensive reads ahead of the gate that decides it needs
      them.** Protocol step 2 orders `craft.md` (13.3 KB) + `routing.md` (12 KB) + `runtimes.md`
      *before* Loop 0 — but Loop 0 is where the padaria verdict is set, and padaria delegates
      nothing, so 18 KB of routing and runtimes is read and never consulted. A flow whose stated
      purpose is saving tokens should decide the shape before paying for the machinery. Related and
      cheaper: the provider-resolution ritual (`opencode models`, `$OPENCODE_MODEL`) is dead weight
      under a runtime where routing is pinned in executor frontmatter, and is conditional on
      something the tool set already reveals. → **tier: low**.

- [ ] **`/roundup` ends by asking for something it could have proposed inside the plan.** Lucas
      (INBOX 2026-08-20): *"editar a mensagem final do /roundup para incluir a sugestão de no plano já
      adicionar um /roundup no final e evitar uma troca extra de mensagens com o usuário. isso é só
      uma ideia, avaliar antes de implantar."* One saved round-trip per session, and the flag is his:
      **evaluate before implanting.** The thing to check first is whether it survives contact with
      `AGENTS.md` § AGENT-FACING TEXT NAMES ONE ACTION — a closing message that names the next
      session's close is naming a second action, which is exactly the rule's failure case, so the
      honest version may belong in the *plan* template rather than in roundup's final message.
      → **tier: low**.

- [ ] **Only one of the craft flow's loops declares a cap, and the check cannot see that.**
      `validate_flow_loops` is whole-file by design — *"one cap governs the flow, and finding where
      a step ends in prose would be a guess"* — so Loop 1's `at most 3 passes` satisfies it for the
      entire flow. Splitting `craft.md` on 2026-08-19 made the gap visible: `craft-build.md` and
      `craft-ship.md` each declare loops and carry no cap of their own, and **Loop 4b is literally
      called "Code Until Green"**. The check was widened to read the whole family rather than
      tightened, deliberately — changing enforcement inside a split is how a split stops being
      reviewable. What is open is the flow question: does 4b need a cap, and 5 and 6, or is the
      one-cap-per-flow rule right and the per-shard reading a false alarm.
      → **tier: medium**, with Lucas — it is his flow and the answer changes what a stuck run does.

- [ ] **Every skill is invisible to a session started outside the workspace.** Lucas (INBOX
      2026-08-18): *"/roundup and maybe other skills are not registered on claude code terminal (and
      maybe other harnesses e.g., opencode terminal and desktop)."* Reproduced 2026-08-18: the
      mirror is healthy — `.claude/commands/` holds all fourteen — but that directory is **project
      scoped**, so a session whose project directory is `$HOME` (a terminal opened outside
      `/mnt/workspace`, the desktop app, a background job) loads none of them and has to read
      `core/skills/<name>.md` by hand. `~/.claude/commands/` is empty; the only globally exposed
      skill is `caveman`, and it gets there through
      [`tools/wos/sync-global-skills`](tools/wos/sync-global-skills), which handles folder-shaped
      skills and not the flat command mirror.
      Two ways, and they are not equivalent: extend the global sync to link the command mirror into
      `~/.claude/commands/` (every skill everywhere, and a workspace skill fires in a repo it knows
      nothing about), or keep project scope and make the failure loud instead of silent. The second
      is smaller and the first is what Lucas asked for; the trade is real enough to name before
      building.
      → **tier: medium**.

- [ ] **`parse_owns` swallows prose as declared paths.** In
      [`hooks/brain/brain_attention.py`](hooks/brain/brain_attention.py), the `>**owns**` block ends
      only at the next `>**field**` or a `##` heading, so a blank line followed by an ordinary
      blockquote stays inside it and every sentence becomes a candidate path. Visible on **every
      commit** as `[Brain] ⚠ <goal>: owns '<prose>' ... which resolves to no repo` — at least
      `craft-flows`, `burocracia-academica`, `ecovila`. The noise is the real cost: it trains the
      reader to skip post-commit output, which is where the gates also speak. Likely fix: end the
      block at the first blank line. Add a case to the brain tests with a goal file whose `owns`
      block is followed by prose.
      → **tier: medium**.
- [ ] **2b — craft-agent tier source + generator.** Create `core/agents/craft-{low,medium,high}.md`
      carrying `tier:`; extract the craft flow's tier→model map to `core/tier-map.json`; add a
      generator that emits `.claude/agents/craft-*.md` with `model:` resolved. Removes the last
      provider-name-in-source violation (`model: haiku`). Symmetric with the skills mirror.
- [ ] **Skill `flow:` field — craft.md.** research.md done (`flow:` comma list, router shape).
      craft.md needs `flow: craft` (or the router slug).
- [ ] **`engineering` is exempted by path, not typed — a privileged special case.** `flows/craft/`
      is skipped by `validate_flows` because the `type` enum has no `engineering` value, so the one
      cluster that does the most work is exactly the one that is not schema-checked. Symmetric fix:
      add `engineering` to the enum, give `craft`/`route`/`architect` real frontmatter (`type`,
      `confirm`, `agents`), delete the path exemption in `sync-skills`. The `uses:` DAG check already
      covers the cluster, so only the type layer is unguarded.
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
      — the first three overlap what `AGENTS.md` + `/craft` + CONTEXT.md already do, so the question is
      overlap vs gap) and the NB-oriented pair captured in `code/isoroll-content/refs/REFS.md`.
      Lucas also asked for a general sweep for **game-asset-generation** skills while doing this.
      A third lead arrived twice (INBOX 2026-08-02, two posts, same list): an **animation/UI skill set** —
      `threejs-skills`, `gsap-skills`, `motion-design-skill` (Lottie), `design-dna` (extract a site's visual
      identity), `genjutsu` (UI system). Same DM-bait shape, names only, no links — ref in
      [refs/REFS.md](refs/REFS.md). Worth a look for `code/isoroll-*` and `code/apptime` if any is real.

## Blocked — waiting on a trigger

Open work whose own reasoning says *not yet*. Each line names the event that reopens it, so § Open
stays a count of what is drainable now. Same discipline as [/ROADMAP-archive.md](../ROADMAP-archive.md) § Blocked.

- [ ] **The `video/` family name describes less than the family delivers.** It gained a page fallback
      — a link with no media goes to `web/fetch` — so what it offers is *link → navigable text*,
      while the directory name still says one medium. Captured by Lucas (INBOX 2026-08-16); the
      asymmetry was written down rather than renamed because [`tools/SPECS.md`](tools/SPECS.md)
      § Naming records that two path sweeps have already happened and a third is not free.
      → **trigger: the next time something else opens `core/tools/` for a path change.** Pay one
      sweep instead of two. A rename with no other reason to touch those paths is the case SPECS
      already rejected. → **tier: medium**.

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
