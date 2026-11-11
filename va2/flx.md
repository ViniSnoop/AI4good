# flx · Vinícius Fernandes de Souza

> folha do artefato [fluxograma e arquitetura](https://lucassf.pages.dev/ai4good/artefatos/3-fluxograma-e-arquitetura). o diagrama está no repositório: [arquitetura.md](../arquitetura.md).

## 0 · a minha ideia e o que eu medi

**FiltroSoberano · Extensão de Navegador.** Leitores, debatedores e produtores de conteúdo utilizam uma extensão de navegador open-source para Chrome, Firefox e Brave ao navegar no X/Twitter, Reddit, YouTube e WhatsApp Web. Em vez de varreduras pesadas em segundo plano, a extensão opera **sob demanda**: ao passar o mouse ou clicar em um botão de atalho em uma postagem suspeita, o modelo de decisão **Laya (Sistema 1, pesos abertos)** avalia em passada única a estrutura do texto localmente no navegador (via WebGPU/ONNX Runtime Web). O modelo não tenta adivinhar se o fato é verídico, mas afere objetivamente **marcadores de retórica apelativa**: pontua a intensidade de pânico moral e urgência fabricada (`score`) e diagnostica táticas formais como ataque pessoal (*ad hominem*) e generalização abusiva (`choice`). O post nunca é censurado ou ocultado; o usuário recebe um rótulo pedagógico (*nudge*) sutil com a técnica identificada e tem a opção de marcar falso positivo, municiando-se de clareza crítica e argumentos frios para não reagir por impulso nem ser manipulado por polarização artificial. (A SLM generativa local foi descartada após o tec para não sobrecarregar a máquina/navegador).

**o que eu medi no tec:** no tec (§ 3 e § 5), a execução do Laya na CPU (`convaiinnovations/laya` via PyTorch) levou menos de 1 segundo por post na triagem de 3 postagens sintéticas em português simulando feeds de redes sociais. O modelo acertou a presença de apelo e urgência no post alarmista (`score 1.91`, urgência `0.92`), mas cometeu erros na separação fina de classes com o checkpoint genérico (que é o base em inglês): confundiu ataque pessoal com pânico moral (prob 0.34) no post 2 e falso dilema com ataque pessoal (prob 0.31) no post 3, com probabilidades dispersas e aviso de probabilidades não calibradas (`uncalibrated`). A execução comprovou viabilidade de Sistema 1 sem latência perceptível humana (<1 s na CPU), descartando a necessidade de SLM de apoio pesada e indicando que para a extensão final em português o alvo de implementação é o checkpoint multilíngue oficial quantizado (`convaiinnovations/laya-multilingual`, 322M parâmetros) executado via `onnxruntime-web`.

## 1 · o fluxograma

**o diagrama:** [arquitetura.md](../arquitetura.md), commit [f3588f0](https://github.com/ViniSnoop/AI4good/commit/f3588f0)

| nº | passo | IA, regra ou pessoa | por que IA, e não uma regra (sem IA) |
|:---|:---|:---|:---|
| 1 | usuário passa o mouse ou clica em "Analisar" sobre post suspeito no feed | pessoa | |
| 2 | content script extrai o texto do post do DOM da página e limpa tags/emojis repetidos | regra | |
| 3 | verificação de tamanho: texto tem pelo menos 15 caracteres? | regra | |
| 3a | se texto < 15 caracteres: exibe alerta de texto curto e encerra a análise | regra | |
| 4 | Laya Multilingual (Sistema 1 via ONNX) infere a tática (`choice`) e a intensidade de apelo (`score`) | IA | *(substitua com suas próprias palavras)* Uma regra determinística (como regex para ofensas explícitas, estruturas "ou... ou" para falso dilema, ou listas de termos alarmistas) quebra na internet real: não capta ataques velados ou sarcásticos sem palavras de baixo calão, gera falsos positivos gravíssimos ao confundir urgência legítima (ex.: alerta real de defesa civil ou notícia com a palavra "urgente") com manipulação apelativa, e não avalia a relação sintática entre premissas e conclusão necessária para identificar falácias estruturais. |
| 5 | dicionário estático mapeia o diagnóstico para badge pedagógico e dica formatada | regra | |
| 6 | content script injeta o badge/tooltip (*nudge*) pedagógico discreto diretamente sobre o post | regra | |
| 7 | usuário lê o rótulo pedagógico, ganha distanciamento reflexivo e decide como agir | pessoa | |
| 7a | conferência humana: usuário pode fechar o badge ou clicar em "Discordar / Falso positivo" | pessoa | |

## 2 · as peças: o que entra, o que sai, onde roda e quanto custa

**a escala do custo por mês:** 1 usuário ativo no X/Twitter ou Reddit inspecionando ~10 postagens suspeitas por dia: **300 postagens inspecionadas por mês**. Cada post tem em média 100 tokens de entrada e produz 50 tokens de resposta estruturada. Para 1 usuário: 30.000 tokens de entrada e 15.000 tokens de saída por mês. Em escala de comunidade com 1.000 usuários ativos: **300.000 postagens por mês** (30.000.000 tokens de entrada e 15.000.000 tokens de saída).

| peça | entra | sai | onde roda, e por quê | tempo e máquina por uso | R$ por mês na escala | medido ou estimado · fonte e data |
|:---|:---|:---|:---|:---|:---|:---|
| Extensão de Navegador (content script + UI) | clique do usuário e elemento HTML do post | texto limpo para o modelo; badge renderizado na interface | navegador local do usuário (Chrome/Firefox/Brave): precisa acessar o DOM diretamente | tempo: <5 ms; máquina: <2 MB de RAM adicional | R$ 0 | **estimado**: manipulação padrão de DOM e eventos em JavaScript |
| ONNX Runtime Web + Cache local | pesos ONNX quantizados e dependências do CDN | runtime inicializado e buffers de tensores prontos | navegador local via WebAssembly / WebGPU e CacheStorage | download inicial único de ~420 MB via Wi-Fi no 1º uso; zero transferência depois | R$ 0 | **estimado**: documentação do [Laya TypeScript](https://github.com/NandhaKishorM/laya/tree/main/laya-ts) e [onnxruntime-web](https://www.npmjs.com/package/onnxruntime-web), 11/11/2026 |
| Laya Multilingual (322M params, Apache 2.0) | texto da postagem (~50 a 500 caracteres) | diagnóstico (`choice`) e intensidade (`score`) | navegador local via WebGPU/WASM: garante privacidade total do feed e custo zero de infraestrutura | tempo: menos de 1 s por post (no tec: <1 s em CPU PyTorch); máquina: ~390 MB encoder + 32 MB heads em INT8 (~420 MB em RAM) | R$ 0 de servidor para o criador; consumo elétrico desprezível por ser sob demanda pontual (~10 posts/dia) | tempo **medido** no tec (<1 s em CPU). arquitetura e memória INT8 **estimadas** a partir do [Laya TypeScript / HF](https://huggingface.co/convaiinnovations/laya-multilingual), 11/11/2026, licença Apache 2.0 |
| alternativa não escolhida: Nuvem (OpenAI gpt-4o-mini via API) | texto da postagem via HTTPS | JSON com classificação e intensidade | servidores da OpenAI: descartada por violar privacidade do feed e criar dependência de conexão/chave | 300 a 800 ms por post (latência de rede + fila de API) | 1 usuário: US$ 0,0135 (~R$ 0,08/mês); 1.000 usuários: US$ 13,50 (~R$ 78,30/mês a R$ 5,80/US$) | **estimado**: US$ 0,15/1M input ($30M = US$ 4,50) + US$ 0,60/1M output ($15M = US$ 9,00) em [openrouter.ai/openai/gpt-4o-mini](https://openrouter.ai/openai/gpt-4o-mini) e [openai.com/api/pricing](https://developers.openai.com/api/docs/pricing), consultado em 11/11/2026 |

*Por que a alternativa na nuvem não foi escolhida:* Embora o custo financeiro para 1.000 usuários (R$ 78,30/mês) seja baixo, a nuvem exige que todo texto inspecionado seja transmitido para os servidores da OpenAI, violando o princípio de privacidade e soberania do usuário sobre seus hábitos de leitura e exposição política. Além disso, a execução local não requer chaves de API pagas nem sofre com queda de conexão.

## 3 · a arquitetura: onde roda cada peça e para onde vão os dados

**o diagrama, com as caixas de onde cada peça roda:** [arquitetura.md](../arquitetura.md), commit [f3588f0](https://github.com/ViniSnoop/AI4good/commit/f3588f0)

| dado pessoal / conteúdo | de quem é | onde fica | quem vê | por quanto tempo | quando é apagado |
|:---|:---|:---|:---|:---|:---|
| texto da postagem inspecionada (pode conter nomes ou dados de terceiros) | do autor do post no feed | memória temporária (RAM) da aba ativa | apenas a extensão no navegador local | frações de segundo durante o forward pass da IA | apagado imediatamente da memória volátil após a inferência, sem qualquer gravação em disco |
| diagnóstico retórico e pontuação gerados | da pessoa usuária | DOM temporário da página aberta | apenas a pessoa usuária na sua tela | enquanto a aba estiver ativa | destruído ao fechar a aba ou recarregar o feed |
| clique de discordância / feedback (passo 7a) | da pessoa usuária | memória volátil da extensão | apenas a pessoa usuária | durante a sessão atual | descartado ao fechar o navegador |
| perfil / URL / metadados do autor | do autor do post | não é extraído nem acessado | ninguém | nunca | não entra no pipeline do sistema |
| arquivos estáticos do modelo (pesos quantizados) | do projeto Laya (pesos abertos) | CacheStorage do navegador | runtime ONNX local | persistente até desinstalação | ao desinstalar a extensão ou limpar o cache do navegador |

**o que sai do aparelho de quem usa, e para onde:** absolutamente nenhum dado lido, digitado ou navegado sai do computador da pessoa. A única requisição externa é feita uma única vez durante a instalação para baixar os arquivos estáticos dos pesos do modelo Laya a partir de um repositório público (CDN do Hugging Face / GitHub Releases), salvando-os no `CacheStorage` do navegador. Não há telemetria, não há registro de analytics e não há servidores intermediários.

**o mínimo que a ideia precisa guardar:** apenas a string de texto do post sob análise na memória RAM volátil durante a inferência (<1 segundo). Nenhum dado de histórico de navegação, perfil ou identificação é persistido.

## 4 · o que mudou na ideia, sem IA

A SLM generativa local foi descartada: a explicação da falácia virou um dicionário estático de regras vinculado à classe do Laya, economizando mais de 2 GB de memória.  
A checagem de tamanho mínimo (<15 caracteres) virou uma regra antes da IA, e o passo 7a incorporou a conferência humana (botão de discordância), onde o erro da IA é contornado pelo próprio usuário.  
A arquitetura foi desagregada entre inicialização (download único de ~420 MB via Wi-Fi para CacheStorage) e inferência em RAM, com foco no checkpoint multilíngue oficial para o português real.  
A comparação com a nuvem provou que, mesmo custando menos de R$ 0,10 por usuário, a execução local se justifica pela privacidade irrevogável do feed.

## 5 · auditoria cega

**o veredito da conversa nova:**

| item | passa ou não passa | trecho que prova | o que encontrei (links abertos, regras tentadas) |
|:---|:---|:---|:---|
| 1 · Fluxograma | NÃO PASSA | § 1, passos 1–7: gesto, extração, verificação, IA, dicionário, injeção e decisão humana. | O caminho principal está completo. Entretanto, 3a não tem linha própria na tabela, o losango não está classificado explicitamente e a justificativa da IA compara apenas contra palavras proibidas e regex. Tentei regras para ad hominem, falso dilema, generalização e pânico moral. Elas cobrem subconjuntos, mas não toda a capacidade pretendida. |
| 2 · Peças, entradas, saídas e custos | NÃO PASSA | § 2: escala de 300 e 300.000 postagens mensais; tabela com extensão, Laya e API. | Licença Apache 2.0 confirmada no [GitHub](https://github.com/NandhaKishorM/laya) e no [Hugging Face](https://huggingface.co/convaiinnovations/laya). A documentação TypeScript confirma WebGPU/WASM, mas evidencia um carregamento inicial muito maior que o estimado. O checkpoint inglês não é o adequado para validar português. O benchmark PyTorch não comprova ONNX/WebGPU. O preço atual da API não confirma a tarifa citada e o cálculo não informa tokens de saída. |
| 3 · Arquitetura, dados e privacidade | NÃO PASSA | § 3: tabela de dados pessoais, retenção em RAM/DOM e afirmação de processamento local. | A arquitetura é coerente como intenção, mas não demonstra o comportamento real. Faltam download e cache dos pesos, dependências externas, inspeção de rede e verificação de logs. O diagrama não descreve todos os fluxos. A auditoria cega do § 5 está vazia. O commit indicado retornou 404. |

**a minha resposta, sem IA:**
1. Auditor acertou: faltava alerta de texto curto e botão de discordar; regex é triagem, IA é que decide no feed.
2. Memória real é ~420 MB (não 130), conta da nuvem agora separa entrada/saída, e o teste em inglês/CPU é só proxy — final é multilíngue.
3. Commit já no GitHub, download do modelo é único e estático, análise do post roda local sem sair da máquina.
