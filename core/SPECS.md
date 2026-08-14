# Core SPECS
> Architecture decisions and conventions for the Core agent library.

---

## Architecture Decisions

### AD-01 — AGENTS.md como entrypoint universal (2026-06-18)
`WORKSPACE.md` renomeado para `AGENTS.md`. Todos agentes (Copilot, Codex, OpenCode, Claude Code) leem `AGENTS.md` nativa ou via `@AGENTS.md` em `CLAUDE.md`. Elimina bifurcação de descoberta entre agentes.

### AD-02 — Frontmatter `description:` obrigatório em skills (2026-06-18)
Todas skills em `core/skills/*.md` devem ter frontmatter YAML com `name:` e `description:`. O `context_synchronizer.py` lê o campo `description:` (incluindo block scalars YAML `>` e `|`) para popular o routing table automaticamente. Template em `core/skills/_template.md`.

### AD-03 — auth/gauth.py como módulo auth compartilhado (2026-06-18, movido 2026-08-14)
Auth OAuth2 Google centralizado em `core/tools/auth/gauth.py`. Todos serviços Google (gmail, drive, calendar, slides futuro) importam deste módulo. Tokens separados por serviço em `~/.config/workspace-{service}/{alias}.token.json`. Credentials em `~/.config/workspace-gmail/credentials.json` (projeto GCP 1048141740528) servem todos os serviços.

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
Qualquer skill que acumule referências externas (papers, links, pesquisas, notas de leitura) deve manter uma pasta `refs/` no **mesmo nível do arquivo da skill**. Exemplo: `core/skills/prepare/refs/`. A pasta `refs/` é **excluída do sync** (o `sync-skills` copia apenas o `<name>.md` e gera o symlink; não toca em subpastas). Isso evita poluir os mirrors com arquivos auxiliares e mantém o source of truth limpo. Future agents must follow this convention when creating or updating skill-related reference folders.

### AD-07 — Agrupamento de sub-skills em pastas (2026-07-05)
Skills que formam um **suite** lógico (compartilham namespace, domínio ou prefixo comum) devem ser agrupadas em uma **pasta**, com uma **skill pai** atuando como roteador. Regras:

1. **Estrutura da pasta:** `core/skills/<suite>/` contém:
   - `SKILL.md` — skill pai (frontmatter YAML obrigatório, `name: <suite>`, atua como roteador/índice)
   - Sub-skills: `<slug>.md` — sem prefixo do suite (ex: `core/skills/foundry/canvas.md` em vez de `foundry-canvas.md`)
   - `refs/` — seguindo AD-06, se houver referências coletivas do suite

2. **Skill pai (SKILL.md):** deve listar as sub-skills em uma tabela com `When to load`, incluir o bloco `<!-- routing:start -->` com links para cada sub-arquivo, e nunca implementar lógica operacional (apenas roteamento/meta-info).

3. **Sub-skills:** cada uma tem frontmatter YAML completo (não herda do pai), e nome curto (sem prefixo).

4. **sync-skills** gera symlinks apenas para o `SKILL.md` do suite. Sub-skills são carregadas manualmente via skill pai (`Load subfiles relevant to the task`).

5. **Motivação:** evita poluir `core/skills/` com dezenas de arquivos flat; mantém skills relacionadas coesas; o padrão `foundry-*` foi o gatilho.

---

### AD-08 — Flows: posse, composição e ciclos (2026-07-23)
Extensão de AD-07 para a camada de **flows**. Contrato completo em [`SCHEMA.md`](SCHEMA.md) § *Composition and cycles*; aqui fica a decisão e o porquê.

1. **Posse define o lugar.** Flow que pertence a uma *dispatcher skill* mora em `core/flows/<skill>/`, e **o nome do arquivo é igual ao sufixo do comando**: `research scout` ⟺ `core/flows/research/scout.md`. Flow sem dono fica flat em `core/flows/`. O eixo é **independência de invocação**, não composição — `scout` compõe `deep`/`literature` e mesmo assim é sub-flow.

2. **Vocabulário: "flow" é o termo canônico.** "Loop" foi aposentado para o sentido de agentes conectados (virou buzzword). *Flow* é mais preciso: um loop vai do fim ao começo sem ramificação e com uma saída só; nossos procedimentos ramificam, escapam e compõem. Loop continua válido só para um repeat de verdade.

3. **Flows compõem** via `uses:`. Composto-vs-folha **não é um tipo** — é só se o flow invoca outros ou não. Não existe camada "orquestrador" no schema.

4. **Dois tipos de ciclo, só um é legal.** Ciclo **definicional** (A é construído a partir de B, B a partir de A) é **proibido** — nunca termina de expandir; o grafo `uses:` tem que ser um DAG, verificado estaticamente. Ciclo de **execução** (um flow volta a um passo anterior) é **permitido**, com teto de iterações + condição de saída — isso é iteração, o estado muda a cada passada. Um trace `A → B → C → A` não viola o DAG: a seta de volta é o loop interno de `A`, não uma aresta que `B`/`C` declaram.

5. **Nenhum flow é privilegiado.** O status de "reference implementation / oracle do validador" que `deepresearch` tinha foi **aposentado** — acoplava a evolução de um flow ao schema. O exemplar é `flows/_template.md`; realismo vem do `validate_flows` rodar sobre *todos* os flows, inclusive o template. (Lucas: *"a template should be a template. just that."*)

6. **Motivação:** o gatilho foi a assimetria `deepresearch` (flow) vs `/research scout` (sub-flow) — que se revelou apenas lexical, mas expôs a falta de regra de posse e de um modelo de composição.

### AD-09 — Fechamento de sessão: julgamento na skill, determinismo no script (2026-08-14)
Fecha as frentes 9.1 e 9.2 do [`ROADMAP.md`](../ROADMAP.md) raiz. Duas camadas, um ritual.

1. **A ferramenta leva o nome da skill.** [`core/tools/wos/roundup`](tools/wos/roundup) e
   `core/skills/roundup.md` são o mesmo ritual, um nível abaixo. Uma segunda palavra para a mesma
   coisa *é* a deriva — `close` foi escrito e rejeitado: soa terminal, e "roundup" significa
   fechamento **e** continuidade. Julgamento (o que apagar, para onde vai o conhecimento, o que a
   INBOX significa) fica na skill; tudo que tem uma resposta certa só fica no script, onde custa uma
   chamada em vez de prosa raciocinada nos turnos mais caros da sessão.

2. **Uma fase sem nada a dizer não contribui linha nenhuma.** Sem cabeçalho, sem "nada a fazer",
   sem próximo passo inventado para preencher a forma. Vale mais aqui que em qualquer lugar: é o
   turno mais caro da sessão *e* a última coisa lida antes de um `/clear`.

3. **A regra acima se aplica ao próprio hand-off.** Com o trabalho terminado e sem próxima ação,
   emitir um resume prompt **fabrica** uma. Então `/handoff` pode recusar — e recusar **apaga**
   `outputs/handoff.md`. É isso que transforma o caminho em sinal: **a existência do arquivo
   significa exatamente uma coisa, que há uma linha de trabalho aberta.** Deixar o bloco velho foi
   rejeitado como perigoso (a próxima janela retoma um fio fechado há sessões) e um stub "nada
   aberto" foi rejeitado por custar uma leitura para descobrir que não há o que ler.

4. **Sujeira no working tree tem dois donos possíveis e o script não distingue.** Ele imprime os
   caminhos e **pergunta de quem são**, em vez de afirmar. Afirmar foi o defeito: os arquivos que
   uma sessão paralela tinha staged leram como trabalho que *esta* sessão esqueceu de commitar, e a
   mensagem pediu um commit que teria varrido o merge de goals inacabado da outra para `main`.
   `--leave-dirty` responde "não é minha". É a única mensagem do script que nomeia duas ações,
   porque a pergunta é irredutivelmente binária.

5. **A promoção faz fast-forward sem checkout** (`git fetch . <src>:<dst>`), então nunca toca o
   working tree — é *isso*, e não uma afirmação geral sobre merges, que torna seguro promover por
   cima da sujeira alheia. Só um merge de verdade precisa mover o HEAD, e sob `--leave-dirty` um
   alvo divergente é reportado, nunca mesclado.

6. **O script recusa e diz por quê** (verify vermelho, alvo atrás do origin) em vez de contornar. O
   caso que ele não enxerga — um branch incoerente sozinho — entra por `--no-promote "<motivo>"`.
   *"O milestone não acabou"* **não** é motivo: trabalho verde, coerente e parcial pertence a
   `develop`.

7. **Nenhuma sessão gera sua sucessora.** Um agente abre sessão nova (`claude --bg` em background,
   `claude -p` headless one-shot, `claude agents --json` lista as ativas, `--session-id` /
   `--fork-session` / `-r` dão identidade explícita — verificado contra a CLI local 2.1.218), mas
   **nada disso move o terminal em que o Lucas digita**. Uma sucessora spawnada trabalharia o mesmo
   branch, sozinha, em paralelo com a sessão viva: divergência comprada ao preço de um `/handoff`.
   Prepara-se o artefato; a atenção o Lucas move sozinho.

Guardas: 20 testes em [`core/tools/test/wos/`](tools/test/wos/CONTEXT.md) — a ferramenta contra
workspaces descartáveis, as skills contra reinlinar o trabalho que o script assumiu.

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

---

## Conventions

- **Um comando cujo status é um gate nunca vai para dentro de um pipe** (achado 2026-08-13, custou um falso "main pushed"). Em `a | tail && b`, o status é o do `tail`, não o do `a` — então `git merge --ff-only x 2>&1 | tail -1 && git push` executa o push mesmo com o merge abortado, e a sessão reporta sucesso de algo que não aconteceu. Para sequências onde cada passo autoriza o próximo: `set -e` e sem pipes, ou capturar o status explicitamente. Filtrar saída é para inspeção, não para decisão.
- **Nome de arquivo: uma palavra só, e a palavra inteira** (preferência do Lucas, 2026-07-23). Truncação perde para a palavra completa: `architect` > `arch`, `literature` > `lit`. Nome que repete o namespace do pai é ruído — sob `research/`, `deepresearch.md` gagueja (`research deepresearch`), então virou `deep.md`. Nomes genéricos e óbvios devem ser **reservados** para o flow que realmente os merece: `explore` ficou com o loop de tentar ideias justamente para deixar `experiment` e `optimize` livres para flows futuros distintos.
- Nova skill (flat): copiar `core/skills/_template.md`, preencher frontmatter.
- Nova skill (suite): criar `core/skills/<suite>/SKILL.md` + sub-arquivos `<slug>.md`.
- Sub-skills relacionadas em pasta são sempre preferidas a skills flat com prefixo longo quando > 2 sub-skills.
- Novos serviços Google: importar `auth/gauth.py`, definir `SCOPES` e o nome do serviço, seguir o padrão de `files/drive_core.py` (seam read+write, account-agnostic) — e registrar o comando de recuperação em `gauth._REAUTH_CMD` no mesmo commit em que a CLI ganha `--reauth`; um teste verifica que todo comando dessa tabela aponta para uma ferramenta que existe.
- Tokens OAuth nunca commitados — ficam em `~/.config/workspace-*/`.
- **Pasta `refs/` em skills**: quando uma skill acumular referências externas, criar `core/skills/<name>/refs/` (ou `core/skills/<suite>/refs/`) e manter todos os arquivos de referência lá. Não criar `refs/` dentro de `.opencode/skills/` ou `.claude/skills/` — esses são mirrors gerados automaticamente.
- **Formato de arquivos em `refs/`**: notas de leitura, links rápidos e sumários informais vão em `*.md`. Referências estruturadas (papers com metadados, datasets com schema, configurações de ferramentas) vão em `*.yaml` com frontmatter ou schema claro. Preferir YAML para anything que uma skill vai parsear ou que precisa de schema.
