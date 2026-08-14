# [ craft | research | year ] always-on autonomous local AI

Build a local AI setup compatible with Claude Code. Optimize agents to run fast and reliably using strategies of dynamically expanding and collapsing context: foldable contexts, smaller models operating under compressed representations. The research direction is clear and the literature is live.

*refs:*  
- https://openreview.net/pdf?id=JaLXQnA2wi  
- https://openreview.net/pdf?id=91jL62CQF1  
- https://arxiv.org/pdf/2603.16021  
- https://github.com/WeaveMindAI/weft  
- https://arxiv.org/pdf/2604.14228  
- https://arxiv.org/pdf/2601.10112  
- https://arxiv.org/pdf/2602.11988  
- https://www.instagram.com/p/DbKa8dzkRv4/ — [src: web:instagram.com] "no-limits local AI video gen" carousel (DM-gated, title cards only extracted so far)  

>**signals**  
transformative · expected · motivated

>**owns**  
`code/dobra` · `code/aiwbot` · `academy/papers/2027-ICLR-dobra`

## selected next achievement
    [read-weft] read the weft implementation paper and repo — most concrete starting point

**ease-start**  
Open the weft repo (github.com/WeaveMindAI/weft). Read the README. Understand what the system does, what it builds on. 30 minutes max.

## backlog

> [ ] [read-weft] read the weft implementation paper and repo — most concrete starting point  
> [ ] [read-foldable] read the foldable contexts paper (arxiv 2603.16021)  
> [ ] [map-landscape] map the 7 cited papers — what problem does each solve, how they connect  
> [ ] [local-setup] set up a local model environment (Ollama or equivalent) compatible with Claude Code  
> [ ] [tiny-quant] avaliar quantização extrema como caminho pro setup local — Qwen3.6-27B rebuildado em 1-bit (3.9GB) / ternário (5.9GB), arquitetura intacta, cabe até em celular (ref em `core/WATCHLIST.md`). Amarra direto em [local-setup]: decide se a RTX 3050 6GB roda um 27B em vez de um 7B (INBOX 2026-07-23)  
> [ ] [tts-local] KittenTTS <25MB em CPU — checar suporte a pt-BR ANTES de qualquer integração; sem pt-BR não serve pra nada aqui (ref em `core/WATCHLIST.md`, INBOX 2026-07-23)  
> [ ] [prototype-context] build a first prototype: dynamic context collapse for a specific task type  
> [ ] [benchmark] measure: speed, reliability, quality vs cloud baseline  
> [ ] [claude-code-alt] set up CLI coding agent alternative to Claude Code — candidates: qwencode + qwen model locally, GLM 5.1 (free cloud), opencode, codex  
> [ ] [local-video-gen] evaluate the local AI video-gen setup as alternative to opencode+nvidia+image-model (INBOX 2026-07-26, IG carousel `DbKa8dzkRv4` — DM-gated, only title cards extracted; may need the "GUIDE" DM or independent search to get the real tool list)  
> [ ] [vipassana-autonomous] explorar deixar um agente rodando com autonomia SEGURA durante os 10 dias de vipassana (1–12 ago, offline), entregando resultados RELEVANTES — candidatos: watcher que constrói/refina continuamente as revisões de estado-da-arte dos papers planejados; pasta sandbox pra prototipar. Pré-requisito duro: **mecânica de autostart de sessões** (o caso "sessão morreu, ninguém acorda o agente" do [workspace-os] triggers pós-janela). Definir escopo seguro ANTES; sem isso, não roda (INBOX 2026-07-23)  

## done

<!-- done:start -->
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-08-13  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |     110 |
| trimester   |     122 |
| semester    |     122 |
| year        |     122 |
| 2-year      |     122 |
| 4-year      |     122 |
<!-- stats:end -->
