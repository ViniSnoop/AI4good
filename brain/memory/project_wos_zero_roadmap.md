---
name: project-wos-zero-roadmap
description: Zerar o ROADMAP do WOS = SHIPPAR tudo, não deletar — pós-v1 Lucas rejeitou explicitamente a leitura de "corta o que não paga"
metadata: 
  node_type: memory
  type: project
  originSessionId: c7f29617-a34b-4367-b30b-7f98ac056b82
  modified: 2026-08-17T02:15:11.352Z
---

**Lucas, 2026-08-16:** *"definitivamente, quero zerar o roadmap do WOS o quanto antes. já usamos
demasiado tempo e esforço na infraestrutura."*

**CORREÇÃO do mesmo dia, depois que os 4 critérios do v1 ficaram verdes.** Proposta de varredura de
triagem (Reject/Refile/Ship item a item, 33 → ~8) foi **recusada**: *"eu sei que resolver tudo numa
sessão não é realista MAS vamos com o tempo SHIPPAR tudo. não tem nada ali pra ser deletado.
realocado sim, deletado não."*

**Why:** "zerar" nunca significou encolher o ledger por corte — significa **acabar o trabalho**. A
seção `## Rejected` continua existindo pro que já foi morto, mas não é destino de item vivo só por
ser pós-v1. O custo de oportunidade que motivou a queixa se resolve entregando, não apagando.

**How to apply**, na ordem em que morde:

1. Item que outro repo é dono → **refile lá** (realocação, não deleção). Ponteiro pra outro ROADMAP
   é duplicata por definição.
2. Item que não trava nada → **continua no backlog**, não vira `## Rejected`. Só vai pra Rejected o
   que for de fato morto, com uma linha dizendo por quê.
3. Achado que vale guardar → seção do `SPECS.md`/`SCHEMA.md` dona da regra. Escrever a regra lá **é**
   o que fechar um item significa. **Caveat learned 2026-08-17: this route also relocates *unbuilt*
   work.** Naming a gate that does not exist yet in a `SPECS.md` closes the roadmap row but not the
   job — five such checks were named in one session. Legitimate (it is realocação), but the item
   count then flatters the work state, so **say plainly how many unbuilt checks moved** whenever this
   route is used in bulk.
4. Pedido de "opções pra sessão" = ele quer **argumentos dos dois lados**, não uma recomendação
   pronta: *"assess and propose options BUT with arguments so I have a better base for the
   decision"*.

**Estado 2026-08-17:** os 4 critérios do v1 estão METs. Duas das três decisões que travavam o ledger
foram tomadas: **SDD retomado** com alvo *todo módulo tocado ganha spec*, ENFORCED (trabalho refilado
pra `code/ROADMAP-spec-drive.md` § P5), e a **ablação roda FORA do WOS**, em variantes montadas do
repo público — o que torna o repo público pré-requisito duro, não vizinho. Sobram **duas** que
precisam dele, e as duas viraram *rounds de discussão e pesquisa*, não perguntas com opções: flows +
agents (ele recusou deletar com base em uso baixo — *"we did not work enough on these yet"*) e o
knowledge graph (frente própria, sessão dedicada). Contagens vivas só por comando:
`core/tools/wos/features --findings` e `wc -l ROADMAP.md`, nunca copiadas.

**Drain strategy, chosen by Lucas 2026-08-17 and validated in one sitting: the count that matters is
not total items, it is *opus-only* items.** Offered three session shapes, he picked an **opus-only
judgement sweep** — no delegation, no parallelism — on the reasoning that the ~17 sonnet-tagged rows
are drainable by cheap sessions any day, while the opus-tagged ones are drainable by nothing else.
Result: total 28 → 21, but **opus-only 11 → 4**, which is the number that unblocks everyone else.
So an opus session on this ledger should spend itself where opus is the scarce input and refuse the
mechanical rows, even when they look faster. Corollary he supplied on the two items he owns: bring
**verdict + evidence, item stays open** — study is agent work, ruling is his.

Texto canônico do constraint em `brain/goals/workspace-os.md` § governing constraint.

Relacionado: [[feedback-delete-weak-features]] (disciplina de deletar vale pra *features fracas*, não
pra itens de ledger — não confundir as duas), [[project-verify-roadmap]].
