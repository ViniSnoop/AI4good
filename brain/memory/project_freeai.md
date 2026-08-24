---
name: project_freeai
description: freeai project — docs-only repo público, PT-BR: tabelas comparativas de opções gratuitas de IA para codar (harnesses, IDE, provedores, modelos)
metadata: 
  node_type: memory
  type: project
  originSessionId: 
  modified: 2026-08-24T12:00:00.000Z
---

**freeai** = mapa das opções gratuitas para codar com IA. Quatro tabelas (harnesses CLI, extensões IDE, provedores com
free tier, modelos open-weights) com links oficiais por linha e carimbo de verificação. PT-BR.

**Remotes**
- origin: https://github.com/lsfcin/freeai.git (PUBLIC, MIT)
- Git flow: main (releases), develop (integration), feature/* (work)
- Branch protection: PR required on main + develop
- Default branch: main

**Key facts for next session**
- current release: v0.1.0
- GitHub Models foi desligado em 30/07/2026 — está na seção "aposentados" de provedores.md
- Qwen Code free tier (2K req/dia OAuth) acabou em abr/2026 — harnesses.md anota
- Cerebras não tem mais free tier permanente — só trial US$5/30 dias com cartão
- Mistral Free (consumer) dá US$10/mês em créditos de API — não é "zero real" mas é generoso
- Gemas numéricas: Gemini CLI 60 RPM/1K dia; Groq até 14,4K dia modelos pequenos; OpenRouter :free 20 RPM/50 dia (1K dia
  com ≥US$10 aporte)
- Rotina de manutenção: revisão mensal dos limites (ROADMAP backlog)
- INBOX.md do workspace tem uma observação sobre o allowlist inerte no .gitignore
