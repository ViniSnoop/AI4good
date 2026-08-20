# Self-description
> Why does this workspace keep asserting things about its own code that one command would refute?
> Holds the discipline problem — a structural claim written into a durable file with no probe
> attached — and the routing descriptions a reader meets first. Open it when the workspace says
> something false ABOUT ITSELF; the outside world is measurement's.
> priority: important

## Front 17 — the workspace describes itself wrongly, and the description is what we build on

Lucas, 2026-08-17, after the fourth correction in one session: *"I am quite tired of phrases like
'the roadmap item was factually wrong'… all we do here are Opus sessions, we have verifications and
other guards, and yet these appear more often than not. I am WARNING us that this is shady and WE
MUST find a way to avoid this… it is taking away all my confidence that we are actually making
progress."* His diagnosis, which is the sharper half: *"you, the model, infer and decide tons of
directions from just a wind of thought, making it a hard truth."*

**Four specimens from that one session, and they share a shape.** The handoff asserted a group seam
was needed where none was; AD-14 asserted tools had nowhere to put a call, reasoning from
skills and generalising; the context-meter item asserted an offer was unbuilt while it sat in the
message string; `core/features.txt`'s header asserted its groups match the tree. Every one is a
**claim about our own codebase, written into a durable file, with no probe attached** — and each was
then inherited by a later session as settled fact. A fifth, mine, in the same hour: four consecutive
reports that a token had not been written, made by checking a directory the tool does not write to,
while the tool printed its real path on its own last line.

**Three more specimens, 2026-08-17, and all three died to a probe that cost one command.** The
registry called `latex` third-party machine state we do not author — one `grep` finds
`hooks/stubgen/tex-*` and `core/tools/paper/`, ours. `heredoc-gate`'s row claimed `blocks`; running
it both ways shows it prints a warning and returns 0, so it **warns**. And § How to read this said
*two* items need Lucas while three were marked 🔴 — the count went stale the day this front opened
as the third. **The pattern is now dated and repeatable: every false claim this session was about
our own tree, was written into a durable file, and was refuted by one `grep`, one `ls`, or one run.**
None needed judgment; they needed anyone to check. That is the evidence this front asked for.

**The asymmetry that makes this tractable.** This workspace already has the discipline — for
*numbers*. *"Re-run it, never quote it"* is everywhere and it works; `ISSUES.md`, `session/usage`
and `--findings` are all quoted-from-nowhere by rule. There is **no equivalent for structural
claims**: *"nothing calls X"*, *"there is nowhere to put Y"*, *"Z is unbuilt"*, *"these groups match
the tree"*. Those are strictly **cheaper** to verify than any number — one `grep`, one `ls`, one run
— and nothing asks anyone to. Guarded the expensive claims, left the cheap ones open.

**This is not Front 15 and the difference is load-bearing.** That front is about technical opinions
on the *outside world*, where the fix is search and a knowledge store. This is **self-description**,
where the answer is already on disk and simply was not read.

1. 🔴 **Open with a research and design sitting, and build nothing before it.** Ruled 2026-08-17: it
   gets its own front and its own session. Candidate mechanisms, none chosen — picking one from a
   wind of thought would be the same failure the front exists to name: a structural claim must carry
   the command that falsifies it; handoffs may not restate a claim without its probe (the handoff is
   the *amplifier* — it is how the seam claim reached today's session pre-loaded as fact); an
   adversarial step in the flows; a defined vocabulary, since several of these were category errors
   a glossary prevents at source (`core/SCHEMA.md` § Vocabulary defines three terms).
   **Bring evidence, not intuition**: the specimens above are dated and re-checkable, and the first
   work is deciding what a *provable* claim about our own code looks like.
   → **tier: high**, with Lucas, in a session about this and nothing else.
## Front 16 — post-v1, and the ledger is open again on purpose

**Ruled 2026-08-16 (Lucas), after all four v1 criteria went green.** The governing constraint
(*"quero zerar o roadmap do WOS o quanto antes"*) was a filter for reaching v1, not a permanent ban:
asked where three real ideas should land, he chose to **reopen this ledger** rather than push them
into `core/ROADMAP.md` or leave them in the INBOX. So v1 is a milestone, not a stopping point —
**but the filter that got us here still applies to what enters**: an item another repo owns is
refiled there, and a finding worth keeping goes into the `SPECS.md` section that owns the rule.

2. 🟡 **measure which `UPPERCASE.md` files are actually read, and what they cost.** Lucas, INBOX
   2026-08-16: *"sinto que arquivos de objetivos (goals) são pouco usados. roadmaps são muito
   usados. gostaria de primeiro ter esse monitoramento de forma automática (zero-token) de quais
   arquivos UPPERCASE.md são lidos e com que frequência (e se possível o custo em tokens de leitura
   deles). tudo isso monitorado no tempo."*

   **Ordering is explicit and it is the whole point: measure first, then act.** He suspects goal
   files are dead weight; this measures it instead of assuming it. The instrument is close to
   existing — [`core/tools/wos/session/context`](core/tools/wos/session/context) already attributes
   context growth per file from the transcripts, so this is mostly a longitudinal store plus a
   per-type rollup, not a new measurement. Results belong in
   [`core/experiments/`](core/experiments/CONTEXT.md), never in this file.
   → **tier: medium**.
3. 🟡 **then reinforce the goal↔roadmap link, possibly enforced.** Same capture, and deliberately
   second: *"depois gostaria de reforçar a conexão entre os goals e os roadmaps, não sei se tem
   como, talvez até algo ENFORCED"*. Every goal file already carries an `>**owns**` block and every
   plan is supposed to live in a `ROADMAP.md`; what is missing is anything asserting the two agree.
   **Do not design this before item 2 reports** — if goal files turn out to be read rarely, the fix
   is not a stronger link to them.
   → **tier: medium**.

4. 🟢 **A truncated routing description is a finding, and three are left.** The mechanism is fixed
   (2026-08-19): the capture reads whole `>` blocks and comment paragraphs, the bound is 360, the
   rule is `core/SCHEMA-outgrowing.md` § What a description must say, and 91 routing blocks were
   regenerated. What remains is the *content* half in three files whose authors wrote past the
   bound — `core/CONTEXT.md`'s ROADMAP row, `core/refs/CONTEXT.md`'s REFS row, and the vendored
   caveman `SKILL.md`. Re-derive the list rather than trusting this one; fix the SOURCE, never the
   cut. **Nothing enforces it yet** — a `…` in a generated block should fail a Tier 0 check, and
   that check is the actual open work here. → **tier: medium**.
