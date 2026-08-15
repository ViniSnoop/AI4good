---
name: feedback-provider-agnostic-naming
description: "Never put provider/model names (NB, Gemini, etc.) in file names, verbs, or dirs — workspace is provider-agnostic"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bb9b9715-4ea6-4628-9115-ce47ee08dba4
---

User feedback (2026-07-07, isoroll multiview session): "we are doing a lot of work to make our workspace agnostic to specific providers/models... putting nb in the name of the files seems a bit too much".

**Why:** the workspace invests heavily in provider-agnostic structure (core/ skills, flows, tier→model mapping volatile). A leading model is fine; baking it into file names couples code to a vendor.

**How to apply:** name modules/verbs/dirs by FUNCTION (imagegen_client, multiview_commands, mv-tile, gen-inbox), keep provider choice as data (alias registry, docs). Applies to any provider: NB/Gemini, OpenAI, Comfy checkpoints, etc. Related: [[fable-quota-strategy]].
