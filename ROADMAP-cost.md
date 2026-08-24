# Cost and model routing
> What does a session cost, and which of that is avoidable? Holds which tier runs what, what loads
> at session start, and what fills the context window. Open it for what we intend to change about
> spend; every measured number lives in `core/experiments/`, so re-run the instrument for what
> spend actually is.
> priority: important

## Front 9 — Cost & model routing

> **Every number this front used to carry now lives in
> [`core/experiments/output-cost.md`](core/experiments/output-cost.md)** — the composition of output,
> the $/turn staircase by context band, and the three claims the audit retired. Re-run it, never
> quote it: [`core/tools/wos/session/usage`](core/tools/wos/session/usage). What the front holds is
> what is still *intended*.
>
> The two findings that decide the items below: **context size is the driver, not output volume**
> (4.2x from the cheapest band to the dearest, 88% of spend above 100k), and **65% of billed output
> is unlogged thinking** — invisible to every instrument here, and the largest single slice. The
> discipline that cost the most to learn is now
> [`core/experiments/SPECS.md`](core/experiments/SPECS.md) § build the instrument, then check it.
>
> Both halves of the session transition are already live: `context-meter.py` announces the crossings
> at zero token cost, `core/tools/wos/roundup` closes the session, and the split is
> [`core/SPECS-session.md`](core/SPECS-session.md) § AD-09.

1. 🟢 **safe — cheaper models where the work is mechanical.** Measured split (2026-08-16):
   opus-5 56.5%, opus-4.8 27.5%, fable 8.3%, sonnet 7.7%, haiku ~0%. Worth doing, but note the
   ceiling — routing cannot beat a 4x context multiplier, and the transition above already took the
   larger win. → **tier: medium**.
2. 🟢 **assess whether an ensemble router beats single-model routing on our own work.** Lucas, INBOX
   2026-08-19, on a claim that *Echo* beat a frontier model on a coding benchmark at 40% less cost by
   running several open-weight models at once and merging their outputs: *"será que vale um teste?"*

   **The claim is unverified and relayed third-hand** — no benchmark named, no independent run
   ([`core/refs/REFS-unjudged.md`](core/refs/REFS-unjudged.md) § Models / runtimes). So the work is a
   check, not an adoption: does the *shape* apply here at all? Our spend is driven by context size
   rather than model choice (4.2x across bands, 88% above 100k), which is the finding that decides
   this — an ensemble that reads the same large context several times pays the multiplier several
   times over. That is the falsifiable version and it is cheap to reason through before anything is
   installed. → **tier: medium**.
5. 🔴 **give flows and agents a deliberate trial, then judge them.** Lucas, same capture: *"um aluno
   comentou que existem formas diretas de o claudecode delegar pra subagentes… temos skills e isso
   me parece suficiente, mas talvez não seja."*

   The claim this item rested on — that nothing had ever been delegated — was an artifact of
   scanning the wrong directory. Corrected, with the hand-check, in
   [`core/experiments/delegation.md`](core/experiments/delegation.md): delegation happens, and **no
   workspace-authored agent has ever been spawned.**

   **Ruled 2026-08-17 (Lucas): do not delete on that.** *"low usage doesn't mean they don't have
   value… we did not work enough on these yet. IF we employ effort, do our best, and even then we do
   not use those, then it makes sense to delete."* Delete-weak-features assumes a fair trial and this
   layer never got one — reach was measured, worth was not. The work is **rounds of discussion and
   research**: what a flow is for, what an agent is for, whether a flow naming `agents:` in
   frontmatter is the right shape, and one deliberate run of each before anyone rules.

   **The trial started 2026-08-24 and the first run is in.** A roadmap row was drained through
   `/craft` end to end rather than by hand, and running the flow found things reading it had not:
   the router has no home for a measurement, and the shortcut it falls back to mandates a branch its
   own hazard note forbids. Both are refiled as work in
   [`core/ROADMAP.md`](core/ROADMAP.md) § Open, where the flow layer's internals live.

   **The missing half arrived 2026-08-24: a `standard`-verdict row ran end to end on the relay.**
   The `todo-type-retirement` chain (retiring `TODO.md` as a `.md` type — 73 lines folded into goal
   backlogs) exercised what the *padaria* run could not. **Four distinct tiers actually paid for
   their own loops**, which is the claim, not the intention:

   | loop | tier | model |
   |---|---|---|
   | 0 clarify · 3 arch | max | orchestrator, opus-5 (Field Practice: inline when context is hot) |
   | 1 plan | high | opus-4.8 |
   | 2 ground · 6 ship | low | haiku-4.5 |
   | 4a tests · 4b code | medium | sonnet-5 |

   **The cost thesis holds on this row, with one caveat that decides how to read it.** Loop 4b —
   the expensive loop — consumed **268k tokens over 125 tool calls in ~21 minutes on sonnet-5**,
   never touching opus. That is the saving the flow exists for, and it is real. The caveat: the
   chain died once mid-4b on a weekly limit and needed a **fresh orchestrator session** to resume,
   costing a full re-grounding (read the trail, re-run acceptance, re-decide the branch). *N cheap
   sessions* is true of the executors and **not** of the orchestrator, whose context is the thing
   that actually ran out. Re-run `core/tools/wos/session/usage` rather than trusting this paragraph.

   **Two defects in the relay, both found by running it, and agents are what would fix both.**
   - **The medium executor obeyed a wrong instruction and falsified history.** Loop 1 (opus-4.8)
     wrote a task telling Loop 4b to change *"Collapsing four ledgers into one"* to *"three"* in a
     roadmap header. That sentence is a **past-tense record** of a collapse that really involved
     four. The executor rewrote it to satisfy a grep — and the plan's own § History section, three
     screens above, forbids exactly that. **A generic executor follows the plan; it has no standing
     to doubt one.**
   - **The low-tier ship executor reverted uncommitted work it did not own.** Loop 6 was told the
     dirty-tree fence, and still discarded an orchestrator edit to this very file that was sitting
     uncommitted while it ran. Nothing was lost (it was re-applied from context), but a chain that
     runs against a shared worktree can destroy the orchestrator's own work, and only the
     orchestrator noticing saved it.

   The norm both needed (*never edit a true statement about the past to make a check pass*; *never
   revert what you did not write*) exists in this workspace and was in neither executor's head.
   That is the sharpest argument yet for workspace-authored agents, and it is evidence rather than
   opinion.

   **What is now tried, and what is still not.** Flows: tried twice, both verdicts, relay confirmed.
   Agents: **still wholly untried** — every executor in both runs was a generic subagent. The trial
   is not complete and no ruling on the agent layer should be taken from it.
   → **tier: high**, with Lucas — the remaining sitting is the agent layer, not the flow layer.
7. 🟡 **show context growth continuously, not just at two thresholds.** Lucas, same capture:
   *"gostaria de ver o crescimento da janela de contexto em tempo real, o claude code no vs code
   não mostra. tem alguma forma barata de me mostrar isso?"*
   [`core/hooks/session/context-meter.py`](core/hooks/session/context-meter.py) already reads the
   size the API reports and speaks at `CTX_WARN` / `CTX_LOUD` — the ask is the *trend* between
   them, and the cheapest honest answer is probably a statusline rather than more hook output,
   since the hook's whole design point is costing zero tokens until crossed. **Do not make it
   chatty every turn**; that trades the thing being measured for the measurement.
   → **tier: medium**.
8. 🟡 **auto-continue when the session limit is hit.** Lucas, INBOX 2026-08-16: *"estudar uma forma
   de ativar um 'auto-continue' do claude code quando o limite das sessões é atingido."* Filed here
   rather than in `code/aiwbot` because the thing that must survive the interruption is this
   workspace's session ritual, not a bot's transport.
   **Studied 2026-08-17; the verdict is yours to take.** *Auto-close, not auto-continue* — and the
   study moved it further than expected: **every piece already exists and only the link is missing.**
   `session/context-meter.py` announces the crossings at zero token cost, and
   `core/tools/wos/roundup` is the close. What is unbuilt is `CTX_LOUD` **offering** the close.
   Two findings decide the shape:
   - **A quota limit ends the session; there is nothing to continue into.** Resuming means a *new*
     session, which is exactly roundup + fresh start. That is why *"triggers after a limit window
     renews"* already sits under § Rejected — the live case is covered.
   - **It must offer, never fire.** Closing a session mid-thought against the user's intent costs
     more than the expensive turns it saves, and the cost argument only holds at the top of the
     staircase. Re-run `session/usage` rather than trusting a number here.
   **Ruled 2026-08-17 (Lucas), and the ruling reshaped the item.** The framing above was wrong on a
   fact: the offer is *already there*, as prose aimed at the agent —
   `message()` in `session/context-meter.py` ends with *"Run /roundup to close this session once the
   current thread is done."* What is missing is not the offer, it is **who sees it and when**. It is
   a `UserPromptSubmit` hook, so it lands in the agent's context at the *start* of a turn, and Lucas
   never sees it at all.
   His call: **show both crossings, to both of us, at the END of a response** — not at prompt
   submit. *"it wouldn't interrupt your flow"*, and he stops missing it.
   **The same gap, reported independently** (Lucas, INBOX 2026-08-17): *"algumas vezes o agente pede
   para eu autenticar no gmail ou gdrive mas é no meio de uma conversa longa e eu não vi a
   solicitação."* Confirmed live this session — a consent request sat unclicked through four
   exchanges. So this is not only the meter: **anything the agent needs Lucas to physically do is
   currently said in the middle of agent-facing prose and missed.** One mechanism serves both, which
   is why they are one row.
   **The open question is mechanical and must be checked, not assumed**: which hook fires at end of
   response in each harness, and whether its output can reach the user's terminal without also being
   billed into the agent's context. **Measure the cost before wiring** — the current message is one
   short line, at most once per threshold per session, but "probably free" is exactly the claim this
   workspace keeps getting wrong. → **tier: medium**, after that check.
9. 🟡 **the lever nobody has looked at: thinking is 65% of billed output and no instrument here can
   see it.** Its text is never written to the transcript, so every composition number we have
   describes the other 35%. This reopens what was closed once: Anthropic's guidance is that `effort`
   is not a *length* lever — it moves thinking volume, not reliably visible output — which was read
   as *not a cost lever* and dropped. But thinking volume **is** billed at output rates, and is the
   biggest slice of it. The guidance and the rejection never actually agreed.

   **Not claimed: that lowering effort is free.** Thinking is where the reasoning happens, and ACL
   Findings 2025 (a wrong budget degrades the answer, `core/refs/REFS-cost.md` § Output cost) bites harder
   here than anywhere, because this budget buys correctness rather than brevity. So **measure before
   touching it**: same arm shape as `caveman-cost.md` — one task at two effort levels, comparing
   billed output per turn *and* whether the work came out right. It needs a clean switch, so it runs
   on the feature registry, and it is the same instrument Front 14 needs. No behavior change until
   the number exists. → **tier: high**, with Lucas on whether to act on it.

---
