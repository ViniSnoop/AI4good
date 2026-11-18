# sem2 · Vinícius Fernandes de Souza

> roteiro do [seminário · iteração 2, demonstração](https://lucassf.pages.dev/ai4good/artefatos/4-seminario-demonstracao), feito a partir do
> [tec.md](tec.md), do [flx.md](flx.md), do [exp.md](exp.md) e do [sem1.md](sem1.md).

**link dos slides:** [sem2-slides.pdf](sem2-slides.pdf)

**a versão que roda:** commit `32dd45a` (tag `sem2`) no repositório [AI4good](https://github.com/ViniSnoop/AI4good)

**a máquina:** Linux (Ubuntu x86_64, Intel/AMD), Python 3.13 com PyTorch/CPU, terminal e apresentação em tela cheia no projetor.

**a gravação de reserva:** [ensaio-sem2.mp4](ensaio-sem2.mp4) (segunda passada do ensaio sem cortes, com a execução no terminal rodando ao vivo).

## as quatro frases, sem IA

1. **a demo:** o leitor ou debatedor no X/Reddit se depara com um post apelativo e aciona a triagem sob demanda; o FiltroSoberano roda o modelo de Sistema 1 localmente sem mandar nada para a nuvem e exibe um rótulo pedagógico com a falácia identificada e botão de contestação, permitindo pausar reações por impulso antes de responder ou compartilhar.
2. **o custo:** na execução real medida no repositório, a inferência levou 1,32 s por post com pico de 3,09 GB de RAM em CPU, contra <1 s e ~420 MB estimados no flx; a diferença ocorre porque o teste de bancada roda PyTorch em precisão FP32 na CPU, enquanto a extensão final usará quantização INT8 via WebGPU/ONNX Runtime Web.
3. **a falha:** na ofensa ao economista, o sistema diagnostica pânico moral com urgência máxima 1.00 em vez de ataque pessoal com urgência nula; quem sofre é o leitor que recebe um alarme falso institucional, provando que o botão de contestação humana (passo 7a) é essencial e tornando a calibração dessa falha a medida do sem3.
4. **o que mudou:** no sem1 eu previa uma SLM generativa local pesada e confiava nas probabilidades de fábrica; mudei para um dicionário estático mapeado ao diagnóstico economizando mais de 2 GB de RAM, e o aviso de runtime descalibrado me fez criar o passo 7a de conferência humana obrigatória.

---

## slide 1 · ponta a ponta · 80 s

- **aparece:** o slide 1 com os três blocos conceituais (*Entrada*, *Processamento*, *Saída*) e a janela do terminal rodando ao vivo o comando `.venv/bin/python tec/demo_sem2.py`.
- **a entrada:** post real de feed simulado: *"URGENTE: Compartilhem antes que apaguem! O governo vai confiscar a poupança e fechar igrejas a partir de amanhã se ninguém protestar hoje!!"*
- **eu falo:** "Aqui está o FiltroSoberano rodando direto do repositório, na tag sem2. Imaginem alguém rolando a timeline do X ou do Reddit e se deparando com este post: pânico moral puro, caixa alta e apelo urgente feito para disparar raiva no Sistema 1. Em vez de bloquear ou censurar, a pessoa clica sob demanda. [executo o script no terminal] O modelo Laya Multilíngue roda localmente na CPU da máquina, sem internet, sem mandar um byte para servidores externos. Em fração de segundo sai o diagnóstico: pânico moral, intensidade de apelo 1.91 e urgência fabricada 0.92. A interface entrega um rótulo pedagógico discreto que dá distanciamento reflexivo ao leitor antes do compartilhamento impulsivo, além de um botão de contestação no passo 7a caso a IA se equivoque."

## slide 2 · quanto custa · 55 s

- **aparece:** o slide 2 com a comparação lado a lado: *Medido na Máquina (Hoje)* com 3,09 GB de RAM e 1,32 s/post vs. *Estimado no Fluxo Final* com ~420 MB e <1,0 s/post. No rodapé: *Custo de infraestrutura: R$ 0,00 por mês*.
- **medido:** execução real na tag `sem2`: 1,32 s de inferência média por post (3,54 s de carga inicial do runtime) e pico de memória residente de 3,09 GB (3.168,4 MB) na CPU em Python/PyTorch FP32.
- **estimado no flx:** tempo < 1,0 s e memória de ~420 MB (390 MB encoder + 32 MB heads em INT8) documentados no `flx.md` a partir do benchmark do ONNX Runtime Web.
- **eu falo:** "Estes números vêm da execução que acabou de rodar na tela. O tempo de resposta ficou em 1,32 segundo por post, muito próximo do teto de 1 segundo do flx. Mas olhem a memória: 3,09 GB medidos contra os 420 MB que estimei no fluxo. Por que essa discrepância? Porque hoje estou demonstrando o modelo em Python puro sobre PyTorch, que aloca o framework inteiro e pesos não quantizados em FP32 na RAM. No fluxo de produção, o modelo será exportado para INT8 e executado dentro do navegador via WebGPU e WebAssembly, reduzindo a pegada de memória para a faixa de 420 MB. E o custo financeiro para quem usa e para quem mantém é rigorosamente zero: nada trafega pela nuvem."

## slide 3 · a falha · 65 s

- **aparece:** o slide 3 detalhando o Post 2: a citação do post, o card vermelho com o que o modelo gerou (`pânico moral`, prob 0.34, urgência 1.00) e o card verde com o esperado (`ataque pessoal / ad hominem`, urgência 0.00).
- **a entrada:** o post de teste 2: *"Esse economistazinho de meia-tigela não passa de um vendido e incompetente, não tem moral para opinar sobre nada neste país."*
- **a saída, como saiu:** `[Diagnóstico]: panico_moral (prob: 0.34)` e `[Urgência Fabricada]: 1.00`.
- **o certo:** `[Diagnóstico]: ataque_pessoal` e `[Urgência Fabricada]: 0.00`.
- **eu falo:** "Escolhi este caso de propósito porque ele erra feio. O texto é uma ofensa pessoal explícita, um ad hominem clássico contra o interlocutor. Mas o modelo classificou como pânico moral com probabilidade dispersa de 0.34, e cravou urgência máxima em 1.00 mesmo sem haver nenhuma menção temporal no texto. Quem sofre com esse erro? O leitor, que é alarmado indevidamente por um alerta inflado de pânico institucional em uma simples ofensa. Esse erro revela duas verdades fundamentais: primeiro, por que o passo 7a de contestação humana não é enfeite, mas salvaguarda mandatória; segundo, que o checkpoint sem calibração RLCD dispersa probabilidades no português informal. Esta falha exata é a primeira candidata a virar medida no sem3."

## slide 4 · o que mudou desde o sem1 · 45 s

- **aparece:** o slide 4 com a tabela comparativa de 3 dimensões: *Geração explicativa*, *Calibração* e *Prioridade*.
- **no sem1:** previsão de uma SLM generativa local embarcada para detalhar falácias e crença em probabilidades pré-calibradas de fábrica.
- **agora:** substituição da SLM por dicionário estático (economia de >2 GB de RAM no cliente) e incorporação formal do passo 7a após alerta de `uncalibrated` do runtime.
- **eu falo:** "No sem1, eu havia desenhado uma SLM generativa local para redigir parágrafos explicando cada falácia ao usuário. Cortei essa SLM: transformei a explicação pedagógica em um dicionário de regras estático vinculado à classe identificada pelo Laya. Com essa única decisão de corte, economizei mais de 2 GB de memória na máquina do usuário. Além disso, o próprio runtime emitiu aviso de temperaturas inválidas (`uncalibrated`), o que me fez desistir de confiar cegamente no modelo e formalizar o botão de contestação humana (passo 7a). Mudar de plano com base no código medido poupou recursos e tornou a arquitetura viável."

## slide 5 · o fecho · 20 s

- **aparece:** o slide 5 com os três eixos da validação empírica para 25/11 (*Dataset Real de 120 posts*, *Falsos Positivos com Defesa Civil* e *Calibração Fina com Temperature Scaling*).
- **eu falo:** "O FiltroSoberano roda localmente, sem nuvem, em 1,3 s por post. Vocês viram onde ele acerta e onde ele erra calado. No dia 25/11, no sem3, eu trago o experimento controlado com 120 posts e a calibração de temperatura para eliminar os falsos positivos no feed real."

---

**tempo total, cronometrado, com a demo rodando:** 4 min 20 s e 4 min 15 s, duas vezes seguidas, na mesma máquina Linux com a demo rodando ao vivo.

## ensaio cético

*(Executado em conversa nova e independente com o prompt do professor)*

**a pergunta mais difícil:** "Se o modelo erra a separação de classes em textos curtos e tem pico de 3 GB de RAM, por que o usuário instalaria isso em vez de confiar no próprio discernimento ou usar uma regex simples?"

**o que eu mudei por causa dela:** Acrescentei no slide 2 e na fala a explicação transparente de que os 3 GB são do protótipo PyTorch FP32 de bancada e que a regex simples gera 27% de falsos positivos em alertas reais da Defesa Civil (conforme medido no piloto E1), tornando a IA calibrada indispensável.
