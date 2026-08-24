# todo-type-retirement — plan

## Carry
slug: todo-type-retirement | branch: feature/roundup-md-cap | root: /mnt/workspace
provider: anthropic | chain-deleg: none
tier-map: anthropic | verified-on: 2026-08-20
test-cmd: `make verify-fast` | e2e-cmd: none (`make entropy` writes the fenced ISSUES.md — DO NOT RUN)
criticality: normal | verdict: standard
subtree: feature | supervision: io-signoff=no arch-review=none arch-review-supervised=no
criteria:
  C1 — every live line of `brain/TODO.md` landed per § Fold Map; nothing lost, nothing invented.
  C2 — `brain/TODO.md` no longer exists on disk (`git rm`).
  C3 — TODO row gone from `core/SCHEMA.md` type table and from `core/SCHEMA-placement.md` COLD row.
  C4 — `TODO.md` row gone from `brain/CONTEXT.md` routing table (by regeneration, not hand-edit).
  C5 — `'life-todo'` gone from `LEDGERS` in `core/hooks/entropy/dashboard/entropy-dashboard.py`
       and from the mirror `LEDGERS` in `core/tools/test/law/entropy/test_entropy_ledger.py`.
       `entropy_ledger.py` `LEDGER_FILES` is FENCED → reported follow-up, not an edit.
  C6 — "four ledgers" phrasing in `ROADMAP-ledger.md` line 10 reads three.
  C7 — no tracked file points a reader at `brain/TODO.md` as a live destination.
  C8 — `make verify-fast` is green.
tasks:
  T1 — new goal seed `google-migration` + `branches/google-migration/` cockpit — brain/goals/, branches/ — high
  T2 — fold `today` + `week` + `month` rows into their destinations — brain/goals/*.md, brain/INBOX.md — medium
  T3 — fold `backlog` rows into their destinations — brain/goals/*.md, brain/INBOX.md — medium
  T4 — move the 31-row drive queue verbatim into the cockpit ROADMAP — branches/google-migration/ROADMAP.md — medium
  T5 — delete the file and its .gitignore allowlist line — brain/TODO.md, .gitignore — low
  T6 — kill the type at every declaration site — core/SCHEMA.md, core/SCHEMA-placement.md, 2 py files, ROADMAP-ledger.md — medium
  T7 — fix live back-pointers at the SOURCE, then regenerate the mirrors — core/skills/*.md, refs, branches, goals — medium
  T8 — regenerate the generated routing blocks — brain/CONTEXT.md, brain/goals/CONTEXT.md, branches/CONTEXT.md — low
  T9 — run `make verify-fast`, green — — low
context: /mnt/workspace/AGENTS.md · /mnt/workspace/brain/CONTEXT.md · /mnt/workspace/brain/SPECS.md
         · /mnt/workspace/brain/goals/CONTEXT.md · /mnt/workspace/core/CONTEXT.md

## Plan
branch: feature/roundup-md-cap  *(pinned by the orchestrator — already checked out, shared worktree.
Do NOT create or switch branches. Loop 2 verifies only; it must not run `git checkout -b`.)*

| id | task | files | done-when | tier | effort |
|----|------|-------|-----------|------|--------|
| T1 | Create the goal seed `brain/goals/google-migration.md` (`# [ career \| admin \| now ] migração Google — conta cin → pessoal, e o Drive para o workspace`, a `## backlog` holding the 8 items the Fold Map assigns to it, plus `## selected next achievement` + `ease-start` per `brain/SPECS.md` § Selected Next Achievement Block and its quality bar). Create `branches/google-migration/CONTEXT.md` (title + one-line description; a directory without one is blocked by the context gate). | `brain/goals/google-migration.md`, `branches/google-migration/CONTEXT.md` | both files exist; the goal file has ≥8 `> [ ] [id]` lines and a non-empty ease-start | high | high |
| T2 | Apply every § Fold Map row whose `source` is `today`, `week` or `month`. **Append** new items at the END of the destination's `## backlog` — never at the top (`brain/SPECS.md`: the selected achievement is the FIRST unchecked item; inserting at the top silently reassigns it). Rows marked `absorb→[id]` edit that existing item's text in place and **must not change its short-id**. Rows marked `INBOX` append one bullet to `brain/INBOX.md`. Rows marked `DELETE` write nothing anywhere. | `brain/goals/*.md`, `brain/INBOX.md` | every non-DELETE row's short-id greppable in its named file; every `absorb` row's named clause present | medium | high |
| T3 | Same procedure as T2 for the § Fold Map rows whose `source` is `backlog`. | `brain/goals/*.md`, `brain/INBOX.md` | same check, backlog rows | medium | medium |
| T4 | Move `brain/TODO.md` lines 54–93 (the `## drive migration` block: its blockquote, the three `###` subsections and all 31 `- [ ]` rows) **verbatim, checkbox state included**, into a new `branches/google-migration/ROADMAP.md` under a `# Fila de download (cin → workspace local)` heading. Do not summarise, reorder or re-tick a single row: each row's `local ← Drive path` pairing is a decision that cannot be re-derived from either side. | `branches/google-migration/ROADMAP.md` | `grep -c '^- \[ \]'` on the new file == 31 | medium | medium |
| T5 | `git rm brain/TODO.md`; delete line 155 `!brain/TODO.md` from `.gitignore`. | `brain/TODO.md`, `.gitignore` | file absent; `git check-ignore -v brain/TODO.md` reports the `brain/*` rule | low | low |
| T6 | Kill the type: drop the `\| `TODO.md` \| What must I do in life this week? \|` row from `core/SCHEMA.md`'s type table; drop `` `TODO.md` `` from the COLD row of `core/SCHEMA-placement.md` line 29; drop the `'life-todo'` entry from `LEDGERS` in `core/hooks/entropy/dashboard/entropy-dashboard.py` (line 57) AND from the mirror `LEDGERS` in `core/tools/test/law/entropy/test_entropy_ledger.py` (line 23), fixing that test's "The four wos ledgers" comment (line 18) to three; change "four ledgers" → "three ledgers" on `ROADMAP-ledger.md` line 10. **Do NOT add `TODO.md` to any retired-token table** — see § Traps. | `core/SCHEMA.md`, `core/SCHEMA-placement.md`, `core/hooks/entropy/dashboard/entropy-dashboard.py`, `core/tools/test/law/entropy/test_entropy_ledger.py`, `ROADMAP-ledger.md` | `grep -n 'TODO' ` on those five files returns nothing | medium | medium |
| T7 | Fix live back-pointers per § Back-pointers, editing `core/skills/inbox.md` and `core/skills/roundup.md` (the SOURCES), then run `core/tools/wos/sync-skills` to regenerate `.claude/commands/*.md`. Hand-edit `academy/refs/REFS.md` (4), `core/refs/REFS-tooling.md` (4), `core/refs/REFS-unjudged.md` (1), `branches/ecovila/CONTEXT.md`, `branches/ecovila/burocracia/CONTEXT.md`, `brain/goals/ecovila.md`, `brain/goals/teaching-materials.md`. | see § Back-pointers | `git grep 'TODO\.md'` returns only the § History set + the ROADMAP rows the orchestrator owns | medium | high |
| T8 | Regenerate the three generated routing blocks so the `TODO.md` row and the new files land in them: `python3 core/hooks/routing/context_synchronizer.py <path>` for `brain/CONTEXT.md`, `brain/goals/CONTEXT.md`, `branches/CONTEXT.md`. Never hand-edit inside `<!-- routing:start -->…<!-- routing:end -->`. | `brain/CONTEXT.md`, `brain/goals/CONTEXT.md`, `branches/CONTEXT.md` | no `TODO.md` row in brain/CONTEXT.md; `google-migration` rows present in the other two | low | low |
| T9 | Run `make verify-fast`. Never `make entropy`. | — | exit 0 | low | low |

## Fold Map
73 live lines. Destination is per-line; `absorb→[id]` means the existing item's text is widened,
no new short-id. Portuguese text stays Portuguese — translating it is a C1 loss.

| src | line (abbrev.) | destination | short-id | judgment |
|-----|----------------|-------------|----------|----------|
| today | antes das 18h30: abrir `academy/teaching/tecnologias-na-educacao/aula02-problemas.excalidraw`, confirmar que carrega, Live collaboration → link no slide 69, conferir se são 8 equipes | `brain/goals/teaching-materials.md` | `excalidraw-aula02` | operational half of the live `[excalidraw-vs-miro]` verdict; **keep the file path, "slide 69" and "8 frames" inline** |
| today | na aula de hoje: decidir o vídeo do slot do carrinho — 4 min do Dietz vs. perguntar "o que envelheceu nesse vídeo de 1999?" | `brain/goals/teaching-materials.md` | `video-carrinho` | class-design decision; candidates already judged in `academy/refs/REFS.md` — cite, don't restate |
| today | depois da aula: anotar quantos alunos falaram na abertura e quantos grupos saíram com o frame preenchido | `brain/goals/teaching-materials.md` | `medir-redesenho` | the honest test of the redesign — sits beside `[metodologia-tecedu]` |
| today | jogar na lixeira o deck `__probe_delete_me` no Drive pessoal (sonda de auth) | `brain/INBOX.md` | — | one-off chore, no commitment behind it; capture, not goal |
| today | sleep by 00:30 — streak-3 starts tonight | DELETE | — | **provably duplicated**: `brain/goals/sleep-regularity.md` line 35 is `[streak-3] 3 consecutive days on target — in bed by 00:30`. Same slug, same content; the TODO line's own tag names it |
| today | mandar os dois questionários pras turmas; links nos `CONTEXT.md` de `academy/teaching/ai4good/` e `.../tecnologias-na-educacao/`; testar respondendo e apagando; depois ler com `core/tools/forms/gforms responses --account personal <form_id>` e decidir o formato das sextas | `brain/goals/teaching-materials.md` | `questionarios-sextas` | **the exact CLI invocation and both CONTEXT.md locations are load-bearing — keep them verbatim in the item** |
| week | desenhar a metodologia completa de Tec. na Educação nos 34 encontros (números em `academy/teaching/tecnologias-na-educacao/CONTEXT.md`): semana-padrão quarta/sexta com papéis fixos, uma pergunta e um produto por encontro, 9 etapas, avaliação nova, dashboard, MODELO+EXEMPLO | `brain/goals/teaching-materials.md` | absorb→`[metodologia-tecedu]` | that item is already 80% of this line and ends with a `ver task na semana em brain/TODO.md` pointer. **Widen it with the two missing clauses** ("quarta e sexta com papéis fixos, uma pergunta e um produto por encontro" + the CONTEXT.md numbers pointer) **and delete the pointer** |
| week | (same line, tail) Pesquisa que falta: gamificação séria, specs/contract grading, avaliação por pares, venues p/ graduandos | DELETE | — | **provably duplicated**: `[pesquisa-que-falta]` (teaching-materials.md line 46) already carries all four, in richer wording |
| week | revisar artigo do svr — prazo ~25/07 (confirmado 23/07) | `brain/INBOX.md` | — | no goal covers peer-review service, and one line does not earn a seed. Deadline is ~4 weeks past → **capture it with "prazo vencido, decidir se ainda vale"**; the agent cannot rule a commitment to a third party dead |
| week | responder megatruth | `brain/goals/paper-megatruth.md` | `responder-time` | distinct from `[mega-01] schedule team meeting` — this is breaking the silence, which GOALS.md § gap names as the goal's actual block. Append at the end per T2; do not reorder |
| week | pedir mudança da data de pagamento do aluguel: dia 5 → dia 10 | `brain/goals/finances.md` | `aluguel-dia-10` | plain finances commitment |
| week | transferir pra painho o valor do terreno/chão do santuário jatobá | `brain/goals/ecovila.md` | absorb→`[finance-terreno]` | that item literally reads "(ver TODO week: transferir valor do terreno...)" — **fold the content in, delete the pointer** |
| week | catalogar as últimas finanças da obra — cockpit em `branches/casinhas/` | `brain/goals/home-casinhas.md` | `gastos-catalogar` | `[obra-system]` names "sync de gastos" as one of S2..S7; this is the concrete now-task, kept separate so it is startable |
| week | responder o desafio público do Jake Van Clief — ele julga os 3 comentários mais curtidos, janela curta ([reel](https://www.instagram.com/reel/DbWA6VOxVq-/)) | `brain/INBOX.md` | — | opportunity, not commitment, and its window opened 2026-07-28. **Keep the full URL** — it is the only handle on the thing |
| week | investigar o caso por trás do reel "this feels like a book burning" e decidir se entra em ai4good | `brain/goals/teaching-materials.md` | `ai4good-book-burning` | teaching-materials is the goal that owns what enters a class; ref stays in `academy/refs/REFS.md`, whose pointer T7 redirects here |
| week | checkup de rotina do workspace: rodar `core/tools/test/verify-fast`, ler `ISSUES.md § Entropy` (a contagem, nunca uma cópia), auditar os 4 critérios de v1 no `/ROADMAP.md`; **e o checkup precisa de um método** — usar as features de verdade (INBOX 2026-08-13) | `brain/goals/workspace-os.md` | `checkup-metodo` | ties `[v1]` and `[mvp-validate]` together. **Keep all three commands/paths and the "método" clause** — the method is the open question, the run is the easy part |
| week | assistir o reel "pacing the frontier" e decidir se entra em ai4good; a extração só trouxe a legenda | `brain/goals/teaching-materials.md` | `ai4good-pacing-frontier` | same rule as the book-burning row; **keep the "só a legenda" caveat** — it is why the item is not yet decidable |
| week | achar e testar o **arXiv Visuals** (link comment-gated); teste honesto = rodar num paper que você conhece a fundo; se sustentar, decidir dois usos: leitura própria e material de aula | `brain/goals/teaching-materials.md` | `arxiv-visuals` | **keep "comment-gated" and both uses** — the two-uses split is the decision, not a detail |
| week | mudar a conta Google padrão do Brave para lsf.cin@gmail.com — primeiro passo da migração, o único que não depende de decidir nada | `brain/goals/google-migration.md` (NEW) | `brave-conta-padrao` | zero-decision first step → this is the new goal's ease-start candidate |
| week | `[pandeiro / show-up]` confirm Pandeirada time, show up Saturday | DELETE | — | **provably duplicated**: the tag *is* the address — `brain/goals/pandeiro.md` line 26 holds `[show-up] go to Pandeirada next Saturday`. A pointer, not an item |
| week | `[sleep / streak-3]` 3 consecutive nights in bed by 00:30 | DELETE | — | **provably duplicated**: same pattern, `brain/goals/sleep-regularity.md` line 35 `[streak-3]`. Second copy of the `today` sleep line as well |
| week | bolsa IC — NÃO submetido; bloqueado por (1) projeto de pesquisa aprovado no CTA, (2) nomes dos alunos candidatos | `brain/goals/career-ufrpe.md` | `bolsa-ic` | **both blockers must survive** — they are what makes the item not-startable, and losing them turns it into guilt |
| week | relatar/assinar processo de progressão CTA — processo **23082.018263/2026-55**, Lenina inseriu no GT CTA, assina seg/ter, pauta de terça | `brain/goals/career-ufrpe.md` | `progressao-cta` | **the process number is irreplaceable — copy it character-for-character**; sits next to `[progressao-map]`/`[progressao-alarm]` |
| week | adiantar publicação da tese do Jarbinhas (ver goal `paper-jarbinhas`) | DELETE | — | **provably a pointer**: the line names its own destination, and `brain/goals/paper-jarbinhas.md` `[jarb-01]`..`[jarb-05]` is that work broken into five steps. Nothing here is not there |
| month | averbação do terreno | DELETE | — | **provably duplicated and strictly poorer**: `brain/goals/home-casinhas.md` line 31 `[averbacao-terreno]` adds the 7º Cartório RGI, the firmas no Memorial, and the BUROCRACIA.md 🔴 link |
| month | PPC ementas: 41/44 reformatadas p/ SIGAA e no Drive; falta pedir a Paulo o conteúdo de FUNDAMENTOS DA EDUCAÇÃO, PROJETO INTEGRADOR EM DESENV. DE ARTEFATOS EDUCACIONAIS e PROJETO INTEGRADOR EM EDUCAÇÃO EM COMPUTAÇÃO (`academy/administration/coordenacao-lc/novo-ppc-bcc/ementas/gaps.md`) → depois criar as 3 já no formato novo | `brain/goals/burocracia-academica.md` | `ppc-ementas-3` | coordination work Lucas owns; **the three discipline names + `gaps.md` path + the 41/44 count must survive** — `gaps.md` already holds the per-discipline detail, so the item cites it rather than restating it |
| month | OR gate body still missing — see ISSUES.md; investigar o tipo `CUSTOM` no grupo do slide 23 | `brain/goals/teaching-materials.md` | `or-gate-shape` | **do NOT treat "see ISSUES.md" as evidence of a record — I grepped `ISSUES.md` and there is no OR-gate entry.** The pointer is dangling, ISSUES.md is fenced, so the item carries its own detail ("slide 23", "shape type CUSTOM") and drops the pointer |
| month | backup/recovery do Google Authenticator — mapear códigos de recuperação por conta + método de restauração | `brain/goals/google-migration.md` (NEW) | `auth-recovery` | 2FA recovery bites exactly when accounts move, which is what this goal does; grouping it there keeps the account work in one place instead of seeding a one-item "security" goal |
| month | confirmar se o crédito Fable (100 usd até setembro) ainda consome do limite por turno/semanal | `brain/goals/workspace-os.md` | `fable-credito` | its natural ledger is `ROADMAP-cost.md`, **which is fenced this session**; workspace-os is the goal that owns the workspace's running cost. **Keep "100 usd até setembro"** — the window is the whole point |
| month | testar geração de imagem via opencode + chave NVIDIA — nanobanana com a key falhou | `brain/goals/rpg-isoroll.md` | `nvidia-imagegen` | sits beside `[bakeoff]`, which is the image-generation arms comparison. Goal file, not `code/isoroll-content/ROADMAP.md`, because C1 admits only goal-or-INBOX |
| month | checar isenção e prazos de cotas SBC — email andreza.leite@ufrpe.br | `brain/goals/burocracia-academica.md` | `sbc-cotas` | **the email address is the handle — keep it inline** |
| month | migrar o calendar de lsf@cin.ufpe.br para lsf.cin@gmail.com — `core/tools/calendar/gcalendar` já lê as três contas | `brain/goals/google-migration.md` (NEW) | `calendar-migrar` | **keep "já lê as três contas"** — it says the migration is data + default account, not tooling |
| month | baixar o calendário acadêmico da UFRPE para o planejamento das aulas | `brain/goals/teaching-materials.md` | `calendario-ufrpe` | plain teaching dependency |
| month | decidir a forma de sincronizar a pasta local com o gdrive — hipótese: instalar o cliente do gdrive, *"funcionaria como um git com commits automatizados?"*; a pergunta real é se o versionamento nativo do Drive basta | `brain/goals/google-migration.md` (NEW) | `drive-sync-method` | **keep Lucas's quote verbatim** and the reframing; this decision is what the download queue below is currently waiting on |
| month | mapear a parte de ensino da vida dentro do WOS e migrá-la inteira para lsf.cin@gmail.com — o mapa vem antes da migração; hoje o ensino está entre `academy/classes/`, a fila de download e a conta do cin | `brain/goals/google-migration.md` (NEW) | `ensino-mapa` | **keep "o mapa vem antes da migração"** — it is the sequencing constraint; note it also collides with the live `academy/classes/` vs `academy/teaching/` split |
| drive migration | blockquote "scaffold done. download each folder, then triage loose/Unorganized items." + `### academy/` 23 rows + `### branches/` 6 rows + `### triage (do last)` 2 rows = **31 checkboxes** | `branches/google-migration/ROADMAP.md` (NEW) | — | **The one honest grouping, and here is why.** These 31 rows are not 31 commitments — they are the steps of one commitment ("bring the Drive in"), which is why one goal item can stand for them. But each row carries state (ticked/unticked) and a `local ← Drive path` pairing that encodes a decision (`UFRPE/Disciplinas/PGP` → `classes/gerencia-de-projetos`) recoverable from neither side alone. So the rows **move verbatim** rather than being summarised, into a cockpit that follows the workspace's own established pattern — `branches/casinhas/` + `brain/goals/home-casinhas.md`, `branches/ecovila/` + `brain/goals/ecovila.md`, `branches/instituto/` + `brain/goals/instituto.md`: the domain cockpit holds the state, the goal holds the why. The three commitments below are what the goal file carries |
| drive migration | ↳ the 23 `### academy/` rows | `brain/goals/google-migration.md` (NEW) | `fila-academy` | one backlog item pointing at the cockpit block; the 23 rows themselves live there |
| drive migration | ↳ the 6 `### branches/` rows | `brain/goals/google-migration.md` (NEW) | `fila-branches` | same |
| drive migration | ↳ the 2 `### triage (do last)` rows (Unorganized/, loose root files incl. recovery codes) | `brain/goals/google-migration.md` (NEW) | `fila-triagem` | same; **"recovery codes" in the loose-files row ties to `[auth-recovery]`** — say so in the item |
| backlog | no Brave, ativar aceleração de buscas por site — o trabalho é levantar quais ferramentas valem um atalho (Maps e Tradutor certos; Amazon, Mercado Livre, ChatGPT em dúvida); decidir a lista com ele antes de configurar | `brain/INBOX.md` | — | the line says its own scope is undecided ("decidir a lista com ele"), which is the ruling's definition of capture rather than commitment. It arrived from INBOX today; **returning it there is not a round-trip — TODO was the wrong stop** |
| backlog | assess "mandato coletivo" (participatory-mandate) as a mechanism-design case to cite/compare | `brain/goals/cria.md` | `mandato-coletivo` | cria *is* the mechanism-design goal; `academy/refs/REFS.md` pointer redirected here by T7 |
| backlog | novo projeto: gerador de animações (claude-code + remotion) | `brain/goals/teaching-materials.md` | absorb→`[research-tools]` | that item already names "claude-code+remotion" as its starting point and was reescopado 2026-08-14. **Absorb, don't delete** — add the clause "(inclui a ideia de um gerador de animações próprio)" so the build intent is not silently downgraded to a research intent |
| backlog | deixar o plan mode como default de sessão nova na extensão VSCode do Claude Code — config do harness; checar `.claude/settings.json` vs. UI; skill `update-config`; casa com o `/roundup` que agora fecha em *plan* | `brain/goals/workspace-os.md` | `plan-mode-default` | **keep the settings.json/UI fork and the `update-config` pointer** — they are what makes it a one-liner or not |
| backlog | decidir quais dos 20 itens da checklist pré-lançamento viram gate para gira/voti/ppc — sobram auth server-side, RLS, rate-limit e headers, que nenhum gate nosso vê | `brain/goals/workspace-os.md` | `security-gates` | it is a question about the enforcement layer, which workspace-os owns. **Keep the four uncovered items named** — they are the actual scope; `core/refs/REFS-unjudged.md` pointer redirected by T7 |
| backlog | avaliar a orquestração graph-native de agentes do Claude Code contra `code/flows`, e checar se "Graph Engineering" existe de fato | `brain/goals/craft-flows.md` | `graph-native` | craft-flows is the orchestration goal. **Keep the second half** — the post itself admits one of the two claims is fake |
| backlog | averiguar o JCode (reimplementação Rust do harness): (1) a ferramenta presta? (2) **é o harness que deixa tudo caro, ou o modelo?** — (2) dá pra medir aqui comparando tokens de scaffolding vs. conteúdo | `brain/goals/workspace-os.md` | `jcode-custo` | **keep both questions and the note that (2) vale mais** — that is the whole judgment in the line, and it is measurable with `core/tools/wos/session` |
| backlog | avaliar as 10 libs de fine-tuning local (Unsloth, LLaMA-Factory, PEFT, Axolotl, TRL, torchtune, LitGPT, SWIFT, DeepSpeed, AutoTrain) para o runner de SLM do dobra na RTX 3050 6GB | `brain/goals/local-ai.md` | `finetune-libs` | sits with `[local-setup]`/`[tiny-quant]`, which already fight the same 6 GB. **All ten names fit on one line — keep them**; a list of ten is not re-derivable |

Line accounting: 6 today + 17 week + 11 month + 31 queue + 8 backlog = **73 source lines**, and
the table has 74 rows because the `week` metodologia line is split across two rows (its body is
absorbed, its "pesquisa que falta" tail is a proved duplicate) and the queue's own summary row is
followed by its three goal-item rows. Destinations: **28** new goal-backlog items in existing
goals · **8** in the new `google-migration` seed (incl. the three `fila-*`) · **4** INBOX
captures · **3** absorptions into existing items · **7** DELETEs, each naming file+line of its
duplicate · **31** rows moved verbatim to the cockpit. Nothing is unrouted.

## Back-pointers (T7)
`.claude/commands/*.md` **are generated mirrors** of `core/skills/*.md` — verified by diffing
`core/skills/inbox.md` against `.claude/commands/inbox.md` (byte-identical) and `roundup.md`
(identical but for four rewritten relative link depths). So: **edit the source, run
`core/tools/wos/sync-skills`, never hand-edit both.**

| file | what changes |
|---|---|
| `core/skills/inbox.md` (5 lines: 13, 24, 76, 139, 156) | the **task** route stops naming `TODO.md`. New rule: *commitment → the backlog of the goal it serves (`brain/goals/*.md`, `[short-id] description` per `brain/SPECS.md`); capture → stays in `INBOX.md`*. Drop the `task: today/week/month/backlog` timeframe signal from the route vocabulary — there are no timeframes left to route to. Update `brain/CONTEXT.md`'s INBOX row, which advertises that same signal |
| `core/skills/roundup.md` (lines 33, 65) | drop `-o -name "TODO.md"` from the ledger-discovery `find`; the routing row for "personal/admin/life/teaching task" now points at the goal backlog |
| `.claude/commands/{inbox,roundup}.md` | regenerated, not edited |
| `academy/refs/REFS.md` (4 lines: 9, 10, 14, 16) | each "task in `brain/TODO.md`" becomes the goal + short-id this plan assigned: `[mandato-coletivo]` in cria; `[ai4good-book-burning]`, `[arxiv-visuals]`, `[ai4good-pacing-frontier]` in teaching-materials |
| `core/refs/REFS-tooling.md` (5 lines: 38, 130, 144, 151, 170) | line 38 → `[jcode-custo]` in workspace-os; **line 130 is a live policy sentence** ("has a paired assessment task in `brain/TODO.md`") → rewrite to name the owning goal's backlog; line 144 points at "the open OCR task in `brain/TODO.md` week" — **there is no OCR line left in TODO.md**, so point it at `brain/goals/ecovila.md` `[org-docs]`, which is the surviving owner; line 151 and 170 → the goal each ref's task landed in |
| `core/refs/REFS-unjudged.md` (line 83) | → `[security-gates]` in workspace-os |
| `branches/ecovila/CONTEXT.md`, `branches/ecovila/burocracia/CONTEXT.md` | "(precisam de OCR — ver `brain/TODO.md`)" → "ver `brain/goals/ecovila.md` `[org-docs]`" |
| `brain/goals/ecovila.md` (lines 19, 21) | `[org-docs]` drops "(ver `brain/TODO.md`)"; `[finance-terreno]` absorbs its TODO line per the Fold Map |
| `brain/goals/teaching-materials.md` (line 45) | `[metodologia-tecedu]` drops "ver task na semana em `brain/TODO.md`" and absorbs it per the Fold Map |
| `.gitignore` line 155 | deleted (T5) |

**History — leave untouched, and this line exists so a later loop does not "helpfully" rewrite
the past:** `ROADMAP-archive.md:76`, `brain/goals/workspace-os.md:78` (inside `## done`, a dated
record of the four-ledger collapse), and `brain/memory/feedback_parallel_sessions.md:26,41`
(incident reports naming the file that existed at the time). These are true statements about the
past; editing them would falsify history to make a grep clean.

## Traps (each one would break a green build or the intent)
- **Never add `TODO.md` to a retired-token table** (`core/SCHEMA-vocabulary.md`). `test_no_retired_token_survives` asserts a retired spelling appears *nowhere tracked*, and the § History set above keeps it appearing forever, by design. Adding it turns verify-fast red with no correct fix.
- **`core/hooks/entropy/entropy_ledger.py` is FENCED** — its `LEDGER_FILES = {…, 'TODO.md', …}` stays. Harmless: `item_slugs()` swallows a missing path (`except OSError: return set()`), so nothing crashes. Reported follow-up, not an edit (§ Follow-ups).
- **`brain/CONTEXT.md`'s TODO row is inside `<!-- routing:start -->…<!-- routing:end -->`** and is regenerated by `core/hooks/routing/context_synchronizer.py`. Hand-editing it satisfies C4 for about one save.
- **A new directory needs a `CONTEXT.md`** or the read gate blocks access to it — hence T1 creates `branches/google-migration/CONTEXT.md` before T4 writes into that directory.
- **New goal files are tracked automatically**: `.gitignore` lines 164–166 allowlist `brain/goals/*.md`. `brain/GOALS.md`'s `<!-- goals:start -->` table and dashboard are generated on commit — do not hand-add a row.
- **Appending to a goal backlog at the top silently reassigns its selected achievement** (`brain/SPECS.md`: the selected achievement *is* the first unchecked item). Append at the end.
- **No new short-id collides with a wos-roadmap slug** — checked against every bracket slug in `ROADMAP.md`, `ROADMAP-*.md` and `core/ROADMAP.md` (`courses-import`, `gdrive-integration`, `mvp-validate`, `notion-read`, `notion-write`, `brain-full-files`, `branches-coverage`, `offline-resilience`, `task-metric`, `spec-driven-development`). Cross-goal repeats are legal by design; cross-ledger ones are criterion-2 violations.

## Orchestrator-directed omissions (recorded, not skipped silently)
- **No ROADMAP.md line was added for this plan**, contrary to Loop 1's own spec: the roadmap row already exists (`ROADMAP-ledger.md` the ledger-discipline front item 1) and a fenced concurrent session owns roadmap edits.
- **~80-line soft cap is breached, by orchestrator sanction.** In a content migration the plan *is* the content: 73 per-line routing judgments cannot be compressed without becoming the batching the ruling forbids. The work itself is one chain — 9 task rows, one repo, no new subsystem — so no `RETURN loop=1 reason=split-needed`.

## Follow-ups to report (not edits in this chain)
1. `core/hooks/entropy/entropy_ledger.py` `LEDGER_FILES` still lists `'TODO.md'` — fenced. Drop it once the concurrent session releases the file.
2. `ROADMAP.md` line 163 and `ROADMAP-ledger.md` the ledger-discipline front item 1 (the row this chain executes) — the orchestrating session deletes them.
3. **`brain/memory/feedback_inbox_ref_task_pairing.md` is the one "history" file that is actually live policy**: it instructs `/inbox` to create paired assessment tasks in `brain/TODO.md`, and it is folded into every session's system prompt. Left untouched per the fence, but flagged loudly — until it is updated to name a goal backlog, the ritual it governs will keep aiming at a deleted file, which is precisely the "leaving the type declared regenerates it" failure this front exists to prevent.

## Plan Review (adversarial, assume small executors)
- *A medium executor reading "fold the TODO lines into goals" would batch by section and invent one summary item per section — the exact failure the ruling names.* → Fixed: the Fold Map decides every line in advance; T2/T3 are pure application, and no row says "decide".
- *A medium executor would translate the Portuguese items to English while "cleaning up", or drop the process number / email / URL / CLI flags as noise.* → Fixed: three rows carry an explicit **keep verbatim** instruction, and the Fold Map preamble makes translation a C1 loss. Still the highest residual risk in the chain, so T2/T3 run at effort=high.
- *"Delete the stale ones" is the obvious shortcut, and 20 of these lines look stale.* → Fixed: exactly 7 DELETE rows exist, each naming a file and line number holding the duplicate. Every other row has a destination; a row without a named duplicate may not be deleted.
- *An executor would hand-edit `.claude/commands/*.md` and `brain/CONTEXT.md`, then watch the next save revert them.* → Fixed: T7 names the source-then-sync-skills route, T8 names the synchronizer, and § Traps says why.
- *An executor would "finish the rename properly" by registering `TODO.md` as a retired token, turning verify-fast red.* → Fixed: § Traps forbids it and explains the test that would fail.
- *An executor would tick the drive-queue checkboxes to "clean up" while moving them, or normalise the arrows.* → Fixed: T4's done-when is a count of `- [ ]` rows == 31, which a re-tick breaks.
- *T1 was medium in the first pass, but `brain/SPECS.md`'s ease-start quality bar demands real links, numbered steps and a 5–10 min ceiling — a medium executor writes "open Drive and start downloading".* → Tier raised on T1 to **high**; `[brave-conta-padrao]` is named in the Fold Map as the zero-decision ease-start candidate.
- *Loop 2 will read "branch:" and try to create it, colliding with the concurrent session in a shared worktree.* → Fixed: the § Plan branch line says pinned, already checked out, verify-only, no `checkout -b`.
- *`ISSUES.md` is fenced but the OR-gate row says "see ISSUES.md" — an executor would add the missing bug entry.* → Fixed: that Fold Map row records the grep result (no such entry exists), instructs carrying the detail into the goal item, and drops the pointer.

verdict: PASS — 3 passes run, zero unresolved FATALs.

executor: craft-high model=anthropic/claude-opus-4.8 tier=high deleg=none
