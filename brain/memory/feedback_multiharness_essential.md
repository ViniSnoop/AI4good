---
name: feedback-multiharness-essential
description: Multi-harness é ESSENCIAL para Lucas — otimizar a cópia, nunca excluir um harness; e nenhum hook morre sem dado
metadata:
  node_type: memory
  type: feedback
---

**Lucas, 2026-08-25**, quando ofereci cortar `.opencode/`, `.zcode/` e os shims (78 arquivos, ~1.500
LOC) por só usar Claude Code: *"ser multiharness é ESSENCIAL, podemos otimizar isso, estudar como é
feito para garantir o mínimo de retrabalho, de cópia e cola, mas nunca excluir."*

Na mesma rodada, sobre cortar hooks: *"por serem automáticos, hooks são a garantia de uma estratégia
de comportamento que é 'zero-token' e não quero cortar nenhum a menos que cheguemos a esta conclusão
a partir de dados e de uma análise mais coerente."*

**Why:** as duas respostas têm a mesma forma — ele recusa cortar uma **capacidade** para ganhar
arrumação. Multi-harness é a tese do workspace (nada que importa mora em diretório de vendor), e
hook automático é a aposta central (zero-token vence prompt). O desperdício que ele aceita atacar é
a **cópia** e a **prosa**, nunca a função.

**How to apply:**

- Multi-harness: a otimização é fonte única + geração, não deleção. As skills já são symlink para
  `core/skills/*.md`; `.claude/commands/*.md` é cópia renderizada porque links relativos mudam de
  profundidade. Se incomodar, a saída é parar de versionar o gerado — nunca apagar um harness.
- Hooks: proposta de corte só chega junto com placar. O item que produz o placar está em
  `ROADMAP.md` § Measurement, e ele já decretou: **nada é deletado antes que ele exista.**
- O alvo de redução que ele quer é `.md`, não código de enforcement.

Relacionado: [[feedback-provider-agnostic-naming]], [[feedback-delete-weak-features]] (sinal fraco
mata *feature*, não mata *capacidade que ele nomeou como essencial*), [[project-wos-zero-roadmap]].
