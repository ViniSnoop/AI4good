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

**Ruled 2026-08-24 (Lucas), and built the same session: a structural claim must live in a field a
parser already reads.** The rule and the reasoning behind the choice live in
[`core/SCHEMA-outgrowing.md`](core/SCHEMA-outgrowing.md) § Every field that names our own code is
verified; the check is `core/hooks/entropy/entropy_fields.py`, blocking on what a commit adds and
reporting on everything. It charged ~100 declarations the day it landed and three were false,
including this front's own claim that `enforced-by` was read by nothing — it is rendered into every
sharded index — and the field table's claim that the generator checked `blocked-by`, which nothing
did.

**What the ruling deliberately does not reach: prose.** Three of the eight specimens live in a
paragraph — a handoff, an AD section, a roadmap row — and they stay unchecked. That was the price of
the option that needs no new habit and reaches backwards, weighed against a marker written at
authoring time (reaches prose, catches nothing already written, depends on a discipline nobody
enforces), a guard at `/handoff` alone (one file, and a skippable ritual), and a fresh cheap session
grading the artifact (highest recall, but *automatic + zero-token* wins wherever a deterministic
option exists — and here one did). The front stays open on the prose half.

1. 🟡 **Charge the semantic half of a field, not only the path.** A gate that exists and does not
   enforce what its row claims is still a false claim: the registry called `heredoc-gate` a
   `blocks` when running it both ways shows it warns and returns 0. Existence is checked; behaviour
   is not. The nearest built answer is `test_features_wiring.py`, which runs a feature both ways and
   fails unless the observable moves — so the question is which fields can carry a probe that cheap,
   not whether the idea works. → **tier: medium**.
2. 🟡 **Count the prose specimens before reopening the ruling.** The accepted cost above is only
   acceptable while prose stops producing them. The specimen list in this front is dated and
   re-checkable, so the next one written into a paragraph gets added here with its date — and the
   ruling is revisited on a count, never on the feeling that it keeps happening.

   **Specimens, 2026-08-25** (both in `ROADMAP-entropy.md`, both refuted by one command, both cut):
   item 8 said the workspace repo's own 200-line half was done while `ROADMAP.md` sat at 204; item 11
   said the goal files' `done` blocks were *"full of finished work"* and *"permanent residue"* while
   they hold 118 lines across 53 files — empty markers, nothing to cut. **Running count: 5 prose
   specimens.** → **tier: medium**.

## Front 16 — post-v1, and the ledger is open again on purpose

**Ruled 2026-08-16 (Lucas), after all four v1 criteria went green.** The governing constraint
(*"quero zerar o roadmap do WOS o quanto antes"*) was a filter for reaching v1, not a permanent ban:
asked where three real ideas should land, he chose to **reopen this ledger** rather than push them
into `core/ROADMAP.md` or leave them in the INBOX. So v1 is a milestone, not a stopping point —
**but the filter that got us here still applies to what enters**: an item another repo owns is
refiled there, and a finding worth keeping goes into the `SPECS.md` section that owns the rule.

4. 🟡 **measure which `UPPERCASE.md` files are actually read, and what they cost.** Lucas, INBOX
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
5. 🟡 **then reinforce the goal↔roadmap link, possibly enforced.** Same capture, and deliberately
   second: *"depois gostaria de reforçar a conexão entre os goals e os roadmaps, não sei se tem
   como, talvez até algo ENFORCED"*. Every goal file already carries an `>**owns**` block and every
   plan is supposed to live in a `ROADMAP.md`; what is missing is anything asserting the two agree.
   **Do not design this before item 4 reports** — if goal files turn out to be read rarely, the fix
   is not a stronger link to them.

   **A mechanism proposed, 2026-08-20 (Lucas, INBOX), and it is his own hedge:** *"definitivamente
   temos que conectar os goals com os roadmaps. talvez no /roundup. talvez, talvez! automaticamente
   lançar warning quando fizer um commit de qualquer arquivo ROADMAP*.md para atualizar o goal linkado
   com aquele roadmap."* Two candidate moments, and they are not equivalent: `/roundup` is a ritual
   the agent runs and can skip, a commit hook is ENFORCED and costs zero tokens — which this
   workspace's own bet says should win. The `>**owns**` block already declares the goal↔path
   direction, so the reverse lookup a warning needs is derivable rather than something to author.
   The *"talvez, talvez!"* is doing real work: **warn, never block.** A gate that stops a commit
   because a goal file was not touched would train people to write empty goal updates.
   → **tier: medium**.
6. 🟡 **audit the goal file format against what actually drives follow-through.** Lucas, 2026-08-20
   (INBOX), on a summary of fifty years of motivation research: *"podemos talvez aproveitar essas
   máximas no design do WOS, dos goals."* The six named: specific goals beat vague intentions
   (Locke & Latham); visible progress sustains effort (Amabile's progress principle); self-directed
   meaning beats willpower (Deci & Ryan); environment and cues shape behaviour more than resolve
   (Wood); social accountability strengthens pursuit; and setbacks get planned for in advance rather
   than absorbed (Gollwitzer's implementation intentions).

   **The reason this is a real audit and not decoration:** our goal files already do the first two —
   a backlog item is specific, and `/compass` renders progress — and do **none** of the last three.
   There is no `if this happens, then I will` field anywhere, which is the one with the strongest
   evidence behind it and the cheapest to add. Read as a critique rather than a checklist, this says
   the format is built for *stating* goals and not for *resuming* them, which is also Lucas's
   recurring complaint about goals feeling unused.

   **Ordered behind item 4, deliberately**, for the same reason item 5 is: if goal files turn out to
   be read rarely, redesigning their fields is the wrong move. Secondhand summary, uncitable as it
   stands — the named researchers are the citable trail, and the ref is in
   [`core/refs/REFS-unjudged.md`](core/refs/REFS-unjudged.md). → **tier: medium**.

