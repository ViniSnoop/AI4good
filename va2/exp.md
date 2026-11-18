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

**o número que derruba a hipótese:** falso positivo acima de 10% (pois rotular alertas legítimos ou opiniões enfáticas como manipulação quebra a confiança do usuário), F1-macro abaixo de 0.70, ou tempo de inferência por post acima de 1,0 s na CPU, avaliado em 30 postagens de teste.

**escrito antes de ver o resultado:** commit registrado no repositório antes de rodar qualquer piloto.

### 2.2 · métricas e ablação

### 2.3 · dados, participantes e ética

### 2.4 · o piloto: o que rodei, o que deu, o que mudou no desenho

## 3 · E2 · o rótulo pedagógico reduz a propensão ao engajamento reativo

### 3.1 · hipótese, linhas de base e o número que derruba

**a hipótese:** ao visualizar postagens com retórica apelativa no feed, leitores expostos ao rótulo pedagógico (*nudge* do FiltroSoberano) reduzem a intenção de engajamento/compartilhamento por impulso em pelo menos 25% em relação ao feed sem intervenção, e acionam o botão de discordância (passo 7a) em menos de 1 em cada 5 análises ($\le 20\%$).

**o jeito de hoje:** navegação padrão no feed sem qualquer intervenção (*status quo* da timeline do X/Reddit, onde o usuário consome e reage diretamente sob o estímulo visceral do post).

**o competidor mais forte:** aviso genérico de plataforma ("*Conteúdo potencialmente enganoso / não verificado*"), similar aos rótulos institucionais de moderação e ao formato inicial do *Community Notes*. Mede se a explicação pedagógica da falácia específica induz mais reflexão do que um aviso punitivo/genérico.

**o número que derruba a hipótese:** redução na intenção de engajamento por impulso inferior a 15% em relação ao controle, ou taxa de contestação/discordância do rótulo pedagógico acima de 25%, avaliado com 20 postagens por participante.

**escrito antes de ver o resultado:** commit registrado no repositório antes de rodar qualquer piloto.

### 3.2 · métricas e ablação

### 3.3 · dados, participantes e ética

### 3.4 · o piloto: o que rodei, o que deu, o que mudou no desenho

## 4 · o que mudou na ideia, sem IA

## 5 · auditoria cega
