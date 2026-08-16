# skills
> Agent skills — provider-agnostic workflows invoked as slash commands or by instruction.

`core/skills/<name>.md` is the only place to edit a skill — the `.opencode/skills/` and
`.claude/skills/` mirrors are generated symlinks.

How to create or edit a skill, the sync commands, the case-sensitivity hazard, what's excluded from
mirroring, and the folder-shaped global-skill pattern (`caveman/`): [`SPECS.md`](SPECS.md).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`caveman/`](caveman/CONTEXT.md) | Ultra-compressed communication mode — vendored suite: router skill, mode… |
| [`foundry/`](foundry/CONTEXT.md) | Foundry VTT v14 module dev reference — skill suite. |
| [`prepare/`](prepare/CONTEXT.md) | Prepare a raw prompt for an agent: optimize, contextualize, and recommend… |

| File | Description |
|------|-------------|
| [`SPECS.md`](SPECS.md) | Contract for creating, editing, and syncing a skill, plus the folder-shaped… |
| [`_template.md`](_template.md) | One-line summary of what this skill does and when to invoke it. Invoke with… |
| [`calendar.md`](calendar.md) | List upcoming events and query date ranges from Google Calendar across all… |
| [`compass.md`](compass.md) | Gentle strategic review of Brain: what has good wind, reorder by motivation… |
| [`dedup.md`](dedup.md) | Semantic duplication audit for a code project: near-duplicate logic that the… |
| [`drive.md`](drive.md) | List, search, and download files from Google Drive across all configured… |
| [`foundry.md`](foundry.md) | Foundry VTT v14 module dev reference — router. Load relevant subfiles before… |
| [`gmail.md`](gmail.md) | Triage Gmail across all configured accounts — classify, confirm routes, write to… |
| [`handoff.md`](handoff.md) | Emit a copy-pasteable resume prompt for the next session. For the full… |
| [`inbox.md`](inbox.md) | Triage brain/INBOX.md — route each entry to a goal, task, reference, project… |
| [`iso-visual.md`](iso-visual.md) | Isoroll visual-semantics reference: image-to-text conventions, known model… |
| [`loops.md`](loops.md) | Run the craft flow: develop a feature in file-relayed loops with model… |
| [`prepare.md`](prepare.md) | Turn a raw task into an optimized agent prompt: interviews for intent… |
| [`research.md`](research.md) | Execute a research workflow from the workspace Core research system. |
| [`roundup.md`](roundup.md) | Full session-close ritual: drain the ledgers, route session knowledge to durable… |
<!-- routing:end -->
