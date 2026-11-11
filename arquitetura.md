# FiltroSoberano · fluxograma e arquitetura

O caminho de uma análise de postagem no feed, do gesto do usuário ao rótulo pedagógico (*nudge*) de retorno.  
Artefato **fluxograma e arquitetura** (`flx`) da disciplina AI for Good.

Formas: **pessoa** `([ ])` · **IA** `{{ }}` · **regra** `[ ]`. Caixas: onde cada peça roda.

```mermaid
flowchart TD
    subgraph NAV["Navegador do usuário (Chrome / Firefox / Brave) · tudo local, sem servidor"]
        A(["1 · Usuário passa o mouse ou clica em 'Analisar' sobre post suspeito no feed"])
        B["2 · Content script extrai o texto do post do DOM e limpa tags/emojis repetidos"]
        C{"3 · Texto tem mais de 15 caracteres?"}
        C_NAO["3a · Alerta na tela: 'Texto muito curto para análise retórica'"]
        D{{"4 · Modelo Laya (Sistema 1, ONNX/WebGPU): infere tática retórica ('choice') e intensidade ('score')"}}
        E["5 · Dicionário estático associa diagnóstico a badge pedagógico e dica de clareza crítica"]
        F["6 · Extensão injeta badge/tooltip educativo discreto diretamente acima do post"]
        G(["7 · Usuário lê o rótulo pedagógico, ganha distanciamento reflexivo e decide como reagir"])
    end

    A --> B
    B --> C
    C -- "Não (<15 chars)" --> C_NAO
    C -- "Sim (≥15 chars)" --> D
    D --> E
    E --> F
    F --> G
```

## Os dados e privacidade

| Dado pessoal / conteúdo | De quem é | Onde fica | Quem vê | Por quanto tempo | Quando é apagado |
|:---|:---|:---|:---|:---|:---|
| Texto da postagem sob análise | Autor do post no feed | Memória temporária (RAM) da extensão | Apenas a extensão no navegador do usuário | Milissegundos (durante a passada do modelo) | Imediatamente após a inferência e exibição |
| Diagnóstico e score gerado | Usuário da extensão | DOM da página ativa (HTML temporário) | Apenas o próprio usuário em sua tela | Enquanto a aba estiver aberta | Ao fechar a aba ou atualizar a página |
| Identidade / URL / Perfil do autor | Autor do post | Não é coletado nem acessado | Ninguém | Nunca é armazenado | Não entra no pipeline |

**O que sai do aparelho de quem usa:** Absolutamente nada. Toda a extração e a inferência do modelo Laya rodam 100% no cliente (navegador local), sem chamadas de API externas nem servidores de telemetria.
