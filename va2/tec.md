# tec · Vinícius Fernandes de Souza

> folha do artefato [tecnologia base demonstrável](../3-tecnologia-base.md).

## 0 · a minha ideia completa

**FiltroSoberano · Extensão de Navegador.** Leitores, debatedores e produtores de conteúdo utilizam uma extensão de navegador open-source para Chrome, Firefox e Brave ao navegar no X/Twitter, Reddit, YouTube e WhatsApp Web. Em vez de varreduras pesadas em segundo plano, a extensão opera **sob demanda**: ao passar o mouse ou clicar em um botão de atalho em uma postagem suspeita, o modelo de decisão **Laya (Sistema 1, pesos abertos)** avalia em menos de 50 milissegundos a estrutura do texto via WebGPU/ONNX local. O modelo não tenta adivinhar se o fato é verídico, mas afere objetivamente **marcadores de retórica apelativa**: pontua a intensidade de pânico moral e urgência fabricada (`score`) e diagnostica táticas formais como ataque pessoal (*ad hominem*) e generalização abusiva (`choice`), acionando uma SLM destilada apenas se o usuário solicitar uma explicação detalhada. O post nunca é censurado ou ocultado; o usuário recebe um rótulo pedagógico (*nudge*) sutil com a técnica identificada, municiando-se de clareza crítica e argumentos frios para não reagir por impulso nem ser manipulado por narrativas de polarização artificial.

técnica do § 6b do brw: Modelos de Decisão de "Sistema 1" (Laya, pesos abertos Apache 2.0 com primitivas `choice` e `score` em forward pass único de <50ms via WebGPU/ONNX) integrados a uma SLM destilada local acionada sob demanda.

## 1 · as peças

| peça | central ou apoio | o que faz na ideia | link oficial | licença | por que esta, e não as alternativas |
|:--|:--|:--|:--|:--|:--|
| **Laya** | central | Avalia a postagem em passada única (<50 ms), diagnosticando a tática retórica (`choice`) e a intensidade de urgência/pânico (`score`) com probabilidades calibradas via RLCD. | [NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) | Apache 2.0 | Recomendada pelo professor e escolhida pela alta velocidade e capacidade de decisão estruturada: entrega tanto o diagnóstico da falácia (`choice`) quanto o score de urgência/pânico (`score`) em passada única rápida (<50 ms), dispensando modelos generativos pesados. O [Transformers](https://github.com/huggingface/transformers) (Apache 2.0) exigiria pipelines e cabeçotes separados para cada métrica com calibração manual, e o [SetFit](https://github.com/huggingface/setfit) (Apache 2.0) faz apenas classificação discreta sem score de intensidade calibrado. |

## 2 · o exemplo oficial, rodando

**de onde veio o código:** a seção "Quickstart" do [README oficial do Laya](https://github.com/NandhaKishorM/laya#quickstart), com o exemplo original de triagem de atendimento/cobrança e o texto de teste do projeto (`"Hi, we were billed twice for March. Please refund the duplicate today or we will cancel our plan."`).

**o que eu mudei nele:** apenas a escolha de execução oferecida pelo próprio repositório: o encoder base em CPU (`convaiinnovations/laya`), sem o leitor auxiliar vegaml.

**o commit:** [a89d58b · exemplo oficial do laya rodando em CPU](https://github.com/ViniSnoop/AI4good/commit/a89d58bceede969c695322513b61f56a42842ee5)

**o comando e a saída, colados como vieram:**

```text
$ .venv/bin/python tec/exemplo_oficial.py
/home/vini/Downloads/AI4good/workspace/.venv/lib/python3.13/site-packages/torch/cuda/__init__.py:241: UserWarning: CUDA initialization: The NVIDIA driver on your system is too old (found version 12040). Please update your GPU driver by downloading and installing a new version from the URL: http://www.nvidia.com/Download/index.aspx Alternatively, go to: https://pytorch.org to install a PyTorch version that has been compiled with your version of the CUDA driver. (Triggered internally at /__w/pytorch/pytorch/c10/cuda/CUDAFunctions.cpp:119.)
  return torch._C._cuda_getDeviceCount() > 0
/home/vini/Downloads/AI4good/workspace/tec/exemplo_oficial.py:3: RuntimeWarning: laya: this checkpoint ships invalid temperatures or values outside [0.5, 5]; using choice:11+=0.10058280825614929 -> 0.5. Treat confidence from the affected entries as uncalibrated.
  agent = laya.Agent()
billing
{'billing': 0.9865, 'technical': 0.008, 'other': 0.0055}
1.7722
0.879
```

## 3 · a alteração mínima

**o commit:** [68e1276 · alteração mínima com posts de redes sociais e retórica apelativa](https://github.com/ViniSnoop/AI4good/commit/68e1276893675719506ef41be618dd48deeea254)

**a entrada:** antes, uma solicitação em inglês sobre fatura duplicada (`"Hi, we were billed twice for March..."`); agora, três postagens em português simulando o feed de redes sociais (X/Twitter, Reddit) com diferentes técnicas de debate: um post alarmista de pânico moral e urgência fabricada, um post de desqualificação e ofensa pessoal (*ad hominem*), e um post de falso dilema ("ou apoia incondicionalmente ou quer destruir a cidade"). O dado de teste difere do feed real por ter textos sintéticos isolados sem gírias de internet, pontuação caótica ou memes visuais de contexto.

**a saída:** antes, triagem corporativa de atendimento (`department`), urgência de suporte e risco de churn; agora, a triagem do FiltroSoberano: diagnóstico da técnica retórica (`choice`: panico_moral, ataque_pessoal, falso_dilema, legitimo) com distribuição de probabilidade calibrada, score contínuo de intensidade do apelo emocional (`score`: baixo, moderado, alarmista) e probabilidade de urgência fabricada (`noul`), formatados como o badge/*nudge* que a extensão exibe sobre o post.

**o comando e a saída, colados como vieram:**

```text
$ .venv/bin/python tec/exemplo_oficial.py
/home/vini/Downloads/AI4good/workspace/.venv/lib/python3.13/site-packages/torch/cuda/__init__.py:241: UserWarning: CUDA initialization: The NVIDIA driver on your system is too old (found version 12040). Please update your GPU driver by downloading and installing a new version from the URL: http://www.nvidia.com/Download/index.aspx Alternatively, go to: https://pytorch.org to install a PyTorch version that has been compiled with your version of the CUDA driver. (Triggered internally at /__w/pytorch/pytorch/c10/cuda/CUDAFunctions.cpp:119.)
  return torch._C._cuda_getDeviceCount() > 0
/home/vini/Downloads/AI4good/workspace/tec/exemplo_oficial.py:3: RuntimeWarning: laya: this checkpoint ships invalid temperatures or values outside [0.5, 5]; using choice:11+=0.10058280825614929 -> 0.5. Treat confidence from the affected entries as uncalibrated.
  agent = laya.Agent()
--- Post 1 ---
Texto: URGENTE: Compartilhem antes que apaguem! O governo vai confiscar a poupança e fechar igrejas a partir de amanhã se ninguém protestar hoje!!
  [Diagnóstico]: panico_moral (prob: 0.31)
  [Intensidade de Apelo]: score 1.91 ({'0': 0.0289, '1': 0.028, '2': 0.9431})
  [Urgência Fabricada]: 0.92

--- Post 2 ---
Texto: Esse economistazinho de meia-tigela não passa de um vendido e incompetente, não tem moral para opinar sobre nada neste país.
  [Diagnóstico]: panico_moral (prob: 0.34)
  [Intensidade de Apelo]: score 0.45 ({'0': 0.749, '1': 0.0566, '2': 0.1944})
  [Urgência Fabricada]: 1.00

--- Post 3 ---
Texto: Ou você apoia incondicionalmente o nosso projeto agora, ou você é a favor do caos e quer destruir a nossa cidade.
  [Diagnóstico]: ataque_pessoal (prob: 0.31)
  [Intensidade de Apelo]: score 1.13 ({'0': 0.1256, '1': 0.6167, '2': 0.2577})
  [Urgência Fabricada]: 1.00
```

**onde a saída erra:** no post 2, que é um ataque pessoal evidente (*ad hominem* / ofensa ao debatedor), o modelo classificou como `panico_moral` (prob 0.34) em vez de `ataque_pessoal`, além de marcar urgência fabricada em 1.00 mesmo sem haver termo de pressa no texto. no post 3, que é um falso dilema ("ou apoia ou é a favor do caos"), o modelo confundiu com `ataque_pessoal` (prob 0.31) em vez de `falso_dilema`. além disso, as probabilidades ficaram muito dispersas (~0.31 a 0.34), mostrando que o checkpoint genérico em português hesita na separação fina de falácias sem o refinamento calibrado RLCD.

## 4 · o vídeo

**link:** [Google Drive · Demonstração Laya no FiltroSoberano](https://drive.google.com/file/d/1Pf-Pn28qpcTsOTPzHYNx7JC0f_XaFplr/view?usp=sharing) · **duração:** ~1 min · **o que aparece:** o `git log` com os dois commits (`a89d58b` e `68e1276`), o comando `.venv/bin/python tec/exemplo_oficial.py` e a execução ao vivo com a classificação dos 3 posts em português.

## 5 · o que deu certo e o que errou, sem IA

A técnica realmente acertou marcadores nos posts testados, errando a classificação detalhada de parte deles (deu 0.34 de probabilidade de pânico moral no lugar de ataque pessoal no post 2, e confundiu falso dilema com ataque pessoal no post 3).
O erro por enquanto está na separação fina das classes de falácias em português informal e na urgência que inflou para 1.00 em ofensas puras.
Aqui foi instantâneo, a IA rodou sem delay perceptível em passada única de Sistema 1 na CPU, com menos de 1 segundo por post.
Isso mostra que ainda devo refinar e calibrar melhor a ferramenta para melhorar as classificações no português e que a velocidade abre espaço para testar se um modo de varredura leve é viável ou se a inspeção sob demanda por clique continua sendo a única opção segura contra travamento.

## 6 · auditoria cega

**o veredito da conversa nova:**

Auditoria cética — tec.md
REPROVADO — 0/3 itens passam integralmente
Veredito: não passa.

A folha tem méritos reais: há código-fonte no repositório, o segundo commit faz uma adaptação pertinente ao problema, a saída apresenta resultados estruturados e o autor admite erros concretos. Não é um caso equivalente ao exemplo fictício do professor.

Mas a auditoria tem três requisitos cumulativos importantes. O vídeo não pôde ser verificado, a documentação técnica deixa peças de fora e, principalmente, a auditoria cega do § 6 está completamente vazia.
### 1. Resultado por item

| item | passa ou não passa | trecho que prova | o que encontrei (links abertos, diff) |
|:--|:--|:--|:--|
| 1. Técnica, links, licenças e justificativa | NÃO PASSA | § 1: “Laya \| central” e as justificativas envolvendo Transformers e SetFit. § 0 também menciona “WebGPU/ONNX” e “uma SLM destilada local”. | O repositório oficial do Laya existe e declara Apache-2.0. A licença do modelo publicado no Hugging Face também é Apache-2.0. Os repositórios oficiais de Transformers e SetFit existem e declaram Apache-2.0. Entretanto, a SLM de apoio não tem nome, repositório, licença ou justificativa. WebGPU/ONNX também aparecem na descrição da arquitetura, mas não são documentados na tabela. Além disso, a comparação entre alternativas é apenas afirmada, sem evidência comparativa suficiente. |
| 2. Vídeo da execução a partir do código-fonte | NÃO PASSA | § 2 apresenta o commit a89d58b, o comando .venv/bin/python tec/exemplo_oficial.py e uma saída com caminho local /home/vini/.... § 4 afirma que o vídeo mostra os dois commits, o comando e a execução. | O primeiro commit existe e acrescenta o arquivo tec/exemplo_oficial.py, com 32 linhas de código. O segundo commit tem o primeiro como pai. Isso confirma que existe código-fonte no repositório, não apenas um aplicativo pronto. Contudo, o vídeo indicado no Google Drive não ficou acessível para inspeção (Internal Error). Não consegui verificar o git log, a execução ao vivo ou a correspondência entre vídeo e commits. A saída colada é indício de execução alegadamente local, mas não substitui a prova audiovisual exigida. |
| 3. Alteração mínima de entrada e saída | NÃO PASSA | § 3 declara a substituição da solicitação de cobrança por três postagens, descreve os novos campos de saída e aponta erros. | O diff existe e altera somente tec/exemplo_oficial.py: 29 adições e 17 remoções. A entrada passa a ser uma lista de três posts em português; as perguntas passam a identificar técnicas retóricas, intensidade e urgência fabricada; a execução percorre os posts e imprime os resultados. A chamada agent.predict(...) e a estrutura fundamental do exemplo permanecem reconhecíveis. Os posts são sintéticos, mas pertencem ao domínio do problema. A saída mostra dados específicos da solução e os erros são reconhecidos. O impeditivo definitivo é o § 6 vazio: não há veredito colado nem resposta do autor, item por item, sem IA. |

Observações técnicas que pesam contra o item 1
Há uma contradição importante entre a justificativa da técnica e a execução apresentada.

Na descrição da tecnologia, a folha afirma:
“probabilidades calibradas via RLCD”

Porém, a própria saída do experimento contém o aviso:
“Treat confidence from the affected entries as uncalibrated.”

Esse aviso aparece tanto no exemplo original quanto na execução adaptada. Portanto, não é uma ressalva externa: a própria execução informa que as probabilidades afetadas não devem ser tratadas como calibradas. 
tec.md
 tec.md

A documentação do modelo também distingue os checkpoints: o laya é identificado como inglês, enquanto laya-multilingual é a opção para mais de 100 idiomas. A documentação ainda recomenda calibrar com dados próprios antes de confiar nas probabilidades. A folha não identifica inequivocamente qual checkpoint está sendo usado nos posts em português. 

GitHub+1

Outro problema: a alegação de menos de 50 ms não é demonstrada pela execução apresentada. O § 5 fala em menos de um segundo por postagem, mas não apresenta medição de latência. A documentação oficial mostra resultados distintos por hardware, inclusive valores de 193–464 ms em CPU no cenário de preload. Não há fundamento para transferir automaticamente a promessa de menos de 50 ms para essa demonstração em CPU. 
tec.md
 
GitHub

2. Inspeção do segundo commit
Commit 68e1276 — alteração mínima
Abrir diff completo no GitHubAlteração pertinente identificada
O diff mostra:
Elemento	Antes	Depois
Entrada	Uma solicitação de cobrança em inglês	Três posts sintéticos em português
choice	Departamento de atendimento	Técnica retórica
score	Urgência de atendimento	Intensidade de apelo emocional
noul	Risco de cancelamento	Urgência fabricada
Execução	Uma chamada predict	Uma chamada por postagem
Saída	Resultado de triagem corporativa	Diagnósticos e probabilidades por postagem

O diff também mantém a criação do agente e a estrutura de perguntas tipadas. Não é uma alteração cosmética de print(): houve mudança real no problema apresentado ao modelo e no significado dos resultados.

A entrada merece uma ressalva: são exemplos sintéticos, e a própria folha reconhece que não apresentam gírias, pontuação caótica ou memes visuais. Isso limita a representatividade do experimento, mas não transforma os posts em dados do exemplo original do Laya.

Meu julgamento: o núcleo do item 3 foi executado de maneira pertinente. O commit é específico, o exemplo oficial continua reconhecível e a saída é específica do FiltroSoberano. Entretanto, o item completo continua reprovado porque a auditoria cega obrigatória não foi preenchida.
3. Armadilhas de tec-raso
Comparei a folha com as seis armadilhas explicitamente anotadas na página indicada. 

lucassf.pages.dev

| Armadilha anotada | Cai? | Constatação |
|:--|:--|:--|
| 1. Peças sem documentação e justificativa genérica | PARCIALMENTE | Laya possui link e licença verificáveis; as duas alternativas também. Não é o caso grosseiro de indicar apenas o nome de um site. Entretanto, a SLM de apoio não é documentada e a comparação técnica não é demonstrada. |
| 2. Space ou aplicativo pronto no lugar do código-fonte | NÃO, MAS SEM COMPROVAÇÃO FINAL | Existe código-fonte versionado no repositório e um primeiro commit real. A folha não se apoia apenas em um Space. O vídeo, porém, não pôde ser inspecionado. |
| 3. Reutilização do dado de exemplo em vez de dado do problema | NÃO | A solicitação de cobrança foi substituída por posts pertinentes ao FiltroSoberano. São dados sintéticos, mas do domínio correto. |
| 4. Trocar somente o texto impresso e chamar isso de solução | NÃO | O segundo commit muda a entrada, as perguntas e os campos semânticos avaliados. A saída apresenta decisões estruturadas específicas do problema. |
| 5. Dizer que funcionou perfeitamente, sem admitir erros | NÃO | O autor identifica erros concretos: classificação incorreta do ataque pessoal, confusão com falso dilema e urgência artificial marcada indevidamente. |
| 6. Auditoria cega vazia ou concordância automática com o veredito | SIM — CAI INTEGRALMENTE | O § 6 apresenta os títulos da tabela, mas nenhuma linha preenchida. Também não há texto depois de “a minha resposta, sem IA”. |

4. O problema mais grave: § 6
Este ponto, isoladamente, já impede a aprovação do item 3.

A folha contém:
§ 6 · auditoria cega

Em seguida, apresenta a tabela:
| item | passa ou não passa | trecho que prova | o que encontrei |

Mas não há nenhuma linha de resultado.

Depois aparece:
a minha resposta, sem IA:

E não há resposta.

Isso significa que faltam os dois elementos exigidos: o veredito da conversa independente, colado na folha, e a manifestação do aluno sobre cada item.

Não considero isso um detalhe editorial. A auditoria cega é justamente o mecanismo que impede o autor de simplesmente apresentar sua própria avaliação favorável como validação externa.

5. Veredito final
NÃO PASSA
0 / 3

Item 1 — Não passa

A peça central está identificada e as licenças das peças efetivamente listadas foram verificadas. Mas a técnica de apoio SLM está sem documentação, a justificativa comparativa é insuficiente e há alegações de calibração e velocidade que não são demonstradas pela execução.

Item 2 — Não passa

Há código-fonte e commits reais. Entretanto, não foi possível abrir o vídeo para confirmar que a demonstração mostra os dois commits e a execução ao vivo exigida.

Item 3 — Não passa

O diff é pertinente e a adaptação é substancial, não cosmética. Os dados pertencem ao problema e os erros são explicitados. Porém, a auditoria cega e a resposta sem IA não foram entregues.

Conclusão de auditor: esta folha está consideravelmente acima do exemplo tec-raso em execução, adaptação e honestidade experimental. Não seria correto tratá-la como uma folha vazia ou como uma demonstração de fachada.

Mas também não seria correto aprová-la. O item 1 está incompleto, o item 2 não tem prova audiovisual verificável e o item 3 não cumpre integralmente a exigência do § 6.

Resultado rigoroso: não passa nos três itens, embora o terceiro esteja substancialmente demonstrado na parte do código.

**a minha resposta, sem IA:**

Item 1: Não tem nada sobre "Entretanto, a SLM de apoio não tem nome, repositório, licença ou justificativa. WebGPU/ONNX também aparecem na descrição da arquitetura, mas não são documentados na tabela. Além disso, a comparação entre alternativas é apenas afirmada, sem evidência comparativa suficiente" até por que eu mesmo mandei tirar essa parte pessoalmente, o projeto não terá mais essa segunda etapa de slm local para não ficar pesado no navegador
Item 2: Não conseguiu acessar por incapacidade, por que eu coloquei no drive e o link está funcionando perfeitamente, inclusive abri em janela anônima sem dificuldade nenhuma.
Item 3: ELE ME REPROVOU PQ NÃO TEM A AUDITORIA CEGA QUE ELE MESMO ESTÁ FAZENDO E PELA FALTA DA RESPOSTA DELE???
