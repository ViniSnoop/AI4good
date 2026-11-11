# FiltroSoberano · fluxograma e arquitetura

O caminho de uma análise de postagem no feed, do gesto do usuário ao rótulo pedagógico (*nudge*) de retorno e conferência humana.  
Artefato **fluxograma e arquitetura** (`flx`) da disciplina AI for Good.

Formas: **pessoa** `([ ])` · **IA** `{{ }}` · **regra** `[ ]`. Caixas: onde cada peça roda.

```mermaid
flowchart TD
    subgraph CDN["CDN pública (Hugging Face / GitHub Releases)"]
        DEP["Pesos ONNX quantizados (laya-multilingual, ~420 MB) e runtime onnxruntime-web"]
    end

    subgraph NAV["Navegador do usuário (Chrome / Firefox / Brave) · execução 100% local"]
        subgraph INSTALACAO["1. Inicialização única (na instalação ou 1º uso)"]
            CACHE[("CacheStorage local do navegador")]
            DEP -- "Download único via Wi-Fi (~420 MB)" --> CACHE
        end

        subgraph FLUXO["2. Ciclo de análise sob demanda no feed"]
            A(["1 · Usuário passa o mouse ou clica em 'Analisar' sobre post suspeito no feed"])
            B["2 · Content script extrai o texto do post do DOM da página e limpa tags/emojis"]
            C["3 (Regra) · Verificação de tamanho: texto tem pelo menos 15 caracteres?"]
            C_NAO["3a · Alerta na tela: 'Texto muito curto para análise' e encerra"]
            D{{"4 · Inferência Laya (Sistema 1 via ONNX Runtime Web / WebGPU): infere tática retórica ('choice') e intensidade ('score')"}}
            E["5 · Dicionário estático associa diagnóstico a badge pedagógico e dica de clareza crítica"]
            F["6 · Extensão injeta badge/tooltip pedagógico discreto diretamente sobre o post"]
            G(["7 · Usuário lê o rótulo pedagógico, confere o diagnóstico e decide como reagir"])
            H(["7a · Conferência humana: usuário pode clicar em 'Discordar / Falso positivo' ou fechar"])
        end
    end

    CACHE -. "Carrega pesos em RAM da aba (<1s)" .-> D
    A --> B
    B --> C
    C -- "Não (<15 chars)" --> C_NAO
    C -- "Sim (≥15 chars)" --> D
    D --> E
    E --> F
    F --> G
    G --> H
```

## Os dados e privacidade

| Dado / conteúdo | De quem é | Onde fica | Quem vê | Por quanto tempo | Quando é apagado |
|:---|:---|:---|:---|:---|:---|
| Texto da postagem (pode conter dados de terceiros) | Autor do post no feed | Memória temporária (RAM) da aba ativa | Apenas a extensão no navegador local | Milissegundos (durante a passada do modelo) | Imediatamente após a inferência, sem gravação em disco |
| Diagnóstico retórico e score gerado | Usuário da extensão | DOM temporário da página ativa | Apenas a pessoa usuária na sua tela | Enquanto a aba estiver aberta | Destruído ao fechar a aba ou atualizar o feed |
| Feedback de discordância (passo 7a) | Usuário da extensão | Memória local da extensão (opcional) | Apenas o usuário | Na sessão atual | Apagado ao fechar a sessão |
| Identidade, URL ou perfil do autor | Autor do post | Não é extraído nem acessado | Ninguém | Nunca entra no pipeline | Não é lido pelo content script |
| Pesos e runtime do modelo | Do projeto Laya (pesos abertos) | CacheStorage local do navegador | Runtime local do navegador | Permanente até desinstalação | Na desinstalação da extensão |

**O que sai do aparelho de quem usa:** Absolutamente nada do conteúdo lido ou analisado. A única comunicação de rede externa é o download inicial único dos arquivos estáticos dos pesos do modelo (CDN pública $\to$ CacheStorage), que não transmite nenhum identificador de usuário, token, histórico ou texto de navegação. Toda a inferência ocorre localmente (client-side) via WebGPU/WASM.
