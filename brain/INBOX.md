# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

ref: F4 Tier-0 pointer-integrity checker (core/tools/test/test_pointer_integrity.py, wired into
`make verify-fast`) shipped 2026-07-25 and found the routing-sync tool itself has two real bugs,
excluded from the gate (out of scope for a link checker, needs a code fix in whatever generates
`<!-- routing:start -->` blocks — likely `.hooks/context_synchronizer.py`):
1. **Unrewritten relative links when hoisting.** A child CONTEXT.md's line-2 description gets
   copied verbatim into the parent's routing-table row, including any relative markdown links it
   contains — those links resolve from the child's directory, not the parent's, so they break one
   level up. Seen live: `branches/casinhas/CONTEXT.md` (burocracia row: `BUROCRACIA.md`, `docs/`)
   and `code/{apptime,dobra,isoroll-content}/CONTEXT.md` (refs row: `REFS.md`). Fix: either strip
   links from hoisted descriptions, or rewrite the path prefix when hoisting.
2. **Stale rows survive file deletion.** The routing block only updates on save of an existing
   file; deleting a file out-of-band leaves a dangling row. Seen live: `core/prompts/CONTEXT.md`
   (rows for `fable-loop-engineering.md`, `fable-multiview.md` — both deleted, per
   [[fable_quota_strategy]] "multiview CONSUMED+deleted") and
   `academy/papers/2027-CHI-cria/outputs/CONTEXT.md` (row for `cria-workflow.md`, also deleted).
   Fix: a prune pass, or hook the delete path too.
— via pointer-integrity build · 2026-07-25

https://www.instagram.com/p/DbKa8dzkRv4/?utm_source=ig_web_copy_link
talvez seja bom ter esse setup acessível pra gente como uma alternativa local pro isso de opencode+nvidia+modelodeimagem
— via aiwbot · 2026-07-25

é bom checar se estamos induzindo ou obrigado um conflito ou mal uso dos agentes no nosso workspace devido as regras, hooks, skills, flows (old loops) e instruções de forma que, por exemplo, nós obrigamos todos os subagentes a relerem todos os CONTEXT.md (talvez queiramos isso mas acredito que não).

é bom levar a sério os nossos custos/uso
What’s contributing to your limits usage?
Day
Week
Approximate, based on local sessions on this machine — does not include other devices or claude.ai
Last 24h · these are independent characteristics of your usage, not a breakdown
59% of your usage came from subagent-heavy sessions
Each subagent runs its own requests. Be deliberate about spawning them — and consider configuring a cheaper model for simpler subagents.
55% of your usage was at >150k context
Longer sessions are more expensive even when cached. /compact mid-task, /clear when switching to new tasks.
22% of your usage came from subagents under "loops"
If this runs frequently, consider configuring its subagents with a cheaper model or tightening their prompts.
25% of your usage came from /roundup
Heavy skills can be scoped down or run with a cheaper model via skill frontmatter.
Skills
% of usage
/roundup
25%
/loops
6%
/handoff
2%
Subagents
% of usage
loops
22%

isso da concentração é triste viu, ainda mais pro melee
é pq a ideia é aquela de que skills compensa né, que dá pra balancear tirando um pouco da capacidade de combate de uma classe pra colocar em "utilidades"
— via aiwbot · 2026-07-24
(kept 2026-07-25 /inbox: not an audio test — RPG/class-design musing, no home yet. Route or delete when you decide.)
