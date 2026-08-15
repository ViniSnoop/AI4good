---
name: project_aiwbot
description: "provider-agnostic bot to drive swappable coding agents (claude/opencode/copilot) from chat — code/aiwbot, live; next is audio in+out"
metadata: 
  node_type: memory
  type: project
  originSessionId: ea825a23-8450-41ac-af0b-fd49df96a79a
  modified: 2026-08-01T05:39:48.352Z
---

`code/aiwbot/` (own git repo, gitflow; named after @lsfaiwbot). Provider-agnostic rebuild of the workspace Telegram bot: one `AgentBackend.send()→AsyncIterator[AgentEvent]` seam normalizes every coding-agent CLI, so provider is data not code. Repo **https://github.com/lsfcin/aiwbot** (PUBLIC, default `main`); config lives in `~/.config/aiwbot/` (gitignored, never in history). Runs live as `aiwbot.service` (systemd --user).

**Why it exists (non-obvious):** official Anthropic Remote Control + Channels solve phone↔desktop sync natively/better but lock 100% into Claude Code → rejected per [[feedback_provider_agnostic_naming]] ("não quero ser refém do claude code"). Architecture = linuz90/claude-telegram-bot's pattern (Agent-SDK single-process, its whole coupling is one `query()` call) rebuilt in Python. See [[reference_linuz90_bot]].

**Status 2026-07-23:** `main` == `develop` == `f1fd896`, pushed, service restarted on it. 139 free tests (`make test`). Phases A/B + Tiers 1-3 + P3 + P2 shipped. Next: **audio in + out**. Read `code/aiwbot/ROADMAP.md` + `SPECS.md` before any session.

**Ranking lens for the backlog — the durable part.** Score every item by *does it remove a reason Lucas has to go back to the PC?* The bot's job is the away-from-PC front door, so value beats size. Lucas overrode two of my calls when I applied it: **outbound media/show-me drops to LAST** ("se o modelo precisar, ele pode construir um artifact") because the gap degrades rather than blocks; and **audio beats live streaming**, with a new ask for audio **output** (TTS answers), because it removes a whole modality barrier instead of prettifying an existing text exchange. Running order (P2 is behind us): **audio in+out** → live streaming → ask_user → show-me → Phase D.

**Verified CLI surfaces (SPECS AD-10)** — settles what blocked P2's design: opencode DOES have plan/build (`--agent`, both primary), `--variant` for effort, `-m provider/model` over 478 models; claude has `--effort low..max`, `--model`, `--permission-mode`. What actually differs is *cardinality*, not existence. `~/.cache/opencode/models.json` carries per-model `limit.context` and `reasoning_options` — that file IS the capability declaration P2 needs, offline and free. opencode's sqlite answers the picker too (done — SPECS AD-12).

**Two traps that cost real debugging, both live-verified** (worth keeping because the data *looks* right): opencode's `session.tokens_*` columns are **lifetime totals, not context occupancy** — a real session read 175% of its window; occupancy is per-message (`input + cache.read + cache.write`) off the last `role=assistant` message. And `part` rows of `type=text` include the **user's own message and injected system-reminders**, so a preview must filter by the parent message's role or it quotes Lucas back at himself.

Fully supersedes the old bot: `core/tools/telegram_daemon.py` was retired in 570fed7 (*"chore(tools): retire the old Telegram bot, superseded by code/aiwbot"*) — it is gone, not a reuse source. Corrected 2026-08-01. Goal context: brain/goals/workspace-os.md [aiwbot] entry.

**Tool paths changed 2026-08-01** — `core/tools/` split into families, so anything here or in aiwbot that shells out to a workspace tool wants the new path (`core/tools/web/search`, `core/tools/video/video`, …). See [[project_wos_fanout_split]].
