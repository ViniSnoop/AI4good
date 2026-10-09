# AI4good Workspace

Workspace da disciplina de **Tópicos Avançados em Inteligência Artificial** (UFRPE) — integrando desenvolvimento de código, experimentação prática e escrita de artigos científicos com fluxos agênticos.

## 📁 Estrutura do Repositório

```
AI4good/
├── code/               # Projetos e atividades práticas da disciplina
│   ├── mlp-heart-disease/  # MLP do zero + visualizador Streamlit
│   ├── scaffold.sh         # Script para iniciar novas atividades
│   └── _templates/         # Modelos de documentação e governança
├── papers/             # Artigos em LaTeX e manuscritos científicos
│   ├── samplepaper.tex     # Template Springer LNCS
│   ├── llncs.cls           # Classe Springer LNCS
│   └── splncs04.bst        # Estilo bibliográfico Springer
├── core/               # Biblioteca de agentes (skills, hooks, ferramentas)
├── docs/               # Guias de configuração e documentação de apoio
│   ├── GITHUB_SETUP.md     # Guia do repositório remoto e branches
│   ├── OVERLEAF_SETUP.md   # Guia de sincronização com o Overleaf
│   └── SETUP_SUMMARY.md    # Resumo da infraestrutura
├── AGENTS.md           # Ponto de entrada canônico e normas do workspace
├── setup.sh            # Script de automação do ambiente
└── opencode.json       # Configuração dos harnesses (opencode + antigravity)
```

## 🚀 Como Começar

### 1. Criar uma Nova Atividade de Código
Para iniciar uma nova atividade ou projeto dentro do repositório com toda a governança padronizada:
```bash
cd code
./scaffold.sh <nome-da-atividade>
```

### 2. Executar Projetos Existentes
Exemplo para o projeto da MLP de Risco Cardíaco:
```bash
cd code/mlp-heart-disease
streamlit run mlp_heart_disease.py
```

### 3. Compilar Artigos em LaTeX
```bash
cd papers
latexmk -xelatex -halt-on-error -interaction=nonstopmode samplepaper.tex
```

## 🌿 Git Flow

O repositório segue o padrão Git Flow:
- `main`: Versões estáveis e entregas validadas.
- `develop`: Branch de integração contínua para as atividades em andamento.
- `feature/<nome>`: Desenvolvimento de novas atividades e experimentos antes do merge em `develop`.

---
Autor: **Vinícius Fernandes de Souza**  
Universidade Federal Rural de Pernambuco (UFRPE)
