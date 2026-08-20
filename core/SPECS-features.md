# The feature registry
> What counts as a feature, what its columns mean, and what may not be undeclared.
> governs: core/features.txt, core/profile.txt
> enforced-by: core/hooks/feature_law.py, core/tools/wos/features

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
should be toggleable"*). `n/a` na coluna `wired` quer dizer *"sem chave em processo; ablacionada por
variante de clone"* — nunca *"isenta"* — e `--findings` para de contá-las, o que é o que torna o
alvo **zero** honesto.

**A coluna `n/a` está VAZIA desde 2026-08-17, e o alvo zero deixou de ter exceções.** As cinco
linhas que a carregavam não eram casos difíceis; eram **erros de categoria** que a palavra
*feature* não tinha definição para pegar (agora tem: [`SCHEMA.md`](SCHEMA.md) § Termos com um
significado). Três — `python-runtime`, `tool-shebangs`, `apptime-verify` — são estado de máquina de
terceiros que este workspace **não autora**: viraram passo de `SETUP.md` (marcados `> substrate:
yes`) mais linha de `core/tools/deps.txt`, que é a regra do codeburn aplicada sem alteração. As
outras duas estavam **mal arquivadas**, e o teste que as pegou é de uma linha de `grep`:
`core/tools/auth/gauth.py` é nosso, logo `google-auth` é um tool com momento próprio; e `latex` era
duas coisas com um slug só — o toolchain `pdflatex` (de terceiros) e a nossa capacidade de papers
(`hooks/stubgen/tex-*` mais a família `core/tools/paper/`), que é uma feature comum e agora é a
linha `latex`, grupo `hooks+tools`.

**O palpite que abriu isto estava errado, e errado da forma cara.** A suspeita era que dois grupos
inteiros — os "fatos de instalação" e `capabilities` — não tinham significado de desligado.
`declared-deps` e `verify-suite` são avisos e gates comuns, plenamente desligáveis. E
`rtk-compaction` — que o palpite jogou no balde de "`capabilities` não custa nada até ser chamada" — é
**o alvo mais valioso da lista inteira**: tem ponto de fiação pronto em
`core/hooks/compact/bash-compact-rewrite.py`, roda em todo Bash, e `core/tools/deps.txt` já
precifica sua ausência em *"the session just costs 60-90% more"*. Uma feature que reescreve toda
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

**Corrigido 2026-08-17: a coluna agora guarda TODOS os caminhos, separados por vírgula**, e a sonda
percorre cada um — *nomear o primário* deixava o resto sem verificação nenhuma, que é exatamente o
buraco descrito acima. O caso que forçou a mudança prova que não é arrumação: `latex` é um gate de
pre-commit **mais** a família de tools que esse gate chama, então uma chave que parasse só o tool
faria `core/hooks/gates/duplication-and-terms.sh` ler a recusa do tool (exit 69) como violação de
terminologia e **bloquear justamente o commit que o desligamento existia para liberar**. Uma feature
que atravessa camadas só é honesta quando toda camada consulta a lei.
Cobertura parcial continua sendo trabalho de quem fia, não do teste.

**As 57 linhas não são 57 tarefas, e o teste de honestidade é o que decide isso.** Os grupos
`hooks`, `context-tree` e `brain` têm um arquivo de enforcement cada — uma chamada por linha,
mecânico. Já `skills` (14) não tem onde pôr uma: uma skill é markdown, não chama função nenhuma, e o
único desligamento real dela é o mirror recusar-se a publicá-la.

**Corrigido 2026-08-17, ao fiar o grupo: `capabilities` NÃO é o par de `skills`, e juntar os dois foi
erro.** O raciocínio acima vale para skill e só para skill. Um tool é uma **CLI que este
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
isso: é uma feature fiada num **hook**, cujo observável é o que ele reescreve e não um código de
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
