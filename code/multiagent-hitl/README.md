# Multi-Agent HITL Simulation (Utopia vs Distopia)
> Simulação estratégica em 20 rodadas com Human-in-the-Loop, SLMs locais no Ollama e Gemini remoto.

## Modelos Locais Configurados (Ollama)
- **Agent Alpha (The Architect)**: `qwen2.5:7b` (Chain-of-Thought & Expansão Sistêmica)
- **Agent Beta (The Adversary)**: `llama3.1:8b` (Contrastive Red-Teaming)
- **Agent Gamma (The Synthesizer)**: `gemini-2.5-flash` via SDK oficial `google-genai`

Modelos alternativos suportados via flag: `gemma3:4b`, `ministral-3:3b`, `mistral:7b`.

## Como Executar
```bash
# 1. Instalar dependências
pip install google-genai requests

# 2. Configurar a chave do Gemini
export GEMINI_API_KEY="sua_chave_aqui"

# 3. Executar com modelos padrão (qwen2.5:7b e llama3.1:8b)
python simulation_hitl.py

# Ou alternando modelos leves:
python simulation_hitl.py --alpha gemma3:4b --beta mistral:7b
```
