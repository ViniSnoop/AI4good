---
name: storage
description: The workspace owns its state; nothing that matters is written to a vendor's private directory.
---

**PROVIDER-AGNOSTIC STORAGE: the workspace owns its state, never a harness.** Agnostic to provider, company and harness — so nothing that matters is written to a vendor's private directory. If a harness insists on its own path, symlink that path into the repo. Live case: `~/.claude/projects/<slug>/memory` → `brain/memory/`, so what the agent writes lands in git.
