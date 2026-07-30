# Done Log
> Achievements archived from goal files. Newest last.
> Format: date | goal | achievement

---

2026-07-19 | loop-engineering | [iterate] ajustar flags de retorno e tabela de roteamento após 7 usos reais (DONE 2026-07-16, sessão de avaliação /loops): `core/flows/loop-engineering.md` recebeu `## Prior Art` (Reflexion/LATM/Voyager + Cognition/LangChain/Anthropic), `## Case Study` (export-manifest integration-gap catch), `## Field Practice` com tabela de overrides, `## Second-opinion verifier` em Loop 3+6 (Voyager-style), `## Status` em Loop 6, `## Loop 6.5 Skill Extraction`; `last-reviewed` na tabela volátil. /loops skill (`core/skills/loops.md`) ganhou pointer de prior art. dobra (`code/dobra/CONTEXT.md` Overview) cross-ref noun.
2026-07-29 | workspace-os | [gmail-link] `core/tools/gmail` + `core/skills/gmail.md` — read-only Gmail across 3 accounts, routes to INBOX/TODO/goals/drafts/attachments.
2026-07-29 | workspace-os | [gcal-link] DONE — `core/tools/calendar` + `/calendar` skill, read-only across the three accounts (personal, cin, ufrpe).
2026-07-29 | workspace-os | [telegram-link] DONE 2026-07-20, then superseded — the original `core/tools/telegram_daemon.py` proved the capture path (text/photo/voice/document from the paired chat → `brain/INBOX.md`, attachments to `brain/attachments/YYYY-MM/`) and is now **deleted**, rebuilt provider-agnostically as `code/aiwbot`. `[whatsapp-inbox-bot]` and `[bot-conversational-ux]` died with it: Telegram's API was lower-friction than WhatsApp Cloud, and the 12-step conversational-UX plan was superseded by the rebuild rather than ported.
2026-07-29 | workspace-os | [skill-collapse] DONE 2026-07-22 — brain collapsed to two verbs: `/inbox` + `/compass`. `/brain-finished` folded into `/compass` as the "close a win" move and retired.
2026-07-29 | workspace-os | [compass-cadence] DONE 2026-07-22 — soft SessionStart line (`.hooks/compass-nudge.py`) gently offers `/compass` when it has been >14d. Ignorable, in-session only, no phone.
2026-07-29 | workspace-os | [goals-sync] FIXED 2026-07-11 — `.hooks/brain_stats.py` existed but never ran: `Path("Brain")` vs the real `brain/` (case mismatch on Linux), plus a title parser that only accepted 2-field headers and so showed 1 of 50 goals. Both fixed.
2026-07-29 | workspace-os | [nested-gitlink-gate] DONE 2026-07-22 — untracked all 10 undeclared gitlinks (files intact), gitignored the nested-repo dirs, added `.hooks/nested-gitlink-gate.sh` to block future ones, and extended `.hooks/gitflow-gate.sh` to enforce the workspace repo itself. The recurring workspace "M" is dead.
