# sem1 · FiltroSoberano · Vinícius Fernandes de Souza

> roteiro do [seminário · preliminares](../4-seminario-preliminares.md), feito a partir do [cmp.md](cmp.md), [tec.md](tec.md) e [flx.md](flx.md).

**link dos slides:** [sem1-slides.pdf](sem1-slides.pdf)

## as quatro frases, sem IA

*(Revise e valide com as suas próprias palavras antes de treinar a fala):*

1. **a ideia:** o debatedor ou leitor no X/Twitter ou Reddit é bombardeado por posts apelativos de pânico moral e urgência fabricada; o FiltroSoberano diagnostica sob demanda a tática retórica em passada única local no navegador, sem censurar o post e sem mandar nenhum dado para a nuvem.
2. **o produto mais próximo:** o Vigil (Univ. de Ghent), porque já opera diretamente no feed do X sobre gatilhos cognitivos de Sistema 1 e moralização sem censura, mas o modo semântico no navegador leva 3,4 segundos de latência com WebLLM e a detecção de moralização exige um servidor externo.
3. **o artigo mais próximo:** Da San Martino et al. (EMNLP 2019), o único que formaliza 18 técnicas de manipulação retórica e apelo emocional a nível de trecho, mas feito para jornalismo em inglês em servidores pesados, deixando em aberto a calibração de incerteza em feeds informais.
4. **o que só a minha faz:** entrega detecção conjunta de retórica apelativa, moralização e urgência fabricada em português 100% no navegador em passada única (<1 s); e pergunta cientificamente se um modelo calibrado de Sistema 1 reduz reações impulsivas no feed sem afogar o usuário em falsos positivos decorrentes do português informal das redes.

---

## slide 1 · a ideia · 40 s

- **aparece:** mockup conceitual do produto no feed: um post alarmista fictício (*"URGENTE: compartilhem antes que apaguem! O governo vai confiscar..."*) com o cursor passando por cima → surgimento de um badge discreto (*"Pânico Moral / Urgência Alta"*) com link de explicação sem ocultar o texto original.  
  Texto de apoio (uma linha): *"FiltroSoberano · clareza crítica sob demanda no feed, 100% local."*
- **eu falo:** *(Roteiro da sua fala — fale com suas palavras, sem ler):*  
  Apresente uma pessoa concreta no feed: alguém navegando no X ou no Reddit que se depara com uma postagem com caixa alta, apelo ao medo e urgência fabricada feita para provocar reação de raiva imediata. Explique que o FiltroSoberano não bloqueia a tela nem censura ninguém: ao passar o mouse ou clicar no post sob demanda, a extensão roda um modelo leve de Sistema 1 direto no navegador e coloca uma etiqueta pedagógica com a falácia identificada, devolvendo o controle reflexivo antes do clique ou da resposta.

## slide 2 · o produto mais próximo · 45 s

- **aparece:** tela oficial do repositório do **[Vigil](https://github.com/aida-ugent/vigil)** (Univ. de Ghent / arXiv 2026), com três linhas de contraste visual:  
  1. *Modo Regex local:* 0,03 ms (rápido, mas cego ao contexto).  
  2. *Modo WebLLM local:* mediana de 3,4 s por post (lento demais para o feed).  
  3. *Detector de moralização:* exige envio para servidor externo.
- **eu falo:** *(Roteiro da sua fala):*  
  Mostre o concorrente que mais ameaça a ideia: o Vigil, desenvolvido na Universidade de Ghent. Diga que ele quase derrubou o projeto ao provar que dá para atuar no feed do X contra vieses e moralização. Em seguida, aponte onde ele falha para o seu usuário: o modo rápido do Vigil é apenas regex estático; o modo semântico no navegador usa um WebLLM generativo que leva quase 3,5 segundos por post; e a análise de moralização depende de um servidor externo. O FiltroSoberano corta essas dependências.

## slide 3 · o artigo mais próximo · 45 s

- **aparece:** primeira página do artigo:  
  *"Fine-Grained Analysis of Propaganda in News Articles"* · Da San Martino et al. · EMNLP 2019 (A1) · [aclanthology.org/D19-1565](https://aclanthology.org/D19-1565/).  
  Destaque para a taxonomia das 18 técnicas de apelo emocional (*Appeal to Fear, Loaded Language, Name Calling*).
- **eu falo:** *(Roteiro da sua fala):*  
  Explique que este é o artigo de referência máxima porque não tenta adivinhar se a notícia é fake ou real, mas mapeia formalmente os fragmentos retóricos de persuasão psicológica. Aponte o risco que o artigo revela para o seu projeto: ele foi projetado para artigos jornalísticos longos e polidos em inglês, rodando em servidores. Redes sociais em português usam ironia, gírias e textos curtos. Esse é o risco científico que você assume e vai medir.

## slide 4 · o que só a minha faz · 55 s

- **aparece:** duas frases e um gráfico/dado do teste preliminar:  
  1. *Para o usuário:* retórica apelativa, moralização e urgência em português, 100% no navegador em passada única (<1 s, zero nuvem).  
  2. *Para a ciência:* um classificador de Sistema 1 local consegue frear o engajamento impulsivo sem irritar o usuário com falsos positivos no português informal?  
  3. *O número incômodo do tec:* no teste em CPU, rodou em <1 s, mas confundiu ataque pessoal com pânico moral (prob 0.34) e acusou probabilidades não calibradas.
- **eu falo:** *(Roteiro da sua fala):*  
  Apresente o diferencial prático: enquanto o PropaLens só olha inglês e o Vigil precisa de servidor ou demora 3,4 segundos, o FiltroSoberano faz a inferência estruturada em fração de segundo sem que nenhum caractere saia da máquina. Depois, lance a pergunta científica que pode dar "não": a ferramenta realmente ajuda a conter reações por impulso sem afogar o usuário em alertas falsos? Mostre honestidade com o teste piloto do `tec.md`, que já provou que o modelo base erra sutilezas no português e exige calibração RLCD.

## slide 5 · o fecho · 15 s

- **aparece:** o logotipo conceitual do FiltroSoberano e a frase: *"A atenção é sua. O raciocínio crítico fica na sua máquina."*
- **eu falo:** *(Roteiro da sua fala):*  
  Encerre firme: as redes sociais monetizam a reação emocional e o pânico moral. O FiltroSoberano dá ao leitor o direito de pausar e pensar, com soberania técnica e privacidade absoluta.

---

**tempo total, cronometrado:** [a cronometrar: meta entre 3 min e 4 min 30 s]

---

## ensaio cético

*(Atenção: execute este passo abrindo uma **conversa nova**, colando o prompt abaixo para que a IA atue como banca cética rigorosa):*

```text
você é um professor cético numa banca de 5 minutos. vou apresentar uma ideia de projeto em 4 pontos:
[cole as 4 frases acima e os slides 1 a 5]. faça as 5 perguntas mais difíceis que você faria, uma por vez,
e espere a minha resposta antes da próxima. não invente referências. no fim, diga em qual ponto
eu não te convenci, e por quê. não reescreva a minha fala.
o padrão é lucassf.pages.dev/ai4good/sem1-excelente; evite o que faz lucassf.pages.dev/ai4good/sem1-raso.
```

**a pergunta mais difícil:** [preencher após rodar na conversa nova]

**o que eu mudei por causa dela:** [preencher com a mudança que você fez na frase ou nos slides]
