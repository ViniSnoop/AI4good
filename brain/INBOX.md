# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

https://www.instagram.com/p/DbQNApxEnCh/?img_index=3&igsh=ODVqMmEzdjZyMWQ2
ver se é verdade e se for estudar como aproveitar no wos
— via aiwbot · 2026-07-31

https://www.instagram.com/p/Da5jnu9E_0n/?img_index=5&igsh=MW93NndwcWZ5MWdteg==
— via aiwbot · 2026-07-31

https://www.instagram.com/reel/DbUJiTmiIRA/?igsh=MTMzYzRkcmFxbjIwbA==
tenho que olhar isso!
— via aiwbot · 2026-07-31

To automatically resume a Claude Code session when the usage limit resets, you can use open-source community tools or custom scripts since native auto-continue is not yet built-in. 
1. Use claude-auto-retry (Recommended) This is a dedicated open-source tool that intercepts the claude command, monitors for rate limits, and automatically sends "continue" when the window opens.
npm i -g claude-auto-retry
claude-auto-retry install
How it works: It uses tmux to send keys to the active pane. It is timezone-aware and requires no dependencies beyond Node.js. 
2. Bash Function (claude_go) For a lightweight solution, add this function to your ~/.bashrc to sleep until the reset time and then resume.
function claude_go() {
  local message="${1:-go on}"
  local reset_time=$(claude -p 'check' | awk '{print $NF}')
  local reset_ts=$(date -d "$reset_time" +%s)
  local now_ts=$(date +%s)
  local sleep_duration=$(( reset_ts - now_ts ))
  if [[ $sleep_duration -lt 0 ]]; then sleep_duration=$(( sleep_duration + 86400 )); fi
  echo "Sleeping until $reset_time..."; sleep "$sleep_duration"
  claude --permission-mode acceptEdits -c "$message"
}
3. Python Script with pyautogui A simple script can type "continue" and press enter after a set timer.
import time, pyautogui
time.sleep(3 * 60 * 60) # Wait 3 hours
pyautogui.typewrite("continue")
pyautogui.press("enter")
Best Practices:
Context Preservation: Users recommend saving a state note (current task, files touched) before the limit hits to ensure the resumed session picks up efficiently. 
Optimization: Reduce context size by disabling unused skills/tools in settings.json to maximize the effective window of your limit.
— via aiwbot · 2026-07-31

https://www.instagram.com/reel/Da5HMCMBY62/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==
pro projeto da ecovila
— via aiwbot · 2026-07-31

review our skills, see if they are effective, if they are verbose or giving extra work. check also for rendundancies, ambiguities, etc

do a routine checkup on our WOS. see if things are working as planned.

pq temos alguns arquivos python sem extensão .py?

https://www.instagram.com/reel/Da7QSJNFCyQ/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==
— via aiwbot · 2026-07-30

será que a IA consegue meditar? digamos, o modelo mais poderoso que tiver, Fable 5, tem como? não aceito o não como resposta, o que dá pra fazer nesse sentido?

routing-sync gera link relativo quebrado no CONTEXT.md pai
— achado durante o replan do isoroll-content · 2026-07-29
`proj: workspace-os` · O gerador do bloco `<!-- routing -->` copia a linha 2 do CONTEXT.md filho
verbatim como descricao. Se essa descricao contem um link relativo (ex: `refs/CONTEXT.md` diz
"tier-1 links in [REFS.md](REFS.md)"), o link resolve no arquivo filho mas quebra no pai, que esta
um nivel acima. Caso concreto: `code/isoroll-content/CONTEXT.md:118` -> `REFS.md` (deveria ser
`refs/REFS.md`). Fix candidato: o gerador reescreve links relativos ao prefixar com o diretorio do
filho, ou simplesmente strip de links na descricao copiada. Bloco e auto-gerenciado, entao editar
a mao nao resolve — some no proximo sync.

https://www.instagram.com/p/DbD_eQ2EhbF/?utm_source=ig_web_copy_link
— via aiwbot · 2026-07-29
[triagem 2026-07-29] extraído: Vyzual AI, "8 breakthroughs de julho 2026" — roundup genérico de
notícias de IA, sem nada específico pra nós. **Proposta: delete.** Deixado aqui só porque apagar
é irreversível — confirma e eu tiro.

https://www.instagram.com/p/DbX9V9bE2XH/?utm_source=ig_web_copy_link
— via aiwbot · 2026-07-29
[triagem 2026-07-29] extraído: Early Startup Days, "construir apps ficou fácil, deixar pronto pra
usuário real é outra história" — observação genérica, sem conteúdo acionável no post.
**Proposta: delete.** Mesmo caso do de cima.

O peso sempre-carregado nao esta no AGENTS.md — esta em regras dentro de CONTEXT.md
— achado 2026-07-30, sessao workspace-os (Lucas: "AGENTS.md ainda quite big, limites do
claudecode sendo atingidos rapido")
`proj: workspace-os` · Medido: AGENTS.md = 33 linhas / ~1.3k tok. Uma unica cascata do
`context-gate` nessa sessao custou **~5k tok** (leu `core/CONTEXT` + `core/tools/CONTEXT` +
`academy/CONTEXT` + `academy/papers/CONTEXT` + `code/CONTEXT` + `code/dobra/CONTEXT`) para
rodar dois `head`. Cortar AGENTS.md otimiza a coisa errada.
Causa raiz: `context-gate` forca a cadeia CONTEXT.md inteira antes de qualquer acesso a
arquivo; SPECS.md e sob demanda. Logo **toda restricao escrita num CONTEXT.md e imposto
cobrado de toda sessao naquele subtree, para sempre.** Piores casos:
- `academy/papers/CONTEXT.md` — 160 linhas (~2.4k tok), ~120 delas sao *restricoes*
  (regra 200 LOC, comentario de primeira linha, schema YAML de refs, taxonomia de tags, 5
  padroes de qualidade de escrita) + uma arvore ASCII `## Project Layout` escrita a mao.
  Nao existe `academy/papers/SPECS.md`. Abrir um `.tex` custa 2.4k tok.
- `code/CONTEXT.md:28` — diz "See SPECS.md for the full table" e **inline a tabela R1-R6
  inteira logo abaixo**. Duplicacao pura.
- `brain/CONTEXT.md:9-14` e `academy/papers/CONTEXT.md:39-52` — inventario de arquivos a mao,
  violando a regra que o Tier 0 deve impor, duplicando o bloco routing gerado.
Fixes candidatos, em ordem de payoff:
1. Extrair restricao de CONTEXT.md -> SPECS.md em cada subtree (comeca por `academy/papers/`).
   Regra geral nova: **CONTEXT.md e sempre-carregado, entao so pode conter identidade +
   roteamento; qualquer regra vai pra SPECS.md.** Candidato a virar check Tier 0.
2. `context-gate` deve exigir apenas o *head curado* do CONTEXT.md (ate
   `<!-- routing:start -->`), nao o bloco gerado. Em `core/tools/CONTEXT.md` o bloco gerado e
   44 das 108 linhas (~1.4k tok de inventario de arquivos).
3. `bash-context-gate` dispara em comando read-only (`head`, `grep`, `ls`, `wc`) e cobra a
   leitura do CONTEXT inteiro do subtree — inverte o incentivo: inspecionar um arquivo passa a
   custar mais que carregar o contexto do subtree.
4. Regra que um hook consegue impor nao precisa ser prosa sempre-carregada: a mensagem de erro
   do hook chega *no* momento da violacao e custa 0 token ate disparar. Quando o Tier 0 da
   Frente 4.1 existir, encolhem em AGENTS.md: allowlist uppercase (7 linhas), DONE WORK IS
   DELETED, CONTEXT nunca lista arquivos, GITFLOW. Fica so o que hook nao checa: FILESYSTEM =
   source of truth, DON'T ASSUME, PREFER EDIT OVER CREATE, SYMMETRY, PLANS LIVE IN ROADMAPS.
   Estimativa: 33 -> ~20 linhas, ~1.3k -> ~750 tok, com enforcement mais forte.

Rota de descarte para nome UPPERCASE fora da allowlist — regra, nao lista
— decidido 2026-07-30 com Lucas (Frente 4.1)
`proj: workspace-os` · Quatro rotas, para que nome novo se resolva sem perguntar:
1. gerado por ferramenta -> instancia lowercase (`TREE.md`->`tree.md`, `LABELS.md`->`labels.md`)
2. *conteudo* escrito a mao -> instancia lowercase (`DRAFT.md`->`draft.md`, x3 papers embriao)
3. *restricao* escrita a mao -> `SPECS.md` (`BRIDGE.md` -> `SPECS.md § Paper Twin`, x3)
4. responde pergunta que nenhum tipo responde -> tipo novo. Unico caso: **`SETUP.md` fica**
   (README e *repo-root only*; 4 dos 8 SETUP.md estao em dir que nao e repo — raiz, `academy/`,
   `code/`, `code/_templates/`). Allowlist 13 -> 14.
Decidido tambem: `SPEC.md` -> `SPECS.md` (colapsa; reescrever a convencao `> spec:`,
`core/hooks/pre-commit` §1d, `core/tools/spec-scan`, `core/tools/spec-contract-check`).

`/caveman compress` nao serve pra doc do workspace — medido e rejeitado
— piloto 2026-07-30, `academy/papers/CONTEXT.md` (pior ofensor: 159 linhas)
`proj: workspace-os` · Resultado: 8571 -> 8552 chars = **19 chars, 0.22%**, em 43s e uma
chamada de modelo (sem `ANTHROPIC_API_KEY` cai no `claude --print`, ou seja **gasta a mesma
quota do Claude Code que se quer economizar**). Seis trocas triviais de palavra
(`requiring`->`needing`, `without overwriting`->`no overwrite`). Extrapolando: 171 CONTEXT.md
= ~2h e 171 chamadas de quota pra economizar ~0.3%. Causa: os docs ja estao caveman-densos —
nao ha gordura lexical. Revertido via `git checkout`.
Corolario: **o ganho de token e estrutural, nao lexical.** Comprimir palavra nao move a agulha;
mover regra de CONTEXT.md pra SPECS.md e cortar inventario gerado move.
Bug menor achado no piloto: o compress **remove a newline final** do arquivo. Tambem
`scripts/compress.py:34` tem `CAVEMAN_MODEL` default `claude-sonnet-4-5` (id desatualizado).

O bloco routing sao DUAS tabelas — a navegacao e barata, o inventario e que custa
— medido 2026-07-30 (Lucas: "ain't the routing the most useful part?")
`proj: workspace-os` · Nos 171 CONTEXT.md:
| bloco | total | manter? |
|---|---|---|
| head curado (regras, cues) | **44.3k tok** | sim, e o conteudo |
| tabela **Subdirectory** (navegacao) | **5.7k tok** (media 34 tok/arquivo) | **sim — e o routing util** |
| tabela **File** (dump de simbolo por arquivo) | **55.8k tok** | nao |
A metade navegacao e barata; a metade inventario e maior que todo o conteudo curado do
workspace somado. Pior caso: `code/aiwbot/tests/CONTEXT.md` = 25 tok de contexto + **4608 tok
de tabela File** (razao 184x). Outros: `code/isoroll-content/src/pipeline` 2581,
`code/isoroll-content/test` 2512, `core/tools` 2020, `code/isoroll-module/src/render` 1736.
Proposta corrigida (a primeira versao era grossa demais, cortava a navegacao junto): a
satisfacao do `context-gate` para no header `| File |`, nao no `routing:start`. Mantem todo
cue e toda navegacao, corta so inventario — que `ls` ou Read pega sob demanda quando ja se
esta no diretorio. Pendente decisao do Lucas.
Bug do gerador achado no caminho: `core/skills/caveman/scripts/CONTEXT.md:27` — descricao do
`__init__.py` e `**facade** — ` repetido 21x (prefixo acumulando no `context_synchronizer.py`),
e 5 linhas com placeholder `← add first-line comment` (classe de placeholder diferente do
`← add description` corrigido na Frente 12.2 — o sweep passou batido nessa string).
