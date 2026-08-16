# wos
> Tools that act on the workspace itself: spec ledger, contract check, skill mirrors.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`session/`](session/CONTEXT.md) | What a session costs and what fills it, read from the local transcripts. No… |

| File | Description |
|------|-------------|
| [`deps`](deps) | probe every dependency declared in core/tools/deps.txt, reporting what each miss breaks; --check exits 1 on any miss |
| [`features`](features) | list every toggleable capability from core/features.txt with its answer in core/profile.txt; --findings counts what cannot be switched off; --check exits 1 on any registry/profile disagreement |
| [`roundup`](roundup) | the deterministic half of the /roundup ritual |
| [`skills/mirror.sh`](skills/mirror.sh) | Mirror generation for the skill library: listing, symlink mirrors, command-file |
| [`skills/validate.sh`](skills/validate.sh) | Frontmatter validation for every layer of the agent library — skills, flows, the |
| [`spec-contract-check`](spec-contract-check) | verify every spec-locked module has a complete SPEC.md contract (Inputs/Outputs/Invariants filled); optionally type-check declared edges. Exit 1 on any gap. See code/ROADMAP-spec-drive.md. |
| [`spec-scan`](spec-scan) | ledger of module SPEC.md status (locked|draft|optout|none) |
| [`sync-global-skills`](sync-global-skills) | link workspace-vendored global skills into $HOME |
| [`sync-skills`](sync-skills) | regenerate skill mirrors from core/skills/*.md |
<!-- routing:end -->
