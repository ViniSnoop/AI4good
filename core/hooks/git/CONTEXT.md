# git
> Gates and self-heals about git state itself: branch shape, gitlinks, .gitignore.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`branch-marker.sh`](branch-marker.sh) | — | — | Branch drift warning — HEAD is shared mutable state between parallel sessions, and nothing said so. `record` stores the branch a session started on; `check` warns at commit time when HEAD has moved since. Warn only, never block: a deliberate mid-session switch is legitimate and common. Decided 2026-08-14 (Lucas) over one-worktree-per-session, which fights the branch sweep in core/skills/roundup.md Phase 5 — a checked-out worktree makes `git branch -d` refuse. |
| [`branch_debt.py`](branch_debt.py) | [`branch_debt.pyi`](branch_debt.pyi) | `unmerged_branches`, `merged_remote_branches` | What the entropy dashboard counts about branches: repos on unmerged work, and remote labels whose commits already landed. |
| [`gitflow-gate.sh`](gitflow-gate.sh) | — | — | Git Flow branch gate — block direct commits to main/master/develop; require feature/|release/|hotfix/ branch names. Scoped to code/ project repos AND the workspace structural repo. Paper repos (academy/papers/*) and any other nested repo are exempt. Called from core/hooks/pre-commit. Convention: AGENTS.md (workspace) / code/SPECS.md § Git Flow (projects). |
| [`gitignore-self-heal.sh`](gitignore-self-heal.sh) | — | — | Self-healing .gitignore allowlist (decided 2026-07-24). Contract: core/hooks/SPECS.md. Every domain folder (core/, code/, academy/, branches/, brain/, models/, datasets/) uses a denylist-first .gitignore pattern (`<domain>/*` + explicit `!<domain>/<dir>/` allow lines), so a brand-new domain subdir is silently untracked until someone remembers to add its line — already bit core/refs/. A subdir with a CONTEXT.md is structural by construction (the existing "this is workspace scaffold" signal): add its allow line and stage it, no human action. A subdir with no CONTEXT.md stays ignored (correctly project-internal/scratch). A subdir listed in gitignore-exceptions.txt is a deliberate, reviewed exception — skipped. A subdir that is its own git repo is skipped too (see the note in the loop). |
| [`nested-gitlink-gate.sh`](nested-gitlink-gate.sh) | — | — | Nested-gitlink gate — block committing undeclared gitlinks (mode 160000) into the workspace structural repo. Internal projects use their own git repos (AGENTS.md); they must NOT be embedded as gitlinks (a fresh clone can't fetch them → broken pins + recurring "M" noise every time you commit inside them). Real submodules declared in .gitmodules are allowed. Called from core/hooks/pre-commit. |
<!-- routing:end -->
