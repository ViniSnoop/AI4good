# [ craft | teaching | near ] teaching materials paradigm

Mudar o paradigma do material de aulas. Slides como arquivos abertos, com animações, acessíveis e editáveis. Sair do PowerPoint/PDF estático e entrar em algo vivo — onde o conteúdo pode ser versionado, transformado por agentes, e verdadeiramente interativo. Before building: understand what's best-in-class today.

**A metade que faltava, dita por Lucas em 2026-08-14: conectividade antes de formato.** Hoje o
material de aula **não mora no workspace** — slides e forms estão no **Google Drive**, a página da
turma está no **Notion**. Enquanto o WOS não enxerga e não edita esses dois lugares, qualquer
discussão de formato é teórica: não há como um agente migrar, versionar ou transformar um material
que ele não alcança. Então a ordem é: **alcançar → organizar → só depois trocar o formato.**

Divisão de responsabilidade, para o item não viver em dois lugares: **este goal é a intenção e a
ordem**; a construção das ferramentas (CLI do Notion, superfície Google em `core/tools/`) é item de
[`core/ROADMAP.md`](../../core/ROADMAP.md). Uma cópia seria bug.

>**signals**  
meaningful · expected · motivated

>**timing**  
Semestre começou em agosto/2026 e Lucas quer isso organizado "em breve" — âncora externa real, não
prazo inventado. O custo de adiar não é perder um deadline, é passar mais um semestre produzindo
material fora do alcance do workspace.

>**owns**  
`core/tools/slides`  
`core/tools/files` · `core/tools/mail` · `core/tools/calendar`  
`academy/teaching`

**A conectividade caiu em 2026-08-19.** O gargalo que este goal declarava — "material fora do
alcance do workspace" — não existe mais para Tecnologias na Educação: o Notion lê (integração "WOS"
viva, página `0bd17453-ea83-4019-ba38-22a79d0114ce`), o Drive pessoal lê, e o `gslides` **escreveu
de verdade num deck real de aula** — 20 slides intercalados e 3 refinados no deck de Design
Thinking, na véspera da aula. `[roundtrip-one]` está feito. A ordem "alcançar → organizar → só
depois trocar o formato" avançou uma casa: o próximo degrau é **organizar**, não conectar.

## selected next achievement
    [metodologia-tecedu] desenhar a metodologia completa de Tecnologias na Educação e fechar o calendário 2026.2

**ease-start**  
Abra `academy/teaching/tecnologias-na-educacao/CONTEXT.md` e `academy/refs/REFS.md` § disciplinas
project-based. Os 34 encontros já estão contados e o padrão de missão do ME310 já está descrito.
Comece escrevendo **uma** semana-padrão: o que a quarta faz, o que a sexta faz.

## backlog

> [ ] [metodologia-tecedu] semana-padrão (quarta e sexta com papéis fixos, uma pergunta e um produto por encontro), as 9 etapas mapeadas nos 34 encontros reais (números em `academy/teaching/tecnologias-na-educacao/CONTEXT.md`), avaliação nova, dashboard que substitui as duas planilhas Google, e o padrão MODELO+EXEMPLO em toda entrega  
> [ ] [pesquisa-que-falta] gamificação séria (sem infantilizar), specs/contract grading, mecanismos de avaliação por pares com propriedades verificáveis, e venues de publicação alcançáveis por graduandos em um semestre  
> [ ] [notion-write] WOS edita a página da turma — o CLI lê; escrever a metodologia nova lá é o que fecha o ciclo para os alunos  
> [ ] [excalidraw-vs-miro] veredito sobre trocar o Miro: a colaboração ao vivo do Excalidraw é efêmera e morre com a aba de quem abriu. Decidir **com a evidência da aula de 2026-08-19**, não antes  
> [ ] [research-tools] research best current teaching tools — interactive slides, animations, open formats — start from the animation entries in `core/refs/REFS-unjudged.md` (claude-code+remotion, Claude Code UI-animation skills). **Reescopado 2026-08-14:** o WOS agora lê e edita os decks direto no Google Slides (`core/tools/slides/gslides`), e Slidev foi deletado — a pergunta aberta não é mais qual formato local adotar, é quanto de animação dá pra autorar como sequência de slides gerada (inclui a ideia de um gerador de animações próprio)  
> [ ] [pick-format] pick a target format or tool — one concrete candidate to prototype with  
> [ ] [migrate-one] convert one existing lecture to the new format as a test  
> [ ] [full-migration] define migration plan for remaining course materials  
> [ ] [excalidraw-aula02] abrir `academy/teaching/tecnologias-na-educacao/aula02-problemas.excalidraw` no excalidraw.com e confirmar que carrega (o JSON foi montado à mão, nunca foi aberto); depois, Live collaboration → copiar o link → trocar `[EXCALIDRAW]` no slide 69 do deck; confirmar se são mesmo 8 equipes (o quadro tem 8 frames)  
> [ ] [video-carrinho] decidir o vídeo do slot do carrinho — trecho de 4 min do Dietz, ou perguntar à turma "o que envelheceu nesse vídeo de 1999?" (candidatos avaliados em `academy/refs/REFS.md`)  
> [ ] [medir-redesenho] anotar dois números depois da aula — quantos alunos falaram no bloco de abertura, e quantos grupos saíram com o frame preenchido; é o teste honesto do redesenho  
> [ ] [questionarios-sextas] mandar os dois questionários pras turmas — links de resposta nos `CONTEXT.md` de `academy/teaching/ai4good/` e `academy/teaching/tecnologias-na-educacao/`; antes, abrir cada link, responder uma vez de teste e apagar a resposta; depois da aula, ler com `core/tools/forms/gforms responses --account personal <form_id>` e decidir o formato das sextas  
> [ ] [ai4good-book-burning] investigar o caso por trás do reel "this feels like a book burning" e decidir se entra nas aulas de ai4good — ref em `academy/refs/REFS.md` (INBOX 2026-07-28)  
> [ ] [ai4good-pacing-frontier] assistir o reel "pacing the frontier" e decidir se entra nas aulas — ref em `academy/refs/REFS.md`; a extração só trouxe a legenda, então o conteúdo ainda é desconhecido (INBOX 2026-08-17)  
> [ ] [arxiv-visuals] achar e testar o arXiv Visuals (paper → explainer animado; link é comment-gated, então achar por fora) — ref em `academy/refs/REFS.md`; teste honesto: rodar num paper que você conhece a fundo e ver se a ordem "conceito mais difícil primeiro" se sustenta ou se é sumarização com narração; se sustentar, decidir dois usos separados: leitura própria e material de aula (INBOX 2026-08-17, *"this IS for me"*)  
> [ ] [or-gate-shape] OR gate body ainda ausente no deck de portas lógicas; investigar o tipo `CUSTOM` no grupo do slide 23, depois decidir se vale seguir debugando  
> [ ] [calendario-ufrpe] baixar o calendário acadêmico da UFRPE para ajudar no planejamento das aulas (INBOX 2026-08-18)  

## done

<!-- done:start -->
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-08-24  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |      26 |
| trimester   |      40 |
| semester    |      40 |
| year        |      40 |
| 2-year      |      40 |
| 4-year      |      40 |
<!-- stats:end -->
