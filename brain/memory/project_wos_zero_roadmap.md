---
name: project-wos-zero-roadmap
description: Zerar o ROADMAP do WOS = shippar o trabalho, mas a PROSA em volta se corta — regra corrigida por Lucas em 2026-08-25
metadata:
  node_type: memory
  type: project
  originSessionId: c7f29617-a34b-4367-b30b-7f98ac056b82
  modified: 2026-08-25T00:00:00.000Z
---

**A regra, nas duas metades que quase se contradizem:**

1. **Trabalho vivo se realoca, não se deleta** (Lucas, 2026-08-16): *"vamos com o tempo SHIPPAR tudo.
   não tem nada ali pra ser deletado. realocado sim, deletado não."* Item que outro repo é dono →
   refile lá. Item que não trava nada → fica no backlog, não vira `## Rejected`.
2. **A prosa em volta do trabalho se corta** (Lucas, 2026-08-25): nove ROADMAPs viraram um de 184
   linhas e 1.645 linhas morreram, sem que um só item vivo sumisse. A norma `cap` agora diz *passou
   do teto, corta* — dividir em irmãos exige OK explícito dele.

**Why:** as duas nunca foram a mesma coisa. "Zerar" significa acabar o trabalho; nunca significou
manter cada parágrafo escrito sobre esse trabalho. O que o item precisa é O QUE / POR QUE /
VERIFICAÇÃO — o COMO é da sessão que atacar o item, e era o COMO que engordava tudo.

**How to apply:**

- Antes de cortar qualquer `.md`, checar se algum hook faz parse dele. `core/SCHEMA.md`,
  `core/norms/*.md` e `ROADMAP*.md` são **dados lidos por código**, não prosa.
- Achado que vale guardar → seção do `SPECS.md`/`SCHEMA.md` dona da regra. Caveat: essa rota também
  realoca trabalho **não construído**, então diga em voz alta quantos checks inexistentes moveram.
- **A contagem que importa não é total de itens, é itens *só-opus*.** Sessão opus gasta onde opus é o
  insumo escasso e recusa as linhas mecânicas, mesmo parecendo rápidas.
- Nos itens que ele decide: trazer **veredito + evidência, item fica aberto**. Estudo é do agente,
  decisão é dele.
- **Sem pressa** (2026-08-19): *"zero é o destino, não meta de sessão."* Deixar item bem
  especificado vale mais que entregá-lo mal.
- Formato de sessão que mais rendeu: *rulings sprint* em plan mode — juntar as decisões 🔴 numa ou
  duas rodadas de `AskUserQuestion` com opções fundamentadas em probe, e só então executar.

Relacionado: [[feedback-concise-wos]], [[feedback-delete-weak-features]] (vale pra *feature fraca*,
não pra item de ledger), [[feedback-multiharness-essential]], [[project-verify-roadmap]].
