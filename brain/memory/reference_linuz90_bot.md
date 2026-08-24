---
name: reference_linuz90_bot
description: linuz90/claude-telegram-bot source read — the reference design for aiwbot; how it does session lineage + its UX feature set
metadata: 
  node_type: memory
  type: reference
  originSessionId: 93775496-3ecc-4c63-92f5-e24a30e2e721
  modified: 2026-07-21T05:45:06.507Z
---

linuz90/claude-telegram-bot (MIT, Bun/TypeScript) — the closest reference for [[project_aiwbot]]. Source read
2026-07-21.

**Repo**: https://github.com/linuz90/claude-telegram-bot — key files: `src/session.ts` (18KB, the whole Anthropic
coupling), `src/handlers/streaming.ts`, `src/handlers/commands.ts`, `docs/personal-assistant-guide.md`.

**Transport**: Claude **Agent SDK** (`@anthropic-ai/claude-agent-sdk`, `query()` in-process) — NOT the CLI subprocess.
This is the "Padrão B" our Phase D targets.

**Session lineage (the important bit)**: `query({ prompt, options: { resume: this.sessionId } })` — plain resume, **NO
fork**. Captures `session_id` ONCE, guarded by `if (!this.sessionId && event.session_id)`, and never overwrites it → one
id, one transcript, whole conversation = single lineage. This is identical behavior to CLI `claude -p --resume <id>`
WITHOUT `--fork-session` (verified live 2026-07-21: plain resume keeps the same id + retains context now that Phase B
dropped `--bg`). Confirms aiwbot's cumulative-VSCode-sessions problem is a stale-AD-3 bug (fork was only mandatory in
the old `--bg` background-agent era), fixable by dropping `--fork-session` from `backend/claude.py` — orthogonal to the
SDK migration.

**Session model**: ONE global singleton current session (`export const session = new ClaudeSession()`) + saved history
of last 5 (`MAX_SESSIONS`, dedup-by-id update-in-place, JSON file) exposed via a `/resume` tap-picker. Different from
aiwbot's session-per-reply-thread (reply_map) model — linuz90 = one current conversation you switch via /resume; aiwbot
= multiple parallel, disambiguated by which message you reply to.

**UX feature set worth stealing** (Lucas's standing ask): streaming live-edit of one message as text/tools/thinking
arrive (throttled, `statusCallback` kinds: thinking/tool/text/segment_end/done — our Phase C); `!`-prefix or `/stop` to
interrupt a running query + message queuing; extended-thinking budget by keyword ("think"→10k, "reason"/deep→50k
tokens); `ask_user` MCP → Telegram inline buttons (Claude asks YOU mid-task); `send_file` MCP → Claude sends files back
to chat (routed by ext to photo/video/audio/document); date/time injected into the first message so Claude doesn't
tool-call for it; voice/photo/doc/audio/video ingestion (voice via OpenAI transcription); command-safety +
path-allowlist gate. Commands: start/new/resume/stop/status.

**Framing**: pitches Claude Code as a general-purpose personal assistant pointed at a CLAUDE.md folder (= our brain/
concept). CLI auth (subscription) recommended over API key for cost.
