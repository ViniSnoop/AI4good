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

### AD-13 — Subagente não passa pelo context gate; quem o invoca é que entrega o contexto (2026-08-15)

`CONTEXT.md` carrega **roteamento**; restrição mora em `SPECS.md` (SCHEMA.md § Boundaries), e o gate que protege
contrato — `spec-read-gate.py` — continua disparando para todo mundo. Então um worker que recebeu
**um caminho explícito** nunca precisou da cadeia: obrigá-lo a lê-la cobra ~2k tok sobre um início de
17,8k, relidos a cada turno. Regra em `hook_input.is_subagent`, chaveada em `agent_id` — o único
campo que distingue worker de thread principal (`agent_type` também vem no principal em sessões
`--agent`).

A isenção **já existia por acidente e era arbitrária**: o worker herdava o `session_id` do pai e com
ele o seen-set, logo ficava sem gate só nas subárvores que o pai por acaso visitou, e pagava a cadeia
inteira em todas as outras.

O dever migrou para o orquestrador, e um hook o cumpre em vez de virar disciplina:
`read/agent-context.py` lê os caminhos citados no prompt do `Agent` e entrega ao worker a linha `>`
de cada subárvore. **Induz, nunca bloqueia.** A divisão em dois eventos é medida, não suposta —
`PreToolUse:Agent` vê o prompt mas não tem `agent_id` e seu `additionalContext` volta para o *pai*;
`SubagentStart` injeta no worker mas não vê o prompt. `prompt_id` é idêntico nos dois e é a chave de
junção, o que torna o briefing **por turno**: vários workers de um mesmo turno recebem a união dos
caminhos citados. Amplo demais, nunca trocado, e insolúvel de outro jeito — o único id do worker
nasce depois que o prompt já passou.

Medição e sonda: [`core/experiments/subagent-context-chain.md`](experiments/subagent-context-chain.md).

### AD-14 — Capacidade que não pode ser desligada é achado, não recurso (2026-08-16)

O bench de ablação rodou uma vez e não produziu **nenhum** sinal, por um motivo só: não havia como
desligar uma funcionalidade de cada vez. Enquanto isso for verdade, nada neste workspace é
mensurável — e nenhuma regra daqui jamais foi medida.

Então o registro é o **instrumento**, não um sistema de configuração. `core/features.txt` declara
cada capacidade (grupo, força de enforcement, escopo, e o que ela te dá); `core/profile.txt` guarda
as respostas desta máquina; `core/hooks/feature_law.py` é o terceiro módulo de lei — `file_law.py`
diz o que um arquivo **é**, `schema_law.py` o que um nome **pode ser**, este diz o que está
**ligado**. O registro **nomeia** qual hook/skill/tool está ligado e nunca reescreve a regra que
aquele hook aplica; checker que reescreve a lei é justamente a deriva que os checkers existem para
pegar.

Três decisões que carregam o peso:

- **A coluna `wired` é honesta ou não serve.** Ela nomeia o arquivo que chama `is_enabled()`, e um
  `-` é contado por `core/tools/wos/features --findings`. Linha que se diz ligada sem estar faria a
  ablação relatar "sem efeito" para algo que nunca foi desligado — o mesmo fracasso silencioso que
  custou o sinal da primeira rodada. Quem cobra isso é a sonda de comportamento em
  `test_features.py`, descrita adiante: a linha só é honesta se desligá-la mudar o observável.
- **`is_enabled` falha ABERTO em slug desconhecido.** Um gate nunca pode parar de enforcar porque
  alguém errou uma linha de dados. Isso é o que torna seguro ligar qualquer gate ao registro: na
  pior hipótese ele se comporta como antes de o módulo existir.
- **`WOS_FEATURES_OFF` só subtrai.** Não existe `WOS_FEATURES_ON`, e a assimetria é de propósito:
  uma rodada de ablação responde *quanto custa este workspace sem X*. Ligar algo é decisão
  versionada no profile, não variável de ambiente que some com o shell.

**A ablação roda FORA do WOS, e isso muda o que "desligável" quer dizer** (Lucas, 2026-08-17). Um
sistema não roda o experimento sobre si mesmo. O harness monta **variantes** de um checkout — uma
funcionalidade a menos em cada — e roda a mesma suíte de tarefas contra todas. As variantes saem do
repositório público (`code/wos/`), o que torna o repo público **pré-requisito duro** da ablação e
obriga a suíte de tarefas a ser sintética, já que o scaffold público leva `brain/` como estrutura
vazia de propósito.

Daí saem **duas rotas de desligamento**, e a coluna `wired` só conhece a primeira:

| rota | como se desliga | quem usa |
|---|---|---|
| chave em processo | `is_enabled()` no arquivo que aplica a regra | `WOS_FEATURES_OFF`, o profile, todo gate |
| variante de clone | a variante é montada sem aquilo | só o harness de ablação |

**Toda capacidade é ablatável; nem toda tem chave em processo** (Lucas: *"ALL features of the WOS
should be toggleable"*). Cinco linhas só têm a segunda rota — `python-runtime` (o `.venv` em que
todo hook executa: desligar não ablaciona a funcionalidade, ablaciona o instrumento, e nenhum gate
sobra para responder), `tool-shebangs` (ergonomia de invocação, sem observável para medir), e
`latex` / `google-auth` / `apptime-verify` (desligar é desinstalar um toolchain de trabalho que o
usuário faria de qualquer jeito). Elas levam **`n/a` na coluna `wired`, com o motivo na própria
linha**, e `n/a` quer dizer *"sem chave em processo; ablacionada por variante de clone"* — nunca
*"isenta"*. `--findings` para de contá-las, e por isso o alvo do contador é **zero**, honestamente.

**O palpite que abriu isto estava errado, e errado da forma cara.** A suspeita era que dois grupos
inteiros — os "fatos de instalação" e `capabilities` — não tinham significado de desligado.
`declared-deps` e `verify-suite` são avisos e gates comuns, plenamente desligáveis. E
`rtk-compaction` — que o palpite jogou no balde de "capability não custa nada até ser chamada" — é
**o alvo mais valioso da lista inteira**: tem ponto de fiação pronto em
`core/hooks/compact/bash-compact-rewrite.py`, roda em todo Bash, e `core/tools/deps.txt` já
precifica sua ausência em *"the session just costs 60-90% more"*. Uma capability que reescreve toda
saída de ferramenta antes do contexto não é passiva.

**A lição: o grupo não decide se algo é mensurável, o ponto de fiação decide.** Classificar por
grupo teria descartado a linha de maior sinal do registro junto com quatro que de fato só têm a
segunda rota.

**A coluna `wired` guarda UM caminho, e algumas capacidades moram em vários** (achado 2026-08-17, ao
ligar `facade-discipline`). A disciplina de fachada é dois arquivos — o bloqueio de import em
`facade/check-facade-imports.py` e o gate de leitura em `facade/facade-gate.py` — e `context-chain`
é três. Guardar só o arquivo nomeado deixaria a funcionalidade **meio desligada**, e uma ablação
mediria o custo de algo que ninguém removeu inteiro: o mesmo fracasso silencioso que a coluna
existe para evitar, um nível abaixo. Regra: **guarde todos os arquivos, nomeie o primário**, e cada
arquivo não-nomeado cita no comentário quem é o primário. A sonda de comportamento não fecha esse
buraco sozinha: ela prova que desligar a linha muda **alguma** coisa, não que mudou tudo que devia.
Cobertura parcial continua sendo trabalho de quem fia, não do teste.

**As 57 linhas não são 57 tarefas, e o teste de honestidade é o que decide isso.** Os grupos
`hooks`, `context-tree` e `brain` têm um arquivo de enforcement cada — uma chamada por linha,
mecânico. Mas `skills` (14) e `capabilities` (11) não têm onde pôr uma: uma skill é markdown e não
chama função nenhuma, e o único desligamento real dela é o mirror recusar-se a publicá-la.

**Decidido 2026-08-17: o teste de honestidade faz UMA pergunta — desligar isto mudaria alguma
coisa? — e a responde do jeito mais forte que cada linha permite.** A versão antiga procurava o slug
literal dentro do arquivo citado, o que **força um ponto de chamada por linha** e não tinha onde
aterrissar para 25 delas.

- **Grupo com costura invocável → sonda de comportamento.** Roda os dois lados, normal e sob
  `WOS_FEATURES_OFF=<slug>`, e falha se o observável não mudar. É isso que **torna legal um ponto de
  fiação compartilhado**: o mirror publica ou não publica a skill, e catorze linhas passam a ter
  prova sem catorze chamadas. É também estritamente mais forte que o grep, que passa numa guarda em
  ramo inalcançável.
- **Linha com ponto de chamada próprio → o arquivo citado nomeia o slug e consulta a lei.** Continua
  valendo porque ali é verdade: um arquivo, uma chamada, o nome está lá.

Os dois mecanismos não são duas listas em sincronia — são a mesma pergunta com evidências
diferentes, e a escolha entre eles é lida da própria linha, não mantida à mão. Inventar 25 pontos de
chamada para uniformizar teria comprado um teste pior. Verificado ao escrever a sonda: com o filtro
do mirror removido, ela falha em `calendar` (*"is still published with `WOS_FEATURES_OFF=calendar`"*)
— um teste que não se viu falhar não é um teste.

O join é o que impede um terceiro vocabulário: `SETUP.md` declara um slug por passo de instalação
(coluna `install`), `core/tools/deps.txt` um slug por dependência (coluna `slug`). Treze cada, quatro
compartilhados — três arquivos, um vocabulário só, cobrado por teste.

### AD-15 — O que uma regra sempre-carregada precisa provar para ficar (2026-08-17)

Vale para todo texto que entra em toda sessão: `AGENTS.md`, cabeça de `CONTEXT.md`, skill sempre
listada. A pergunta **não é tamanho**. É: *isto poderia ser um parâmetro de ferramenta, um enum, ou a
mensagem de erro de um hook, em vez de prosa?* O que sobrevive a essa pergunta é prosa que se paga.
Três colunas por regra:

| coluna | quando | o que acontece |
|---|---|---|
| **delete** | um gate **bloqueante e catracado** já aplica a regra | sai da prosa; o hook é a regra |
| **move** | um check *poderia* aplicá-la, mas nenhum aplica hoje | **fica na prosa** até o gate bloquear |
| **keep** | julgamento que check nenhum segura | fica, e a razão fica junto |

**O discriminador entre `delete` e `move` é bloqueio, não existência de detector** — foi o que separou
duas linhas vizinhas de `AGENTS.md` nesta passada. `UPPERCASE.md = tipo` saiu porque
`checks/type-gate.py` barra o commit. `DONE WORK IS DELETED` ficou: `entropy/entropy_ledger.py` tem o
detector de prosa-de-obra-feita, mas `type-gate.py` importa dele só a metade de wiki-links, então a
regra é **relatada e nunca barrada** — apagar a prosa com base num relatório é trocar enforcement por
nada. Um detector existente e desligado é a coluna `move`, não a `delete`.

**Contrapesos, porque a poda indiscriminada é o único jeito de a auditoria piorar as coisas**
(keep-list do método `prompt-audit`): contexto nunca é cruft; cruft ≠ comprimento; **nenhuma remoção
se justifica por contagem de caracteres sozinha**. Auditoria que não acha nada não muda nada.

**Nota de escopo:** isto vale para texto **sempre carregado**. Prosa em `SPECS.md`, lida sob demanda,
não paga esse pedágio e não está sob esta regra.

**E isto não é item de custo.** `AGENTS.md` é uma fração de um dígito do turno 1
([`core/experiments/context-window.md`](experiments/context-window.md) — releia, não cite daqui):
cortá-lo pela metade não economiza nada mensurável, e vender isso como economia repete o erro que a
frente de custo levou três semanas para desfazer. O ganho é enforcement, não tokens.

A moldura veio de um post de prática (`[C]`, `core/refs/REFS.md`) que afirma corte de **>80%** do
system prompt do Claude Code. **O número é auto-relatado, sem benchmark publicado — não é citável.** O
que é testável, e é todo o valor, é a moldura: nossos próprios hooks já provam a metade mecânica dela
— a mensagem de erro de um hook é uma instrução de custo zero que chega exatamente quando se aplica.

### AD-16 — Dúvida não se cobra na hora de afirmar; cobra-se na hora de guardar (2026-08-17)

O pedido era um jeito de impedir que a IA seja confiante e errada. **Pedir dúvida em prosa é a metade
barata e já foi tentada**: o workspace é grosso de *re-execute, nunca cite* e isso não impediu nem o
número errado que guiou uma frente por três semanas nem quatro explicações do hook rtk afirmadas e
retiradas. Então a pergunta não é como pedir cautela, é **onde ela vira gate**. Três faixas, e a
primeira contradiz a premissa de onde este item nasceu:

**1. Regra escrita, checker nenhum — é aqui que está o ganho barato, e inclui a nossa própria.** A
disciplina do `core/experiments/` (`Method` executável, `Results` datado, `Limitations` nunca
omitido) e os marcadores de tier do `core/refs/REFS.md` (`[A]`/`[B]`/`[P]`/`[V]`/`[C]`) são as duas
regras que este workspace cita como prova de que sabe duvidar — e **nenhuma das duas é verificada por
nada**: nenhum teste exige `## Method`, nenhum check de entropia varre `core/experiments/`. Elas
funcionaram porque poucas sessões cuidadosas as seguiram, não porque algo cobra. É INDUCED se
passando por ENFORCED, que é exatamente o defeito que esta frente existe para pegar. Ambas são
fechadas, pequenas e mecanicamente checáveis: é a próxima Tier 0 óbvia.

**2. Enforced por construção — o mecanismo que já funciona e ninguém tinha nomeado assim.** Escreva a
afirmação **onde algum parser já lê**, e ela passa a ser auditada a cada commit de graça. É o que a
lei-em-dado faz (`core/SCHEMA.md` é parseado, nunca reescrito num checker), e por isso *"checker que
reescreve a lei é a deriva que os checkers pegam"* é, no fundo, uma regra de dúvida. Provado em
flagrante ao escrever a AD-15: uma frase minha em § The one exception adicionou dois tipos falsos ao
allowlist, e `test_law_comes_from_schema` derrubou o commit — o teste não avaliou minha confiança,
avaliou o artefato.

**3. Não é cobrável — pare de tentar.** A verdade de uma afirmação técnica nova, dita num turno. Gate
nenhum segura isso. O que o workspace faz em vez disso é **baratear o erro e acelerar a descoberta**,
que é o que os testes fizeram acima.

**Corolário que esta sessão pagou, irmão do *build the instrument, then check the instrument*:
afirmação sobre a nossa própria camada de enforcement se checa no ponto de chamada, nunca no módulo.**
`entropy_ledger.py` tem o detector de prosa-de-obra-feita, mas `type-gate.py` importa dele só
`wiki_link_hits` — quem parasse em *"o módulo tem o check"* apagaria de `AGENTS.md` uma regra que na
prática não é cobrada por ninguém. Ter o detector e cobrar o detector são fatos diferentes.

## Conventions

- **Um arquivo não-rastreado não apenas fica sem backup — ele opta por sair de todo check que o
  workspace tem** (achado 2026-08-15). `code/ROADMAP-spec-drive.md` caía na regra `code/*` do
  `.gitignore`, então cada edição ficou presa numa máquina só e ninguém viu que o rollout tinha
  parado de andar. No instante em que entrou no corpus, falhou `verify-fast` em três tokens
  retirados no rename `loops`→`flows` de julho: a varredura da época passou por todos os outros
  arquivos e não podia enxergar este. Por um mês ele seguiu mandando o leitor para um arquivo de
  flow que já tinha outro nome. **Um arquivo invisível continua dando instruções enquanto apodrece**
  — é exatamente isso que a disciplina de allowlist no `.gitignore` compra.
- **Sequencie a proibição ANTES do rename, nunca depois** (achado 2026-08-16, e a ordem inversa
  custaria um sweep de 50 arquivos). Proibir citar número de item e renomear `Frente`→`Front`
  pareciam a mesma varredura. Não eram: **91 das 160 menções eram citações que a proibição deleta
  de saída**, então fazer a proibição primeiro reduziu o rename a três arquivos. Na ordem inversa,
  91 ponteiros teriam sido cuidadosamente movidos e depois apagados. Corolário do mesmo achado:
  **uma regra que só um leitor cuidadoso aplica é uma regra que o corpus ultrapassa** — em quinze
  dias de prosa, o corpus acumulou 91 citações numeradas, duas delas dentro dos próprios checks
  cujo trabalho é achar ponteiro morto, e duas apontando para frentes que nunca existiram.
- **Um achado com mais de uma semana é hipótese, não fato — re-rode antes de gastar uma decisão
  nele** (achado 2026-08-14, e o custo foi quase uma frente inteira de trabalho inventado). Uma
  auditoria de integridade git listou quatro problemas; re-checados quinze dias depois, **três dos
  quatro tinham se resolvido sozinhos** — o `Makefile` estava não-rastreado em *zero* repos (os três
  citados haviam ido para `.Trash-1000`), a árvore duplicada do `shortvid` foi junto, e dos dois
  repos ditos RED um passa 225 testes e o outro virou spec com a implementação deletada. O quarto o
  Lucas deletou na mesma sessão. **Os achados de uma auditoria apodrecem mais rápido que o ledger que
  os guarda**, então o ledger guarda o comando que os produziu, nunca a lista.
- **`make entropy` é o que verifica um rename; `git grep` só encontra por onde começar** (achado
  2026-08-17, e foi assim que um rename foi declarado pronto **duas vezes**). `git grep` da raiz lê
  *este* repo apenas — cada projeto em `code/` é um repo git separado e é invisível para ele. O
  dashboard de entropia caminha nos repos aninhados; o `git grep` não. Corolário que generaliza:
  **um rename incompleto é indistinguível de entropia nas folhas, e só é consertável no gerador.**
- **Um check que prova que algo *aconteceu* vence um que prova que não deu erro** (achado 2026-08-14,
  sobre seis bugs drenados de uma vez). **Todos os seis eram silenciosos**: saíam com status 0,
  bloqueavam sem mensagem, ou escreviam um arquivo que ninguém relia — o caminho de declaração JS não
  emitia nada *havia anos*, `pre-edit.py` recusava edições sem dizer por quê, o stubgen escrevia
  dentro de um espelho do próprio caminho. Um bug que se anuncia é consertado no dia em que nasce, então
  **o que sobrevive num tree é selecionado por ser mudo**, e o único detector era o olho do Lucas. Ao
  caçar o próximo, pergunte *"o que isto produz, e está lá?"* antes de ler o código atrás de uma
  exceção — e prefira o check transversal ao check de um arquivo só (nenhum stub gerado dentro de um
  caminho duplicado; nenhum gate que bloqueia sem escrever em stderr).
- **Um comando cujo status é um gate nunca vai para dentro de um pipe** (achado 2026-08-13, custou um falso "main pushed"). Em `a | tail && b`, o status é o do `tail`, não o do `a` — então `git merge --ff-only x 2>&1 | tail -1 && git push` executa o push mesmo com o merge abortado, e a sessão reporta sucesso de algo que não aconteceu. Para sequências onde cada passo autoriza o próximo: `set -e` e sem pipes, ou capturar o status explicitamente. Filtrar saída é para inspeção, não para decisão.
- **Seção de `.md` se cita pelo nome, nunca pelo número** (achado 2026-08-15, custou 8 ponteiros
  quebrados em 6 arquivos). Um número é um ponteiro que envelhece na primeira seção inserida, e
  envelhece *em silêncio*: `[SETUP.md §6]` continuava resolvendo para um arquivo que existe, só que
  para a seção errada — nenhum check de integridade de link pega isso. O root `SETUP.md` tinha
  chegado a ter `§10` antes de `§9`. Referência boa: `[SETUP.md](SETUP.md) § Web search` — o texto
  âncora sobrevive a qualquer reordenação, e se a seção for renomeada a busca falha em vez de
  apontar para o lugar errado.
- **Nome de arquivo: uma palavra só, e a palavra inteira** (preferência do Lucas, 2026-07-23). Truncação perde para a palavra completa: `architect` > `arch`, `literature` > `lit`. Nome que repete o namespace do pai é ruído — sob `research/`, `deepresearch.md` gagueja (`research deepresearch`), então virou `deep.md`. Nomes genéricos e óbvios devem ser **reservados** para o flow que realmente os merece: `explore` ficou com o loop de tentar ideias justamente para deixar `experiment` e `optimize` livres para flows futuros distintos.
- Nova skill (flat): copiar `core/skills/_template.md`, preencher frontmatter.
- Nova skill (suite): criar `core/skills/<suite>/SKILL.md` + sub-arquivos `<slug>.md`.
- Sub-skills relacionadas em pasta são sempre preferidas a skills flat com prefixo longo quando > 2 sub-skills.
- Novos serviços Google: importar `auth/gauth.py`, definir `SCOPES` e o nome do serviço, seguir o padrão de `files/drive_core.py` (seam read+write, account-agnostic) — e registrar o comando de recuperação em `gauth._REAUTH_CMD` no mesmo commit em que a CLI ganha `--reauth`; um teste verifica que todo comando dessa tabela aponta para uma ferramenta que existe.
- Novo provedor **sem** OAuth: seguir `notes/notion` — segredo guardado ao lado da ferramenta, toda
  falha imprimindo a instrução completa, segredo entrando por stdin (AD-12).
- Tokens OAuth nunca commitados — ficam em `~/.config/workspace-*/`.
- **Pasta `refs/` em skills**: quando uma skill acumular referências externas, criar `core/skills/<name>/refs/` (ou `core/skills/<suite>/refs/`) e manter todos os arquivos de referência lá. Não criar `refs/` dentro de `.opencode/skills/` ou `.claude/skills/` — esses são mirrors gerados automaticamente.
- **Formato de arquivos em `refs/`**: notas de leitura, links rápidos e sumários informais vão em `*.md`. Referências estruturadas (papers com metadados, datasets com schema, configurações de ferramentas) vão em `*.yaml` com frontmatter ou schema claro. Preferir YAML para anything que uma skill vai parsear ou que precisa de schema.
