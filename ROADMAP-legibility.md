# Legibility
> Lucas can no longer read his own workspace, and that is the root cause.
> priority: essential

## Front 18 — Lucas can no longer read his own workspace, and that is the root cause

Lucas, 2026-08-18, closing the session that drained the feature registry: *"sometimes the WOS is
growing with decisions I didn't recall making… some words that are hard for me to instantly
understand are ledger, seam, probe… I feel sometimes things are growing and I am losing the
understanding of what is happening in WOS. this whole renaming / wiring of features, hooks, tools,
etc, was due to that in my opinion."*

**That last clause is the finding.** The feature registry, the group rename, the `capability` sweep —
weeks of work — were all downstream attempts to fix a legibility problem nobody had named. Treating
them as separate cleanups is why each one only helped for a while. His two rules, in his words:

1. **Language is the thing.** *"this whole WOS is meant for LLMs, language IS the thing"* — so a
   word chosen badly is not a documentation defect, it is a defect in the system itself. Semantic
   symmetry is part of it: one idea, one word, everywhere.
2. **Simpler, better organised, more often than not.** *"our language choices can be simpler… this
   would help me and you (harness+model)."* Both readers, not just the human.

This front never closes. It is the standing check that the workspace stays understandable to the
person who owns it, and the place to route the next *"when was that decided?"*

1. 🔴 **The deep sitting: research and brainstorm what this front actually is, then build.**
   The opening question — *"is it a front at all"* — was answered in the 2026-08-18 sitting. **Ruled
   (Lucas): it IS a front, standing; and all three halves below (18.2/18.3/18.4) are real work, none
   killed.** What is NOT settled is the front's shape — Lucas: *"this deserves discussion, research
   and brainstorming, I don't think we will handle all we need in this small assessment."* So the
   halves may split, merge or gain a fourth, and their ordering is open. This row does not close when
   the halves are listed; it closes when the front has had the research sitting it asks for.

   **Opening material, carried as a hypothesis to test — not a fact** (this is the Front 17
   discipline applied to itself): *Fronts 15, 17 and 18 may be three faces of one root — the
   workspace emits durable text its readers cannot trust or parse.* 17 = the agent writes false
   structural claims about our own code; 15 = false confident claims about the outside world; 18 =
   words and quiet decisions Lucas cannot read. Lucas's own line is the evidence for it — the
   feature-registry and rename churn was *"downstream of a legibility problem nobody had named."*
   **Falsification path:** if the three halves land and 15's and 17's symptoms do not ease, the
   framing was wrong and these stay three separate fronts. Bring evidence to the sitting, not the
   framing pre-accepted. **First evidence in, and it cuts for the root:** legibility is a *measurable*
   property, not taste — generated context bloat lowers agent task success and raises cost, and
   instruction accretion degrades adherence to the earliest, highest-consequence rules (ETH Zurich
   2026 and the AGENTS.md-bloat literature, [`core/refs/REFS-legibility.md`](core/refs/REFS-legibility.md) § Legibility
   prior art). The corollary is sharp: the fix is subtraction, so solving *"I cannot read my
   workspace"* by adding explanation makes it worse for both readers.

   **The 2026-08-18 sitting ran the diagram half:** 18.3's shape is ruled below, 18.2's criterion is
   refined, and 18.4 is reshaped by the decision-record finding. What the front still owes its own
   session: the **jargon audit** (18.2's internal replacement work) and the **one-root test** above —
   both deferred here deliberately, neither cheap enough to fold into a mixed session.
   → **tier: high**, with Lucas, its own session about this and nothing else.

2. 🟡 **Replace the words that need a glossary to be read.** A definition is a patch; the fix is the
   plain word. Named by Lucas: **ledger**, **seam**, **probe**. Found beside them in one pass over
   our own prose: **ratchet**, **corpus**, **substrate**, **fanout**, **hop**, **shim**, **spine**,
   **surface**, **law**, **drift**, **honesty test**, **boy-scout**. Some earn their keep and some
   are showing off, and telling those apart is the work — *gate* is worth its definition, *seam*
   almost certainly is not (it means "the place the switch goes").

   Two products, in order: a **plain-word replacement** per term that survives the cut, applied
   across the corpus the way `capability` → `feature` was; and the survivors defined in **one place**
   — [`core/SCHEMA-vocabulary.md`](core/SCHEMA-vocabulary.md) § Vocabulary already holds three definitions and is the home,
   so nothing new gets built for this. **Criterion ruled 2026-08-18 (Lucas): the best, most precise
   word wins, and simpler breaks the tie** — he will learn a new word if it is genuinely the best one,
   and drop a word that is only showing off. Mature terminology practice says the same (precision over
   economy, clarity a hard constraint — [`core/refs/REFS-legibility.md`](core/refs/REFS-legibility.md) § Legibility prior
   art), so the rule is confirmed, not invented.

   **First case run, and it changed what the audit is looking for.** Lucas, 2026-08-18, on the
   registry's `enforcement: none`: *"what is none… that it does nothing? is none the best word?"*
   The word was fine; it was carrying **two facts** — "fires by itself and applies no pressure" and
   "you call it" — and that ambiguity had already made a session report the workspace's capability
   layer as its largest block of dead weight. The fix was a second column (`runs: automatic |
   on-demand`), not a better word. **So the audit's first question is whether a confusing term is
   underspecified rather than badly named**; a rename would have buried the defect under a nicer
   label. Rejected on the way: `serves` as a replacement value, and `passive`/`active` as the new
   column's values — `active` collides with "switched on", which this registry declares everywhere.

   **A word list beats asking a model, and Lucas proved it while naming the diagram tool** — he
   went to a thesaurus, came back with *architect / blueprint / diagram / scheme*, and picked one.
   So the audit gets an instrument: a small `core/tools/web/thesaurus` over an open synonym API
   (Datamuse needs no key), zero tokens per lookup against a model asked to free-associate. It
   offers candidates; the criterion above still decides. → **tier: low** to build, before the audit
   runs, not blocking it. → **tier: medium** for the audit itself, after the sitting.

3. 🟡 **Keep trying shapes for the *is* picture until Lucas can read it, then cut.** The page opens
   on a heat grid split by what starts a feature, with five findings under it, above the detail
   tabs. **What is open is not "build a summary" but "which drawings earn their place"**, and Lucas
   sets the pace: *"we are still at the level of trying different visualizations to cut it later,
   so no rush in discarding anything yet."*

   **The question was restated and it is not the one this row used to hold.** Lucas: *"1) in a
   glance see if WOS is well tied, if it has loose ends, if it has too much noise, discardable
   things, see the value in a glance, 2) spot the GAPS, what is missing."* That is a **health**
   read, not the inventory read the first version answered — an inventory says what is there,
   health says what is loose, what is dead weight, what is absent. All three original drawings are
   inventories, which is the deeper reason none of them landed.

   **Both queued shapes are drawn, so the cut is now the whole of this row.** They answer Lucas's
   standing want — *"I am missing seeing some trees, graphs… sequences of thing1 → thing2 → thing3…
   how things are connected or not"* — and both sit above the tab strip. Where a graph pays is
   settled by evidence rather than taste: Ghoniem says matrices beat node-link past ~20 nodes
   ([`core/refs/REFS-tooling.md`](core/refs/REFS-tooling.md) § Workspace visualization), which is why the 107-node
   routing tree reads as wallpaper and a six-node fan-in does not.

   - **the lifecycle sequence — KEPT (Lucas, 2026-08-18).** One band per session moment, the
     on-demand features detached beside the chain. It passed the health read at a glance, so it
     stays and every shape beside it is judged against it.
   - **the wiring fan-in — drawn in THREE shapes, and two of them die at Lucas's next look.**
     `views/diagram_fanin.py` holds a converging node-link plus a bars renderer called at both
     grains, because he asked to compare rendered output rather than a mockup. 69 features resolve
     to 47 wiring points and two carry 24 of them. `views/CONTEXT.md` carries the cut condition so
     the rack cannot outlive the decision. → **tier: low**, one look and two deletions.

   Every finding on the page carries a target read off a declaration, and the one nobody has
   decided — *are declared layers holding no feature a defect?* — prints `undecided` so it cannot
   pass for a met one. Pinned by `test_diagram_health.py`. → **tier: medium** for the row.

   **The picture's boundary — DEFERRED by Lucas, 2026-08-18**, after the worry was measured:
   *"to respect the context tree I think we may leave as it is now… let's not overcomplicate this
   for now, we have bigger priorities."* What settles it is that **WOS versions nothing at all
   inside a nested repo** — `git ls-files academy/papers/2027-ICLR-dobra` returns zero files, and
   the same holds for `code/dobra` and `branches/casinhas`. Each paper and project owns every one
   of its own files in its own repository. What reaches the picture is the paper's **name**, from
   the routing table in `academy/papers/CONTEXT.md`, so the leak is one row of a parent's index
   rather than versioned content. The candidate rule if it is ever taken up: a directory whose
   children are instances rather than structure stops at its own name — and the declared signal
   for "instance" already exists, since every one of them is its own git repo.

   **One ruling still Lucas's**, raised by an outside critique of the page: `core/features.txt`
   opens by saying **no feature in this workspace has ever been measured**, and the diagram of the
   workspace's self-knowledge never says so. That is the ablation front's subject and belongs to it
   rather than here, so what is open is only whether the page should carry the sentence at all.

   **The cut list is collected and deliberately unspent**, per the pacing above: the treemap
   answers neither question, the routing spine is 107 nodes to say two numbers, and the tab
   mechanism hides two thirds of the page from the diff and the printed artifact. **Do not act on
   it** until the new shapes have been seen — and one candidate is already dead on evidence, see
   the row below.

4. 🟡 **The other two pictures — *becoming* and *goal*.** *Becoming* is generated from git history;
   *goal* is authored intent, the only one of the three not tree-derived, since the future is not on
   disk. **Both wait on the row above** — a second and third picture that cannot be read at a glance
   multiplies the problem rather than the value. Goal is the one that pays: **goal − is = the
   roadmap made visible**, what is left to build seen rather
   than listed. The data for *becoming* is proven and waiting — per-nested-repo `git log` via
   `nested_repos()` + [`core/hooks/git/branch_debt.py`](core/hooks/git/branch_debt.py).

   **The standing rules the built half already keeps, and the next two inherit:** generated from the
   tree and never drawn by hand; zero-token and deterministic (no timestamp, no sha, so `--check`
   means something); one self-contained HTML file committed in-tree; every edge either renders
   declared data or is labelled *inferred*; total and fail-loud, printing `parsed N of M` and naming
   what it could not read.

   **A summary does not replace the detail, and that is now measured rather than assumed.** In a
   41-subject controlled experiment across three countries, an overview beat a state-of-the-practice
   table by +24% correctness and −12% time, concentrated on exactly the *spread* and *impact*
   questions Lucas is asking — **but the table stayed faster for precise lookups and the authors
   conclude the two complement each other** (Wettel, Lanza & Robbes, ICSE 2011,
   [`core/refs/REFS-tooling.md`](core/refs/REFS-tooling.md) § The health shelf). So the summary goes *above* the
   enforcement matrix, and the standing proposal to cut that matrix is dead on evidence.

   **Nothing on the page is inferred**, so the next two pictures inherit a page with no
   apologies on it: [`core/hooks/trigger/`](core/hooks/trigger/CONTEXT.md) reads the firing moment
   out of the registrations, and what it cannot place is counted as a gap. **The transferable
   finding is that a registry asked to be authored turned out to be derivable** — the same shape as
   the `runs` column the session before, and the rule the next picture should carry into git
   history too: look for the declaration before writing a new one.
   → **tier: medium** for *becoming*; *goal* needs Lucas's intent before it can be drawn.

5. 🔴 **Which sectors deserve an `ARCHITECTURE.html`, and what does each one need that the
   workspace document does not?** Lucas, 2026-08-18, on seeing the first one: *"I envision an
   ARCHITECTURE.html file for each code project… maybe an ARCHITECTURE.html file even for papers, we
   have to think this through, which sectors of the WOS deserve one and which are the
   particularities."* The renderers are already reusable and `core/hooks/generated.txt` already
   globs `*/ARCHITECTURE.html`, so the build is not the hard part — **the question is what each
   sector's picture is *of*.** A code project has properties the workspace does not: call structure,
   sequence over time, module dependency. A paper has others again. Answering that per sector is the
   work; generating one document per repo before answering it would produce twenty-five drawings
   nobody reads. → **tier: high**, with Lucas, before any second document is generated.

6. 🟡 **A session must not decide things quietly, and the record of *why* must survive.** The
   complaint under all of the above is *"decisions I didn't recall making."* Two shapes, the second
   reshaped by the research (seed, not yet ruled — [`core/refs/REFS-legibility.md`](core/refs/REFS-legibility.md)
   § Legibility prior art): the hand-off names **what this session decided without asking**, separate
   from what it did (a decision that cannot be stated in one line was too big to take alone, so the
   section is a filter as well as a record); and, for decisions with lasting blast radius, a **minimal
   decision record** — Context / Decision / Consequences, one file each, superseded rather than
   rewritten. That record logs the rejected option space git commit messages lose, so it captures
   *why*, not work-product, and does **not** contradict "done work is deleted, git is the history" —
   the § Rejected list here is already a partial version of it. Shape belongs in
   [`core/SPECS-session.md`](core/SPECS-session.md) § AD-09; [`core/skills/handoff.md`](core/skills/handoff.md)
   carries the hand-off half. → **tier: medium**.
