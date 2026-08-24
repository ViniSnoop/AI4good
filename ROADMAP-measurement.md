# Measurement and doubt
> Does any of this scaffold actually help, and what catches the agent being confidently wrong?
> Two halves with one cause: the ablation that would measure whether a rule earns its keep, and
> the gates that would make a claim carry its evidence. Open it before trusting a number or a
> technical opinion; the experiment's design lives in its paper twin.
> priority: important
> blocked-by: ROADMAP-portability.md

## Front 14 — ablation: nothing in this workspace has ever been measured

> **The paper twin is [`academy/papers/wos-ablation/`](academy/papers/wos-ablation/CONTEXT.md)**
> (2026-08-16). Lucas: *"o WOS pode virar um artigo. o estudo de ablação, se bem feito, me parece
> bem publicável."* The ablation and the paper are one artifact, so the experimental design lives
> there and this front holds only the build work it depends on.

1. 🟡 **build the instrument, then run the ablation.** Lucas, INBOX 2026-08-15: *"um engenheiro
   líder da Anthropic sugeriu de tempos em tempos a gente 'deletar' o CLAUDE.md e ver como modelos
   top (como o Opus) performam, dizendo que poderíamos nos surpreender. ou seja, diminuir a carga de
   instruções. esta recomendação é bem forte pro nosso caso. tudo que o WOS faz (ou pelo menos boa
   parte) é contornar ingenuidades do modelo. realmente precisamos fazer um benchmark com estudos de
   ablação em breve."*

   **The premise is falsifiable and nobody has tried to falsify it.** This workspace exists to
   compensate for model failures; a stronger model may not need the compensation, and every rule
   that outlives its failure is pure cost. The claim cuts at the whole scaffold, not just the docs.

   **It runs OUTSIDE this workspace, and that is a correction, not a detail** (Lucas, 2026-08-17:
   *"the ablation test WILL NOT be done INSIDE the WOS. we can't do that. this will be an
   experiment!"*). A system cannot run the experiment on itself. The harness builds **variants** of
   a checkout — one feature off in each — and runs one task suite against all of them. The variants
   come from the **public repo** (his call), which has two consequences taken deliberately: the
   public scaffold is a **hard precondition** of this item, and the task suite must be **synthetic**,
   since that scaffold ships `brain/` as empty structure by design. Designing the suite is study
   work and belongs to the paper twin.

   **The other precondition is the reason the last attempt produced nothing.**
   [`core/ROADMAP.md`](core/ROADMAP.md) § ablation-bench ran once and yielded no signal for exactly
   one reason: there was no clean way to turn a single feature off. The toggle registry is not a
   sibling of this item, it is its instrument — *"it also would ease ablation tests so we can indeed
   see the impacts of each option"* (Lucas, 2026-08-14). Building the bench before the switch
   repeats the failure. Two ways a feature goes off, and the registry only knows the first:
   an in-process switch, or a variant built without it — [`core/SPECS-features.md`](core/SPECS-features.md) § AD-14.

   **Named for measurement by Lucas (INBOX 2026-08-16), and the list is the scope:** *"incluir na
   nossa medição do estudo de ablação as funcionalidades da fachada, das interfaces, do limite de
   LOC, limite de arquivos, enfim, fazer o planejamento desse estudo com bastante calma."* Facade
   discipline, interface-first reads, the 150/200-line cap and the 7/10-file fanout cap — the four
   restraint gates nobody has ever measured, each of which shapes how every file in this workspace
   is written. *"com bastante calma"* is a constraint on the study, not a mood: these are the
   workspace's most load-bearing rules, so a weak design produces a number that gets quoted forever.

   Scope is the whole enforcement layer, not the `.md` corpus: hooks, skills, tools, `AGENTS.md`
   itself. The corpus drain is downstream — its verdicts are judgement calls today precisely because this
   instrument does not exist, and it says so rather than implying they are measured.

   **Re-affirmed as the priority, 2026-08-20 (Lucas, INBOX):** *"o WOS precisa ser avaliado, mais uma
   vez, suas features, seus arquivos, tá tudo um pouco grande e sinto que um pouco como uma
   macarronada… acho que o teste de ablação vai ser de fato o principal. vai ajudar a tirar ruído
   também porque vamos naturalmente perceber cargas desnecessárias."* Note what he expects of it that
   this row does not currently promise: the ablation as a **subtraction instrument**, telling him
   which loads are unnecessary — not only whether the scaffold helps in aggregate. Design the suite so
   a per-feature verdict is readable, or it answers the smaller question.

   **Outside evidence that the premise is live, captured 2026-08-20** — Anthropic reportedly runs
   exactly this and found stripping system prompts can leave the model *slightly more intelligent*,
   instructions constraining rather than helping. Secondhand and uncitable as it stands; the ref and
   its provenance are in [`academy/papers/wos-ablation/refs/REFS.md`](academy/papers/wos-ablation/refs/REFS.md).
   → **tier: high** for the design, medium to run it.

---
## Front 15 — the agent is confidently wrong, and nothing catches it

Lucas, INBOX 2026-08-16: *"vi um comentário sobre o OPUS ter MUITA SEGURANÇA sobre pontos que na
verdade ele estava errado… eu gostaria que todas as opiniões técnicas da IA fossem tomadas com base
em pesquisas."* His two proposals: a **knowledge base** — a curated store, cheap to look up, refreshed
when a stored fact is old enough to have moved — and an **instruction**: *"YOU DON'T KNOW THINGS,
don't feel too certain, search before giving precise technical opinions."*

**This workspace has the case study, and it is not hypothetical.** Front 9 was steered for three
weeks by a confident, re-runnable, wrong number. The instrument agreed with the script it replaced,
which read as confirmation and was not, because both shared one misunderstanding. Before that, four
consecutive explanations of the rtk hook were asserted and retracted. In neither case was the agent
short of information; it was short of the habit of checking.

**What that case study says about the two proposals, and it cuts against the easy one.** The
instruction is the cheap half and is the half already tried: the workspace is thick with
*re-run it, never quote it* prose, and it did not prevent either failure. Prose asking for doubt is
INDUCED, and this repo's whole bet is that INDUCED loses to ENFORCED. So the front's real question
is **what a confidence check looks like as a gate**, not as a paragraph.

Three sub-questions, in the order they can be answered:

1. 🔴 **What is the store, and what earns a row? — POSTPONED 2026-08-17, and the postponement is the
   ruling.** Asked to pick between a new structure and a query layer over what exists, Lucas declined
   the frame: *"are we talking about the knowledge graph? this is an entirely new front in my view…
   there are some conceptual collisions, redundancies and ambiguities we must solve. also, building
   it is not simple… we have to be extra careful on this design."* It opens with research and a
   design sitting of its own, or it does not open.

   Inherited, so the next session starts warm: the two live stores are
   [`brain/memory/`](brain/memory/CONTEXT.md) (26 files, wikilinked, in every system prompt) and
   `core/refs/REFS.md` (209 lines, tier-marked, and absent from the most-re-read list — nobody reads
   it). A third store is the failure named EDIT > CREATE, so resolving the collisions is the first
   work item, not a caveat.
   → **tier: high**, with Lucas, in a session about this and nothing else.

2. 🔴 **a check that greps for a name is not evidence, and one of ours proved it by passing wrongly.**
   `test_features_wiring.py` asked whether a row claiming a switch really had one by checking that
   the feature's slug appeared somewhere in the named file. On 2026-08-18 the `symmetry` norm
   **passed that check by accident** — on the word *asymmetry*, in an unrelated comment, in a file
   that never mentioned the norm at all. The registry would have reported the rule as switchable
   while nothing switched it: the exact silent pass this front exists for, inside the test written
   to prevent it.

   Fixed where it was found — that file's grep is now scoped and the real work is done by
   behavioural checks that run the feature both ways. What is **not** done is the sweep: **how many
   other checks in this repo prove a name is present rather than that a behaviour happened**, which
   is [`core/SPECS.md`](core/SPECS.md) § Conventions applied to our own suite for the first time.
   **Lucas asked (2026-08-18) to be walked through this rather than have it decided for him.**

   **The sweep ran 2026-08-24 and the result reframes the question. The row stays open for his
   ruling; what follows is evidence, not a decision.** Eighty-eight assertions in the suite match
   the shape *"a literal appears in some text"*. The great majority are **not** the failure: they
   assert on the **output of a program the test just ran**, which is behaviour observed, not a name
   grepped. Roughly ten read a **source file** instead — and those split in two, which is the thing
   worth deciding:

   - **The property really is textual, and grep is the right instrument.** *"This module does not
     keep a second copy of the law"* is a claim about source text and nothing else. Three checks are
     this shape (`entropy_fanout`'s one-home test, `subagent_gate`'s, the stubgen-output one), and
     each already pairs its positive with a **negative** assert — `f'= {WARN}' not in source`,
     `"'agent_id'" not in body`. The negative is the load-bearing half; the positive is a weak
     witness that the import exists at all.
   - **The property is behavioural and the grep is standing in for it.** This is the family that
     failed. `test_features_wiring` asserts a wired file "asks feature_law whether it is on" by
     `'feature_law' in body or 'tool_law' in body` — **an OR of two common tokens matched anywhere,
     comments and docstrings included**, which is a weaker witness than the one that passed on
     *asymmetry*. `test_gate_messages` proves a block "reaches the user" by finding the word
     `stderr` in the gate's source.

   **So the rule to rule on is not "stop grepping".** It is: *does the claim describe the text or
   the run?* A no-second-copy rule is textual and its negative assert is the real check. "This gate
   consults the registry", "this block reaches the user" are runtime claims, and for those a
   substring is a proxy that has already been caught passing wrongly once.
   → **tier: medium**, and it is the cheapest item in this front by a wide margin.

3. 🔴 **The agent agrees with the frame it was handed, and nothing catches that either.** Lucas
   (INBOX 2026-08-18, routed here 2026-08-18 by his ruling — it is this front seen from the decision
   side rather than the assertion side): *"resolver de forma definitiva o viés de confirmação dos
   modelos (e dos harness). pelo menos no PLAN mode. ou em todos os casos de tomada de decisão."*

   His own three-part shape, and the third part is the constraint: **first** a mechanism to notice
   that a decision is being taken at all; **second** *"não quero transformar os agentes em críticos
   ferrenhos e cegos"* — the cure must not be a contrarian reflex, which is the same failure with
   the sign flipped; **third** a method — detect the decision, grade its criticality, research it,
   investigate impacts, then ground the pros and cons (adversarial shapes, flows, SDD are candidates
   he named and explicitly did **not** pick). His words on scope: *"não quero também definir COMO
   resolver esse problema agora… esse é um problema grande que deve ser resolvido com pesquisa."*

   **Why it sits here rather than opening a front:** this front already says the agent emits
   confident claims nothing checks. A plan the agent produced by agreeing with the premise it was
   handed is one of those claims, and PLAN mode is where it is most expensive — the whole session
   downstream is built on it. **Do not open this with a prompt rule** either, for the reason stated
   directly above.
   → **tier: high**, with Lucas, research first and its own sitting.

**Do not open this with a prompt rule.** That is the cheapest-looking move and the one the evidence
above already rejects.

**A third specimen of the failure, captured 2026-08-20, and it arrives with the rejected cure
attached.** Reported claim: the model treats a claim repeated across many sites as many independent
confirmations, even when every copy traces to one anonymous source — laundering a single unsourced
assertion into apparent consensus. That is this front's subject seen from the *evidence-weighing*
side rather than the assertion side, and it is worth keeping because our own case study has the same
shape: the instrument that agreed with the script it replaced *read as confirmation and was not,
because both shared one misunderstanding*. The proposed fix in the source is one extra prompt line
telling the model to trace claims to origin — **the exact INDUCED move this front already rejects**,
so it is filed as a specimen and not as a candidate mechanism. Ref and provenance:
[`core/refs/REFS-unjudged.md`](core/refs/REFS-unjudged.md).
## Silent failure is the failure mode this workspace actually has

The rule this cost six bugs to learn is [`core/SPECS.md`](core/SPECS.md) § Conventions: **a check
that proves something *happened* beats one that proves it did not error.**
