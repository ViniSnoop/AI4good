# Library shape
> How the agent library is arranged, and how a tool family and its auth attach.
> governs: core/skills/, core/flows/, core/tools/, core/agents/

### AD-01 — AGENTS.md como entrypoint universal (2026-06-18)
`WORKSPACE.md` renomeado para `AGENTS.md`. Todos agentes (Copilot, Codex, OpenCode, Claude Code)
leem `AGENTS.md` nativa ou via `@AGENTS.md` em `CLAUDE.md`. Elimina bifurcação de descoberta entre
agentes.

### AD-02 — Frontmatter `description:` obrigatório em skills (2026-06-18)
Todas skills em `core/skills/*.md` devem ter frontmatter YAML com `name:` e `description:`. O
`context_synchronizer.py` lê o campo `description:` (incluindo block scalars YAML `>` e `|`) para
popular o routing table automaticamente. Template em `core/skills/_template.md`.

### AD-03 — auth/gauth.py como módulo auth compartilhado (2026-06-18, movido 2026-08-14)
Auth OAuth2 Google centralizado em `core/tools/auth/gauth.py`. Todos serviços Google (gmail, drive,
calendar, slides futuro) importam deste módulo. Tokens separados por serviço em
`~/.config/workspace-{service}/{alias}.token.json`. Credentials em
`~/.config/workspace-gmail/credentials.json` (projeto GCP 1048141740528) servem todos os serviços.

### AD-04 — Slides: editar Google Slides direto, sem formato local (2026-08-14, revoga Slidev)
**Revoga a decisão de 2026-06-18 por Slidev (Markdown + Vue) e o porte Google Slides → Slidev.**
O argumento original era que a fonte de verdade não era editável por agente, então valia exportar
para um formato de texto versionável. Verificado nesta data que **é editável**: `presentations.create`
+ `batchUpdate` criam, escrevem e reposicionam elementos remotamente, e movimento se autora como
sequência de slides gerada (`duplicateObject` + `updatePageElementTransform`) — que sobrevive ao
export para PDF, o requisito que o Lucas nomeou. Com isso, o porte só produzia uma segunda cópia
para manter em sincronia. Slidev e o pipeline de porte foram **deletados**, não rebaixados.
Consequência: o material de aula continua onde os alunos veem, e o WOS o edita lá.
Ferramenta: `core/tools/slides/gslides`. Fatos da API: `core/tools/slides/SPECS.md`.

### AD-06 — Convenção de pastas `refs/` em skills (2026-07-05)
Qualquer skill que acumule referências externas (papers, links, pesquisas, notas de leitura) deve
manter uma pasta `refs/` no **mesmo nível do arquivo da skill**. Exemplo:
`core/skills/prepare/refs/`. A pasta `refs/` é **excluída do sync** (o `sync-skills` copia apenas o
`<name>.md` e gera o symlink; não toca em subpastas). Isso evita poluir os mirrors com arquivos
auxiliares e mantém o source of truth limpo. Future agents must follow this convention when creating
or updating skill-related reference folders.

### AD-07 — Agrupamento de sub-skills em pastas (2026-07-05)
Skills que formam um **suite** lógico (compartilham namespace, domínio ou prefixo comum) devem ser
agrupadas em uma **pasta**, com uma **skill pai** atuando como roteador. Regras:

1. **Estrutura da pasta:** `core/skills/<suite>/` contém:
   - `SKILL.md` — skill pai (frontmatter YAML obrigatório, `name: <suite>`, atua como roteador/índice)
   - Sub-skills: `<slug>.md` — sem prefixo do suite (ex: `core/skills/foundry/canvas.md` em vez de `foundry-canvas.md`)
   - `refs/` — seguindo AD-06, se houver referências coletivas do suite

2. **Skill pai (SKILL.md):** deve listar as sub-skills em uma tabela com `When to load`, incluir o
   bloco `<!-- routing:start -->` com links para cada sub-arquivo, e nunca implementar lógica
   operacional (apenas roteamento/meta-info).

3. **Sub-skills:** cada uma tem frontmatter YAML completo (não herda do pai), e nome curto (sem prefixo).

4. **sync-skills** gera symlinks apenas para o `SKILL.md` do suite. Sub-skills são carregadas
   manualmente via skill pai (`Load subfiles relevant to the task`).

5. **Motivação:** evita poluir `core/skills/` com dezenas de arquivos flat; mantém skills
   relacionadas coesas; o padrão `foundry-*` foi o gatilho.

---

### AD-08 — Flows: posse, composição e ciclos (2026-07-23)
Extensão de AD-07 para a camada de **flows**. Contrato completo em [`SCHEMA.md`](SCHEMA.md) §
*Composition and cycles*; aqui fica a decisão e o porquê.

1. **Posse define o lugar.** Flow que pertence a uma *dispatcher skill* mora em
   `core/flows/<skill>/`, e **o nome do arquivo é igual ao sufixo do comando**: `research scout` ⟺
   `core/flows/research/scout.md`. Flow sem dono fica flat em `core/flows/`. O eixo é
   **independência de invocação**, não composição — `scout` compõe `deep`/`literature` e mesmo assim
   é sub-flow.

2. **Vocabulário: "flow" é o termo canônico.** "Loop" foi aposentado para o sentido de agentes
   conectados (virou buzzword). *Flow* é mais preciso: um loop vai do fim ao começo sem ramificação
   e com uma saída só; nossos procedimentos ramificam, escapam e compõem. Loop continua válido só
   para um repeat de verdade.

3. **Flows compõem** via `uses:`. Composto-vs-folha **não é um tipo** — é só se o flow invoca outros
   ou não. Não existe camada "orquestrador" no schema.

4. **Dois tipos de ciclo, só um é legal.** Ciclo **definicional** (A é construído a partir de B, B a
   partir de A) é **proibido** — nunca termina de expandir; o grafo `uses:` tem que ser um DAG,
   verificado estaticamente. Ciclo de **execução** (um flow volta a um passo anterior) é
   **permitido**, com teto de iterações + condição de saída — isso é iteração, o estado muda a cada
   passada. Um trace `A → B → C → A` não viola o DAG: a seta de volta é o loop interno de `A`, não
   uma aresta que `B`/`C` declaram.

5. **Nenhum flow é privilegiado.** O status de "reference implementation / oracle do validador" que
   `deepresearch` tinha foi **aposentado** — acoplava a evolução de um flow ao schema. O exemplar é
   `flows/_template.md`; realismo vem do `validate_flows` rodar sobre *todos* os flows, inclusive o
   template. (Lucas: *"a template should be a template. just that."*)

6. **Motivação:** o gatilho foi a assimetria `deepresearch` (flow) vs `/research scout` (sub-flow) —
   que se revelou apenas lexical, mas expôs a falta de regra de posse e de um modelo de composição.

### AD-10 — `core/tools/` classifica por capacidade; o provedor é a folha (2026-08-14)
Regra: **diretório = o que a ferramenta faz, arquivo = quem a fornece** (`mail/gmail`,
`calendar/gcalendar`, `files/gdrive`, `slides/gslides`, `auth/gauth.py`). É a regra
provider-agnostic da biblioteca ([`CONTEXT.md`](CONTEXT.md) linha 4) aplicada um nível acima: trocar
de provedor muda uma folha, nunca uma família. `google/` era a única pasta classificando por
fabricante, e era por isso que nenhum rename dela parecia certo — o problema não era o nome, era o
eixo. Duas refinações que impedem isso de virar um gol contra de fanout: **criar a família só quando
a ferramenta chega nela** (sem `sheets/` vazio esperando), e **`CONTEXT.md` só a partir do segundo
arquivo** — o gerador de routing dobra um diretório sub-`WARN_FILES` no pai a menos que ele se
declare, então uma família de uma ferramenta custa um hop e *zero* linhas de tabela.
Custo declarado: foi a **segunda** vez que todo caminho de `core/tools/` mudou (a primeira foi o
split de 2026-07-31). Uma terceira não é de graça — está escrito no
[`tools/CONTEXT.md`](tools/CONTEXT.md).

### AD-11 — Uma leitura usa o consentimento mais forte que a conta já deu (2026-08-14)
Quando um alias tem token de escrita, o caminho de leitura usa **ele**, não pede um segundo. O
consentimento de edição já contém o de leitura, então exigir outra ida ao browser não compra
segurança nenhuma — só cria dois tokens que morrem de forma independente (foi exatamente o que
aconteceu: o token `slides` estava morto enquanto o `slides-write` recém-consentido estava vivo).
Contas que só receberam a concessão de leitura seguem intactas. Vale para qualquer serviço novo com
split read/write — `notes/notion` deve nascer assim.

### AD-12 — Provedor sem OAuth: o auth mora ao lado da ferramenta (2026-08-14)
`notes/notion` autentica por **segredo de integração interna**, não por OAuth2, então não importa
`auth/gauth.py` — e o módulo que guarda o segredo (`notes/notion_auth.py`) fica **na família**, não
em `auth/`. Não é exceção à AD-10: é a regra de locality do [`tools/CONTEXT.md`](tools/CONTEXT.md)
("módulo importado por exatamente uma família mora ao lado da ferramenta") batendo com a de auth.
`gauth` está em `auth/` porque quatro famílias o importam; este muda de lugar no dia em que uma
segunda família precisar de token do Notion, não antes.

Duas consequências que a CLI carrega e nenhum tool Google tem:

1. **A divisão é a mesma do Google; o que muda é qual metade é de quem.** A regra vale para
   qualquer provedor (está no [`tools/CONTEXT.md`](tools/CONTEXT.md), não aqui): **o Lucas só faz
   o que não tem forma de comando** — clique dentro da UI do provedor, tela de consentimento,
   segredo cunhado dentro da conta dele. No Google o agente dispara o consentimento e ele escolhe
   a conta; no Notion ele cunha o segredo e conecta a página, cola o valor na conversa, e o agente
   guarda. Entregar a ele o comando de guardar é a tarefa que o agente podia ter absorvido
   (correção dele, 2026-08-14: *"run it for me and ask me to do only what only I myself can do"*).
   O segredo entra por **stdin** via pipe de builtin, nunca por argumento — argv é legível por
   qualquer processo do usuário e sobrevive no histórico do shell. Um teste guarda a divisão:
   nenhum caminho de CLI pode aparecer acima da linha `AGENT:`.
2. **404 é falha de compartilhamento até prova em contrário.** O Notion responde o mesmo código para
   "não conectado a esta integração" e "id não existe", e o primeiro é muito mais comum: conteúdo é
   *invisível* para a integração, não proibido. A mensagem diz isso nessa ordem — começar por "id
   errado" manda o Lucas para o lado errado.

Sobre AD-11 (leitura usa o consentimento mais forte): no Notion não existe split read/write de
token — as capacidades são escolhidas na criação da integração, então um segredo com *Read +
Update + Insert* já é a concessão inteira.

---
