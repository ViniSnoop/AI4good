---
name: project-wos-zero-roadmap
description: Lucas quer zerar o ROADMAP do WOS o quanto antes — infra já consumiu tempo demais; isso filtra o que pode entrar no ledger
metadata: 
  node_type: memory
  type: project
  originSessionId: c7f29617-a34b-4367-b30b-7f98ac056b82
  modified: 2026-08-16T16:20:20.839Z
---

**Lucas, 2026-08-16:** *"definitivamente, quero zerar o roadmap do WOS o quanto antes. já usamos
demasiado tempo e esforço na infraestrutura."*

**Why:** o WOS é meio, não fim — existe pra servir pesquisa, aulas e os projetos
([[project-instituto]], [[project-spacemantics]], [[project-dobra]]) e virou o próprio trabalho.
Lucas já relatou "sentir-se perdido" duas vezes com a massa do ledger; a queixa agora não é sobre
navegação, é sobre custo de oportunidade.

**How to apply:** é um **filtro sobre o que pode existir no ledger**, não um pedido de velocidade.
Na ordem em que morde:

1. Item que outro repo é dono → **refile lá**, nunca segurar no ledger do wos. Regra do próprio
   workspace: um ponteiro pra outro ROADMAP é duplicata por definição.
2. Item que não trava o v1 → candidato a `## Rejected`, não a backlog.
3. Achado que vale guardar → vai pra seção de `SPECS.md`/`SCHEMA.md` dona da regra. Escrever a
   regra lá **é** o que fechar um item significa.

v1 = 4 critérios, 2 e 3 já METs. O que resta é o critério 4 (clonable), que é a front de
portabilidade e clonabilidade inteira. Texto canônico em `brain/goals/workspace-os.md`
§ governing constraint; isto aqui só lembra que existe.

Relacionado: [[feedback-delete-weak-features]] (mesma disciplina aplicada a features),
[[project-verify-roadmap]].
