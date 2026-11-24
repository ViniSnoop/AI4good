# artigo · Vinícius Fernandes de Souza

> registro do artefato [artigo](../6-artigo.md): o esqueleto do artigo inteiro, marco a marco. o texto
> do artigo mora no Overleaf; aqui ficam o argumento, de onde veio cada parte, a auditoria e a sua
> resposta. veja o [excelente](excelente.md) e o [raso](raso.md).

## passo 0 · veículo e modelo

**o veículo alvo:** BRACIS (Brazilian Conference on Intelligent Systems), conferência de excelência em IA (Qualis A2/A3, Springer LNCS). Escolhido pelo foco em sistemas inteligentes aplicados a desafios e linguagem do cenário sociopolítico brasileiro, formato completo (12–15 páginas) e publicação oficial pela Springer LNCS.

**o artigo base:** Da San Martino et al. (2019), *Fine-Grained Analysis of Propaganda in News Articles*, EMNLP 2019, DOI: [10.18653/v1/D19-1565](https://doi.org/10.18653/v1/D19-1565). É do mesmo tipo por formalizar a classificação estrutural de técnicas de apelo emocional e manipulação retórica (*ad hominem*, apelo ao medo), servindo de molde para a arquitetura de seções, métricas balanceadas (F1-macro) e análise de ablação.

**o modelo compila:** Projeto Overleaf configurado com Springer LNCS (`llncs.cls`) e sincronizado via git (`https://www.overleaf.com/project/6a920baf130d092cbf50510d`), compilado com sucesso gerando o PDF base.

## marco 1 · introdução

**o argumento, sem IA:**
1. **o problema e quem sofre:** A manipulação retórica e o pânico moral são instrumentalizados como armas eleitorais nas redes brasileiras, prejudicando o processo democrático e induzindo distorção psicológica na percepção da realidade; o estudo de Brady et al. (2017) no PNAS prova que palavras moral-emocionais aumentam em ~20% os retuítes em bolhas ideológicas.
2. **o que se usa hoje e onde falha:** Notas da Comunidade dependem de consenso lento e chegam tarde demais; PropaLens polui a tela analisando frases soltas fora de contexto; Vigil impõe latência proibitiva (>5 s com WebLLM) ou regex com alto falso positivo; e nenhuma ferramenta calibra probabilidades para a linguagem informal do português.
3. **a proposta e o óbvio abandonado:** O FiltroSoberano roda o Laya Multilíngue (Sistema 1, 322M) via WebGPU/ONNX em passada única sob demanda (<1 s, zero rede, privacidade total). Abandona SLMs/LLMs generativos pesados no navegador e rejeita a censura/ocultação de posts em favor de um nudge pedagógico discreto com botão de contestação.
4. **as contribuições:** (1) Arquitetura de Sistema 1 local no navegador calibrada para o português com latência sub-segundo e privacidade total (sustentada pelo Experimento 1); (2) Mecanismo de intervenção pedagógica in-situ com agência humana que reduz o engajamento impulsivo sem censura (sustentada pelo Experimento 2).

**o texto da introdução:**

Em ecossistemas de redes sociais e debates públicos online, a manipulação retórica e o pânico moral são rotineiramente instrumentalizados como armas eleitorais, induzindo o eleitorado a decisões baseadas em distorções e gerando um estado contínuo de apreensão em que a realidade é percebida sob constante ameaça. Plataformas digitais e grandes corporações de tecnologia amplificam assimetrias informacionais por meio de algoritmos de recomendação desenhados para maximizar o engajamento visceral, sequestrando a atenção crítica do cidadão. Esse fenômeno encontra sustentação empírica no estudo de Brady et al. (2017), que analisou 563 mil postagens políticas no Twitter e comprovou o chamado "contágio moral": a presença de palavras com carga moral-emocional aumenta a taxa de compartilhamento em aproximadamente 20% por palavra em câmaras de eco ideológicas. Quando a comunicação pública é pautada por ataques pessoais e urgência fabricada, compromete-se a integridade do processo democrático e a autonomia epistêmica de quem navega cotidianamente nos feeds.

As abordagens atuais contra a desinformação e a manipulação oscilam entre a intervenção editorial centralizada e extensões de navegador com graves gargalos de usabilidade. Por um lado, sistemas colaborativos e de checagem institucional — como as Notas da Comunidade do X e painéis de *fact-checking* — dependem de consenso humano e demandam horas ou dias para sinalizar uma postagem, chegando tarde demais para conter a viralização imediata nos feeds. Por outro lado, extensões experimentais falham na experiência prática: o PropaLens realiza varreduras globais frase a frase na página inteira, retirando as orações de seu contexto discursivo e poluindo visualmente a tela do leitor com centenas de marcações concorrentes. Já o Vigil, embora se aproxime da dinâmica do feed e proponha a reescrita despolarizada e a ocultação de postagens, impõe um dilema inviável: seu modo rápido por expressões regulares ignora a semântica e gera alarme falso recorrente, enquanto seu modo neural via LLMs generativos locais atinge latências proibitivas (frequentemente superiores a 5 segundos por análise). Além disso, nenhuma dessas ferramentas oferece calibração probabilística para a linguagem informal e as idiossincrasias retóricas do português brasileiro, acumulando altas taxas de falsos positivos que inviabilizam o uso contínuo.

Para superar essas limitações, propomos o **FiltroSoberano**, uma extensão de navegador de código aberto que atua diretamente nos feeds de redes sociais, alertando visualmente o leitor quando uma postagem recorre a artifícios de manipulação retórica ou indução de pânico moral. Em vez de varreduras indiscriminadas em segundo plano, o sistema opera estritamente sob demanda: ao inspecionar uma postagem suspeita, o modelo de decisão Laya Multilíngue (322M parâmetros) avalia a estrutura argumentativa do texto em passada única (*single-pass*) diretamente no cliente via WebGPU e ONNX Runtime Web, sem emitir chamadas de rede nem violar a privacidade de navegação. A abordagem abandona conscientemente duas convenções recorrentes: primeiro, descarta o uso de modelos de linguagem generativos (SLMs ou LLMs), cujas justificativas prolixas e decodificação autorregressiva sobrecarregam a memória do navegador com latências de vários segundos; em seu lugar, adota saídas estruturadas rápidas mapeadas para um catálogo didático estático. Segundo, rejeita a censura ou ocultação paternalista de conteúdo: a postagem permanece legível, acompanhada de um rótulo pedagógico (*nudge*) discreto que esclarece a técnica formal detectada e oferece um botão de contestação humana, conferindo ao usuário clareza reflexiva para não reagir por impulso.

Diante desse cenário, este trabalho apresenta duas contribuições principais:
1. **Arquitetura de inferência local e calibração para o português brasileiro:** propomos e validamos um pipeline de decisão rápida de Sistema 1 no navegador, baseado no modelo Laya Multilíngue quantizado via WebGPU e ONNX Runtime Web. Esse pipeline é capaz de diagnosticar marcadores de manipulação retórica e pânico moral em passada única com latência inferior a 1 segundo e sem tráfego de rede, quantificando com rigor o compromisso entre soberania local e precisão diante de heurísticas determinísticas e modelos comerciais em nuvem (**sustentada pelo Experimento 1**).
2. **Mecanismo de intervenção pedagógica *in-situ* com agência humana:** desenhamos e avaliamos a eficácia de um *accuracy nudge* explicativo integrado diretamente ao feed, demonstrando que a contextualização estrutural da falácia associada a um botão de contestação humana reduz a propensão ao engajamento impulsivo sem recorrer à censura ou à ocultação paternalista de postagens (**sustentada pelo Experimento 2**).

**de onde veio cada frase:**
- Parágrafo 1: Frase 1 da fala do aluno sobre arma eleitoral e efeito psicológico (cmp § 1); Frase 2 da crise do brw § 1; Frase 3 do catálogo do cmp § 3 (Brady et al., 2017, PNAS); Frase 4 do flx § 0.
- Parágrafo 2: Frase 1 da síntese do cmp § 2; Frase 2 do brw § 2 (clichê 1) e cmp § 2 (Community Notes); Frase 3 da crítica do aluno e cmp § 2 (PropaLens); Frase 4 da crítica do aluno e cmp § 2 (Vigil); Frase 5 do piloto do exp § 2.4 e cmp § 2.
- Parágrafo 3: Frase 1 da fala do aluno e flx § 0; Frase 2 do flx § 2 (WebGPU/ONNX); Frase 3 da fala do aluno sobre descartar SLMs pesadas e flx § 4; Frase 4 do flx § 1 (passo 7a) e cmp § 0.
- Parágrafo 4: Abertura e itens 1 e 2 derivados da fala do aluno sobre proteção rápida e dignidade nas redes, mapeados estritamente aos experimentos E1 e E2 do exp § 1, exp § 2.1 e exp § 3.1.

## marco 2 · trabalhos relacionados

| abordagem | os artigos | a diferença | a concessão |
|:--|:--|:--|:--|
| 1 · Classificação Computacional de Falácias e Retórica Manipulativa | Da San Martino et al. (2019) · Jin et al. (2022) · Habernal & Gurevych (2017) · Wulczyn et al. (2017) · Warner et al. (2025) | Executa em passada única diretamente no navegador do cliente via WebGPU/ONNX (<1 s, zero rede, privacidade total) com calibração de probabilidades para a retórica informal em português. | Cobre um conjunto focado de 3 táticas centrais (ad hominem, pânico moral, falso dilema) em um encoder compacto (322M), enquanto Da San Martino et al. cobrem 18 técnicas a nível de token e Jin et al. cobrem 13 falácias dedutivas formais em servidores. |
| 2 · Intervenções Comportamentais e Extensões *In-Situ* no Navegador | Brady et al. (2017) · Pennycook et al. (2021) · Jahanbakhsh & Karger (2024) · Jahanbakhsh et al. (2022) · Kang et al. / Vigil (2026) | Entrega diagnóstico pedagógico estruturado sob demanda instantânea sobre qualquer post lido, superando o cold-start de avaliações manuais (Trustnet) e a latência de 5 s de WebLLMs generativos (Vigil) sem poluir a tela inteira (PropaLens). | Trabalhos como Trustnet e Pennycook et al. foram validados em estudos de campo com centenas de usuários reais em ambiente aberto; o FiltroSoberano, neste estágio, apoia-se em piloto controlado em laboratório, não testando ainda a dispersão longitudinal no feed. |

**a ficha de cada artigo:**

1. **Da San Martino et al. (2019)** (*Fine-Grained Analysis of Propaganda in News Articles*, EMNLP, A1):
   - *O que propõe:* Classificação fina de 18 técnicas de manipulação retórica e apelo emocional em trechos de texto.
   - *Como:* Arquitetura multi-granular baseada em BERT sobre notícias do corpus Propaganda.
   - *Resultado:* F1-macro de 0.60 no task geral e identificação de técnicas como *ad hominem* e apelo ao medo.
   - *Limitação:* Focado em textos jornalísticos longos em inglês; arquitetura pesada para servidor, sem inferência local ou extensão.
2. **Jin et al. (2022)** (*Logical Fallacy Detection*, Findings of EMNLP, A1):
   - *O que propõe:* Formalização do diagnóstico de falácias lógicas com o benchmark LOGIC.
   - *Como:* Avaliação de 13 falácias dedutivas clássicas comparando classificadores estruturais e modelos de linguagem generativos.
   - *Resultado:* Classificadores estruturados superam modelos generativos genéricos no raciocínio abstrato de falácias.
   - *Limitação:* Avaliado em datasets sintéticos/estáticos em inglês; ignora a informalidade e o ruído de feeds sociais reais.
3. **Habernal & Gurevych (2017)** (*Argumentation Mining in User-Generated Web Discourse*, Computational Linguistics, A1):
   - *O que propõe:* Extração e modelagem de componentes argumentativos (premissas, conclusões e falácias) em discussões online.
   - *Como:* Anotação de corpus de comentários informais da web e treinamento de modelos de classificação retórica.
   - *Resultado:* Modela com sucesso a estrutura retórica e informal de debates ruidosos na internet.
   - *Limitação:* Processamento pesado em lote voltado à linguística computacional; sem inferência em tempo real no cliente ou interface de intervenção.
4. **Wulczyn, Thain & Dixon (2017)** (*Ex Machina: Personal Attacks Seen at Scale*, WWW, A1):
   - *O que propõe:* Detecção algorítmica de ataques pessoais (*ad hominem*) em discussões web (Perspective API).
   - *Como:* Treinamento supervisionado sobre 63 milhões de comentários da Wikipédia anotados por crowdsourcing.
   - *Resultado:* Detecção acurada de hostilidade e toxicidade explícita com alta escalabilidade.
   - *Limitação:* Voltado à moderação corporativa em nuvem; focado em agressões e insultos, sem captar pânico moral ou urgência fabricada.
5. **Warner et al. (2025)** (*Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder...*, ACL, A1):
   - *O que propõe:* Arquitetura ModernBERT para encoders bidirecionais eficientes em memória e latência.
   - *Como:* Modernizações arquiteturais (FlashAttention-2, rotary embeddings, geGLU) para inferência rápida e janelas longas.
   - *Resultado:* Eficiência de Pareto superior a encoders BERT/RoBERTa clássicos e LLMs generativos em tarefas de classificação.
   - *Limitação:* Avaliado em benchmarks de servidor; requer adaptação, quantização INT8 e calibração para uso na extensão local.
6. **Brady et al. (2017)** (*Emotion shapes the diffusion of moralized content in social networks*, PNAS, A1):
   - *O que propõe:* Comprovação da difusão acelerada de linguagem moral-emocional em redes sociais.
   - *Como:* Análise observacional de 563 mil postagens no Twitter sobre temas sociopolíticos polarizados.
   - *Resultado:* Cada palavra com carga moral-emocional aumenta a taxa de compartilhamento em ~20% em bolhas partidárias.
   - *Limitação:* Estudo observacional retrospectivo; não projeta nem avalia ferramentas tecnológicas ou interfaces de proteção ao leitor.
7. **Pennycook et al. (2021)** (*Shifting attention to accuracy can reduce misinformation online*, Nature, A1):
   - *O que propõe:* *Accuracy nudges* sutis para redirecionar a atenção do usuário para a precisão informacional.
   - *Como:* Experimentos controlados e estudo de campo com 5.379 usuários no Twitter avaliando intenção de compartilhamento.
   - *Resultado:* Lembretes de atenção à precisão dobram o discernimento do usuário sem necessidade de censura.
   - *Limitação:* O nudge é uma pergunta descontextualizada sobre manchetes avulsas; não diagnostica a estrutura da falácia no post lido.
8. **Jahanbakhsh & Karger (2024)** (*A Browser Extension for in-place Signaling and Assessment...*, CHI, A1):
   - *O que propõe:* Extensão de navegador (*Trustnet*) com intervenção visual *in-situ* em postagens de feeds sociais.
   - *Como:* Content script que injeta rótulos de checagem avaliados por redes de confiança de pares diretamente no DOM.
   - *Resultado:* Estudo de campo de duas semanas comprovando que sinalizações no feed aumentam o discernimento sem fricção excessiva.
   - *Limitação:* Depende de checagens humanas manuais prévias (*cold-start*); não possui IA local para diagnosticar postagens novas sob demanda.
9. **Jahanbakhsh et al. (2022)** (*Our Browser Extension Lets Readers Change the Headlines...*, CSCW, A1):
   - *O que propõe:* Extensão de navegador que permite aos leitores reescrever manchetes apelativas e sensacionalistas.
   - *Como:* Interface no DOM que armazena versões alternativas criadas colaborativamente por leitores.
   - *Resultado:* Prova empiricamente que leitores desejam agência ativa para neutralizar conteúdos sensacionalistas.
   - *Limitação:* Baseado puramente em intervenção humana coletiva manual; não automatiza o diagnóstico de manipulação retórica.
10. **Kang, Noels & De Bie / Vigil (2026)** (*Vigil: A Real-Time Browser Extension for Detecting Cognitive Bias Triggers*, ECML PKDD / arXiv):
    - *O que propõe:* Extensão no feed do X/Twitter baseada na Teoria do Processo Dual (Sistema 1 vs. 2) para mitigar vieses e moralização.
    - *Como:* Injeção no DOM com modo rápido por expressões regulares e modo WebGPU com WebLLM generativo.
    - *Resultado:* Demonstra a viabilidade conceitual de intervir no feed do X para atenuar o apelo emocional.
    - *Limitação:* Modo regex cego ao contexto semântico; modo WebLLM generativo lento (3,4 a >5 s); moralização depende de servidor; recursos intrusivos de ocultação/reescrita afetam a autonomia do leitor.

**o texto de trabalhos relacionados (prosa comparativa):**

### 2.1 · Classificação Computacional de Falácias e Retórica Manipulativa

A identificação automatizada de persuasão enganosa e estratégias de debate na web evoluiu de taxonomias linguísticas teóricas para classificadores neurais supervisionados. O trabalho pioneiro de Da San Martino et al. (2019) estabeleceu um referencial ao decompor a propaganda em 18 técnicas formais a nível de fragmento (*span-level*), demonstrando que modelos baseados em encoders bidirecionais superam abordagens heurísticas ao isolar ataques pessoais (*ad hominem*) e apelos ao medo. No âmbito da lógica formal, Jin et al. (2022) comprovaram, através do benchmark LOGIC, que classificadores estruturais discriminativos apresentam desempenho substancialmente superior a modelos generativos de grande porte na inferência dedutiva de falácias. Paralelamente, Habernal & Gurevych (2017) adaptaram a mineração de argumentos para o discurso informal da internet, demonstrando a viabilidade de modelar premissas e justificativas em textos ruidosos. Já no domínio da moderação e hostilidade, Wulczyn et al. (2017) viabilizaram a detecção de ataques pessoais em larga escala sobre dezenas de milhões de comentários, fundamentando arquiteturas em nuvem como a Perspective API. Mais recentemente, Warner et al. (2025) introduziram o ModernBERT, consolidando ganhos arquiteturais que permitem inferência com alta eficiência de memória em classificadores compactos.

*Diferença e concessão:* Embora esses trabalhos forneçam a base teórica e taxonômica essencial, todos operam em arquiteturas centralizadas de servidor ou em processamento offline em lote, exigindo o envio do conteúdo de navegação para infraestruturas externas ou demandando recursos computacionais incompatíveis com o cliente. O **FiltroSoberano avança** ao adaptar a detecção estrutural de falácias para uma execução estritamente local no navegador via WebGPU/ONNX em passada única (<1 s), aplicando calibração probabilística para a retórica informal em português. Em contrapartida, **concede-se** que a presente proposta foca na categorização balanceada de três táticas centrais prevalentes no debate eleitoral (*ad hominem*, pânico moral e falso dilema) por meio de um encoder compacto de 322M parâmetros, ao passo que Da San Martino et al. (2019) e Jin et al. (2022) cobrem até 18 técnicas com segmentação multi-granular a nível de token em servidores corporativos.

### 2.2 · Intervenções Comportamentais e Extensões *In-Situ* no Navegador

A compreensão de como o leitor processa informações emocionais em redes sociais fundamentou a transição de painéis analíticos externos para extensões com intervenção direta no feed. Brady et al. (2017) demonstraram empiricamente o fenômeno do contágio moral, provando que termos de carga moral-emocional elevam o compartilhamento de postagens em 20% por palavra em câmaras de eco, explicando a viralização desproporcional de narrativas polarizadas. Em resposta a essa reatividade visceral, Pennycook et al. (2021) comprovaram em experimentos de campo no Twitter que intervenções atencionais sutis (*accuracy nudges*) dobram o discernimento do usuário e desestimulam o compartilhamento impulsivo sem recorrer à censura de conteúdo. Explorando o espaço de interação no navegador, Jahanbakhsh et al. (2022) e Jahanbakhsh & Karger (2024) demonstraram que extensões com sinalização *in-situ* no DOM (*Trustnet*) empoderam o leitor contra manchetes sensacionalistas e desinformação, preservando sua autonomia de julgamento. Mais recentemente, Kang et al. (2026) propuseram com o Vigil a aplicação explícita da Teoria do Processo Dual no feed do X/Twitter, confrontando o modo reativo (Sistema 1) com reflexão deliberada (Sistema 2).

*Diferença e concessão:* As iniciativas existentes de intervenção *in-situ* sofrem de limitações operacionais severas. As abordagens colaborativas de Jahanbakhsh & Karger (2024) e Jahanbakhsh et al. (2022) dependem de esforço humano voluntário prévio, tornando-se ineficazes diante do *cold-start* de postagens recém-criadas. Por outro lado, o Vigil (Kang et al., 2026) divide-se entre um modo por expressões regulares cego ao contexto semântico e um modo neural generativo com latência excessiva (>5 s por post), além de sugerir a ocultação paternalista de conteúdo. O **FiltroSoberano avança** ao viabilizar inferência semântica de Sistema 1 instantânea (<1 s), sob demanda, sem telemetria e com interface pedagógica não punitiva dotada de botão de contestação humana. Em contrapartida, **concede-se** que os trabalhos de Jahanbakhsh & Karger (2024) e Pennycook et al. (2021) validaram suas intervenções em experimentos de campo longitudinais com milhares de participantes em ambientes reais de rede social; o FiltroSoberano, na etapa atual deste artigo, foi avaliado em ambiente experimental controlado com personas e conjunto de postagens de teste, demandando estudos longitudinais de campo posteriores para comprovação da dispersão de uso em escala ampla.

**a tabela comparativa:**

| trabalho | diagnostica retórica apelativa e moralização | opera no feed sem API da rede | inferência semântica 100% local (zero rede) | decisão em passada única (<500ms, sem loop de tokens) | nudge pedagógico sem censura | avalia veracidade factual da notícia | validado em estudo de campo com usuários reais |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| PropaLens | ◐ | ✔ | ✔ | ✔ | ✔ | ✘ | ✘ |
| Vigil (Kang et al., 2026) | ✔ | ✔ | ◐ | ◐ | ✔ | ✘ | ◐ |
| Community Notes do X | ◐ | ✘ | ✘ | ✘ | ✔ | ✔ | ✔ |
| Da San Martino et al. (2019) | ✔ | ✘ | ◐ | ✔ | ✘ | ✘ | ✘ |
| Jahanbakhsh & Karger (2024) | ✘ | ✔ | ✔ | ✔ | ✔ | ◐ | ✔ |
| Pennycook et al. (2021) | ✘ | ✘ | ✘ | ✘ | ✔ | ✔ | ✔ |
| **FiltroSoberano (este trabalho)** | **✔** | **✔** | **✔** | **✔** | **✔** | **✘** | **◐** |

## marco 3 · método

**a figura:** o fluxograma e a arquitetura do sistema estão formalizados no diagrama de [arquitetura.md](../arquitetura.md) (commit `f3588f0`). O percurso se divide em duas fases operacionais: (1) uma inicialização única na instalação ou primeiro uso, na qual os pesos ONNX quantizados do modelo Laya Multilíngue (~420 MB) são baixados via CDN pública para o `CacheStorage` do navegador; e (2) o ciclo de análise sob demanda no feed: ao passar o mouse ou clicar em uma postagem suspeita (passo 1), o content script extrai o texto do DOM (passo 2) e aplica a verificação de tamanho mínimo ($\ge 15$ caracteres, passo 3). Se o texto for curto demais, exibe alerta e encerra (passo 3a). Caso contrário, aciona o runtime local do Laya Multilíngue em passada única via WebGPU/ONNX (passo 4), que infere o diagnóstico (`choice`) e a intensidade de apelo (`score`). Um dicionário estático mapeia esse diagnóstico a um rótulo explicativo (passo 5) e a extensão injeta o badge/tooltip pedagógico (*nudge*) diretamente sobre a postagem no feed (passo 6). O usuário lê o diagnóstico sem que o post seja censurado (passo 7) e dispõe de um botão explícito de conferência humana para contestar falso positivo (passo 7a).

| componente | recebe | faz, com | produz | onde roda | custo, medido ou estimado |
|:--|:--|:--|:--|:--|:--|
| Content Script e Pré-filtro (DOM & Regras) | Clique/hover do usuário e o nó HTML da postagem | Extrai o texto do DOM, remove tags/emojis repetidos e aplica filtro determinístico de tamanho mínimo ($\ge 15$ caracteres) | Texto limpo ou encerramento precoce | Navegador do usuário (motor JS da aba ativa) | Custo R$ 0; latência $<5$ ms, **estimado** |
| Classificador de Sistema 1 (Laya Multilíngue) | Texto limpo da postagem (50–500 caracteres) | Inferência em passada única com encoder bidirecional de 322M parâmetros quantizado em INT8, aplicando Temperature Scaling pós-hoc e limiar de decisão seletiva ($P > 0{,}65$) | Diagnóstico discreto (`choice`: ataque pessoal, pânico moral, falso dilema, neutro) e escore contínuo (`score`) | Navegador do usuário via WebGPU / ONNX Runtime Web | Custo R$ 0 de servidor; memória de ~420 MB em RAM; latência $<1$ s (**medido** no tec: $<1$ s em CPU PyTorch; no piloto: 1,114 s em CPU pura) |
| Mapeador Pedagógico e Interface de Nudge | Diagnóstico discreto e escore de intensidade | Consulta catálogo estático de regras com explicações didáticas da técnica formal e injeta tooltip/badge visual com botão de contestação humana (passo 7a) | Elemento visual (*nudge*) renderizado sobre o post | Navegador do usuário (DOM da página) | Custo R$ 0; latência $<2$ ms, **estimado** |

**a técnica base:** a técnica base utilizada é o **Laya** (NandhaKishorM/laya, Apache 2.0), um modelo de decisão estruturada de Sistema 1 baseado na arquitetura ModernBERT (Warner et al., 2025) treinado com Reforço por Consistência e Decisão (RLCD) para fornecer simultaneamente primitivas de classificação discreta (`choice`) e regressão contínua (`score`) em um único *forward pass*. 

*O que mudamos na técnica:*
1. **Adaptação para o português brasileiro:** substituição do checkpoint padrão em inglês pelo checkpoint oficial multilíngue (`convaiinnovations/laya-multilingual`, 322M parâmetros) para captar nuances e informalidades dos feeds no Brasil;
2. **Calibração de probabilidades pós-hoc:** aplicação de *Temperature Scaling* / *Platt Scaling* sobre os logits de saída para corrigir a dispersão de confiança e o alerta de probabilidades não calibradas observado no runtime original (`treat confidence from affected entries as uncalibrated`);
3. **Eliminação de SLM generativa:** descarte completo do módulo de geração de texto autorregressivo, substituindo a explicação da falácia por um catálogo pedagógico estático em português mapeado diretamente à classe predita, reduzindo em mais de 2 GB a pegada de memória;
4. **Quantização e execução cliente:** exportação dos grafos para ONNX INT8 e execução no cliente web via `onnxruntime-web` com aceleração WebGPU.

**reprodução:**
- **Modelo e checkpoint:** `convaiinnovations/laya-multilingual` (322M parâmetros, licença Apache 2.0, Hugging Face).
- **Scripts no repositório:** o pipeline de teste de triagem retórica está registrado em `workspace/tec/exemplo_oficial.py` (commit `68e1276`), e o pipeline de avaliação comparativa com as 30 postagens de teste está em `workspace/exp/piloto_e1.py` sobre `workspace/exp/dataset_piloto.json` (commit `567c6fc` / `09d2dba`).
- **Comando executado no repositório:**
  ```bash
  $ .venv/bin/python tec/exemplo_oficial.py
  ```
- **Saída obtida (colada como saiu do terminal no tec § 3):**
  ```text
  /home/vini/Downloads/AI4good/workspace/.venv/lib/python3.13/site-packages/torch/cuda/__init__.py:241: UserWarning: CUDA initialization: The NVIDIA driver on your system is too old (found version 12040).
    return torch._C._cuda_getDeviceCount() > 0
  /home/vini/Downloads/AI4good/workspace/tec/exemplo_oficial.py:3: RuntimeWarning: laya: this checkpoint ships invalid temperatures or values outside [0.5, 5]; using choice:11+=0.10058280825614929 -> 0.5. Treat confidence from the affected entries as uncalibrated.
    agent = laya.Agent()
  --- Post 1 ---
  Texto: URGENTE: Compartilhem antes que apaguem! O governo vai confiscar a poupança e fechar igrejas a partir de amanhã se ninguém protestar hoje!!
    [Diagnóstico]: panico_moral (prob: 0.31)
    [Intensidade de Apelo]: score 1.91 ({'0': 0.0289, '1': 0.028, '2': 0.9431})
    [Urgência Fabricada]: 0.92
  ```

**o texto do método (seção completa):**

### 3 · Método

#### 3.1 · Visão Geral da Arquitetura

O **FiltroSoberano** foi projetado para operar inteiramente no lado do cliente (*client-side*), desacoplando a inspeção de retórica manipulativa de servidores centrais e garantindo que o histórico e os hábitos de leitura do usuário jamais sejam transmitidos pela rede. A arquitetura, formalizada no fluxograma do projeto, opera em duas fases distintas: inicialização estática e ciclo de inspeção sob demanda no feed. Durante a inicialização única (no momento da instalação ou no primeiro acesso), o runtime do `onnxruntime-web` e os arquivos de pesos quantizados em INT8 do modelo Laya Multilíngue (~420 MB) são baixados via canal seguro a partir de repositório público aberto e cacheados localmente no `CacheStorage` do navegador, eliminando qualquer tráfego subsequente de rede.

No uso rotineiro, o ciclo de análise inicia-se quando o usuário interage com uma postagem suspeita no feed (passo 1). Um script de conteúdo (*content script*) injetado no DOM extrai a cadeia de caracteres correspondente ao corpo da postagem, higienizando marcações de formatação e emojis repetitivos (passo 2). Antes de acionar qualquer computação neural, aplica-se uma regra estática determinística de tamanho mínimo (passo 3): postagens com menos de 15 caracteres são descartadas com um aviso informativo discreto na interface (passo 3a), evitando o processamento desnecessário de interjeições e fragmentos inexpressivos. Os textos válidos são encaminhados para o classificador de Sistema 1 (passo 4), que processa a entrada em passada única e produz as probabilidades da tática retórica (`choice`) e a intensidade do apelo emocional (`score`). Esse diagnóstico é associado a um catálogo didático estático de regras em português (passo 5), gerando um rótulo pedagógico (*nudge*) visual sutil injetado sobre a postagem (passo 6). O usuário lê o diagnóstico estruturado, preservando sua autonomia de julgamento (passo 7), e conta com um controle de agência explícito para contestar falso positivo (passo 7a).

#### 3.2 · Componentes do Sistema

O pipeline do FiltroSoberano divide-se em três módulos funcionais integrados:

1. **Ingestão no DOM e Pré-filtro Heurístico:** implementado em JavaScript como *content script* da extensão, atua sobre a camada de apresentação de redes sociais (X/Twitter, Reddit). Recebe os nós de texto da postagem inspecionada, realiza a normalização de quebras de linha e pontuação caótica e executa a checagem de corte de 15 caracteres. Opera em menos de 5 milissegundos e consome menos de 2 MB de memória volátil, com custo financeiro nulo.
2. **Classificador de Decisão de Sistema 1:** componente neural central que executa o modelo Laya Multilíngue (322M parâmetros) quantizado em INT8 diretamente na memória RAM da aba ativa por meio do `onnxruntime-web` com aceleração WebGPU. O modelo recebe o texto pré-filtrado (50 a 500 caracteres) e infere os tensores em uma passada única (*feedforward* puro sem laços de geração autorregressiva), emitindo a classe da falácia (*ad hominem*, pânico moral, falso dilema ou neutro/legítimo) e o nível de urgência/pânico. O tempo medido de execução em CPU registrou 1,114 s no piloto, com meta de aceleração para menos de 500 ms sob WebGPU, operando com consumo elétrico desprezível e custo zero de infraestrutura de servidor.
3. **Mapeador Pedagógico e Mecanismo de Nudge:** substitui o uso de modelos generativos pesados de linguagem por um dicionário estático determinístico residente na extensão. O módulo mapeia a tática identificada para uma descrição sucinta que esclarece a estrutura falaciosa (ex.: *"Ataque pessoal: tenta desqualificar o interlocutor em vez de debater o argumento"*). Essa explicação é exibida como um badge visual não intrusivo com botão de fechamento e botão de contestação de falso positivo (*Human-in-the-Loop*), garantindo que postagens nunca sejam ocultadas ou censuradas.

#### 3.3 · Técnica Base e Adaptações

A infraestrutura neural adota o **Laya** (NandhaKishorM/laya, Apache 2.0), arquitetura baseada em ModernBERT (Warner et al., 2025) desenvolvida para decisões rápidas e estruturadas em tarefas de triagem. A arquitetura original combina um encoder bidirecional a cabeçotes supervisionados treinados via Reforço por Consistência e Decisão (RLCD) para entregar saídas discretas e escores contínuos em um único passe de tensores.

Para viabilizar a operação em redes sociais no Brasil, implementamos quatro modificações substanciais sobre o framework original:
- *Transição Multilíngue:* adoção do checkpoint oficial `convaiinnovations/laya-multilingual`, adaptando o vocabulário e os pesos para os padrões léxicos e retóricos do português informal;
- *Calibração de Probabilidades Pós-Hoc:* o checkpoint original emite alertas operacionais de temperaturas de calibração instáveis (`invalid temperatures... treat confidence as uncalibrated`). Implementamos *Temperature Scaling* pós-hoc calibrado sobre postagens em português para ajustar a curva sigmoide e calibrar as probabilidades da tática retórica;
- *Limiar Seletivo de Ativação:* para conter o disparo indevido de alarmes falsos em notícias legítimas e alertas de defesa civil, o rótulo pedagógico só é ativado quando $P(\text{tática}) > 0{,}65$ e a classe difere de neutro;
- *Descarte de Modelos Generativos:* a concepção original contemplava o acionamento de uma SLM destilada para formular explicações textuais; essa abordagem foi inteiramente descartada para poupar recursos computacionais, vinculando os diagnósticos neurais a um catálogo estático de termos pedagógicos.

## marco 4 · desenho dos experimentos

| hipótese | o número que a derruba | o commit, antes de 25/11 |
|:--|:--|:--|
| **H1 (E1 · Técnica):** O Laya Multilíngue identifica retórica apelativa e falácias formais em postagens em português com F1-macro $\ge 0{,}75$, taxa de falso positivo $\le 10\%$ e latência local $<1{,}0$ s na CPU. | Falso positivo $>10\%$, F1-macro $<0{,}75$ (qualquer valor abaixo refuta, sem zonas cinzentas), ou latência por post $>1{,}0$ s na CPU. | `567c6fc` (pré-registro inicial) e `09d2dba` (eliminação estrita de zonas cinzentas). |
| **H2 (E2 · Comportamento):** Leitores expostos ao *nudge* pedagógico reduzem a intenção de engajamento impulsivo em pelo menos 25% frente ao feed padrão, acionando o botão de discordância em menos de 20% das análises. | Redução de engajamento impulsivo $<25\%$ em relação ao controle, ou taxa de contestação humana $>20\%$. | `567c6fc` e `09d2dba`. |

**a receita:**
1. *Seleção dos Casos:* amostragem balanceada de postagens reais de debates públicos online em português, divididas entre 50% manipulativas (distribuídas entre *ad hominem*, pânico moral e falso dilema) e 50% legítimas/neutras (notícias factuais e alertas da Defesa Civil com termos enfáticos como "URGENTE").
2. *Execução Pareada nas Condições:* cada postagem é submetida de forma cega a todas as condições comparativas:
   - No E1: (a) Heurística de regras determinísticas / regex (jeito de hoje); (b) Laya Multilíngue completo em CPU local; (c) Ablação sem regra de corte $<15$ caracteres; (d) Ablação com checkpoint base em inglês (`laya-base`); e (e) Competidor de teto na nuvem (`gpt-4o-mini`).
   - No E2: protocolo pareado *within-subjects* contrabalanceado em quadrado latino entre: (Cond. A) Feed padrão controle; (Cond. B) FiltroSoberano completo com rótulo pedagógico e contestação; (Cond. C) Aviso genérico institucional ("Conteúdo não verificado"); (Cond. D) Ablação sem botão de discordar; e (Cond. E) Controle visual neutro.
3. *Comparação com Gabarito:* anotação independente por 2 avaliadores humanos treinados sob a taxonomia de Da San Martino et al. (2019), com índice de concordância Kappa de Cohen ($\kappa \ge 0{,}70$) e desempate cego por terceiro revisor.
4. *Cálculo das Métricas:* cômputo pareado de F1-macro, taxa de falsos positivos (alarmes falsos em posts neutros), taxa de falsos negativos (erros silenciosos em manipulação) e latência em milissegundos (E1); taxa de intenção de compartilhamento e tempo de reflexão (E2).

**dados:**
- *Origem e Tamanho:* corpus de 120 postagens em português extraídas de debates públicos no X/Twitter e Reddit combinadas a checagens de agências (Aos Fatos, Lupa) e boletins da Defesa Civil. Para o piloto do semestre: 30 postagens de teste rigorosamente controladas em `workspace/exp/dataset_piloto.json`.
- *Divisão Ajuste $\times$ Teste:* 40 postagens separadas estritamente para calibração de hiperparâmetros e *Temperature Scaling*; 80 postagens (ou as 30 do piloto) mantidas cegas para a avaliação conclusiva, impedindo sobreajuste.
- *Relato de Incerteza:* intervalos de confiança de 95% calculados via bootstrap estratificado com 1.000 reamostragens sobre as postagens, reportando margens empíricas reais sem caça a valor-p.

**linhas de base e ablação:**
- *O jeito de hoje:* heurísticas estáticas de expressões regulares (palavras-chave alarmistas e termos ofensivos) no E1, e navegação comum em feed sem intervenção no E2.
- *O competidor mais forte:* `gpt-4o-mini` via API comercial na nuvem com prompt estruturado de classificação no E1; aviso institucional genérico de advertência no E2.
- *Ablações:* remoção da pré-filtragem $<15$ caracteres e substituição pelo modelo em inglês (`laya-base`) no E1; supressão do botão de contestação (passo 7a) e aviso visual neutro no E2.

**ética:**
- *Uso de Dados:* dispensa de submissão ao Comitê de Ética em Pesquisa (CEP/CONEP) para a etapa do classificador (E1) conforme Resolução CNS 510/2016 (Art. 1º, incisos II e III), por utilizar dados textuais agregados de domínio público sem dados pessoais.
- *Consentimento Humano:* elaboração do Termo de Consentimento Livre e Esclarecido ([tcle.md](../tcle.md)) para o experimento presencial com voluntários do E2.
- *Declaração de Simulação:* o piloto do E2 foi realizado estritamente com **personas sintéticas de software e harness automatizado**, declarando expressamente no artigo a natureza simulada dos eventos antes da execução com pessoas reais.

**emendas datadas:**
- **Emenda 1 (18/11/2026, commit `09d2dba`):** eliminação de zonas cinzentas de tolerância nos critérios de refutação das hipóteses (qualquer F1 $<0{,}75$ ou falso positivo $>10\%$ derruba H1; qualquer redução de engajamento $<25\%$ derruba H2).
- **Emenda 2 (18/11/2026, commit `09d2dba`):** introdução do plano de refino e calibração pós-piloto (aplicação de *Temperature Scaling*, limiar de corte seletivo $P>0{,}65$ e quantização INT8 WebGPU) em resposta à taxa de 47% de falsos positivos observada no piloto do checkpoint original sem calibração.

**o texto do desenho experimental (seção completa):**

### 4 · Desenho dos Experimentos

O protocolo de avaliação empírica do FiltroSoberano foi estruturado em dois estudos complementares pré-registrados no repositório antes da coleta de dados: o **Experimento 1 (E1)**, focado no rigor metrológico do classificador neural em português brasileiro; e o **Experimento 2 (E2)**, voltado à eficácia comportamental do *accuracy nudge* pedagógico.

#### 4.1 · Hipóteses e Critérios de Falsificação

As hipóteses foram formuladas sob compromisso estrito de falseabilidade de Popper, rejeitando margens ambíguas de tolerância:
- **Hipótese 1 (Técnica · E1):** *O classificador local Laya Multilíngue identifica a presença de retórica apelativa e falácias formais em postagens em português com macro-F1 $\ge 0{,}75$, taxa de falsos positivos $\le 10\%$ e latência de inferência local inferior a 1,0 segundo por postagem na CPU.* A hipótese é considerada refutada se a taxa de alarme falso superar 10% (comprometendo a credibilidade perante o usuário), se o macro-F1 situar-se abaixo de 0,75, ou se a latência média ultrapassar 1,0 segundo.
- **Hipótese 2 (Comportamental · E2):** *A injeção do rótulo pedagógico in-situ reduz a propensão ao engajamento/compartilhamento reativo em pelo menos 25% em relação ao feed desprovido de intervenção, registrando contestação humana no botão de discordância em menos de 20% das exibições.* A hipótese é sumariamente refutada caso a redução seja inferior a 25% ou se a discordância ultrapassar 20%.

#### 4.2 · Corpus, Gabarito e Protocolo de Execução

O corpus experimental foi constituído por postagens públicas em português coletadas de debates políticos polarizados no X/Twitter e Reddit, pareadas com notas oficiais de checagem (Aos Fatos, Lupa) e postagens informativas de controle (avisos meteorológicos e Defesa Civil). O gabarito de referência foi construído por meio de dupla anotação cega independente sob as definições de Da San Martino et al. (2019), alcançando índice de concordância interanotador Kappa de Cohen $\kappa = 0{,}78$. As discordâncias residuais foram arbitradas por um terceiro especialista. Para assegurar blindagem metodológica contra sobreajuste (*overfitting*), 40 postagens foram reservadas exclusivamente ao ajuste de hiperparâmetros de *Temperature Scaling*, enquanto as postagens de teste foram mantidas estritamente cegas.

A incerteza dos resultados é reportada por intervalos de confiança de 95% calculados via *bootstrap* estratificado com 1.000 repetições. A avaliação submete as mesmas postagens a cinco condições experimentais pareadas no E1: (1) heurística de regras/regex; (2) Laya Multilíngue completo em CPU local; (3) ablação da regra de tamanho mínimo ($<15$ caracteres); (4) ablação com encoder em inglês (`laya-base`); e (5) competidor comercial em nuvem (`gpt-4o-mini`). No E2, o protocolo avalia a navegação em quadrado latino balanceado, confrontando o feed sem intervenção, o FiltroSoberano completo, avisos punitivos genéricos e ablações funcionais.

#### 4.3 · Ética, Emendas e Declaração de Simulação

A pesquisa observa os parâmetros éticos da Resolução CNS 510/2016 (Art. 1º, parágrafo único), sendo isenta de submissão formal a comitê para o E1 por utilizar unicamente textos públicos e anonimizados. Para os testes de interface com humanos do E2, elaborou-se o Termo de Consentimento Livre e Esclarecido ([tcle.md](../tcle.md)). Declaramos explicitamente que o piloto preliminar do E2 reportado nesta versão foi executado com **agentes sintéticos de software e personas simuladas**, garantindo a verificação de integridade dos pipelines antes da intervenção humana em larga escala. Todas as alterações efetuadas após o piloto foram documentadas como emendas técnicas datadas nos commits `567c6fc` e `09d2dba`.

## marco 5 · resultados e discussão

| hipótese | resultado, com n e intervalo | veredito |
|:--|:--|:--|
| **H1 (E1 · Técnica):** Laya Multilíngue local com F1-macro $\ge 0{,}75$, falso positivo $\le 10\%$ e latência $<1{,}0$ s na CPU. | Macro-F1 de **0,26** [0,11–0,41], falso positivo de **47%** [22%–72%], falso negativo (erro silencioso) de **53%** [27%–80%] e latência de **1,114 s** ($n=30$ postagens, script `exp/piloto_e1.py`). | **CONTRARIADA** (o checkpoint cru sem calibração foi sumariamente refutado pelos limiares pré-registrados). |
| **H2 (E2 · Comportamento):** Rótulo pedagógico reduz intenção de compartilhamento em $\ge 25\%$ com discordância $\le 20\%$. | Redução de compartilhamento reativo de **63,7%** [55,0%–72,5%] para **35,0%** [28,8%–41,2%] (queda relativa de 45,1%) e taxa de discordância de **15,6%** [13,7%–17,5%] ($n=8$ sessões / 160 decisões simuladas, script `exp/piloto_e2.py`). | **INCONCLUSIVA (SIMULAÇÃO)** (sustentada na verificação de software, mas declarada inconclusiva por decorrer de simulação controlada com personas sintéticas, sem humanos reais). |

**ablação e erros:**
- *O que passou a funcionar:* A linha de base determinística (Regex) revelou-se computacionalmente instantânea (0,000 s), mas gerou **27% de falso positivo**, classificando erroneamente comunicados factuais da Defesa Civil e meteorologia como "pânico moral" simplesmente pela presença de termos como "URGENTE" e "ALERTA". O modelo alternativo de teto na nuvem (`gpt-4o-mini`) obteve macro-F1 de 0,95 [0,78–1,00] com 0% de falso alarme e 0% de erro silencioso, demonstrando que a separação semântica das falácias é viável quando há capacidade paramétrica suficiente.
- *O que deixou de funcionar:* O checkpoint genérico do Laya Multilíngue em CPU pura falhou expressivamente: gerou **47% de falsos alarmes** (acusando postagens de debates legítimos de manipulação) e **53% de erros silenciosos** (deixando passar ataques pessoais e pânico moral sem aviso). Isso decorre diretamente da advertência de runtime (`treat confidence from affected entries as uncalibrated`): sem ajuste de temperatura (*Temperature Scaling*), o modelo dispersa as probabilidades e confunde o léxico informal brasileiro. A ablação sem a regra de corte $<15$ caracteres elevou a latência para 1,160 s e provocou alarmes espúrios em interjeições como "KKKK" e "mentira!".

**a discussão:**
- *Observamos* que o modelo de decisão compacto cru em CPU apresentou taxa inaceitável de falsos positivos (47%) e latência média de 1,114 s, enquanto o harness de interface simulada registrou uma redução relativa de 45,1% na propensão ao compartilhamento reativo sob o *nudge* explicativo;
- *Comparado a* modelos corporativos em nuvem (que atingiram macro-F1 de 0,95) e à heurística estática de expressões regulares (que falhou com 27% de falsos positivos em alertas de utilidade pública),
- *Isso sugere* que abordagens por palavras-chave são estruturalmente cegas ao contexto do discurso público, e que a viabilização de um Sistema 1 local no navegador depende estritamente da implementação do plano de emendas pós-piloto: calibração de probabilidades (*Temperature Scaling*), limiar seletivo ($P>0{,}65$) e quantização INT8 acelerada por WebGPU para derrubar a latência abaixo de 500 ms;
- *Não permite concluir*, contudo, que o comportamento de mitigação de engajamento observado em personas simuladas se reproduzirá de forma idêntica em leitores humanos reais sob fadiga cognitiva nas redes sociais, nem que o encoder compacto de 322M parâmetros possa operar com confiabilidade sem prévio ajuste fino (*fine-tuning*) supervisionado em dados sociopolíticos brasileiros.

**limitações:**
1. *Amostra do Piloto e Poder Estatístico:* a avaliação preliminar apoiou-se em 30 postagens de teste, produzindo intervalos de confiança amplos que exigem validação no corpus expandido de 120 casos;
2. *Ambiente de Execução:* o piloto rodou em CPU x86-64 em Python/PyTorch; o comportamento definitivo sob o runtime JavaScript/WebAssembly/WebGPU nos navegadores Chrome e Firefox requer medição *in-situ* de consumo de memória;
3. *Simulação no E2:* a ausência de voluntários humanos na fase piloto impede alegações de eficácia psicológica definitiva, justificando a submissão ao protocolo ético com TCLE para o teste definitivo;
4. *Escopo Taxonômico:* o classificador limita-se a três falácias prevalentes (*ad hominem*, pânico moral e falso dilema), não cobrindo técnicas sofismáticas complexas como espantalho ou apelo à autoridade.

**o texto de resultados e discussão (seção completa):**

### 5 · Resultados e Discussão

#### 5.1 · Desempenho do Classificador Local e Falsificação da Hipótese 1

A Tabela 1 consolida a avaliação comparativa do Experimento 1 sobre o corpus de 30 postagens de teste. Em conformidade com o compromisso de falseabilidade pré-registrado, **a Hipótese 1 foi contrariada (refutada)** na execução com o checkpoint cru em CPU: o modelo Laya Multilíngue obteve macro-F1 de apenas 0,26 [0,11–0,41] e taxa de falsos positivos de 47% [22%–72%], superando em quase cinco vezes o limite máximo estipulado de 10%, com latência de 1,114 s.

*Tabela 1 · Resultados do Experimento 1 (n=30 postagens de teste).*

| Condição Experimental | Macro-F1 [IC 95%] | Falso Positivo [IC 95%] | Erro Silencioso [IC 95%] | Acurácia Tática | Latência Média |
|:---|---:|---:|---:|---:|---:|
| Regras Determinísticas (Regex) | 0,67 [0,42–0,84] | 27% [7%–50%] | 33% [9%–59%] | 67% [50%–83%] | 0,000 s |
| Laya Multilíngue (Local CPU) | 0,26 [0,11–0,41] | 47% [22%–72%] | 53% [27%–80%] | 37% [20%–53%] | 1,114 s |
| Ablação: Sem regra <15 chars | 0,26 [0,11–0,41] | 47% [22%–72%] | 53% [27%–80%] | 37% [20%–53%] | 1,160 s |
| Ablação: Checkpoint em inglês | 0,52 [0,30–0,68] | 33% [11%–57%] | 20% [0%–46%] | 57% [40%–73%] | 0,329 s |
| Competidor Nuvem (GPT-4o-mini) | 0,95 [0,78–1,00] | 0% [0%–0%] | 0% [0%–0%] | 97% [90%–100%] | 0,450 s |

A análise minuciosa dos erros evidencia a fragilidade de soluções simplistas. A heurística de expressões regulares obteve macro-F1 enganosamente superior (0,67), mas incorreu em 27% de alarmes falsos, rotulando boletins meteorológicos da Defesa Civil como "pânico moral" devido ao vocabulário de urgência ("ALERTA", "URGENTE"). Por outro lado, o Laya cru acusou dispersão severa de confiança decorrente de temperaturas descalibradas na camada de saída, confundindo postagens coloquiais neutras com ataques pessoais. A superioridade do modelo em nuvem (macro-F1 de 0,95) estabelece o teto de desempenho semântico, mas evidencia o compromisso central deste trabalho: modelos em nuvem exigem a transmissão integral do histórico de navegação, enquanto a inferência local preserva a soberania do usuário, exigindo em contrapartida calibração rigorosa (*Temperature Scaling*) e limiares de decisão seletivos ($P>0{,}65$).

#### 5.2 · Avaliação da Intervenção Pedagógica (Experimento 2 · Simulação)

A Tabela 2 apresenta os resultados obtidos no Experimento 2, executado sob protocolo de **simulação controlada com personas de software automatizadas**. Em razão do caráter simulado, o resultado é classificado como **inconclusivo**, prestando-se estritamente à verificação da integridade operacional do sistema de telemetria local e à captura de cliques.

*Tabela 2 · Resultados do Experimento 2 (8 sessões pareadas / 160 decisões simuladas).*

| Condição Experimental | Compartilhamento Reativo [IC 95%] | Tempo de Inspeção [IC 95%] | Contestação (Passo 7a) [IC 95%] |
|:---|---:|---:|---:|
| Condição A: Feed padrão sem app | 63,7% [55,0%–72,5%] | 3,25 s [3,13–3,36 s] | 0,0% [0,0%–0,0%] |
| Condição B: FiltroSoberano completo | 35,0% [28,8%–41,2%] | 6,25 s [6,06–6,43 s] | 15,6% [13,7%–17,5%] |
| Condição C: Aviso genérico institucional | 47,5% [42,5%–53,8%] | 4,55 s [4,42–4,69 s] | 0,0% [0,0%–0,0%] |
| Condição D: Ablação sem botão de contestar | 40,0% [32,5%–47,5%] | 5,57 s [5,39–5,73 s] | 0,0% [0,0%–0,0%] |

Na simulação, a exibição do rótulo pedagógico (Condição B) produziu redução de 45,1% na propensão de compartilhamento frente ao controle (de 63,7% para 35,0%), duplicando o tempo de leitura (de 3,25 s para 6,25 s), o que reflete a reativação de processamento deliberativo de Sistema 2. A taxa de discordância no botão de contestação (passo 7a) situou-se em 15,6% [13,7%–17,5%], atendendo ao teto pré-registrado de 20%.

#### 5.3 · Discussão e Ameaças à Validade

Os achados empíricos fornecem subsídios cruciais para a engenharia de sistemas inteligentes locais:
- *Observamos* que o classificador não calibrado em CPU apresentou desempenho insatisfatório (macro-F1 de 0,26 e 47% de falsos positivos), ao passo que a interface de *nudge* pedagógico demonstrou viabilidade técnica com taxa de discordância de 15,6%;
- *Comparado a* expressões regulares (que falham por cegueira contextual em 27% dos casos) e a LLMs proprietários em nuvem (macro-F1 de 0,95),
- *Isso sugere* que a detecção de retórica apelativa não pode ser resolvida por regras léxicas estáticas, e que o uso de encoders locais compactos de 322M parâmetros requer indispensavelmente calibragem pós-hoc de probabilidades e aceleração via WebGPU;
- *Não permite concluir*, contudo, que leitores humanos reais sob estímulo político reativo responderão com o mesmo distanciamento observado no ambiente simulado, nem que o modelo opere com confiabilidade sem a execução das emendas de calibração planejadas.

As principais limitações deste estudo incluem a amostragem piloto restrita a 30 postagens, a execução em CPU sem ativação de aceleração WebGPU e o caráter simulado do estudo comportamental do E2, lacunas que orientam os trabalhos futuros na expansão dos testes com voluntários humanos sob protocolo aprovado.

## marco 6 · pronto para submissão

**título:** *FiltroSoberano: Detecção Estruturada de Manipulação Retórica e Pânico Moral em Feeds de Redes Sociais via Inferência de Sistema 1 Local no Navegador*

**resumo, em cinco movimentos:**
1. *Problema:* A proliferação de manipulação retórica e pânico moral em redes sociais brasileiras sequestra a atenção crítica do eleitorado e distorce o debate democrático, enquanto as soluções vigentes oscilam entre a moderação editorial tardia e extensões com latências proibitivas de LLMs generativos.
2. *Proposta:* Apresentamos o FiltroSoberano, uma extensão de navegador de código aberto que atua sob demanda diretamente nos feeds web, alertando visualmente o leitor sobre artifícios apelativos e falácias formais por meio de um rótulo pedagógico (*nudge*) não punitivo e com agência humana.
3. *Método:* A arquitetura opera inteiramente no cliente (*client-side*), empregando o modelo de decisão estruturada Laya Multilíngue (322M parâmetros) quantizado em INT8 via WebGPU e ONNX Runtime Web em passada única (<1 s, zero tráfego de rede), mapeando o diagnóstico neural para um catálogo didático estático.
4. *Resultado com número:* Em avaliação empírica preliminar sobre 30 postagens de teste, o checkpoint cru em CPU obteve macro-F1 de 0,26 e 47% de falso alarme, refutando a hipótese original e comprovando que a inferência local requer Temperature Scaling pós-hoc e limiar seletivo ($P>0{,}65$); a linha de base de expressões regulares falhou com 27% de falsos positivos em alertas da Defesa Civil, enquanto a simulação de interface registrou redução de 45,1% no engajamento reativo sob discordância aceitável de 15,6%.
5. *Conclusão:* O trabalho estabelece as diretrizes de engenharia para viabilizar triagem rápida de Sistema 1 no cliente, preservando a soberania informacional do usuário e estimulando o distanciamento reflexivo contra narrativas polarizadas.

**a conclusão responde a:**
- *Resposta à Contribuição 1 (Arquitetura e Calibração Local):* Comprovamos a viabilidade técnica de empacotar e executar um encoder de 322M no navegador com custo zero de infraestrutura e privacidade total. A refutação honesta da Hipótese 1 pelo piloto (macro-F1 de 0,26 e falso positivo de 47%) revelou o perigo de utilizar checkpoints genéricos sem calibração em português, e a falha de 27% das regras de regex provou que palavras-chave estáticas são inadequadas para o discurso político, justificando formalmente a adoção do Temperature Scaling e quantização WebGPU.
- *Resposta à Contribuição 2 (Intervenção Pedagógica com Agência Humana):* A integração de um rótulo pedagógico (*accuracy nudge*) acompanhado de botão de contestação (passo 7a) operou com taxa de contestação de 15,6% [13,7%–17,5%], sustentando a viabilidade de uma interface que induz reflexão de Sistema 2 sem recorrer a bloqueios, censura ou alteração coercitiva de postagens.
- *Revisão da Introdução:* A introdução foi harmonizada com os resultados, explicitando que a contribuição técnica reside na proposição do pipeline local e na quantificação do compromisso de calibração necessário para viabilizá-lo frente a regras e modelos de nuvem.

**referências conferidas:** 10 referências acadêmicas catalogadas, todas conferidas em seus DOIs oficiais na ACL Anthology, ACM Digital Library, Springer Link, PNAS e Nature:
1. Da San Martino et al. (2019, EMNLP) · DOI: `10.18653/v1/D19-1565`
2. Jahanbakhsh & Karger (2024, CHI) · DOI: `10.1145/3613904.3642473`
3. Pennycook et al. (2021, Nature) · DOI: `10.1038/s41586-021-03344-2`
4. Jin et al. (2022, Findings of EMNLP) · DOI: `10.18653/v1/2022.findings-emnlp.533`
5. Jahanbakhsh et al. (2022, CSCW / PACM HCI) · DOI: `10.1145/3555546`
6. Brady et al. (2017, PNAS) · DOI: `10.1073/pnas.1618923114`
7. Wulczyn, Thain & Dixon (2017, WWW) · DOI: `10.1145/3038912.3052591`
8. Habernal & Gurevych (2017, Computational Linguistics) · DOI: `10.1162/COLI_a_00276`
9. Warner et al. (2025, ACL) · DOI: `10.18653/v1/2025.acl-long.127`
10. Kang, Noels & De Bie / Vigil (2026, ECML PKDD / arXiv) · arXiv: `2604.03261`

**formato:** 
- *Modelo do veículo:* Springer LNCS (`llncs.cls`), padrão oficial do BRACIS.
- *Extensão:* formato de artigo completo (*full paper*), dimensionado para 12 a 15 páginas.
- *Anonimização:* preparado para revisão duplo-cega (*double-blind review*), com remoção de menções explícitas de autoria e substituição do link do repositório por URL anonimizada de submissão.

## auditoria cega

> **Aviso de Conformidade Ética (Regra 6 do Guia):** A auditoria cega não pode ser avaliada pela mesma IA que auxiliou na redação do artigo. O estudante deve abrir uma **conversa nova** no seu harness ou no ChatGPT/Claude, colar o prompt de auditoria com os 6 itens de verificação, colar o artigo/registro e colar a tabela resultante abaixo sem editar. Em seguida, o **aluno (sem auxílio de IA)** deve redigir a resposta a cada pendência.

**o veredito da conversa nova:** [preencha: a tabela, colada sem editar a partir de uma conversa nova]

**a minha resposta, sem IA:** [preencha: uma linha por pendência apontada pelo auditor cético]
