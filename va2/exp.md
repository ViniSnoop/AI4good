# exp · Vinícius Fernandes de Souza

> folha do artefato [desenho dos experimentos](https://lucassf.pages.dev/ai4good/artefatos/3-desenho-dos-experimentos). os pré-registros e pilotos estão no repositório.

## 0 · a minha ideia, e o que ficou para medir

**FiltroSoberano · Extensão de Navegador.** Leitores, debatedores e produtores de conteúdo utilizam uma extensão de navegador open-source para Chrome, Firefox e Brave ao navegar no X/Twitter, Reddit, YouTube e WhatsApp Web. Em vez de varreduras pesadas em segundo plano, a extensão opera **sob demanda**: ao passar o mouse ou clicar em um botão de atalho em uma postagem suspeita, o modelo de decisão **Laya Multilíngue (Sistema 1, pesos abertos)** avalia em passada única a estrutura do texto localmente no navegador (via WebGPU/ONNX Runtime Web). O modelo afere objetivamente marcadores de retórica apelativa: pontua a intensidade de pânico moral e urgência fabricada (`score`) e diagnostica táticas formais como ataque pessoal (*ad hominem*) e falso dilema (`choice`). O post nunca é censurado ou ocultado; o usuário recebe um rótulo pedagógico (*nudge*) sutil com a técnica identificada e tem a opção de marcar falso positivo (passo 7a), municiando-se de clareza crítica e argumentos frios para não reagir por impulso nem ser manipulado por polarização artificial.

**o que eu medi no tec:** no tec (§ 3 e § 5), a execução do Laya na CPU (`convaiinnovations/laya` via PyTorch) levou menos de 1 segundo por post na triagem de 3 postagens sintéticas em português simulando feeds de redes sociais. O modelo acertou a presença de apelo e urgência no post alarmista (`score 1.91`, urgência `0.92`), mas cometeu erros na separação fina de classes com o checkpoint genérico em inglês: confundiu ataque pessoal com pânico moral (prob 0.34) e falso dilema com ataque pessoal (prob 0.31), com aviso de probabilidades não calibradas (`uncalibrated`). A viabilidade de Sistema 1 sem latência perceptível (<1 s) foi comprovada, descartando a SLM generativa pesada e apontando para o checkpoint multilíngue oficial quantizado (`convaiinnovations/laya-multilingual`, 322M parâmetros) via `onnxruntime-web`.

**o que o flx deixou para o experimento:** a SLM generativa local foi descartada (a explicação virou dicionário estático mapeado ao diagnóstico do Laya); a checagem de tamanho mínimo (<15 caracteres) virou regra antes da IA; o passo 7a incorporou a conferência humana (botão de discordância/falso positivo); e a arquitetura foi fixada para inferência em RAM local via WebGPU/ONNX. Ficou para o experimento medir: (1) na técnica, se o modelo diagnostica com precisão táticas de manipulação retórica em postagens em português sem gerar falsos positivos em linguagem coloquial enfática ou alertas legítimos, e qual o impacto do erro silencioso (falso negativo não avisado ou falso positivo desnecessário); (2) no usuário, se a exibição do rótulo pedagógico (*nudge*) *in-situ* de fato induz distanciamento reflexivo (reduzindo intenção de compartilhamento/reação por impulso) e como o usuário interage com o botão de discordância (passo 7a) sem fadiga cognitiva.

## 1 · os experimentos e a comunidade de cada um

| exp. | a pergunta que ele responde | o que é testado | a comunidade e os veículos | o experimento publicado que eu sigo |
|:--|:--|:--|:--|:--|
| E1 | O classificador local diagnostica marcadores de retórica apelativa e falácias formais em postagens em português sem gerar falsos positivos em posts cotidianos legítimos? | a técnica | Processamento de Linguagem Natural e Inteligência Artificial: ACL, EMNLP, NAACL, COLING | [Da San Martino et al., EMNLP 2019](https://aclanthology.org/D19-1565/): *Fine-Grained Analysis of Propaganda in News Articles*. Mede a tarefa real de identificar técnicas de persuasão e apelo emocional com F1 por classe e separação de fragmentos |
| E2 | A injeção in-situ do rótulo pedagógico (nudge) reduz a intenção de compartilhamento por impulso e induz distanciamento reflexivo no leitor de redes sociais? | uma pessoa usando, num nicho (redes sociais / desinformação) | Interação Humano-Computador, Ciências Comportamentais e Redes: CHI, CSCW, Nature Human Behaviour | [Pennycook et al., Nature 2021](https://doi.org/10.1038/s41586-021-03344-2): *Shifting attention to accuracy can reduce misinformation online*. Experimento controlado de intervenção in-situ em rede social medindo discernimento e taxa de compartilhamento sob nudge vs. feed padrão |

## 2 · E1 · o classificador diagnostica retórica manipulativa em português

### 2.1 · hipótese, linhas de base e o número que derruba

**a hipótese:** em postagens em português simulando feeds de redes sociais, o Laya Multilíngue identifica a presença de retórica apelativa e falácias formais com F1-macro $\ge 0.75$, com taxa de falso positivo $\le 10\%$ (acusar post neutro ou alerta legítimo de manipulação) e latência de inferência local inferior a 1,0 s por post na CPU.

**o jeito de hoje:** heurística determinística baseada em regras e expressões regulares (regex de termos ofensivos explícitos, listas estáticas de vocabulário alarmista e padrões conectivos "ou... ou" de falso dilema). Mostra se o modelo de linguagem estruturado realmente agrega valor discriminativo sobre palavras-chave estáticas.

**o competidor mais forte:** o PropaLens e o Vigil não possuem modelos locais calibrados para língua portuguesa nem rodam no nosso dataset de teste. No lugar, um caminho alternativo maior, na nuvem: `gpt-4o-mini` com prompt estruturado de classificação de falácias nos mesmos posts. Ele não representa a extensão local com privacidade, mas serve de teto de desempenho para quantificar o preço pago pela inferência local no navegador.

**o número que derruba a hipótese:** falso positivo acima de 10% (pois rotular alertas legítimos ou opiniões enfáticas como manipulação quebra a confiança do usuário), F1-macro abaixo de 0.75 (qualquer F1 < 0.75 refuta a hipótese, eliminando zonas cinzentas de tolerância), ou tempo de inferência por post acima de 1,0 s na CPU, avaliado em 30 postagens de teste.

**escrito antes de ver o resultado:** commit [567c6fc](https://github.com/ViniSnoop/AI4good/commit/567c6fc), anterior à execução de qualquer piloto e à tabela de resultados.

### 2.2 · métricas e ablação

| métrica | o que mede | por que esta, e não outra | de onde vem |
|:---|:---|:---|:---|
| F1-macro das táticas | média harmônica balanceada entre as classes formais | mede o acerto sem deixar classes raras dominarem a avaliação | [Da San Martino et al., EMNLP 2019](https://aclanthology.org/D19-1565/) |
| **falso positivo (alarme falso)** | post neutro ou alerta legítimo classificado indevidamente como manipulação | se for frequente, o usuário desinstala o app por excesso de alertas indevidos (*crying wolf*) | predição seletiva ([Geifman e El-Yaniv, NeurIPS 2017](https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html)) |
| **falso negativo (erro silencioso)** | post apelativo manipulativo que passa sem qualquer aviso | **é o erro que ninguém percebe**: o leitor consome a manipulação achando que o post foi "aprovado" | o mesmo ([Geifman e El-Yaniv, NeurIPS 2017](https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html)); métrica central da hipótese |
| acurácia exata de tática (`choice`) | acerto do rótulo específico da falácia diagnosticada | separa se o modelo apenas detectou pânico genérico ou se identificou a falácia correta | Da San Martino et al. (2019) |
| latência por post (s) | tempo de execução do forward pass local em CPU | se for acima de 1 s, gera travamento e atrito perceptível na rolagem do feed | benchmarks de inferência local e ONNX Web |

| ablação: o que eu tiro ou troco | o que espero ver | o que ela prova sobre a ideia |
|:---|:---|:---|
| heurística de regras/regex (jeito de hoje) | alto falso negativo e falso positivo em ironia e gírias | que expressões regulares estáticas não compreendem a sintaxe argumentativa |
| Laya Multilíngue completo (local, INT8) | equilíbrio ótimo de F1 com latência <1 s | que o checkpoint multilíngue viabiliza Sistema 1 local no navegador |
| ablação: checkpoint base em inglês (`laya-base`) | confusão de classes e dispersão de probabilidade no português | que pesos multilíngues são indispensáveis para posts em português |
| ablação: sem regra de tamanho mínimo (<15 chars, passo 3) | explosão de falsos positivos em interjeições ("KKKK", "mentira!") | que a regra estática de pré-filtragem do fluxograma faz falta antes da IA |
| competidor alternativo na nuvem (`gpt-4o-mini`) | F1 alto, mas dependência de rede, latência oscilante e sem privacidade | quantifica o preço da privacidade e da soberania da execução local |

**como vou reportar a incerteza:** intervalo de confiança de 95% via bootstrap estratificado sobre as postagens (1.000 reamostras). Como a inferência local com pesos fixos e temperatura zero é determinística, a incerteza reflete a amostragem do corpus de teste.

### 2.3 · dados, participantes e ética

| | resposta |
|:---|:---|
| origem dos dados | amostra de postagens públicas em português do X/Twitter e Reddit de debates públicos, combinada com checagens de fatos (Aos Fatos/Lupa) e notícias factuais de controle (Defesa Civil, meteorologia e reportagens) |
| quantos, e por que esse número | 120 postagens no experimento final (60 manipulativas com classes balanceadas: ad hominem, pânico moral, falso dilema; e 60 controles legítimos/neutros). Pela aproximação normal de proporções ($1{,}96\sqrt{\frac{p(1-p)}{n}}$), 60 controles para $p=0{,}10$ produzem margem de erro amostral de $\pm 7{,}6$ pontos percentuais a 95% de confiança ([Fleiss et al., 2003](https://doi.org/10.1002/0471445428)). No piloto do semestre: 30 postagens de teste |
| como coletar e quem faz o gabarito | coleta de texto público sem metadados pessoais; gabarito independente por 2 anotadores sob a taxonomia de Da San Martino et al. (2019), reportando a concordância de Kappa de Cohen ($\kappa$). Discordâncias resolvidas por terceiro revisor |
| ajuste $\times$ teste | 40 postagens separadas exclusivamente para calibrar limiares de probabilidade e regras; 80 postagens mantidas cegas para o teste definitivo |
| consentimento e comitê de ética | dispensado de submissão ao CEP conforme Resolução CNS 510/2016 (Art. 1º, parágrafo único, incisos II e III) por utilizar apenas textos de domínio público em bancos de dados sem identificação individual |
| dados pessoais e descarte | nenhum dado pessoal é coletado ou retido. O corpus contém apenas o texto das postagens com menções de usuários e links removidos (§ 3 do flx) |
| como coletar e quem faz o gabarito | coleta de texto público sem metadados pessoais; gabarito independente por 2 anotadores sob a taxonomia de Da San Martino et al. (2019), reportando a concordância de Kappa de Cohen ($\kappa$) |
| ajuste $\times$ teste | 40 postagens separadas exclusivamente para calibrar limiares de probabilidade e regras; 80 postagens mantidas cegas para o teste definitivo |
| consentimento e comitê de ética | dispensado de submissão ao CEP conforme Resolução CNS 510/2016 (Art. 1º, parágrafo único, incisos II e III) por utilizar apenas textos de domínio público em bancos de dados sem identificação individual |
| dados pessoais e descarte | nenhum dado pessoal é coletado ou retido. O corpus contém apenas o texto das postagens com menções de usuários e links removidos (§ 3 do flx) |

### 2.4 · o piloto: o que rodei, o que deu, o que mudou no desenho

**o script e o commit:** [piloto_e1.py](exp/piloto_e1.py) executado no repositório sobre o corpus de 30 postagens de [dataset_piloto.json](exp/dataset_piloto.json) (15 manipulativas cobrindo pânico moral, ad hominem e falso dilema; e 15 de controle cobrindo notícias factuais, alertas da Defesa Civil com a palavra "URGENTE" e textos curtos).

**a tabela, colada como saiu:**

| condição | F1-macro [IC 95%] | falso positivo [IC 95%] | falso negativo (silencioso) | acurácia tática | latência (s) |
|:---|---:|---:|---:|---:|---:|
| Linha de base: Regras determinísticas (Regex) | 0.67 [0.42–0.84] | 27% [7%–50%] | 33% [9%–59%] | 67% [50%–83%] | 0.000 s |
| Laya Multilíngue completo (Local CPU) | 0.26 [0.11–0.41] | 47% [22%–72%] | 53% [27%–80%] | 37% [20%–53%] | 1.114 s |
| Ablação: Sem regra de tamanho mínimo (<15c) | 0.26 [0.11–0.41] | 47% [22%–72%] | 53% [27%–80%] | 37% [20%–53%] | 1.160 s |
| Ablação: Checkpoint base em inglês | 0.52 [0.30–0.68] | 33% [11%–57%] | 20% [0%–46%] | 57% [40%–73%] | 0.329 s |
| Competidor alternativo: Nuvem (GPT-4o-mini) | 0.95 [0.78–1.00] | 0% [0%–0%] | 0% [0%–0%] | 97% [90%–100%] | 0.450 s |

**o que o piloto prova, e o que ele não prova:** a hipótese pré-registrada não se sustentou no modelo genérico local em CPU: a taxa de falso positivo atingiu 47% [22%–72%] (quase cinco vezes o teto de 10%) e o erro silencioso (falso negativo) foi de 53% [27%–80%], com latência de 1,114 s na CPU. O piloto prova empiricamente por que a linha de base de regras estáticas quebra no mundo real: ela gerou 27% de falso positivo acusando os alertas legítimos da Defesa Civil de pânico moral apenas pela presença das palavras "URGENTE" e "ALERTA". O piloto confirma o alerta oficial do runtime do Laya (`invalid temperatures... treat confidence as uncalibrated`): sem calibração prévia de probabilidades (RLCD), o checkpoint dispersa a confiança e confunde termos informais brasileiros. O competidor na nuvem atingiu F1 de 0,95 com 0% de falsos positivos, escancarando a distância entre modelos gigantes e encoders locais compactos. O piloto não prova nada sobre o desempenho final do modelo multilíngue calibrado e quantizado em INT8 via WebGPU (`onnxruntime-web`), pois rodou o checkpoint cru em PyTorch/CPU sem fine-tuning.

**o que mudou no desenho por causa dele:** (1) o modelo local exige calibração formal de temperatura/probabilidades antes de definir o limiar de ativação do badge, caso contrário o alarme falso (47%) destrói a usabilidade da extensão. (2) na CPU pura a latência ultrapassou 1,0 s (1,114 s): a extensão no navegador terá que obrigatoriamente rodar os pesos quantizados INT8 com aceleração via WebGPU para manter o tempo abaixo de 500 ms. (3) alertas oficiais legítimos precisam de uma lista de exceção ou verificação de entidade antes do envio para a inferência.

## 3 · E2 · o rótulo pedagógico reduz a propensão ao engajamento reativo

### 3.1 · hipótese, linhas de base e o número que derruba

**a hipótese:** ao visualizar postagens com retórica apelativa no feed, leitores expostos ao rótulo pedagógico (*nudge* do FiltroSoberano) reduzem a intenção de engajamento/compartilhamento por impulso em pelo menos 25% em relação ao feed sem intervenção, e acionam o botão de discordância (passo 7a) em menos de 1 em cada 5 análises ($\le 20\%$).

**o jeito de hoje:** navegação padrão no feed sem qualquer intervenção (*status quo* da timeline do X/Reddit, onde o usuário consome e reage diretamente sob o estímulo visceral do post).

**o competidor mais forte:** aviso genérico de plataforma ("*Conteúdo potencialmente enganoso / não verificado*"), similar aos rótulos institucionais de moderação e ao formato inicial do *Community Notes*. Mede se a explicação pedagógica da falácia específica induz mais reflexão do que um aviso punitivo/genérico.

**o número que derruba a hipótese:** redução na intenção de engajamento por impulso inferior a 25% em relação ao controle (qualquer redução < 25% refuta a hipótese), ou taxa de contestação/discordância do rótulo pedagógico acima de 20%, avaliado com 20 postagens por participante.

**escrito antes de ver o resultado:** commit [567c6fc](https://github.com/ViniSnoop/AI4good/commit/567c6fc), anterior à execução de qualquer piloto e à tabela de resultados.

### 3.2 · métricas e ablação

| métrica | o que mede | por que esta, e não outra | de onde vem |
|:---|:---|:---|:---|
| taxa de engajamento impulsivo (%) | proporção de posts manipulativos em que o leitor declara intenção de compartilhar/retuitar | é a medida comportamental clássica de propagação de desinformação | [Pennycook et al., Nature 2021](https://doi.org/10.1038/s41586-021-03344-2) |
| tempo de reflexão / inspeção (s) | segundos que o participante observa o post antes de decidir agir | mede se o leitor pausou o Sistema 1 e ativou reflexão deliberada de Sistema 2 | modelos de tempo de reação em IHC (CHI) |
| taxa de discordância / falso positivo (passo 7a) | frequência com que o usuário clica em "Discordar / Falso Positivo" | mede o trabalho de correção e calibração humana sobre a IA | [Jahanbakhsh & Karger, CHI 2024](https://doi.org/10.1145/3613904.3642473) |
| carga cognitiva e aceitação (SUS reduzido) | facilidade de leitura e percepção de não intrusividade do badge | garante que o rótulo pedagógico não polui o feed nem gera fadiga | usabilidade e IHC |

| ablação / condição testada | o que espero ver | o que ela prova sobre a ideia |
|:---|:---|:---|
| Condição A: controle (feed padrão sem app) | alta taxa de engajamento impulsivo e menor tempo de leitura | linha de base do comportamento habitual do leitor |
| Condição B: FiltroSoberano completo (rótulo pedagógico + passo 7a) | redução de $\ge 25\%$ no compartilhamento impulsivo e aumento no tempo | que a explicação didática da falácia induz postura reflexiva |
| Condição C: competidor com aviso genérico ("Conteúdo Suspeito") | menor redução de impulso que a explicação e risco de efeito reverso | que apontar a falácia específica educa mais que um rótulo punitivo |
| Condição D: ablação sem botão de discordar (sem passo 7a) | menor aceitação e sensação de censura algorítmica opaca | que a agência humana de contestação é essencial para a confiança |

**como vou reportar a incerteza:** diferença média pareada (Condição B − Condição A) por participante, com intervalo de confiança de 95% via bootstrap sobre os voluntários (sem caça a valor-p, conforme [Dragicevic, 2016](https://doi.org/10.1007/978-3-319-26633-6_13)).

### 3.3 · dados, participantes e ética

| | resposta |
|:---|:---|
| origem dos participantes | leitores e debatedores adultos de redes sociais no Brasil que utilizam navegadores desktop |
| quantos, e por que esse número | para o artigo científico definitivo: 40 a 50 participantes em desenho pareado *within-subjects* contrabalanceado em quadrado latino, garantindo poder estatístico (>0.80) para detectar reduções de tamanho de efeito moderado ($d \ge 0.45$) em intenção de compartilhamento ([Pennycook et al., Nature 2021](https://doi.org/10.1038/s41586-021-03344-2)). Para o piloto do semestre: 1 persona de IA rodando sobre o harness de software exclusivamente para verificar integridade de scripts e fluxo de eventos |
| desenho experimental | contrabalanceamento em quadrado latino: cada participante avalia 20 postagens (10 no feed padrão controle e 10 com o FiltroSoberano ativo), alternando a ordem de apresentação para eliminar viés de aprendizagem |
| consentimento e comitê de ética | projeto pronto para submissão ao Comitê de Ética em Pesquisa (CEP/CONEP via Plataforma Brasil) para a coleta humana do artigo (Res. CNS 510/2016 e Lei 14.874/2024), acompanhado de Termo de Consentimento Livre e Esclarecido ([tcle.md](tcle.md)). O piloto do semestre roda com dados sintéticos e persona técnica de software, sendo dispensado de parecer prévio por não envolver intervenção sobre seres humanos |
| dados pessoais e descarte | logs identificados apenas por código alfanumérico anônimo (P01, P02), registrando estritamente tempos de leitura e escolhas de clique. Não há captura de voz, vídeo, cookies ou navegação pessoal. Dados armazenados em máquina local e destruídos após o fechamento da pesquisa |

### 3.4 · o piloto: o que rodei, o que deu, o que mudou no desenho

**o script e o commit:** [piloto_e2.py](exp/piloto_e2.py) simulando 8 sessões contrabalanceadas em quadrado latino com 20 postagens por sessão (10 manipulativas e 10 legítimas) sob as 4 condições do experimento. A execução utilizou harness automatizado de software para registrar eventos de leitura, decisões de compartilhamento e cliques no botão de contestação.

**a tabela, colada como saiu:**

| condição | compartilhamento reativo [IC 95%] | tempo de inspeção (s) [IC 95%] | taxa de discordância (7a) [IC 95%] |
|:---|---:|---:|---:|
| Condição A: Controle (Feed padrão sem app) | 63.7% [55.0%–72.5%] | 3.25 s [3.13–3.36 s] | 0.0% [0.0%–0.0%] |
| Condição B: FiltroSoberano completo (Pedagógico + 7a) | 35.0% [28.8%–41.2%] | 6.25 s [6.06–6.43 s] | 15.6% [13.7%–17.5%] |
| Condição C: Competidor (Aviso genérico de plataforma) | 47.5% [42.5%–53.8%] | 4.55 s [4.42–4.69 s] | 0.0% [0.0%–0.0%] |
| Condição D: Ablação sem botão de contestação (sem 7a) | 40.0% [32.5%–47.5%] | 5.57 s [5.39–5.73 s] | 0.0% [0.0%–0.0%] |

**o que o piloto prova, e o que ele não prova:** o piloto prova que a infraestrutura de medição e registro de eventos da extensão funciona de ponta a ponta: o harness captura os tempos de leitura, as decisões de compartilhamento e os cliques no botão de discordância (passo 7a) sem perda de dados e sem travar a interface. A taxa de discordância registrada na condição B foi de 15,6% [13,7%–17,5%], operando dentro do limiar de tolerância aceitável pré-registrado ($\le 20\%$). No entanto, **o piloto não prova absolutamente nada sobre o comportamento de leitores humanos reais**: os números refletem uma simulação controlada de software desenhada exclusivamente para validar se os scripts e o protocolo de coleta funcionam antes de levar o projeto a campo ou ao comitê de ética.

**o que mudou no desenho por causa dele:** (1) o registro de tempo de inspeção exige um teto de corte (*timeout* de 30 s) para descartar sessões em que o voluntário simplesmente trocou de aba ou se distraiu durante a leitura. (2) o botão de contestação do passo 7a precisa registrar o motivo específico da discordância ("Falso positivo: o post é legítimo" versus "Discordo do nome da falácia") para não misturar erro de detecção com divergência de taxonomia na análise estatística definitiva.

## 4 · o que mudou na ideia, sem IA

O Laya cru em CPU não sustenta a hipótese (47% de falsos positivos e 1,11 s de latência): a calibração de probabilidades (RLCD) e a quantização INT8 acelerada em WebGPU viraram pré-requisitos obrigatórios.  
A regra determinística de regex quebrou em alertas legítimos (27% de falso positivo): alertas oficiais (Defesa Civil) precisam de lista de bypass prévia antes de qualquer análise.  
A ablação do E2 evidenciou a necessidade de uma condição de controle visual neutro de mesmo tamanho, isolando o efeito da explicação didática da simples interrupção atencional.  
O passo 7a do fluxograma incorporou distinção entre discordância de tática e falso positivo factual, prevenindo que divergências conceituais contaminem o indicador de erro da IA.

## 5 · auditoria cega

**o veredito da conversa nova (Auditor Cético):**

| Item | Passa ou não passa | Trecho que prova | O que encontrei |
|:---|:---|:---|:---|
| E1 — Hipótese falsificável | PASSA, com ressalvas | §2.1: F1-macro ≥ 0,75, falso positivo ≤ 10% e latência < 1 s | Critérios mensuráveis e refutáveis; limiar unificado sem zonas cinzentas de tolerância |
| E1 — Linha de base | PASSA | §2.1: heurística determinística baseada em regex | Linha de base concreta; piloto revelou que a regex gera 27% de falso alarme |
| E1 — Limiar prévio | PASSA (verificado no git local) | §2.1: commit `567c6fc` | Commit registrado localmente no repositório antes de rodar os scripts de piloto |
| E1 — Métricas | PASSA | §2.2: F1-macro, falso positivo, falso negativo silencioso e latência | Métricas fundamentadas em Da San Martino (2019) e Geifman & El-Yaniv (2017) |
| E1 — Ablação | PASSA | §2.2: regex, checkpoint inglês, regra de tamanho e nuvem | Demonstrou perda no inglês e que a regra estática evita falsos alarmes em interjeições |
| E1 — Piloto | PASSA (como teste negativo honesto) | §2.4: 30 postagens; F1 de 0,26 e falso positivo de 47% | O piloto refutou a hipótese original; autor admitiu a falha sem maquiar os dados |
| E1 — Dados e ética | PASSA | §2.3: 120 postagens com anotação dupla; dispensa Res. 510/2016 | Margem corrigida para ±7,6 pp; dispensa justificada por textos públicos sem metadados |
| E2 — Hipótese falsificável | PASSA | §3.1: redução de ≥ 25% e contestação ≤ 20% | Hipótese com números claros que podem ser falsificados por dados de campo |
| E2 — Linha de base | PASSA | §3.1: feed padrão sem intervenção | Comparação direta e natural do status quo de consumo de redes |
| E2 — Limiar prévio | PASSA | §3.1: commit `567c6fc` | Registrado antes da execução do piloto de software |
| E2 — Métricas | PASSA | §3.2: compartilhamento, tempo de inspeção, discordância e SUS | Métricas comportamentais clássicas de intervenção online (Pennycook et al., 2021) |
| E2 — Ablação | PASSA | §3.2: condições A, B, C e D | Compara feed padrão, pedagógico, aviso genérico institucional e sem botão 7a |
| E2 — Piloto com pessoas | PASSA (com ressalva metodológica) | §3.3 e §3.4: persona de IA em harness de software | Válido estritamente como teste de código e eventos; folha declara que não mede humanos |
| E2 — Dados e participantes | PASSA | §3.3: 40 a 50 participantes previstos para o artigo | Amostra planejada com poder estatístico adequado para o estudo definitivo |
| E2 — Ética | PASSA | §3.3: TCLE elaborado ([tcle.md](tcle.md)) e previsão de submissão ao CEP | Protocolo ético pronto para submissão; piloto de software dispensado de parecer |

**a minha resposta, sem IA:**
1. Realmente tinha ficado uma área cinzenta entre 0,70 e 0,75 que agora já foi corrigida, deixando a regra de reprovação estrita em F1 < 0,75 e registrada antes do piloto.
2. Ainda temos que planejar um refino/calibração de probabilidades (RLCD) e quantização para o Laya antes de ir para produção, pois o modelo cru na CPU errou muito no piloto.
3. No contexto da disciplina vai ter que ser só com a IA mesmo para validar os scripts e o harness, não tem como fazer o teste com 24 pessoas agora, impossível; o teste com pessoas fica como protocolo futuro com o TCLE para o CEP. 

