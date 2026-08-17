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
mecânico. Já `skills` (14) não tem onde pôr uma: uma skill é markdown, não chama função nenhuma, e o
único desligamento real dela é o mirror recusar-se a publicá-la.

**Corrigido 2026-08-17, ao fiar o grupo: `capabilities` NÃO é o par de `skills`, e juntar os dois foi
erro.** O raciocínio acima vale para skill e só para skill. Uma capability é uma **CLI que este
workspace escreve**, então ela tem um momento próprio — o momento em que é invocada — e recusar ali é
observável mais forte do que qualquer publicador compartilhado ofereceria: a sonda de comportamento
passa a responder **por linha**, não uma resposta só para o grupo inteiro. A costura é
`core/tools/tool_law.py`, que carrega o pulo de `sys.path` e nada mais, e o guard é a primeira
instrução do `main`, antes do argparse — desligado vale inclusive para `--help`, e invocar sem
argumento vira sonda determinística. Sai com `EX_UNAVAILABLE` (69), deliberadamente não 1: um braço de
ablação precisa distinguir *desligado* de *rodou e falhou*, e toda ferramenta daqui já sai 1 em erro
real.

**A lição repete a do palpite que abriu esta AD, um nível acima: o grupo não decide nada.** Foi o
ponto de fiação que decidiu antes (`rtk-compaction` era o alvo de maior sinal do registro e o palpite
por grupo o descartaria) e é o ponto de fiação que decide agora. `rtk-compaction` continua provando
isso: é uma capability fiada num **hook**, cujo observável é o que ele reescreve e não um código de
saída, então a sonda das CLIs é escopada por caminho de fiação — nunca por grupo.

**Fica um achado aberto, e de propósito:** `codeburn` é binário npm instalado por fora, sem wrapper
nosso onde pôr guard. Ele **não** foi marcado `n/a` de passagem — esta AD fecha esse conjunto em
cinco, e admitir um sexto é decisão do Lucas, não faxina de quem estava fiando.

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

### AD-15 — What an always-loaded rule must prove to keep its place (2026-08-17)

Applies to text loaded in **every session**: `AGENTS.md`, `CONTEXT.md` heads, always-listed skills.
The question is **not length**. It is: *could this be a tool parameter, an enum, or a hook's error
message instead of prose?* What survives that question is prose that pays for itself. Three columns
per rule:

| column | when | what happens |
|---|---|---|
| **delete** | a **blocking, ratcheted** gate already applies it | leaves the prose; the hook is the rule |
| **move** | a check *could* apply it, but none does today | **stays in the prose** until a gate blocks |
| **keep** | judgment no check can hold | stays, and its reason stays with it |

**The discriminator between `delete` and `move` is blocking, not the existence of a detector** — it
is what separated two neighbouring `AGENTS.md` lines in this pass. `UPPERCASE.md = a type` left
because `checks/type-gate.py` stops the commit. `DONE WORK IS DELETED` stayed:
`entropy/entropy_ledger.py` owns the finished-work detector, but `type-gate.py` imports only its
wiki-link half, so the rule is **reported and never blocked** — deleting prose on the strength of a
report trades enforcement for nothing. An existing, unwired detector is the `move` column.

**Counterweights, because indiscriminate pruning is the one way this audit makes things worse** (the
`prompt-audit` keep-list): context is never cruft; cruft ≠ length; **no deletion is justified by
character count alone**. An audit that finds nothing changes nothing.

**Scope note:** this governs **always-loaded** text. Prose in a `SPECS.md`, read on demand, does not
pay that toll and is not under this rule.

**And this is not a cost item.** `AGENTS.md` is a single-digit fraction of turn 1
([`core/experiments/context-window.md`](experiments/context-window.md) — re-run it, never quote from
here): halving it saves nothing measurable, and selling that as savings repeats the error the cost
front spent three weeks undoing. The gain is enforcement, not tokens.

The frame came from a practitioner post (`[C]`, `core/refs/REFS.md`) claiming a **>80%** cut to
Claude Code's system prompt. **That number is self-reported with no published benchmark — not
citable.** What is testable, and is the whole value, is the frame: our own hooks already prove its
mechanical half — a hook's error message is a zero-token instruction arriving exactly when it applies.

### AD-16 — Doubt is not charged when asserting; it is charged when storing (2026-08-17)

The ask was a way to stop the agent being confidently wrong. **Asking for doubt in prose is the cheap
half and has already been tried**: this workspace is thick with *re-run it, never quote it*, and that
prevented neither the wrong number that steered a front for three weeks nor four asserted-then-
retracted explanations of the rtk hook. So the question is not how to request caution, it is **where
caution becomes a gate**. Three bands, and the first contradicts the premise this item was filed
under:

**1. Rule written, nothing checking — the cheap win, and it includes our own.** The
`core/experiments/` discipline (runnable `Method`, dated `Results`, `Limitations` never omitted) and
`core/refs/REFS.md`'s tier markers (`[A]`/`[B]`/`[P]`/`[V]`/`[C]`) are the two rules this workspace
cites as proof it knows how to doubt — and **neither is verified by anything**: no test asserts a
`## Method`, no entropy check reads `core/experiments/`. They held because a few careful sessions
followed them, not because anything charges for them. That is INDUCED wearing ENFORCED's costume,
the exact defect this front exists to catch. Both stores are small and closed: the obvious next Tier 0.

**2. Enforced by construction — the mechanism that already works, never named as one.** Write the
claim **where a parser already reads**, and it is audited on every commit for free. That is what
law-in-data does (`core/SCHEMA.md` is parsed, never restated in a checker), which makes *"a checker
that restates the law is the drift checkers exist to catch"* a doubt rule at heart. Proved in the act
of writing AD-15: one sentence of mine in § The one exception added two false types to the allowlist,
and `test_law_comes_from_schema` failed the commit — the test weighed no confidence, it read the
artifact.

**3. Not chargeable — stop trying.** The truth of a fresh technical claim, spoken in a turn. No gate
holds that. What the workspace does instead is **make the error cheap and its discovery fast**, which
is what the tests did above.

**Corollary this session paid for, sibling to *build the instrument, then check the instrument*: a
claim about our own enforcement layer is checked at the call site, never at the module.**
`entropy_ledger.py` owns the finished-work detector, but `type-gate.py` imports only `wiki_link_hits`
— anyone stopping at *"the module has the check"* would have deleted an `AGENTS.md` rule that nothing
in practice enforces. Owning a detector and charging for it are separate facts.

### AD-17 — Delegation is already mandatory where an executor reads the assignment; elsewhere it is advice (2026-08-17)

The ask: *"gostaria que ele delegasse mais ao sonnet pra economizar… seria ótimo se tivesse uma forma
mais garantida"*, with the **plan** as the proposed trigger — the moment work is cut into tasks is
the cheap point to decide who executes each one.

**That trigger is already built, in two places.** The Loop 1 plan table in
`core/flows/craft/craft.md` carries `tier` and `effort` columns **per task row**, and the same loop's
adversarial review charges that each row be executable by its assigned tier. `ROADMAP.md` carries a
`model` line per item. Making *the plan carry the assignment* is not what is missing.

**What is missing is an executor that reads it.** Inside `/craft` there is one: `runtimes.md` spawns
per tier, and the measurement shows the effect — of 37 spawns in
[`experiments/delegation.md`](experiments/delegation.md), **9 are the `craft-*` mirrors**, the only
structural ones; the rest are ad-hoc builtins. Outside `/craft` nothing reads the tag, so it is
advice — the same defect class as the first-line comment, where the rule existed and the number grew
anyway. **Hence the reading of the opus-heavy split: it measures how much work bypasses the flow that
routes**, not per-task indiscipline. The lever is routing more work through `/craft`, not building a
second router beside it.

**Delegating ≠ parallelising, and conflating them is what makes the proposal feel risky.** Offered a
shape with parallel workers, Lucas chose **no parallelism** (2026-08-17) — and refusing concurrent
workers in one checkout is not refusing a cheaper model per task. The common case, and the one that
moves the split, is **sequential** delegation.

**The chargeable half, and it is cheap:** `core/tools/wos/roundup` already prints the per-session
split at every close. Have the plan **declare its expected split** and roundup compare declared
against actual. It forces nobody to delegate; it makes deviation **visible and dated** instead of
invisible — which is what turned the other fronts. That is band 1 → 2 of AD-16, and the feedback loop
needs no new instrument.

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
