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
   o que fechar um item significa.
4. Pedido de "opções pra sessão" = ele quer **argumentos dos dois lados**, não uma recomendação
   pronta: *"assess and propose options BUT with arguments so I have a better base for the
   decision"*.

**Estado 2026-08-16:** os 4 critérios do v1 estão METs. O registro de features shippou —
`core/features.txt` + `core/profile.txt` + `core/hooks/feature_law.py` + `core/tools/wos/features`,
regra em `core/SPECS.md` § AD-14. Sobram ~32 itens no ledger. Ainda precisam de decisão do Lucas:
agents-vs-skills, SDD (retomar/rescopar/matar) e a knowledge base — a ablação saiu dessa lista por
decisão dele (não precisa de ruling, só da precondição). Próximo gargalo real dela: 60 das 62
features ainda não são desligáveis, e a lista viva está em `core/tools/wos/features --findings`,
nunca copiada.

Texto canônico do constraint em `brain/goals/workspace-os.md` § governing constraint.

Relacionado: [[feedback-delete-weak-features]] (disciplina de deletar vale pra *features fracas*, não
pra itens de ledger — não confundir as duas), [[project-verify-roadmap]].
