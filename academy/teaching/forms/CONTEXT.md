# forms
> Questionários aplicados às turmas: cada um escrito como spec versionado, aplicado por `gforms`.

O spec é o original; o Google fica com a cópia. Aplicar e ler as respostas:

```bash
core/tools/forms/gforms new       --account personal --folder <pasta_drive> <spec>.json
core/tools/forms/gforms responses --account personal <form_id>
```

Formato do spec e os dois grants de auth: [`core/tools/forms/`](../../../core/tools/forms/CONTEXT.md).
Pasta padrão no Drive pessoal — `teaching/` raiz, id `1zeq4m5eQM2na5dw6i5KWhY9VAEaINe2Y` — quando o
questionário serve a mais de uma disciplina.

| Spec | Turmas | `formId` |
|------|--------|----------|
| [`2026-2-rotina-e-setup.json`](2026-2-rotina-e-setup.json) | AI4Good + Tecnologias na Educação, 2026.2 | *(pendente: Forms API ainda desligada no projeto GCP)* |

**Anônimo por padrão, e isso é uma decisão.** A API não liga coleta de e-mail, então a resposta não
carrega identidade. É o preço de perguntar a um aluno se ele tem computador em casa: com nome, a
resposta vira a que não constrange. Em troca, nenhuma ação individual sai daqui — o que se decide
com esses dados é formato de aula, não atendimento a fulano.

<!-- routing:start -->
## Routing

<!-- routing:end -->
