# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

https://www.instagram.com/reel/Dbk11QVtZB8/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==
— via aiwbot · 2026-08-16

maybe we should keep looking for options on how to minimize output tokens

I think it is best to change the final output of the /roundup 
from
Read outputs/handoff.md and continue.
to
Read outputs/handoff.md and plan what you'll do in this session.
my argument is that there are advantages on planing a session, but I want to discuss this in detail with Opus


https://www.instagram.com/reel/DcEBQNPNPzs/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==
— via aiwbot · 2026-08-16

estudar uma forma de ativar um "auto-continue" do claude code quando o limite das sessões é atingido

https://www.instagram.com/p/Db9DJojGKfS/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==
anotar em algum lugar, talvez um goal sobre viagens
— via aiwbot · 2026-08-15

vi um comentário sobre o OPUS ter MUITA SEGURANÇA sobre pontos que na verdade ele estava errado. será que temos como corrigir isso. de fato eu gostaria que todas as opiniões técnicas da IA fossem tomadas com base em pesquisas. fiquei pensando se podemos desenvolver uma base do conhecimento (KNOWLEDGE BASE), um grafo ou algum outro tipo de estrutura muito fácil de acessar (tipo por hash), que sempre teria a informação curada, com base em estudo, leituras, pesquisas e dicernimento crítico. outra coisa que pensei é instruir o modelo / os agentes dizendo que "YOU DON'T KNOW THINGS, don't feel too certain, search before giving precise technical opinions". e aí induzir ele a olhar a KNOWLEDGE BASE, inclusive se tiver lá mas for algo antigo que pode ter sido atualizado então continuar a pesquisa e atualizar, e se não tiver na base então fazer uma pesquisa mais profunda e inserir. sempre fui fã da ideia de knowledge graph, talvez isso aqui passe por esse ponto.

o AGENTS.md voltou a parecer meio grande pra mim... avaliar ele com bastante carinho

de forma geral output tokens são bem mais caros que input tokens. estudar formas de reduzirmos os output tokens. vi no instagram uma medida que não gosto mas que me fez pensar, de pedir para o opus "SHUT UP SHUT UP, JUST DO THE WORK AND SHUT UP".

o WOS pode, e acho que seria uma boa, virar um artigo. o estudo de ablação, se bem feito, me parece bem publicável.

definitivamente, quero zerar o roadmap do WOS o quanto antes. já usamos demasiado tempo e esforço na infraestrutura.

claude code report, we may have to look to this from time to time
What’s contributing to your limits usage?
Day
Week
Approximate, based on local sessions on this machine — does not include other devices or claude.ai
Last 24h · these are independent characteristics of your usage, not a breakdown
73% of your usage was at >150k context
Longer sessions are more expensive even when cached. /compact mid-task, /clear when switching to new tasks.
44% of your usage came from subagent-heavy sessions
Each subagent runs its own requests. Be deliberate about spawning them — and consider configuring a cheaper model for simpler subagents.
14% of your usage came from /roundup
Heavy skills can be scoped down or run with a cheaper model via skill frontmatter.
Skills
% of usage
/roundup
14%
/handoff
2%
Subagents
% of usage
Explore
3%
general-purpose
1%

---
issues found 2026-08-16, agent-written:

`core/hooks/checks/pre-edit.py:11` sets `WORKSPACE_ROOT = parents[2]`, which is
`/mnt/workspace/core`, not the workspace root — so `is_vendored()` always returns False there and
the vendored exemption never applies at edit time. `vendored.txt` patterns are workspace-relative
(`academy/papers/*/sigconf*.tex`, `code/corpora/depth_anything_v2/*`), so editing a vendored .py
past 200 lines is blocked by the size gate that vendored.txt exists to waive. Latent, not observed.

`core/hooks/facade/facade-scan.py` is documented as **Informs** but prints to stdout on exit 0,
which Claude Code shows in transcript mode only — the model never sees it. The channel that does
reach the model is `hookSpecificOutput.additionalContext`, now verified working on PreToolUse
(`core/hooks/SPECS.md`). So one of our hooks has been talking to nobody.

Dead item-number pointers in code: `Frente 9.2` is cited in `core/tools/wos/roundup` (x2),
`test_roundup.py`, `test_roundup_skills.py` (x2) — and that item is deleted. ROADMAP.md § How to
read this already bans citing item numbers from code; nothing enforces it. A Tier 0 check could.

