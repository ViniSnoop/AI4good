# tecnologias-na-educacao
> Disciplina Tecnologias na Educação — material e questionários da turma. Espelha `teaching/tecnologias-na-educacao/` no Drive pessoal.

Aulas 2026.2: quarta 18h30 e sexta 20h10.

## Calendário 2026.2 — os números fixos

Resolução CEPE/UFRPE nº 960, de 2025-11-20. **Início 10/08/2026 · término 12/12/2026 · provas
finais 14–18/12.** Não recontar isto: 18 quartas (12/08→09/12) e 18 sextas (14/08→11/12), **menos
28/10 (qua, Dia do Servidor Público Federal) e 20/11 (sex, Consciência Negra) = 17 + 17 = 34
encontros.**

Semanas quebradas, onde a presença cai: 07/09 seg · 12/10 seg · 02/11 seg · 08/12 ter (feriado
municipal do Recife, e a última quarta do semestre, 09/12, cai logo depois). Marcos da universidade
que competem por atenção: 27/10 Feira de Profissões · 19/11 Fórum de Internacionalização ·
03/12 Cantata Natalina.

## Material da aula

O deck de cada aula mora no Drive pessoal, em `material/aulas`
(`18L_A9hTVyIQGYUouJg0qS9R_3jwQ8oWX`), e é editado no lugar por
[`gslides`](../../../core/tools/slides/CONTEXT.md). **Contribuição em deck existente é aditiva**:
slides novos entram entre os antigos, os antigos são refinados no lugar, nada é deletado nem pulado.

| Aula | Deck | Gerador |
|------|------|---------|
| 02 — Design Thinking e Problemas na Educação | `1sPvsyaAMkCUf5Ok5O94V3xrB5kF77fYRMzEPgisZdKY` | [`add_aula02.py`](add_aula02.py) + [`aula02_conteudo.py`](aula02_conteudo.py) |

O quadro colaborativo da aula 02 é [`aula02-problemas.excalidraw`](aula02-problemas.excalidraw),
gerado por [`build_excalidraw.py`](build_excalidraw.py) — um frame por equipe mais um frame de
EXEMPLO preenchido. **A colaboração ao vivo do Excalidraw é efêmera e ancorada em quem abriu a
sala**: fechar a aba mata o trabalho da turma, então o arquivo tem de ser salvo antes do fim da aula.
O Miro persiste sozinho; este não.

Questionários são specs versionados, aplicados por [`gforms`](../../../core/tools/forms/CONTEXT.md):

```bash
core/tools/forms/gforms new --account personal \
  --folder 10tmlq_os3ltiS-UzdEMG8mj45ni5t45O academy/teaching/tecnologias-na-educacao/<spec>.json
core/tools/forms/gforms responses --account personal <form_id>
```

`10tmlq_os3ltiS-UzdEMG8mj45ni5t45O` é a pasta desta disciplina no Drive pessoal — cada turma tem a
sua, e o mesmo questionário vira um form separado em cada uma, porque a leitura das respostas é
por turma.

| Spec | `formId` | Link de resposta |
|------|----------|------------------|
| [`2026-2-rotina-e-setup.json`](2026-2-rotina-e-setup.json) | `1QyOkwdY9nNZPLLh179tSRyadgh6Cl-p9R1XM7qRTWkY` | [viewform](https://docs.google.com/forms/d/e/1FAIpQLScOoEjTI-l64rgUSBMQ198J_B9ssrai_tIVAcPAOYe-uWklww/viewform) |

<!-- routing:start -->
## Routing

| File | API | Description |
|------|-----|-------------|
| [`add_aula02.py`](add_aula02.py) | `build` | Aula 02: intercala slides novos no deck existente e refina dois slides. |
| [`aula02_conteudo.py`](aula02_conteudo.py) | — | Conteudo da aula 02 — o que entra no deck e onde. |
| [`build_excalidraw.py`](build_excalidraw.py) | `frame`, `rect`, `ellipse`, `text`, `bloco` | Gera o quadro da aula 02: um frame por equipe + um frame de exemplo preenchido. |
<!-- routing:end -->
