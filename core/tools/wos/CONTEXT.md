# wos
> Tools that act on the workspace itself: spec ledger, contract check, skill mirrors.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`roundup`](roundup) | the deterministic half of the /roundup |
| [`skills/mirror.sh`](skills/mirror.sh) | ← add first-line comment |
| [`skills/validate.sh`](skills/validate.sh) | ← add first-line comment |
| [`spec-contract-check`](spec-contract-check) | verify every spec-locked module has a complete SPEC.md contract (Inputs/Outputs/Invariants filled); optionally type-check declared edges. Exit 1 on any gap. See code/SPEC-DRIVE.md. |
| [`spec-scan`](spec-scan) | ledger of module SPEC.md status (locked|draft|optout|none) |
| [`sync-global-skills`](sync-global-skills) | link workspace-vendored global skills into $HOME |
| [`sync-skills`](sync-skills) | regenerate skill mirrors from core/skills/*.md |
| [`usage`](usage) | where session spend goes: by model, |
<!-- routing:end -->
