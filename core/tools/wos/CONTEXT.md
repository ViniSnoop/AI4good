# wos
> Tools that act on the workspace itself: spec ledger, contract check, skill mirrors.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`diagram/`](diagram/CONTEXT.md) | The workspace drawn from its own declarations: one generated HTML picture, zero tokens, no model. |
| [`session/`](session/CONTEXT.md) | What a session costs and what fills it, read from the local transcripts. No network, no model. |

| File | Description |
|------|-------------|
| [`deps`](deps) | probe every dependency declared in core/tools/deps.txt, reporting what each miss breaks; --check exits 1 on any miss |
| [`features`](features) | list every toggleable feature from core/features.txt with its answer in core/profile.txt; --findings counts what cannot be switched off; --check exits 1 on any registry/profile disagreement |
| [`roundup`](roundup) | the deterministic half of the /roundup ritual Verification gate, entropy regen, branch promotion. Prints the three state facts /handoff needs and anything that needs a decision; nothing else. |
| [`skills/mirror.sh`](skills/mirror.sh) | Mirror generation for the skill library: listing, symlink mirrors, command-file copies, and orphan pruning. Sourced by core/tools/wos/sync-skills — a FRAGMENT that relies on $SRC, $MIRRORS and $COMMANDS_DIR from the caller. |
| [`skills/validate.sh`](skills/validate.sh) | Frontmatter validation for every layer of the agent library — skills, flows, the flow composition DAG, and agents. The law itself is core/SCHEMA.md; these only enforce it. Sourced by core/tools/wos/sync-skills; relies on $SRC and $WORKSPACE from the caller. |
| [`spec-contract-check`](spec-contract-check) | verify every spec-locked module has a complete SPEC.md contract (Inputs/Outputs/Invariants filled); optionally type-check declared edges. Exit 1 on any gap. See code/ROADMAP-spec-drive.md. |
| [`spec-scan`](spec-scan) | ledger of module SPEC.md status (locked|draft|optout|none) Spec-driven-development coverage ratchet. A module = a dir with a CONTEXT.md under code/. See code/ROADMAP-spec-drive.md. |
| [`sync-global-skills`](sync-global-skills) | link workspace-vendored global skills into $HOME |
| [`sync-skills`](sync-skills) | regenerate skill mirrors from core/skills/*.md |
<!-- routing:end -->
