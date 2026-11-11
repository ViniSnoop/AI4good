# flx · Vinícius Fernandes de Souza

> folha do artefato [fluxograma e arquitetura](https://lucassf.pages.dev/ai4good/artefatos/3-fluxograma-e-arquitetura). o diagrama está no repositório: [arquitetura.md](../arquitetura.md).

## 0 · a minha ideia e o que eu medi

**FiltroSoberano · Extensão de Navegador.** Leitores, debatedores e produtores de conteúdo utilizam uma extensão de navegador open-source para Chrome, Firefox e Brave ao navegar no X/Twitter, Reddit, YouTube e WhatsApp Web. Em vez de varreduras pesadas em segundo plano, a extensão opera **sob demanda**: ao passar o mouse ou clicar em um botão de atalho em uma postagem suspeita, o modelo de decisão **Laya (Sistema 1, pesos abertos)** avalia em passada única a estrutura do texto localmente no navegador (via WebGPU/ONNX ou CPU). O modelo não tenta adivinhar se o fato é verídico, mas afere objetivamente **marcadores de retórica apelativa**: pontua a intensidade de pânico moral e urgência fabricada (`score`) e diagnostica táticas formais como ataque pessoal (*ad hominem*) e generalização abusiva (`choice`). O post nunca é censurado ou ocultado; o usuário recebe um rótulo pedagógico (*nudge*) sutil com a técnica identificada, municiando-se de clareza crítica e argumentos frios para não reagir por impulso nem ser manipulado por polarização artificial. (A SLM generativa local foi descartada após o tec para não sobrecarregar a máquina/navegador).

**o que eu medi no tec:** no tec (§ 3 e § 5), a execução do Laya na CPU (`convaiinnovations/laya` via PyTorch) levou menos de 1 segundo por post na triagem de 3 postagens sintéticas em português simulando feeds de redes sociais. O modelo acertou a presença de apelo e urgência no post alarmista (`score 1.91`, urgência `0.92`), mas cometeu erros na separação fina de classes com o checkpoint genérico: confundiu ataque pessoal com pânico moral (prob 0.34) no post 2 e falso dilema com ataque pessoal (prob 0.31) no post 3, com probabilidades dispersas e aviso de probabilidades não calibradas (`uncalibrated`). A execução comprovou viabilidade de Sistema 1 sem latência perceptível humana (<1 s na CPU), descartando a necessidade de SLM de apoio pesada e confirmando a inspeção pontual sob demanda.

## 1 · o fluxograma

**o diagrama:** [arquitetura.md](../arquitetura.md)

| nº | passo | IA, regra ou pessoa | por que IA, e não uma regra (sem IA) |
|:---|:---|:---|:---|
| 1 | usuário passa o mouse ou clica em "Analisar" sobre post suspeito no feed | pessoa | |
| 2 | content script extrai o texto do post do DOM da página e limpa tags/emojis repetidos | regra | |
| 3 | verificação de tamanho: texto com menos de 15 caracteres encerra com alerta curto | regra | |
| 4 | Laya (Sistema 1) infere a tática retórica (`choice`) e a intensidade de apelo (`score`) | IA | *(substitua com suas próprias palavras)* Uma regra de palavras proibidas ou regex quebraria porque falácias formais (como falso dilema ou ataque pessoal velado) dependem da relação entre sujeito e argumento, e não de termos fixos; além disso, palavras como "urgente" ou "grave" ocorrem legitimamente em notícias sem que haja apelo manipulativo. |
| 5 | dicionário estático mapeia o diagnóstico para badge pedagógico e dica formatada | regra | |
| 6 | content script injeta o badge/tooltip (*nudge*) pedagógico discreto diretamente sobre o post | regra | |
| 7 | usuário lê o rótulo pedagógico, ganha distanciamento reflexivo e decide como agir | pessoa | |

## 2 · as peças: o que entra, o que sai, onde roda e quanto custa

**a escala do custo por mês:** 1 usuário ativo no X/Twitter ou Reddit inspecionando ~10 postagens suspeitas por dia: **300 postagens inspecionadas por mês** (~30.000 tokens de texto). Em escala de comunidade com 1.000 usuários ativos: **300.000 postagens por mês** (~30.000.000 tokens de texto).

| peça | entra | sai | onde roda, e por quê | tempo e máquina por uso | R$ por mês na escala | medido ou estimado · fonte e data |
|:---|:---|:---|:---|:---|:---|:---|
| Extensão de Navegador (content script + UI) | clique do usuário e elemento HTML do post | texto limpo para o modelo; badge renderizado na interface | navegador local do usuário (Chrome/Firefox/Brave): precisa acessar o DOM diretamente | <5 ms; <1 MB de RAM | R$ 0 | **estimado**: manipulação nativa de DOM em JavaScript |
| Laya (pesos abertos, Apache 2.0) | texto da postagem (~50 a 500 caracteres) | diagnóstico (`choice`) e intensidade (`score`) | navegador local via WebGPU/ONNX: garante privacidade total do feed e custo zero de infraestrutura | tempo: menos de 1 s por post; máquina: ~130 MB de RAM (ONNX int8) ou ~500 MB (FP32) | R$ 0 | tempo **medido** no tec. memória **estimada** do modelo; repositório e licença em [github.com/NandhaKishorM/laya](https://github.com/NandhaKishorM/laya), 11/11/2026 |
| alternativa não escolhida: Nuvem (OpenAI gpt-4o-mini via API) | texto da postagem via HTTPS | JSON com classificação e intensidade | servidores da OpenAI: descartada por violar privacidade do feed e criar dependência de conexão/chave | 300 a 800 ms por post (latência de rede + API) | ~US$ 0,006 (menos de R$ 0,05) para 1 usuário; ~US$ 6,75 (~R$ 39) para 1.000 usuários (a R$ 5,80/US$) | **estimado**: US$ 0,15/1M input e US$ 0,60/1M output em [openai.com/pricing](https://openai.com/pricing), consultado em 11/11/2026 |

## 3 · a arquitetura: onde roda cada peça e para onde vão os dados

**o diagrama, com as caixas de onde cada peça roda:** [arquitetura.md](../arquitetura.md)

| dado pessoal / conteúdo | de quem é | onde fica | quem vê | por quanto tempo | quando é apagado |
|:---|:---|:---|:---|:---|:---|
| texto da postagem inspecionada | do autor do post no feed | memória temporária (RAM) da extensão | apenas a extensão no navegador local | frações de segundo durante a passada da IA | apagado imediatamente da memória após a inferência |
| diagnóstico e pontuação gerados | da pessoa usuária | DOM temporário da página aberta | apenas a pessoa usuária na sua tela | enquanto a aba estiver ativa | destruído ao fechar a aba ou recarregar o feed |
| perfil / URL / identificador do autor | do autor do post | não é extraído nem armazenado | ninguém | nunca | não entra no pipeline do sistema |

**o que sai do aparelho de quem usa, e para onde:** absolutamente nada. O FiltroSoberano roda 100% no dispositivo do usuário (client-side) via WebGPU/ONNX Runtime Web. Não existe servidor intermediário, banco de dados remoto ou telemetria em nuvem.

**o mínimo que a ideia precisa guardar:** apenas a sequência de caracteres do texto do post selecionado na memória volátil durante o forward pass do modelo (<1 s). Não é persistido nenhum dado em disco, cache permanente, cookies ou banco de dados local.

## 4 · o que mudou na ideia, sem IA

A SLM generativa local foi descartada: a explicação da falácia virou um dicionário estático de regras vinculado à classe do Laya, economizando ~2 GB de memória.  
A checagem de tamanho mínimo (<15 caracteres) virou uma regra antes da IA, evitando acionamentos inúteis.  
A comparação com a nuvem mostrou que ela custaria menos de R$ 0,05 por usuário, mas o processamento local foi mantido pela privacidade total do feed, não pelo custo.  
O fluxograma delimitou a fronteira clara: o modelo só atua no diagnóstico sintático-semântico, enquanto toda a interface e o conselho crítico são regras fixas.

## 5 · auditoria cega

**o veredito da conversa nova:**

| item | passa ou não passa | trecho que prova | o que encontrei (links abertos, regras tentadas) |
|:---|:---|:---|:---|
| 1 · fluxograma (IA, regra ou pessoa) | | | |
| 2 · entradas, saídas, onde roda e custo | | | |
| 3 · arquitetura, dados e privacidade | | | |

**a minha resposta, sem IA:**
1. 
2. 
3. 
