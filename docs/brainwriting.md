# brw · Vinícius Fernandes de Souza

> folha do artefato [brainwriting híbrido](../3-brainwriting-hibrido.md). siga o guia passo a passo
> e preencha cada seção aqui. as decisões são suas, e decidir é saber explicar.

## 1 · onde atacar

**crise** (marque 1 com `x`):

| | crise |
|:-:|:--|
| [ ] | perda do raciocínio crítico e alienação (*slop*) |
| [ ] | a verdade sob mira e colapso epistêmico (*fakes*) |
| [x] | manipulação política e democracia (*bots*) |
| [ ] | crise ecológica da IA (água e energia) |
| [ ] | alimentação com veneno e ultraprocessados (vs. feiras agroecológicas) |
| [ ] | endividamento e dreno das *bets* |
| [ ] | moradia e especulação (casas vazias) |
| [ ] | concentração de plataformas e trabalho |
| [ ] | outra: [preencha: a crise, e em 1 linha por que é relevante] |

por que esta crise: Em períodos eleitorais, redes sociais e Big Techs amplificam manipulações e assimetrias algorítmicas (como no caso da Meta AI restringindo candidatos), sequestrando a atenção do eleitor por meio de pânico moral e guerras informacionais.

**tecnologias de IA** (marque 3 e chame de A, B, C):

| | tecnologia de IA |
|:-:|:--|
| [x] A | modelos locais / no aparelho (*SLMs*, 1B–7B) |
| [ ] | sistemas multiagente e agência (*tools*, MCP) |
| [ ] | visão computacional e OCR |
| [ ] | voz (fala ↔ texto) e interfaces sem tela |
| [x] B | grafos e RAG (redes de grafos, busca vetorial) |
| [ ] | modelos de difusão / geração visual |
| [x] C | outra: modelos de decisão estruturada de "Sistema 1" (Laya: choice, score e noul em inferência local) |

**infraestruturas tradicionais** (marque 3 e chame de 1, 2, 3):

| | infraestrutura |
|:-:|:--|
| [ ] | plataformas de dois lados (*matching*, como Uber) |
| [ ] | geolocalização, GPS e mapas |
| [ ] | e-commerce, marketplaces e catálogos |
| [x] 1 | mensageria leve e bots (WhatsApp Web, Telegram) |
| [x] 2 | redes sociais, feeds e comunidades (X, Facebook, YouTube, Reddit) |
| [ ] | pagamento instantâneo (Pix, moeda local) |
| [ ] | crowdsourcing e curadoria coletiva |
| [x] 3 | outra: extensões e plugins de navegador (injeção no DOM via JavaScript / WebGPU local) |

## 2 · clichês

| clichê | o que acerta | onde fica raso |
|:--|:--|:--|
| Checadores de fatos comunitários (ex: Notas da Comunidade do X/Twitter) | Busca corrigir desinformação com fontes abertas e descentralização da checagem. | Depende da iniciativa voluntária de usuários; demora para aprovar consensos em bolhas polarizadas e chega tarde demais. |
| Moderação automatizada por IA para bloquear propagandas e conteúdos eleitorais enganosos | Reconhece a velocidade necessária para barrar desinformação massiva em escala de plataforma. | Torna-se ferramenta de censura e assimetria política opaca (como abusos corporativos de Big Techs bloqueando candidatos específicos). |
| Obrigatoriedade de marcas d'água / selos criptográficos em mídias geradas por IA | Cria padrão técnico rastreável para atestar procedência de fotos e vídeos de campanhas. | Facilmente removido por modelos open source locais; gera falsa sensação de que mídias sem selo são necessariamente autênticas. |
| Cartilhas e campanhas de letramento digital e conscientização do eleitor | Fortalece a autonomia crítica e o discernimento individual no longo prazo. | Desconsidera a sofisticação da micro-segmentação psicológica e o design viciante das redes, transferindo a culpa sistêmica para o indivíduo. |
| Criação de uma "IA neutra oficial" ou assistente público para comparar candidatos | Visa oferecer acesso isonômico a propostas e planos de governo sem intermediários partidários. | Ilusão de neutralidade algorítmica; modelos herdam premissas e vieses de treinamento, sendo vulneráveis a pressões institucionais de quem os financia. |

## 3 · matriz 3 × 3 e a minha ideia

cada célula: **nome** · frase de até 20 palavras (quem usa, o que faz).

| | 1 · mensageria web | 2 · redes sociais e feeds web | 3 · extensões de navegador |
|:--|:--|:--|:--|
| **A · modelos locais (SLMs)** | **Sentinela Privada** · Cidadãos usam modelo offline no navegador para analisar mensagens eleitorais recebidas sem enviar conversas para servidores corporativos. | **FeedSoberano** · Usuários reescrevem manchetes apelativas e sensacionalistas em resumos factuais neutros diretamente no feed via SLM local. | **Explicador Local** · Usuários clicam em postagens sinalizadas para gerar explicações lógicas em duas linhas sobre as falácias detectadas. |
| **B · grafos e RAG** | **Grafo de Disparos** · Usuários verificam se um texto recebido faz parte de campanha de disparos em massa catalogada na base vetorial. | **Mapeador de Bots** · Pesquisadores cruzam grafos de retuítes e menções para identificar fazendas de contas automatizadas em redes sociais. | **RAG Cívico** · Extensão cruza promessas de candidatos no feed com uma base vetorial local contendo os planos de governo oficiais. |
| **C · modelos de decisão (Laya)** | **ZapAudit** · Usuários inspecionam mensagens no WhatsApp Web sob demanda com Laya gerando score de urgência artificial e golpe. | **Radar de Feed** · Leitores ativam classificação por atalho que pontua o nível de agressividade e apelo emocional de uma postagem. | **FiltroSoberano** · Usuários acionam inspeção sob demanda com Laya para diagnosticar marcadores de retórica apelativa e pânico moral no feed. |

**as 9 no mapa impacto × viabilidade:**

| | viabilidade alta | viabilidade baixa |
|:--|:--|:--|
| **impacto alto** | **FiltroSoberano** — inspeção sob demanda leve no navegador sem travar a interface; teste de viabilidade direta no semestre.<br>**Explicador Local** — fornece munição analítica sob demanda; viável acoplando SLM compacta ativada por clique. | **Mapeador de Bots** — alto potencial de inteligência pública; inviável no semestre por exigir acesso a APIs pagas e restritas de redes sociais.<br>**RAG Cívico** — conecta propostas a planos oficiais; mas manter base vetorial atualizada no navegador exige infraestrutura pesada. |
| **impacto baixo** | **ZapAudit** — evita golpes rápidos, mas o WhatsApp Web dificulta injeção contínua no DOM; teste pequeno.<br>**Radar de Feed** — apenas pontua agressividade sem explicar; viável, mas muda pouco o comportamento crítico.<br>**Sentinela Privada** — analisa mensagens isoladas; fácil de testar, mas não resolve o fluxo massivo de feeds. | **Grafo de Disparos** — depende de sincronização comunitária de mensagens privadas para alimentar o grafo; atrito de adesão.<br>**FeedSoberano** — reescrever posts completos com SLM gera latência na rolagem e cansa o leitor; teste complexo. |

**as duas perguntas: o argumento do interesse próprio e a alternativa sem IA:**

| ideia | quem usa ganha, para si | o que custa a ele | o que resolve sem IA avançada | se sustenta? |
|:--|:--|:--|:--|:--|
| Sentinela Privada | descobre se uma mensagem no WhatsApp Web é suspeita | encaminhar ou copiar o texto para a ferramenta | um buscador de checagens prontas | **não**: buscar em agências de checagem resolve |
| FeedSoberano | lê feeds sem o tom apelativo do sensacionalismo | espera de 2 a 3 segundos por post para reescrita | um leitor de modo texto / modo leitura sem anúncios | **não**: o custo de esperar a reescrita supera o ganho |
| Explicador Local | entende a estrutura da manipulação para vencer debates | um clique no post suspeito para pedir explicação | uma lista estática de falácias lógicas | **sim** |
| Grafo de Disparos | sabe se a corrente de mensagens é artificial | doar metadados de mensagens para a rede | estatísticas de frequência de envio | **não**: listas de correntes famosas já resolvem |
| Mapeador de Bots | visualiza cartéis de impulsionamento na rede | configurar credenciais e parâmetros de coleta | scripts convencionais de análise de frequência | **não**: métricas comuns de repetição já acham bots |
| RAG Cívico | descobre se a fala bate com o plano de governo | abrir painel lateral e esperar a busca semântica | buscar por palavra-chave no PDF do plano | **sim** |
| ZapAudit | alerta imediato de golpe ou fraude financeira na conversa | instalar extensão e manter WhatsApp Web aberto | regras regex de palavras-chave suspeitas ("PIX", "urgente") | **não**: regras regex simples já alertam palavras de golpe |
| Radar de Feed | vê score de polarização sem precisar ler a briga | processamento local de cada post | contadores de palavras agressivas pré-definidas | **não**: dicionários de palavras tóxicas já fazem score |
| FiltroSoberano | diagnostica manipulação retórica com um clique sem lag | acionar a inspeção sob demanda com atalho ou clique | nada: a semântica contextual de apelo ao medo escapa de filtros regex | **sim** |

onde discordei da IA, e por quê: A IA inicialmente tratava a análise contínua em tempo real de todo o feed como indispensável, o que travaria o navegador em hardwares comuns. Discordei e adotei a inspeção sob demanda: a extensão só aciona o Laya (modelo de decisão de Sistema 1, open-source) quando o usuário clica ou passa o cursor sobre um post específico. Isso viabiliza um teste de semestre real: consigo medir em laboratório a acurácia do Laya em identificar marcadores de apelo ao medo e ataques pessoais em 50 postagens reais com resposta em menos de 50 ms por clique.

**minha ideia escolhida:** **FiltroSoberano** · Usuários acionam inspeção sob demanda com Laya para diagnosticar marcadores de retórica apelativa e pânico moral no feed.

**por que ela, sem IA, em até 3 linhas:**
A navegação nas redes virou um campo minado de manipulação emocional desenhada para gerar indignação rápida.
A inspeção sob demanda com Laya viabiliza diagnóstico instantâneo no navegador sem travar a interface nem consumir recursos ociosos.
A ferramenta devolve o controle crítico ao usuário na hora de ler postagens duvidosas, sem censura e com privacidade total.

## 4 · motores

| motor | o que foi [verbo] | nome | frase | o que mudou em relação à ideia | o que quem usa ganha para si | se sustenta nas duas perguntas? |
|:--|:--|:--|:--|:--|:--|:--|
| inverter | o que foi invertido: o sentido da auditoria: em vez do usuário inspecionar o post, gera relatório da manipulação que o algoritmo tentou impor a ele. | **Dossiê Algorítmico** | Usuários geram relatórios semanais das táticas de manipulação mais frequentes em sua timeline para auditar as redes. | De proteção pontual sob demanda para compilação periódica de auditoria do feed. | Gera provas concretas de como o algoritmo direciona pautas para seu perfil. | **não**: exige esforço de compilação sem benefício prático imediato na navegação. |
| canalizar | o que foi canalizado: a irritação com manchetes sensacionalistas, convertida em alerta pedagógico de urgência fabricada. | **Nudge de Serenidade** | Usuários ativam badge sutil que indica postagens com score de urgência artificial acima de 80% ao passar o mouse. | Canaliza a indignação para uma pausa reflexiva antes de reagir ao post. | Evita engajar por impulso em provocações vazias no feed. | **sim** |
| transplantar | o que foi transplantado, e de onde: a ferramenta de "inspecionar elemento" dos desenvolvedores para a retórica política. | **Lupa Retórica** | Como um desenvolvedor inspeciona o código HTML, o leitor inspeciona a estrutura retórica de um post com um clique. | Transplanta a interface de inspeção técnica de navegadores para a crítica textual cidadã. | Vê os artifícios de linguagem usados no post em segundos. | **sim** |
| reescalar | o que foi reescalado: a escala da decisão: de um usuário para uma redação de checagem ou sala de aula. | **Painel de Redação** | Estudantes e jornalistas analisam lotes de notícias simultâneas com Laya categorizando as falácias mais usadas. | De extensão individual de clique para ferramenta de análise de texto em lote. | Triagem rápida de dezenas de matérias sem leitura manual exaustiva. | **não**: planilhas com scripts de automação tradicionais atendem redações. |
| trocar a persona | quem saiu, quem entrou: saiu o leitor casual, entraram influenciadores e debatedores de internet. | **Armadura do Debatedor** | Criadores de conteúdo usam atalho de teclado para diagnosticar a falácia do adversário e fundamentar sua resposta. | O usuário passa a ser o debatedor ativo que precisa rebater provocações públicas. | Desmonta armadilhas retóricas do adversário e vence discussões públicas. | **sim** |
| trocar o contexto | de onde, para onde: de redes sociais abertas para portais de notícias corporativas e mercado financeiro. | **Filtro Corporativo** | Profissionais usam a extensão em portais de notícias para identificar sensacionalismo em matérias econômicas. | Transfere do contexto eleitoral para a análise de notícias financeiras. | Identifica alarmismo antes de tomar decisões de investimento. | **não**: o mercado já possui relatórios especializados de análise fundamentalista. |
| trocar a tecnologia | de qual, para qual: de Laya puro para Laya combinado com regras simbólicas de pré-filtragem. | **Filtro Híbrido** | A extensão usa regras simbólicas para descartar texto curto neutro e aciona o Laya apenas quando há carga adjetiva forte. | Adiciona camada prévia de regras rápidas para economizar chamadas locais do modelo. | Resposta ainda mais instantânea no clique com consumo mínimo de memória. | **sim** |
| juntar | o que foi juntado: classificação estruturada de Sistema 1 (Laya) + explicação didática de Sistema 2 (SLM destilada). | **FiltroSoberano Duo** | Laya classifica instantaneamente a técnica retórica no badge, e uma SLM local gera a explicação de duas linhas ao expandir. | Une a velocidade da decisão (<50ms) com a didática argumentativa da linguagem natural. | Entende o porquê da manipulação sem travar a navegação. | **sim** |
| restringir | o que foi restringido: a conectividade; a extensão opera sem permissão de acesso à internet (`permissions: []` no manifest). | **Filtro Zero-Net** | A extensão funciona com modelo Laya embutido via WebGPU sem permissão de rede para envio de dados. | Restringe a zero o tráfego de saída, garantindo sigilo matemático sobre o histórico lido. | Certeza absoluta de que seus hábitos de leitura nunca serão monitorados. | **sim** |

## 5 · o que fica e o que sai

**o que eu gostei:** Gostei da **inspeção sob demanda** via Laya (Sistema 1) combinada à SLM para explicações apenas sob clique (**FiltroSoberano Duo**): elimina totalmente o travamento do navegador, resolve o problema de memória do Manifest V3 e mantém a experiência ágil. Também aprovei o **Nudge de Serenidade**, que alerta sobre urgência artificial sem censurar nem esconder o conteúdo.

**o que achei interessante:** A **Armadura do Debatedor**: utilizar a detecção rápida de marcadores retóricos como ferramenta para fundamentar contra-argumentos atende diretamente ao desejo individual de não ser passado para trás em discussões na internet.

**o que eu descarto, e por quê:** Descarto a **varredura passiva contínua de todo o feed** (inexequível em hardware médio e causadora de travamento de tela). Descarto tentar **checar fatos ou veracidade de notícias** (um modelo offline não tem conhecimento de mundo do dia). Descarto a **ocultação de postagens**, pois remover posts geraria acusação de censura e bolhas reversas; a ferramenta deve apenas orientar pedagogicamente.

**minha ideia completa:** **FiltroSoberano · Extensão de Navegador**

Leitores, debatedores e produtores de conteúdo utilizam uma extensão de navegador open-source para Chrome, Firefox e Brave ao navegar no X/Twitter, Reddit, YouTube e WhatsApp Web.  
Em vez de varreduras pesadas em segundo plano, a extensão opera **sob demanda**: ao passar o mouse ou clicar em um botão de atalho em uma postagem suspeita, o modelo de decisão **Laya (Sistema 1, pesos abertos)** avalia em menos de 50 milissegundos a estrutura do texto via WebGPU/ONNX local.  
O modelo não tenta adivinhar se o fato é verídico, mas afere objetivamente **marcadores de retórica apelativa**: pontua a intensidade de pânico moral e urgência fabricada (`score`) e diagnostica táticas formais como ataque pessoal (*ad hominem*) e generalização abusiva (`choice`), acionando uma SLM destilada apenas se o usuário solicitar uma explicação detalhada.  
O post nunca é censurado ou ocultado; o usuário recebe um rótulo pedagógico (*nudge*) sutil com a técnica identificada, municiando-se de clareza crítica e argumentos frios para não reagir por impulso nem ser manipulado por narrativas de polarização artificial.

## 6 · refinamento

**a · e se todo mundo usasse?**

o tamanho da crise hoje:
- 70% da população brasileira declara preocupação expressa com a dificuldade de distinguir conteúdos reais de notícias falsas e manipulações nas redes ([Reuters Institute / Oxford Digital News Report 2023](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2023/brazil)).
- 63% dos brasileiros utilizam redes sociais e aplicativos de mensagens como principal fonte semanal de notícias e debate político ([Reuters Institute / Oxford Digital News Report 2023](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2023/brazil)).
- Nas eleições brasileiras, o Sistema de Alertas de Desinformação Eleitoral (SIADE) do TSE já registrou mais de 30 mil denúncias formais de disparos coordenados e desinformação eleitoral ([Tribunal Superior Eleitoral - TSE](https://www.tse.jus.br/comunicacao/noticias/2022/Novembro/sistema-de-alerta-do-tse-recebeu-mais-de-30-mil-denuncias-nas-eleicoes-2022)).
- Mais de R$ 250 milhões foram gastos oficialmente em impulsionamento pago de propaganda e conteúdo político em Big Techs nas eleições recentes, alimentando algoritmos que premiam engajamento polarizado ([Dados de Prestação de Contas - DivulgaCandContas TSE](https://divulgacandcontas.tse.jus.br/)).

se todo mundo usasse por 5 anos (a minha aposta):
- se a extensão alcançasse 15% dos usuários que debatem e consomem política na web (cerca de 3 milhões de debatedores, jornalistas e formadores de opinião ativos no desktop), o contágio de campanhas polarizadas perderia a força de reverberação nos nós de maior influência da rede.
- se a taxa de engajamento reativo por impulso caísse 50% entre esses usuários multiplicadores, o modelo de negócios de perfis sensacionalistas e fazendas de pânico moral perderia tração financeira, reduzindo a rentabilidade dos R$ 250 milhões investidos em impulsionamento tóxico.
- as denúncias no SIADE do TSE por descontextualização deliberada seriam reduzidas significativamente, uma vez que a retórica apelativa seria identificada e desarmada publicamente nos próprios comentários antes de viralizar.

por que cada pessoa usaria: o usuário casual usa por higiene mental (para não cair em armadilhas de urgência artificial e pânico moral); o debatedor de internet usa por ego e vaidade (para obter em segundos o diagnóstico da técnica retórica do adversário e fundamentar sua tréplica); o comunicador usa para não passar vergonha repercutindo narrativas distorcidas. Ninguém precisa de altruísmo cívico.

**b · a IA que não pode faltar.** técnica: Modelos de Decisão de "Sistema 1" (Laya, pesos abertos Apache 2.0 com primitivas `choice` e `score` em forward pass único de <50ms via WebGPU/ONNX) integrados a uma SLM destilada local acionada sob demanda.

por que sem ela não roda: Expressões regulares ou listas de palavras-chave ignoram o contexto semântico e geram falsos positivos grotescos (ex.: confundem uma denúncia séria com pânico moral). Por outro lado, LLMs generativos tradicionais demoram segundos e travam o navegador se executados continuamente. O Laya é insubstituível porque executa a decisão em milissegundos em uma única passagem matemática, avaliando a forma estilística do argumento sem demandar conexão externa. Sem essa IA local estruturada, a ideia ou travaria o hardware comum ou exigiria servidores corporativos que violariam a privacidade.

**c · críticas de quem está de fora**

| crítica | saída 1 | saída 2 | minha decisão |
|:--|:--|:--|:--|
| O processamento de modelos no navegador gera lentidão (*jank*) no scroll e colide com limites de memória do Manifest V3. | Executar o modelo na nuvem via API paga e devolver os resultados ao navegador. | Abandonar a varredura passiva contínua e acionar o Laya estritamente sob demanda (hover ou clique do usuário) no post em foco. | **saída 2**: o processamento ocorre apenas quando requisitado pelo usuário em um elemento individual, garantindo consumo de recursos próximo a zero em repouso e respeitando o ciclo de vida do navegador. |
| Modelos offline congelados não possuem conhecimento de fatos recentes e confundem denúncias graves com pânico moral. | Integrar APIs de busca em tempo real para checagem fática em bases jornalísticas. | Restringir o escopo do modelo à análise de marcadores de retórica formal e apelo emocional (ad hominem, urgência artificial), sem julgar a veracidade do fato. | **saída 2**: o modelo avalia exclusivamente a forma do argumento (estilo e persuasão), deixando explícito ao usuário que a ferramenta analisa a retórica apelativa e não a verdade factual da notícia. |
| A desinformação em massa no Brasil corre nos celulares (WhatsApp e TikTok nativos), tornando extensões desktop inócuas para a base do eleitorado. | Tentar desenvolver um teclado virtual customizado para interceptar conversas no Android. | Focar a ferramenta deliberadamente nos nós multiplicadores de opinião (jornalistas, ativistas, debatedores e criadores de conteúdo que operam no desktop). | **saída 2**: delimitação consciente de público; a extensão não tenta atingir toda a população mobile, mas sim blindar a camada de debatedores e comunicadores que desmascaram narrativas na origem antes de viralizarem. |

## 7 · resumo, sem IA

1. Campanhas de desinformação utilizam pânico moral e retórica apelativa para sequestrar a atenção do eleitor e inflar figuras sem planos reais.
2. O FiltroSoberano é uma extensão de navegador open-source para inspeção de técnicas retóricas sob demanda em postagens sociais no desktop.
3. A IA entra com o Laya (modelo de decisão rápida de Sistema 1), que analisa instantaneamente marcadores estilísticos de manipulação via WebGPU local sem censurar conteúdos.
4. Se todos os formadores de opinião usassem, as narrativas manipulativas seriam desarmadas na origem, desmontando a rentabilidade dos disparos em massa.
5. Cada pessoa usa para preservar sua estabilidade emocional contra pânico fabricado e desmascarar artifícios retóricos de adversários em debates.
