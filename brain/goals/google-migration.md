# [ career | admin | now ] migração Google — conta cin → pessoal, e o Drive para o workspace

Tirar a vida acadêmica e pessoal de dentro de `lsf@cin.ufpe.br` e assentá-la em `lsf.cin@gmail.com`,
e trazer o Drive do cin para dentro do workspace local. São duas metades que se puxam: a **conta**
(navegador, calendar, 2FA) e o **conteúdo** (a fila de download). A ordem é mapear → decidir a forma
de sincronizar → mover; migrar antes de mapear só reproduz o espalhamento numa conta nova. Cockpit
com a fila e o estado por pasta: [`branches/google-migration/`](../../branches/google-migration/CONTEXT.md).

>**signals**  
useful · expected · motivated

>**owns**  
`branches/google-migration`

## selected next achievement
    [brave-conta-padrao] mudar a conta Google padrão do Brave para lsf.cin@gmail.com — o primeiro passo da migração, e o
    único que não depende de decidir nada

**ease-start**  
5 minutos no Brave, sem decidir nada:
1. Abrir `https://accounts.google.com` → clicar na foto do perfil (canto superior direito) → **Sair de todas as
   contas**.
2. Entrar **primeiro** com `lsf.cin@gmail.com` — a primeira conta logada é a que o Google trata como padrão (`/u/0`).
3. Só então **Adicionar conta** para `lsf@cin.ufpe.br` e para a da UFRPE — elas passam a ser `/u/1` e `/u/2`.
4. Conferir: abrir `https://drive.google.com` numa aba nova e ver se a URL fica em `/u/0`, com a conta pessoal.

O passo seguinte, `[drive-sync-method]`, é decisão e não clique — deixe para outra sessão.

## backlog

> [ ] [brave-conta-padrao] mudar a conta Google padrão do Brave para lsf.cin@gmail.com — primeiro passo da migração, e o
> único que não depende de decidir nada (INBOX 2026-08-18)  
> [ ] [drive-sync-method] decidir a forma de sincronizar a pasta local com o gdrive na parte acadêmica, principalmente
> das aulas — a hipótese do Lucas é instalar o próprio cliente do gdrive e deixar ele sincronizar, *"funcionaria como um
> git com commits automatizados?"*. Checar a viabilidade: o cliente sincroniza estado, não histórico, então a pergunta
> real é se o versionamento nativo do Drive basta ou se a pasta precisa ser um repo de verdade. É a decisão que a fila
> de download em `branches/google-migration/ROADMAP.md` está esperando, que hoje pressupõe download manual (INBOX
> 2026-08-18)  
> [ ] [ensino-mapa] mapear a parte de ensino da vida dentro do WOS e migrá-la inteira para lsf.cin@gmail.com — **o mapa
> vem antes da migração**: hoje o ensino está espalhado entre `academy/classes/`, a fila de download e a conta do cin.
> Decidir onde ensino mora no WOS, depois mover; senão a migração só reproduz o espalhamento numa conta nova. Colide com
> o split vivo entre `academy/classes/` e `academy/teaching/` (INBOX 2026-08-18)  
> [ ] [fila-academy] baixar as 23 pastas de `### academy/` da fila — as linhas, com o par `local ← Drive path` de cada
> uma, vivem em `branches/google-migration/ROADMAP.md`  
> [ ] [fila-branches] baixar as 6 pastas de `### branches/` da fila — mesmas linhas, mesmo arquivo  
> [ ] [fila-triagem] as 2 linhas de `### triage (do last)`: a pasta `Unorganized/` e os arquivos soltos da raiz. Os
> **recovery codes** estão entre os arquivos soltos, então esta linha amarra direto em `[auth-recovery]`  
> [ ] [calendar-migrar] migrar o calendar de lsf@cin.ufpe.br para lsf.cin@gmail.com — `core/tools/calendar/gcalendar` já
> lê as três contas, então a migração é de dados e de conta padrão, não de ferramenta (INBOX 2026-08-18)  
> [ ] [auth-recovery] backup/recovery do Google Authenticator — várias contas com 2FA nele; se o celular quebrar/sumir,
> como recuperar? Mapear códigos de recuperação por conta + método de restauração antes que vire pesadelo (INBOX
> 2026-07-24)  
> [ ] [aulas-para-pessoal] transferir todas as aulas do Drive do cin para o pessoal, e só então deletar os slides e
> materiais do lado do cin — a deleção é o último passo, nunca simultânea (INBOX 2026-08-24)  
> [ ] [notion-links-simples] mudar o padrão de links no Notion: link simples no calendário em vez de "Mention" em seção
> separada, apontando já para os slides do Drive pessoal — depende de `[aulas-para-pessoal]`, senão os links novos
> apontam para o Drive que vai morrer (INBOX 2026-08-24)  

## done

<!-- done:start -->
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-08-24  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |       3 |
| trimester   |       3 |
| semester    |       3 |
| year        |       3 |
| 2-year      |       3 |
| 4-year      |       3 |
<!-- stats:end -->
