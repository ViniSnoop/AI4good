# Cost and model routing
> Where session spend goes, which tier runs what, and what loads every session.
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
   → **tier: high**, with Lucas — several sittings, not one pass.
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
   Findings 2025 (a wrong budget degrades the answer, `core/refs/REFS.md` § Output cost) bites harder
   here than anywhere, because this budget buys correctness rather than brevity. So **measure before
   touching it**: same arm shape as `caveman-cost.md` — one task at two effort levels, comparing
   billed output per turn *and* whether the work came out right. It needs a clean switch, so it runs
   on the feature registry, and it is the same instrument Front 14 needs. No behavior change until
   the number exists. → **tier: high**, with Lucas on whether to act on it.

---
## Front 3 — Memory and always-loaded context

0. 🟢 **measure `.claude/commands/`, then decide — the only unmeasured thing left at session start.**
   `mirror.sh` copies all 13 skills a *second* time as slash commands (52 KB on disk). That copy is
   folded into the system prompt, so it lands inside the **77% residual** that
   [`session/context`](core/tools/wos/session/context) cannot decompose — it is invisible to every
   number we have. It may be a real chunk of the residual or nothing at all, and the honest order is
   measure first: the cheapest probe is a session with the directory emptied, comparing turn-1
   context. **Do not cut it on suspicion** — that is the mistake the 1.6-3.5x inflation already
   taught. Record the result in [`core/experiments/context-window.md`](core/experiments/context-window.md).
   → **tier: medium**.

---
