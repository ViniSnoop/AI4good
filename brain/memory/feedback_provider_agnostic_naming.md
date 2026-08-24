---
name: feedback-provider-agnostic-naming
description: "Never put provider/model names (NB, Gemini, etc.) in file names, verbs, or dirs — workspace is provider-agnostic"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bb9b9715-4ea6-4628-9115-ce47ee08dba4
---

User feedback (2026-07-07, isoroll multiview session): "we are doing a lot of work to make our workspace agnostic to
specific providers/models... putting nb in the name of the files seems a bit too much".

**Why:** the workspace invests heavily in provider-agnostic structure (core/ skills, flows, tier→model mapping
volatile). A leading model is fine; baking it into file names couples code to a vendor.

**How to apply:** name modules/verbs/dirs by FUNCTION (imagegen_client, multiview_commands, mv-tile, gen-inbox), keep
provider choice as data (alias registry, docs). Applies to any provider: NB/Gemini, OpenAI, Comfy checkpoints, etc.
Related: [[fable-quota-strategy]].

**Widened 2026-08-17, and it is not only filenames.** Lucas reacted to me saying *"sonnet wires it"* about a roadmap
step: *"nothing in WOS should be tied to a specific vendor/company/model."* The rule covers **work assignments and how I
speak to him**, not just paths. Both ledgers carried 26 routing directives reading `model: sonnet` / `model: opus`; they
now read `tier: high|medium|low`, and which model fills a tier is data in `core/flows/craft/routing.md`.

The line that decides a given mention: **directive vs data.** Assigning work by model name is the violation; a
*measured* split ("opus-5 56.5%, sonnet 7.7%") or a quoted stale model id inside a bug report is legitimate, because
there the model is the fact being reported. This is why it cannot become a flat retired token — a presence check would
fire on the honest uses, so any guard has to read position. Related: [[project-wos-zero-roadmap]].
