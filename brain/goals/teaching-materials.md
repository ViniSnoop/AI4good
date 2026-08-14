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

## selected next achievement
    [inventory-material] mapear o que existe e onde — pastas do Drive por disciplina, páginas do Notion, o que é fonte e o que é cópia

**ease-start**  
Abra o Drive e o Notion lado a lado e liste, em dez linhas, quais disciplinas têm material e onde
cada uma mora. Sem organizar nada ainda — só o inventário.

## backlog

> [ ] [inventory-material] mapear o que existe e onde — pastas do Drive por disciplina, páginas do Notion, o que é fonte e o que é cópia; sem isso não dá pra saber o que "conectar" significa  
> [ ] [notion-read] WOS lê a página da turma no Notion — depende do CLI rastreado em `core/ROADMAP.md` (REST oficial + token de integração interna, sem MCP)  
> [ ] [notion-write] WOS edita a página da turma — escrita só depois que a leitura estiver confiável  
> [ ] [roundtrip-one] editar **uma** aula real pelo CLI e devolver ao lugar onde os alunos veem; é o teste honesto de que a conexão existe  
> [ ] [research-tools] research best current teaching tools — interactive slides, animations, open formats — start from the animation entries in `core/WATCHLIST.md` (claude-code+remotion, Claude Code UI-animation skills). **Reescopado 2026-08-14:** o WOS agora lê e edita os decks direto no Google Slides (`core/tools/slides/gslides`), e Slidev foi deletado — a pergunta aberta não é mais qual formato local adotar, é quanto de animação dá pra autorar como sequência de slides gerada  
> [ ] [pick-format] pick a target format or tool — one concrete candidate to prototype with  
> [ ] [migrate-one] convert one existing lecture to the new format as a test  
> [ ] [full-migration] define migration plan for remaining course materials  

## done

<!-- done:start -->
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-08-14  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |      15 |
| trimester   |      25 |
| semester    |      25 |
| year        |      25 |
| 2-year      |      25 |
| 4-year      |      25 |
<!-- stats:end -->
