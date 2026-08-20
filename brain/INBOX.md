# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

https://www.instagram.com/reel/DZIdVD6Rrjl/?igsi=NTc4MTIwNjQ2YQ==
usar esse modelo em AI4Good

definitivamente temos que conectar os goals com os roadmaps. talvez no /roundup. talvez, talvez! automaticamente lançar warning quando fizer um commit de qualquer arquivo RODAMAP*.md para atualizar o goal linkado com aquele roadmap.

não sei onde está o teste de ablação do wos no roadmap... será que a gente jogou fora?

entropy pulou para mais de 800... temos um limite de 200 LOC por arquivo, mas nesse caso diria que o melhor é resolver tudo antes de fazer um split. agora claro, pra cada caso tentar resolver na causa raiz, não de modo superficial. ao mesmo tempo, acho que o ISSUES.md deveria carregar essas medidas de entropia descentralizadas. cada ISSUES.md vai fazer a medida de entropia local. o ISSUES.md raiz coleta dos outros ISSUES.md as medidas de entropia e expõe, faz o roteamento, e também mede a entropia do diretório raiz (WOS)

uma forma de pensar context folding é "mimaps" ou "3D model lod". como texturas e modelos, arquivos de texto poderiam ter versões de resolução máxima + 2 níveis, médio, mínimo, e 1-parágrafo. será que no claude code a gente tem acesso ao contexto? a gente pode manipular o contexto das sessões?

editar a mensagem final do /roundup para incluir a sugestão de no plano já adicionar um /roundup no final e evitar uma troca extra de mensagens com o usuário. isso é só uma ideia, avaliar antes de implantar

o WOS precisa ser avaliado, mais uma vez, suas features, seus arquivos, tá tudo um pouco grande e sinto que um pouco como uma macarronada... acho que o teste de ablação vai ser de fato o principal. vai ajudar a tirar ruído também por que vamos naturalmente perceber cargas desncessárias.

https://www.instagram.com/reel/DcMSk7Rxcdu/?igsi=MWg2ZHJibnFqazFiYQ==
pro nosso teste de ablação
— via aiwbot · 2026-08-19

AGENTS.md não menciona o SPECS.md nem o ROADMAP.md, me pergunto se esse padrão se repete nos CONTEXT.md das subpastas. é isso mesmo? será que não deveríamos incluir pelo menos 1 ponteiro para deixar os agentes cientes desses arquivos? ou eles já ficam cientes por outros caminhos? se o SPECS.md fica escondido aí nos encaminhamos para um drift dos repositórios em que a definição se distancia da execução. outra coisa, fico pensando se não deveríamos incluir os resultados das verificações/testes no BUGS.md, e talvez trocar o nome BUGS.md (não sei se ISSUES.md). poderíamos incluir nele as medições de entropia do repo tbm.

https://www.instagram.com/reel/DbtoVzfkk4M/?igsi=MThnZngwZnZ4dW9zMg==
— via aiwbot · 2026-08-19

https://www.instagram.com/reel/Dbi79TLPs1G/?igsi=MTh0NXByaGh4Ym03dA==
weave again, we should at least trt it at some point
— via aiwbot · 2026-08-19

https://www.instagram.com/p/DcMhaH6AYJR/?img_index=4&igsi=ejlyaTkwOTV6bzVv
— via aiwbot · 2026-08-19

https://www.instagram.com/reel/DcNQt9juXpA/?igsi=MW1qc2c0NXI1djIxeA==
— via aiwbot · 2026-08-19

https://www.instagram.com/reel/DcOCgBkNNjK/?igsi=eHdieGlpbW10cHhi
— via aiwbot · 2026-08-19

matraix deve entrar nas minhas aulas, os practical tweaks pro claude tbm devem ser interessantes
https://www.instagram.com/p/Db3di5dEpS4/?igsi=NTc4MTIwNjQ2YQ==
— via aiwbot · 2026-08-18

WOS roadmap voltou a crescer, bastante! então sugiro voltarmos a investir energia para fechar ele. tá gigante agora. mas logo agora, já hoje, acho que podemos melhorar a carga desse ROADMAP de 1200 linhas. não tem como me convencer que é positivo um arquivo assim tão grande. então talvez possamos agilizar a decisão e colocar ela à frente em prioridade, a decisão se ativamos 200 LOC limit para arquivos .md também. neste caso acho que temos que adicionar um limite de caracteres por linha para os modelos não tornarem isso uma bagunça. e aí nesse caso acho que naturalmente, cada "front" do roadmap acabaria indo para um subarquivo. ou isso, ou fazemos algo mais leve sem o block mas já fazendo a divisão do arquivo. digo isso por que esses 1200 linhas já entram no contexto do agente na primeira mensagem. o custo disso deve ser alto, além da confusão de se ter muitas especificidades sobre várias frentes de uma vez só no contexto.

https://www.instagram.com/p/DcL8ma9DaRs/
sem dúvidas é útil pra gente
— via aiwbot · 2026-08-18

https://www.instagram.com/reel/Db1fYnbyoAX/?igsh=Zng0Y2I2ZXZzMmZq
será que vale um teste?
— via aiwbot · 2026-08-18

https://www.instagram.com/reel/DcJ3PUDyIvS/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==
interessado especialmente nos casos em que podemos rodar algo localmente
— via aiwbot · 2026-08-17
