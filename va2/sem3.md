# sem3 · Vinícius Fernandes de Souza

> roteiro do [seminário · iteração 3, como vai ser o teste](https://lucassf.pages.dev/ai4good/artefatos/4-seminario-teste), feito a partir do
> [exp.md](exp.md), do [cmp.md](cmp.md), do [sem2.md](sem2.md) e do repositório.

**link dos slides:** [sem3-slides.pdf](sem3-slides.pdf)

**o commit da regra:** commit `832a0de` (registrado antes do teste com parecer do ensaio cético) e limiares consolidados no [exp.md](exp.md).

**a máquina e a versão:** Linux (Ubuntu x86_64), Python 3.13, PyTorch/ONNX Runtime; eu rodo, na tag `sem3`.

**a ética:** teste sem pessoas (dados de domínio público em postagens de redes sociais e comunicados factuais/Defesa Civil, sem dados pessoais, dispensado de CEP conforme Res. CNS 510/2016, art. 1º, parágrafo único, II e III). O teste comportamental com usuários (E2) fica como protocolo futuro com TCLE ([tcle.md](tcle.md)) para quando houver submissão e aprovação no comitê de ética.

---

## as quatro frases, sem IA

1. **o competidor:** O jeito de hoje em extensões leves é a heurística de regex (como no modo local do Vigil), que no meu piloto de 30 postagens gerou 27% de falso positivo acusando comunicados da Defesa Civil de pânico moral.
2. **o que quero mostrar:** Quero mostrar que o FiltroSoberano reduz a taxa de falsos positivos para menos de 10% com F1-macro acima de 0,75 na detecção de falácias em postagens selecionadas em português, comparado à heurística de regex, operando localmente no navegador em menos de 1 segundo por post.
3. **a comparação:** 60 postagens públicas em português — 30 manipulativas com falácias anotadas sob Da San Martino et al. (2019) e 30 legítimas com notícias e alertas da Defesa Civil — passam pelas duas condições sob o mesmo gabarito cego, com margem amostral declarada de $\pm 10$ pontos percentuais.
4. **o caminho até o pitch:** O harness de medição do piloto já roda; no dia 25/11 executo a bateria de 60 posts (cerca de 1 minuto no total) calculando o intervalo de 95% por bootstrap, e no pitch de 02/12 apresento a tabela final consolidada com a demonstração de 1 post ao vivo na extensão.

---

## slide 1 · o competidor e o que ele consegue · 60 s

- **aparece:** a tabela com os números do piloto: *Linha de base (Regex)*: F1 0.67, Falso Positivo 27% [7%–50%], Latência 0.000 s. Ao lado, o card do *Vigil (Kang et al., 2026)* destacando o modo regex (0,03 ms, cego à semântica) e o modo WebLLM (3,4 s de latência mediana).
- **a medida dele, e o número:** taxa de falso positivo em alertas legítimos (27%, 4 em 15 no piloto de 30 postagens de controle) e latência de inferência.
- **eu falo:** "Para combater manipulação retórica no navegador, as soluções existentes caem em dois extremos: ou usam modelos gigantes na nuvem que violam a privacidade do usuário, ou adotam heurísticas estáticas de regex para serem rápidas, como faz o tier local do Vigil. No meu piloto com 30 postagens no repositório, medi exatamente esse jeito de hoje: a regex roda instantaneamente, mas gerou 27% de falsos positivos, acusando avisos legítimos da Defesa Civil de pânico moral apenas por conterem palavras como 'URGENTE'. O Vigil tenta resolver isso com WebLLM no navegador, mas leva 3,4 segundos por post e terceiriza a moralização para servidores externos. O nosso competidor direto na bancada é essa heurística de regex, que representa o que o usuário tem hoje para rodar localmente sem travar o feed."

## slide 2 · o que quero mostrar e como vou medir · 95 s

- **aparece:** a frase do alvo em destaque e a régua de decisão antes do teste:
  - *Passou:* Falso positivo $\le 10\%$, F1-macro $\ge 0{,}75$, latência $< 1{,}0$ s (IC 95% estritamente dentro).
  - *Caiu:* Falso positivo $> 10\%$ ou F1-macro $< 0{,}75$ (IC 95% estritamente fora).
  - *Inconclusivo:* Intervalo de confiança de 95% encosta ou cruza o limiar de 10% ou 0,75.
- **o alvo:** taxa de falsos positivos (alarmes falsos que induzem o usuário a desinstalar a extensão) e F1-macro das falácias (identificação correta de ad hominem e apelo emocional). Não meço satisfação nem escala SUS, pois facilidade de uso não garante que o alarme seja confiável.
- **passou, caiu, inconclusivo:** limiares estritos pré-registrados no commit `567c6fc`. O intervalo de 95% será obtido por bootstrap com 1.000 reamostras sobre os resultados dos posts.
- **eu falo:** "Eu não vou medir se os usuários 'acharam o app fácil' ou 'gostaram do botão'. Se a extensão for linda mas rotular notícias normais como manipulação, ela destrói a confiança de quem lê. A minha medida de sucesso é a taxa de falsos positivos e o F1-macro na detecção de falácias formais. E a regra foi escrita antes do resultado, no commit 567c6fc: para passar, o modelo calibrado precisa manter o falso positivo abaixo de 10% e o F1 acima de 0,75, com latência inferior a 1 segundo. Se o falso positivo superar 10%, a hipótese caiu. E se o intervalo cruzar a fronteira de 10%, o resultado é estritamente inconclusivo. Eu não prometo provar a solução universal de falácias em português; prometo testar se esta arquitetura local específica supera a linha de base nas condições de bancada."

## slide 3 · como será a comparação · 95 s

- **aparece:** o esquema visual:
  `60 posts em português (30 manipulativos + 30 controles legítimos)`  
  $\longrightarrow$ `[Condição A: FiltroSoberano Local Calibrado]` $\times$ `[Condição B: Linha de Base Regex]`  
  $\longrightarrow$ `Métricas: Falso Positivo (IC 95%), F1-macro e Latência`.  
  No rodapé: *Margem de erro amostral ($n=30$ controles, $p=0{,}10$): $\pm 10{,}7$ pontos percentuais (Fleiss et al., 2003)*.
- **quem ou o que entra:** 60 postagens públicas em português não utilizadas no ajuste de temperatura. 30 manipulativas cobrindo ad hominem, pânico moral e falso dilema; e 30 controles legítimos (Defesa Civil, meteorologia e notícias factuais).
- **as condições:** Condição A (FiltroSoberano com checkpoint Laya Multilíngue calibrado via temperature scaling) contra Condição B (heurística determinística de regex).
- **o que fica igual:** as mesmas 60 postagens exatas, a mesma máquina Linux de bancada, e o mesmo gabarito cego.
- **o gabarito:** montado previamente com anotação baseada na taxonomia formal de Da San Martino et al. (EMNLP 2019), sem que os modelos conheçam os rótulos durante a passada.
- **eu falo:** "A comparação é estritamente pareada: os mesmos 60 posts passam pelos dois caminhos. A amostra de 60 posts foi dimensionada para viabilizar a execução em sala de aula no dia 25. Com 30 postagens de controle, a aproximação normal de proporções nos dá uma margem amostral de aproximadamente mais ou menos 10 pontos percentuais. Eu não escondo essa margem: é exatamente por ela existir que o resultado inconclusivo está formalizado. Se o nosso intervalo bater em 11%, eu não digo que funcionou quase; digo com rigor que faltaram casos para ter certeza estatística. E o que esse teste não prova: não prova a eficácia de intervenção no comportamento humano; prova estritamente a calibração técnica do motor de decisão local."

## slide 4 · como chegar ao pitch com resultado · 60 s

- **aparece:** a linha do tempo:  
  *18/11 (Hoje):* A regra pré-registrada e o protocolo de teste.  
  *25/11 (Sala de Aula):* Execução da bateria dos 60 posts no notebook (~1 min).  
  *27/11:* Conferência dos intervalos de confiança via script de bootstrap.  
  *02/12 (Pitch Final):* Apresentação da tabela de resultados e demo de 1 post ao vivo.
- **já pronto:** script de avaliação (`piloto_e1.py`) e harness de métricas já funcionais e testados no piloto.
- **o teste pequeno:** rodado com 30 posts no piloto de `exp.md`. Ele revelou que o modelo cru dispersava probabilidades (47% de falsos positivos), o que motivou a calibração de temperatura antes do teste de 60 posts.
- **plano B:** se a aceleração via WebGPU no navegador apresentar variação na máquina, a inferência roda localmente em CPU via ONNX Runtime INT8, mantendo rigorosamente as mesmas métricas.
- **eu falo:** "Tudo o que precisamos para rodar no dia 25 já está codificado e testado. O script que avalia os posts e calcula as métricas já rodou no piloto com 30 postagens. A 1 segundo por post, a execução das 60 postagens em sala levará cerca de 1 minuto cravado. O script gera os dados brutos e faz as 1.000 reamostras de bootstrap matematicamente em meio segundo para calcular o intervalo de 95%. Se o runtime WebGPU oscilar, meu plano B roda em CPU com ONNX Runtime. No dia 02/12, no pitch, levo os números consolidados na tabela e demonstro 1 post ao vivo no navegador para a banca ver a interface pedagógica em ação."

## slide 5 · o fecho · 40 s

- **aparece:** *O que o teste de 25/11 responde:* A capacidade técnica de um classificador local calibrado superar a linha de base de regex em postagens de teste.  
  *O que ele não responde:* A pretensão universal sobre modelos de linguagem ou a mudança atitudinal de leitores no feed real.
- **eu falo:** "Com este desenho, chegamos ao pitch com um experimento exploratório rigoroso: ou o FiltroSoberano prova que consegue diagnosticar falácias com menos de 10% de alarme falso localmente nesta amostra, ou a regra me obriga a admitir que a arquitetura não sustentou a hipótese. Demonstrar que a técnica ainda não supera o problema nas condições locais também é um resultado científico legítimo. O teste do dia 25 resolve essa fronteira técnica. O passo seguinte, fora da disciplina, é levar o protocolo com o TCLE que já preparamos ao Comitê de Ética para medir o comportamento de leitores humanos."

---

**tempo total, cronometrado:** 5 min 50 s e 5 min 45 s, duas passadas consistentes.

---

## ensaio cético

*(Executado em conversa nova e independente com o prompt oficial do professor)*

**a pergunta mais difícil:** "Você admitiu que escolheu 60 postagens por conveniência e viabilidade de tempo, e não por cálculo de poder estatístico. Como você sustenta critérios estatísticos tão rígidos de aprovação (passou/caiu) e conclusões sobre detecção de falácias em português com uma amostra pequena escolhida por conveniência?"

**o que eu mudei por causa dela:**  
1. **Redimensionei a ambição da conclusão:** No slide 2 e no slide 5, deixei claro que o teste é um experimento de bancada exploratório sobre esta arquitetura local específica, e não uma prova categórica sobre toda a detecção de falácias em português.  
2. **Declarei abertamente a margem de erro estatística:** No slide 3, inseri a margem de erro de $\pm 10{,}7$ pontos percentuais derivada de Fleiss et al. (2003) para $n=30$ controles.  
3. **Fortaleci o papel do 'Inconclusivo':** Justifiquei que, devido a essa margem amostral, a zona de inconclusivo é uma salvaguarda científica essencial: se o intervalo cruzar os 10%, o trabalho assume com transparência que não é possível afirmar o resultado, transformando a limitação amostral em integridade metodológica.
