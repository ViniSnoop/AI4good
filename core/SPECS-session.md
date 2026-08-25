# Session and subagents
> How a session closes, and who carries context when work is handed off.
> governs: core/skills/roundup.md, core/hooks/session/, core/hooks/read/agent-context.py

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

8. **O fechamento CONTA a INBOX; quem drena é a sessão seguinte** (2026-08-25). Drenar abre links
   com as ferramentas de vídeo e web — o trabalho mais caro daqui — no turno mais caro. Um close
   drenou zero *por causa* do preço e deixou 19 entradas. A contagem já chega de graça pelo
   `INBOX-NUDGE` do SessionStart; o close só a repassa como `Next action` do `/handoff`.

9. **Qual linha o script imprime é assunto do script.** As skills copiam verbatim e não nomeiam
   nenhuma: uma lista de rótulos em prosa é segunda cópia que apodrece sem quebrar nada — as duas
   prometiam três linhas enquanto o script imprimia seis. O que a sessão custou e se o workspace
   encolheu vêm primeiro; o resto é estado para a próxima sessão.

Guardas: 20 testes em [`core/tools/test/wos/`](tools/test/wos/CONTEXT.md) — a ferramenta contra
workspaces descartáveis, as skills contra reinlinar o trabalho que o script assumiu.

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
