# git
> Gates and self-heals about git state itself: branch shape, gitlinks, .gitignore.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`branch-marker.sh`](branch-marker.sh) | Branch drift warning — HEAD is shared mutable state between parallel sessions, and nothing said so. |
| [`gitflow-gate.sh`](gitflow-gate.sh) | Git Flow branch gate — block direct commits to main/master/develop; require feature/|release/|hotfix/ |
| [`gitignore-self-heal.sh`](gitignore-self-heal.sh) | Self-healing .gitignore allowlist (decided 2026-07-24). Contract: core/hooks/SPECS.md. |
| [`nested-gitlink-gate.sh`](nested-gitlink-gate.sh) | Nested-gitlink gate — block committing undeclared gitlinks (mode 160000) into the |
<!-- routing:end -->
