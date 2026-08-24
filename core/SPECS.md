# Core SPECS
> Architecture decisions and conventions for the Core agent library.

---

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
- **A afirmação descreve o TEXTO ou a EXECUÇÃO?** (regra do Lucas, 2026-08-24, depois do sweep que
  começou com `test_features_wiring` passando por acidente na palavra *asymmetry*, num comentário,
  num arquivo que nunca mencionou a norma.) Um check que procura um nome não é evidência de que
  algo aconteceu — e a pergunta que decide qual instrumento usar é essa, não "grep é proibido".
  - **Afirmação textual** — *"este módulo não guarda uma segunda cópia da lei"* é uma afirmação
    sobre o texto e nada mais. Pode usar grep, mas **o assert negativo é o check**: `f'= {WARN}'
    not in source`, `"'agent_id'" not in body`. O assert positivo é testemunha fraca (prova só que
    o import existe). Um check que lê fonte e só tem assert positivo é defeito.
  - **Afirmação de runtime** — *"este gate consulta o registry"*, *"este bloqueio chega ao
    usuário"*. Aí substring é proxy, e um proxy desses já foi pego passando errado. **Rode a
    coisa e observe.** Se o alvo não puder ser executado direto (fragmento shell sourced, lib,
    plugin node), leia a fonte **sem comentários** — não é o mesmo que rodar, e o comentário no
    check tem que dizer isso.
  Sem meta-test que força a regra: um check varrendo a suíte atrás de asserts sem par negativo
  seria, ele próprio, um grep provando uma afirmação sobre testes — exatamente o cheiro que a
  regra existe para nomear.
  **A regra se demonstrou sozinha na hora de aplicá-la**: `"bash-context-gate.py".endswith(
  "context-gate.py")` é `True`, então o primeiro rascunho do harness entregou ao gate de Bash um
  payload de Read e o caso passou *por não bloquear*. Um grep teria ficado verde; a execução falhou
  alto. Daí duas coisas: **caso de teste casa com o basename exato, nunca com sufixo**, e um teste
  que roda a coisa erra ruidosamente onde o proxy erra em silêncio.
- **Um comando cujo status é um gate nunca vai para dentro de um pipe** (achado 2026-08-13, custou um falso "main
  pushed"). Em `a | tail && b`, o status é o do `tail`, não o do `a` — então `git merge --ff-only x 2>&1 | tail -1 &&
  git push` executa o push mesmo com o merge abortado, e a sessão reporta sucesso de algo que não aconteceu. Para
  sequências onde cada passo autoriza o próximo: `set -e` e sem pipes, ou capturar o status explicitamente. Filtrar
  saída é para inspeção, não para decisão.
- **Seção de `.md` se cita pelo nome, nunca pelo número** (achado 2026-08-15, custou 8 ponteiros
  quebrados em 6 arquivos). Um número é um ponteiro que envelhece na primeira seção inserida, e
  envelhece *em silêncio*: `[SETUP.md §6]` continuava resolvendo para um arquivo que existe, só que
  para a seção errada — nenhum check de integridade de link pega isso. O root `SETUP.md` tinha
  chegado a ter `§10` antes de `§9`. Referência boa: `[`SETUP-accounts.md`](SETUP-accounts.md) § Web search` — o texto
  âncora sobrevive a qualquer reordenação, e se a seção for renomeada a busca falha em vez de
  apontar para o lugar errado.
- **Nome de arquivo: uma palavra só, e a palavra inteira** (preferência do Lucas, 2026-07-23). Truncação perde para a
  palavra completa: `architect` > `arch`, `literature` > `lit`. Nome que repete o namespace do pai é ruído — sob
  `research/`, `deepresearch.md` gagueja (`research deepresearch`), então virou `deep.md`. Nomes genéricos e óbvios
  devem ser **reservados** para o flow que realmente os merece: `explore` ficou com o loop de tentar ideias justamente
  para deixar `experiment` e `optimize` livres para flows futuros distintos.
- Nova skill (flat): copiar `core/skills/_template.md`, preencher frontmatter.
- Nova skill (suite): criar `core/skills/<suite>/SKILL.md` + sub-arquivos `<slug>.md`.
- Sub-skills relacionadas em pasta são sempre preferidas a skills flat com prefixo longo quando > 2 sub-skills.
- Novos serviços Google: importar `auth/gauth.py`, definir `SCOPES` e o nome do serviço, seguir o padrão de
  `files/drive_core.py` (seam read+write, account-agnostic) — e registrar o comando de recuperação em
  `gauth._REAUTH_CMD` no mesmo commit em que a CLI ganha `--reauth`; um teste verifica que todo comando dessa tabela
  aponta para uma ferramenta que existe.
- Novo provedor **sem** OAuth: seguir `notes/notion` — segredo guardado ao lado da ferramenta, toda
  falha imprimindo a instrução completa, segredo entrando por stdin (AD-12).
- Tokens OAuth nunca commitados — ficam em `~/.config/workspace-*/`.
- **Pasta `refs/` em skills**: quando uma skill acumular referências externas, criar `core/skills/<name>/refs/` (ou
  `core/skills/<suite>/refs/`) e manter todos os arquivos de referência lá. Não criar `refs/` dentro de
  `.opencode/skills/` ou `.claude/skills/` — esses são mirrors gerados automaticamente.
- **Formato de arquivos em `refs/`**: notas de leitura, links rápidos e sumários informais vão em `*.md`. Referências
  estruturadas (papers com metadados, datasets com schema, configurações de ferramentas) vão em `*.yaml` com frontmatter
  ou schema claro. Preferir YAML para anything que uma skill vai parsear ou que precisa de schema.

<!-- routing:start -->
## Routing

| Shard | Description | Governs | Enforced by |
|-------|-------------|---------|-------------|
| [`SPECS-discipline.md`](SPECS-discipline.md) | What an always-loaded rule must prove, when doubt costs, when to delegate. | AGENTS.md, core/norms/, core/agents/, core/flows/craft/ | — |
| [`SPECS-features.md`](SPECS-features.md) | What counts as a feature, what its columns mean, and what may not be undeclared. | core/features.txt, core/profile.txt | core/hooks/feature_law.py, core/tools/wos/features |
| [`SPECS-library.md`](SPECS-library.md) | How the agent library is arranged, and how a tool family and its auth attach. | core/skills/, core/flows/, core/tools/, core/agents/ | — |
| [`SPECS-session.md`](SPECS-session.md) | How a session closes, and who carries context when work is handed off. | core/skills/roundup.md, core/hooks/session/, core/hooks/read/agent-context.py | — |
<!-- routing:end -->
