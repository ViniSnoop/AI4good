# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

LINHA DE BASE do port, medida hoje em Windows sem bash nenhum: 433 passam, 138 falham, 1 skip de 572.
E a categoria das falhas mudou meu entendimento do trabalho: só 96 são exec/shebang (OSError +
FileNotFoundError, esperadas). As outras 150 são AssertionError de UM padrão só — o código emite
`C:\Users\lucas\workspace\academy\papers` onde o teste espera `academy/papers`. O pathlib resolveu o
SISTEMA DE ARQUIVOS e não resolveu o VOCABULÁRIO DE PATH: toda vez que um path vira texto (linha de
routing table, chave de registry, linha do ISSUES.md, comparação com features.txt) ele sai no
separador do SO. Proposta: barra normal, sempre, para todo path que é DADO — `.as_posix()` no
boundary, Path só para tocar disco. É o que o git faz internamente há 20 anos. E não é concessão a
Windows: torna routing table e entropy dashboard byte-idênticos entre máquinas, que é justamente o
que `test_the_output_is_deterministic` já pede. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

6 falhas de UnicodeDecodeError: parte do código abre arquivo sem `encoding='utf-8'` e pega o default
do SO (cp1252 no Windows brasileiro). Todo `.md` do workspace é UTF-8, então o default do SO nunca é
a resposta certa em lugar nenhum — inclusive em Linux, onde só funciona por acidente de locale.
proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

os hooks NÃO ativam sozinhos depois de um clone, e o SETUP.md afirma que sim. `.claude/settings.json`
e `.zcode/config.json` são versionados com `/mnt/workspace/...` hardcoded em ~20 comandos, e o passo
"Workspace path" só reescreve shebang de core/tools. Em qualquer clone fora daquele path a camada de
enforcement inteira fica morta em silêncio — o modo de falha exato que o deps.txt existe pra eliminar.
Vale pro Windows e vale pro aluno que clonar em ~/wos. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

as três bifurcações por-SO do WOS estão todas quebradas, e isso é argumento e não coincidência:
start-session.ps1 imprime WORKSPACE.md (arquivo que não existe; o real é AGENTS.md) enquanto o .sh
imprime AGENTS.md e ainda se descreve como "Neutral session-start entrypoint"; .agentrc.json aponta
start_session_windows pro .ps1 quebrado; caveman/hooks/activate.js escolhe caveman-statusline.ps1 no
Windows e esse arquivo não existe no repo. A correção não é consertar os .ps1, é deletá-los. Um
entrypoint que roda nos dois. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

a convenção de segredo "dir 700 / file 600" (SETUP-accounts.md, e a entrada de 26/08 sobre os tokens
664/775) não tem equivalente escrito pra nenhum sistema sem modo POSIX. No Windows a permissão é ACL,
não modo. Isso não é um passo de install, é uma pergunta do seam de plataforma: secure_dir() /
secure_file() ao lado de interpretador e package manager. E o Lucas tem razão que deveria vir cedo —
um segredo escrito frouxo não fica seguro depois. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

deps.txt não tem como dizer "esta dep só existe neste sistema", e o caso do secretstorage é pior do
que parece. Medido no Windows hoje: `pip install secretstorage` sai 0 e `import secretstorage` sai 0
— ou seja, a probe declarada em deps.txt fica VERDE. Mas o Secret Service é D-Bus, que só existe em
Linux, então a dep está presente e inútil ao mesmo tempo. É um falso verde, que é pior que um falso
vermelho: a coluna `breaks` promete avisar quando a feature some, e aqui ela não avisa. O redesenho
do `kind` precisa de um teto de aplicabilidade por sistema, e a probe precisa medir função e não
importação. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

o permissions.allow do .claude/settings.json versionado é todo `Bash(git -C * log *)`. Numa máquina
onde o agente chama a tool PowerShell, nenhum desses padrões casa e o usuário leva prompt de permissão
em tudo. Mesma classe do /mnt/workspace: config versionada assumindo um ambiente. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

README.md descreve um WOS que não existe mais: diz que "the registry that would let you switch one off
is unbuilt … Today it is all or nothing", mas features.txt (76 features), profile.txt e
`wos/features --on|--off` estão lá e funcionam. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

estudar uma forma de 

acho que vale a pena mudar o momento do aviso do limite da "context window" pra aparecer sempre no final de cada resposta de forma que eu, usuário, veja ela. 

https://www.instagram.com/reel/DcimG9JtYGp/?utm_source=ig_web_copy_link
talvez ajude como estratégia pra analisar e simplificar o WOS
— via aiwbot · 2026-08-27

https://www.instagram.com/reel/DcbkoD5R3U4/?utm_source=ig_web_copy_link
tem a ver com ideias de startapps minhas
— via aiwbot · 2026-08-27

terminar o port dos materiais das aulas (teaching) do drive do cin para o drive pessoal

quero fazer isso
https://askubuntu.com/questions/1368874/can-google-drive-desktop-be-used-on-ubuntu
para ter o gdrive pessoal linkado com o WOS nas pastas relevantes, acho que principalmente a academy. tem que estudar como fazer esse setup direitinho e principalmente conceitualmente, como vai funcionar esse "versionamento híbrido", WOS, subpastas, github-gdrive, etc...

https://www.instagram.com/reel/Dcdw08PNlPy/?igsi=eWZrNTVrOW9zbGk3
talvez ele esteja certo
hooks > skills > agents > loops/flows
— via aiwbot · 2026-08-25

https://www.instagram.com/p/DcURStsG5o8/?utm_source=ig_web_copy_link&igsi=NTc4MTIwNjQ2YQ==
— via aiwbot · 2026-08-25

https://www.instagram.com/reel/Dcbm_z0REi5/?utm_source=ig_web_copy_link&igsi=NTc4MTIwNjQ2YQ==
aprender essa
— via aiwbot · 2026-08-24

jogar na lixeira o deck `__probe_delete_me` no Drive pessoal (sonda de auth, criada por engano)
— moved here from the old to-do file · 2026-08-24

revisar artigo do svr — prazo original ~25/07, já vencido; decidir se ainda vale a pena
— moved here from the old to-do file · 2026-08-24

responder o desafio público do Jake Van Clief com nossas ideias/visão — ele julga os 3 comentários mais curtidos, janela
curta (reel: https://www.instagram.com/reel/DbWA6VOxVq-/)
— moved here from the old to-do file · 2026-08-24

no Brave, ativar aceleração de buscas por site — o atalho da barra de endereço que o Lucas usava no Chrome (`y` + Tab
abre a busca do YouTube ali mesmo); o trabalho não é ativar, é levantar quais ferramentas valem um atalho: Maps e Google
Tradutor são certos, Amazon/Mercado Livre/ChatGPT são candidatos com dúvida — decidir a lista com ele antes de
configurar, atalho de uma letra é recurso escasso
— moved here from the old to-do file · 2026-08-24

https://www.instagram.com/p/DcZW29CnMmx/?img_index=3&igsi=MTMzNGlkaHVlbXI3MQ==
pro free ai. no free ai ter um padrão, pra cada setup ter informações padronizadas, o passo a passo, a quantidade e
forma de uso, a precisão/ qualidade, fornecer a fonte, dizer quando isso foi observado e a cada commit checar se o setup
ainda está free ou se foi alterado, ter uma versão um pt-br e outra em en-us... rankear eles por recomendação. lembrar
que o glm 5.3 tá free, que o ox alpha via opencode tbm.
— via aiwbot · 2026-08-24

https://www.usemitra.com.br/produtos?utm_medium=paid&utm_source=ig&utm_id=120247342335620133&utm_content=120247342335580133&utm_term=120247342335590133&utm_campaign=120247342335620133&fbclid=PAaWdyZAT4ExBwZG9mAmV4dG4DYWVtATAAYWRpZAGrNFIgEwUVc3J0YwZhcHBfaWQPNTY3MDY3MzQzMzUyNDI3AAGnHkLlTris8xoRYyaFDZK3tobCLvAKfVyfgrymOnA8lsfJx50uvowAfUiiiX4_aem_W7i1QSnZgfoKNcJgLS7HXA
comprar camisas
— via aiwbot · 2026-08-24

https://www.instagram.com/reel/Dbd8XDWSM1A/?igsi=MXZhejkwZWF0ZzFncw==
colocar um alguma das minhas aulas de ai4good
— via aiwbot · 2026-08-24

montar uma lista de indicações de jogos, filmes, séries, artistas/bandas, álbuns, livros e quadrinhos. na lista ter
links, preços, notas uma mini descrição e talvez algum outro critério de classificação
https://www.instagram.com/reel/DcRMVoSxpNY/?igsi=MThmdjA0eGcxcW54eA==
— via aiwbot · 2026-08-24

https://www.instagram.com/p/Db8TS-UFC8N/?img_index=7&igsi=bHFpNGJsbzhmdHQ0
solarpunk é a vibe de ai4good
— via aiwbot · 2026-08-24

https://www.instagram.com/p/DcY8rf9jUY7/?img_index=5&igsi=MTBtZTRjOGpxc3lmMw==
talvez seja útil pro texpace e spacemantics
— via aiwbot · 2026-08-24

https://www.instagram.com/reel/DY2wj1svR_m/?igsi=MTAwb2dxYWJ3amRkYQ==
— via aiwbot · 2026-08-21

https://www.instagram.com/p/DcQ1847jA8l/?img_index=1&igsi=cHVobWwweWdrc2l1
— via aiwbot · 2026-08-21

https://www.instagram.com/reel/DcTIPKyt7Am/?igsi=bHIxMGJqZnBwbDd5
— via aiwbot · 2026-08-21

https://www.instagram.com/reel/DcQfL4Zty0L/?igsi=MTZ0emxpdzlrdWw0MA==
será que a gente adianta uma liberação geral pro opus?
— via aiwbot · 2026-08-21

https://www.instagram.com/reel/DbQrgz6haNi/?igsi=MWI2bXV1ZXo4dG5kdw==
será que texpace e spacemantics tem a ver com essa semantic layer?
— via aiwbot · 2026-08-21

https://www.instagram.com/p/DbiVrYngBiV/?img_index=3&igsi=MXBud3JkZjIwdnl2aQ==
headroom parece ressoar com a ideia que dei de mipmaps e 3d model lod pra contextos de llm
— via aiwbot · 2026-08-21

tokens OAuth do Google estão 664 e os diretórios 775 — legíveis por qualquer usuário da máquina.
vale um chmod 700/600 em ~/.config/workspace-{drive,drive-write,gmail,docs,forms}. não mexi porque
tightening de permissão pode quebrar outra ferramenta rodando com outro usuário — decisão sua.
— sessão checkpoints de pesquisa · 2026-08-26

doc de sonda de formato ficou no Drive pessoal: "probe-formato-checkpoints". a CLI do gdocs não tem
delete. ou apaga na mão, ou vale um `gdocs trash` na ferramenta.
— sessão checkpoints de pesquisa · 2026-08-26

o repositório público que os alunos clonam (ROADMAP 🟡) virou dependência real: a faixa "com o WOS"
do passo a passo dos checkpoints está escrita e inerte até ele existir. enquanto isso o prazo de
1 mês do LOOP A depende de uma ferramenta que o aluno não tem.
— sessão checkpoints de pesquisa · 2026-08-26
