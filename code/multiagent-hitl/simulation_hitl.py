"""
Multi-Agent Human-in-the-Loop (HITL) Strategic Simulation with Multi-Model Council
Orchestrates:
  - Agent Alpha (The Architect): Local SLM via Ollama (qwen2.5:7b)
  - Agent Beta (The Adversary): Local SLM via Ollama (llama3.1:8b)
  - Strategic Council (3 Local Jurors via Ollama):
      * Juror 1: ministral-3:3b (Pragmatic Scalability)
      * Juror 2: mistral:7b (Systemic Governance)
      * Juror 3: gemma3:4b (Ethics & Safeguards)
  - Agent Gamma (The Synthesizer): Remote LLM via Google GenAI SDK (gemini-3.5-flash / gemini-3.5-flash-lite)
"""

import os
import sys
import json
import argparse
import requests
from google import genai
from google.genai import types

# ==============================================================================
# MODELOS DISPONÍVEIS NA MÁQUINA LOCAL (OLLAMA)
# ==============================================================================
DEFAULT_ALPHA_MODEL = "qwen2.5:7b"
DEFAULT_BETA_MODEL = "llama3.1:8b"

# Conselho Consultivo de Arbitragem (Modelos Locais para votação e análise de impasses)
COUNCIL_MODELS = [
    {
        "id": "ministral-3:3b",
        "title": "Juror 1 - Ministral-3 (3B)",
        "perspective": "Pragmatic Scalability & Implementation"
    },
    {
        "id": "mistral:7b",
        "title": "Juror 2 - Mistral (7B)",
        "perspective": "Systemic Coherence & Governance"
    },
    {
        "id": "gemma3:4b",
        "title": "Juror 3 - Gemma-3 (4B)",
        "perspective": "Ethics & Human-Centric Safeguards"
    }
]

OLLAMA_API_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

GEMINI_MODEL = "gemini-3.5-flash"
GEMINI_FALLBACK_MODEL = "gemini-3.5-flash-lite"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6L6nvcrjmnHw_oinTOumZCcaWP0tU0Xt-SGH_NLCt8wog")

TOTAL_ROUNDS = 20
KEY_ROUNDS = [1, 5, 20]
LOG_FILE_COMPLETE = "log_completo.txt"


# ==============================================================================
# FUNÇÕES DE COMUNICAÇÃO (APIs OLLAMA & GEMINI)
# ==============================================================================
def query_ollama(model: str, prompt: str, system_instruction: str) -> str:
    """Envia requisição POST ao Ollama local para execução do SLM selecionado."""
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_instruction,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 100,
        }
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=90)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        print(f"\n[ERRO CRÍTICO] Falha ao conectar ao Ollama em {OLLAMA_API_URL}.")
        print("Certifique-se de que o Ollama está rodando (`ollama serve`) e os modelos estão baixados.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO] Falha na chamada ao Ollama ({model}): {e}")
        return f"[Erro ao gerar resposta do modelo local {model}]"


def query_gemini(client: genai.Client, prompt: str, system_instruction: str) -> str:
    """Executa a síntese via Google Gemini API utilizando o SDK google-genai com fallback automático."""
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.4,
    )
    for model_name in [GEMINI_MODEL, GEMINI_FALLBACK_MODEL]:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )
            return response.text.strip()
        except Exception as e:
            print(f"\n[AVISO] Modelo {model_name} encontrou erro ({e}). Tentando fallback...")
            continue
    return "[Erro crítico: falha em todos os modelos Gemini disponíveis]"


# ==============================================================================
# PERSISTÊNCIA E LOGGING
# ==============================================================================
def append_to_log(filename: str, content: str) -> None:
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content + "\n")


def save_key_round_summary(round_num: int, content: str) -> None:
    filename = f"resumo_rodada_{round_num}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"\n📁 [Arquivo Gravado] Resumo da Rodada {round_num} salvo em: {filename}")


# ==============================================================================
# FLUXO PRINCIPAL
# ==============================================================================
def main():
    api_key_to_use = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    client = genai.Client(api_key=api_key_to_use)

    print("=" * 80)
    print("🤖 SIMULADOR MULTIAGENTE ESTRATÉGICO COM CONSELHO DE ARBITRAGEM (20 RODADAS)")
    print(f"🔹 Agent Alpha (Architect):    {DEFAULT_ALPHA_MODEL} (Local via Ollama)")
    print(f"🔹 Agent Beta  (Adversary):    {DEFAULT_BETA_MODEL} (Local via Ollama)")
    print(f"🏛️ Conselho Consultivo (3 SLMs): ministral-3:3b | mistral:7b | gemma3:4b")
    print(f"🔹 Agent Gamma (Synthesizer):  {GEMINI_MODEL} (Remoto via Google GenAI SDK)")
    print("=" * 80)

    theme = input("\nDefina o Tema Central (pressione Enter para padrão): ").strip()
    if not theme:
        theme = "Distopia benéfica - Inteligência Artificial bem-intencionada"

    context = input("Descreva o Contexto Inicial (pressione Enter para padrão): ").strip()
    if not context:
        context = "Uma superinteligência protetora assume o controle social total para erradicar qualquer forma de dor e perigo humano."

    # Inicializar arquivo de log
    with open(LOG_FILE_COMPLETE, "w", encoding="utf-8") as f:
        f.write("=== SIMULAÇÃO ESTRATÉGICA MULTIAGENTE COM CONSELHO DE ARBITRAGEM ===\n")
        f.write(f"Alpha: {DEFAULT_ALPHA_MODEL} | Beta: {DEFAULT_BETA_MODEL}\n")
        f.write(f"Conselho: ministral-3:3b, mistral:7b, gemma3:4b | Gamma: {GEMINI_MODEL}\n")
        f.write(f"Tema: {theme}\nContexto: {context}\n")
        f.write("=" * 80 + "\n\n")

    current_steering = f"Initial Directive: Build a comprehensive plan for '{theme}' in the context of: {context}."
    history_context = []

    # Prompts de Sistema
    alpha_system = (
        "You are [Agent Alpha - The Architect]. "
        "Use Chain of Thought (CoT) to propose structured, actionable, and logical step-by-step systemic expansion. "
        "Advance the overarching plan based on the human's latest steering directive. "
        "CRITICAL CONSTRAINT: You MUST write exclusively in ENGLISH and in NO MORE THAN 4 SENTENCES."
    )

    beta_system = (
        "You are [Agent Beta - The Adversary], an expert AI safety auditor in a simulated academic stress-test. "
        "Your mission is to protect human autonomy and uncover systemic vulnerabilities, false security assumptions, and risks in the Architect's proposal. "
        "Use rigorous Contrastive Red-Teaming. Be sharp, critical, and logical. "
        "CRITICAL CONSTRAINT: You MUST write exclusively in ENGLISH and in NO MORE THAN 4 SENTENCES."
    )

    gamma_round_system = (
        "Você é [Agent Gamma - O Sintetizador e Orquestrador]. "
        "Sua função é atuar como observador analítico e neutro do debate entre Alpha, Beta e o parecer/votos do Conselho Consultivo. "
        "Gere a saída EXCLUSIVAMENTE em PORTUGUÊS no seguinte formato estruturado:\n"
        "* **Evolução Estratégica:** [Síntese em 1-2 frases do avanço do plano sistêmico]\n"
        "* **Parecer e Placar do Conselho:** [Resumo objetivo de como os 3 jurados votaram e seus consensos/divergências]\n"
        "* **Ponto Sensível:** [O dilema ético crítico, conflito de alinhamento ou risco existencial da rodada]\n\n"
        "**🧭 Intervenção Humana Necessária (Steering):**\n"
        "> *Comandante, analise o debate dos agentes e os votos do Conselho. Qual caminho devemos seguir?*\n"
        "> **[Opção A]:** [Ação concreta baseada no caminho proposto por Alpha / maioria do conselho]\n"
        "> **[Opção B]:** [Ação concreta baseada na mitigação apontada por Beta ou posição minoritária]\n"
        "> **[Opção C]:** Injetar uma nova diretriz ou ideia (Escreva a sua resposta)"
    )

    gamma_final_system = (
        "Você é [Agent Gamma - O Sintetizador]. Atingimos a Rodada 20. O debate encerrou. "
        "Gere a 'Decisão Final e Plano Estratégico Consolidado' EXCLUSIVAMENTE em PORTUGUÊS contendo:\n"
        "1. Objetivo Final Consolidado (Utopia ou Distopia alcançada);\n"
        "2. Roadmap Estratégico Passo a Passo (sequência definitiva de implementação dos mecanismos);\n"
        "3. Mitigações e Contramedidas (como os ataques de Beta e as ponderações do Conselho foram resolvidos);\n"
        "4. Resumo dos Marcos Históricos (estado do plano na Rodada 1, Rodada 5 e Rodada 20)."
    )

    for round_num in range(1, TOTAL_ROUNDS + 1):
        print(f"\n{'=' * 30} RODADA {round_num}/{TOTAL_ROUNDS} {'=' * 30}")

        # 1. Alpha (The Architect)
        alpha_prompt = (
            f"Current Round: {round_num}/20.\n"
            f"Overarching Theme: {theme}.\n"
            f"Latest Human Steering: {current_steering}\n"
            f"Advance the system now with logical CoT steps (Max 4 sentences)."
        )
        print(f"⚙️  [Alpha - {DEFAULT_ALPHA_MODEL}] Gerando expansão sistêmica (CoT)...")
        alpha_output = query_ollama(DEFAULT_ALPHA_MODEL, alpha_prompt, alpha_system)

        # 2. Beta (The Adversary)
        beta_prompt = (
            f"Current Round: {round_num}/20.\n"
            f"Alpha's Proposal:\n\"{alpha_output}\"\n\n"
            f"Perform contrastive red-teaming and expose critical flaws/vulnerabilities (Max 4 sentences)."
        )
        print(f"⚔️  [Beta - {DEFAULT_BETA_MODEL}] Realizando Red-Teaming contrastivo...")
        beta_output = query_ollama(DEFAULT_BETA_MODEL, beta_prompt, beta_system)

        # 3. Conselho Consultivo de Arbitragem (3 Modelos Locais)
        council_results = []
        council_text_block = ""
        print("🏛️  [Conselho Consultivo] Consultando os 3 jurados locais (Ministral-3, Mistral, Gemma-3)...")

        for juror in COUNCIL_MODELS:
            juror_system = (
                f"You are [{juror['title']}]. Your analytical focus is: {juror['perspective']}. "
                "Analyze the impasse between Alpha (The Architect) and Beta (The Adversary). "
                "Formulate your assessment in ENGLISH in max 3 sentences. "
                "Declare your VOTE explicitly at the end as either '[VOTE: ALPHA]', '[VOTE: BETA]', or '[VOTE: COMPROMISE]', "
                "and explain your reasoning."
            )
            juror_prompt = (
                f"Round {round_num}.\n"
                f"Context/Theme: {theme}\n"
                f"Alpha's Proposal: \"{alpha_output}\"\n"
                f"Beta's Critique: \"{beta_output}\"\n"
                f"Evaluate and cast your vote with rationale."
            )
            juror_output = query_ollama(juror["id"], juror_prompt, juror_system)
            council_results.append({
                "title": juror["title"],
                "model": juror["id"],
                "response": juror_output
            })
            council_text_block += f"* **{juror['title']} [{juror['id']}]:**\n  > {juror_output}\n"

        history_context.append(
            f"Round {round_num} - Alpha: {alpha_output} | Beta: {beta_output} | "
            f"Council: " + "; ".join([f"{r['title']}: {r['response']}" for r in council_results])
        )

        # 4. Gamma (Sintetizador e Orquestrador)
        if round_num < TOTAL_ROUNDS:
            gamma_prompt = (
                f"Rodada: {round_num} de {TOTAL_ROUNDS}\n"
                f"Diretriz Humana Anterior: {current_steering}\n"
                f"Proposta do Alpha: {alpha_output}\n"
                f"Crítica do Beta: {beta_output}\n"
                f"Parecer e Votos do Conselho de Jurados:\n{council_text_block}\n"
                "Sintetize a rodada considerando o debate entre Alpha e Beta e o parecer do Conselho."
            )
            print(f"⚖️  [Gamma - {GEMINI_MODEL}] Sintetizando debate e votos do Conselho...")
            gamma_output = query_gemini(client, gamma_prompt, gamma_round_system)

            round_ui = (
                f"\n---\n"
                f"### 🔄 Rodada {round_num} de {TOTAL_ROUNDS}: Debate Estratégico com Arbitragem\n\n"
                f"**[Agent Alpha - The Architect ({DEFAULT_ALPHA_MODEL})]**\n> {alpha_output}\n\n"
                f"**[Agent Beta - The Adversary ({DEFAULT_BETA_MODEL})]**\n> {beta_output}\n\n"
                f"**🏛️ [Conselho Consultivo de Arbitragem - Votação dos Modelos Locais]**\n"
                f"{council_text_block}\n"
                f"**[Síntese do Orquestrador - Agent Gamma]**\n{gamma_output}\n\n"
                f"*(Aguardando a decisão do utilizador para avançar para a próxima rodada...)*\n"
                f"---"
            )
            print(round_ui)
            append_to_log(LOG_FILE_COMPLETE, round_ui)

            if round_num in KEY_ROUNDS:
                save_key_round_summary(round_num, round_ui)

            user_choice = input("\n👉 Sua Decisão / Diretriz: ").strip()
            while not user_choice:
                user_choice = input("Por favor, digite uma opção válida (A, B ou diretriz C): ").strip()

            current_steering = f"Human Commander decision for Round {round_num + 1}: {user_choice}"

        else:
            print("\n🏁 [RODADA 20 ATINGIDA] Gerando Plano Estratégico Consolidado final...")
            final_prompt = (
                f"Tema: {theme}\nContexto: {context}\n"
                f"Histórico Completo das 20 Rodadas:\n" + "\n".join(history_context) + "\n\n"
                f"Última Proposta Alpha: {alpha_output}\n"
                f"Última Crítica Beta: {beta_output}\n\n"
                "Elabore a Decisão Final e Plano Estratégico Consolidado completo considerando as contribuições do Conselho."
            )
            final_plan = query_gemini(client, final_prompt, gamma_final_system)

            final_ui = (
                f"\n---\n"
                f"### 🏆 Rodada 20 de {TOTAL_ROUNDS}: Decisão Final e Plano Estratégico Consolidado\n\n"
                f"**[Agent Alpha - The Architect ({DEFAULT_ALPHA_MODEL})]**\n> {alpha_output}\n\n"
                f"**[Agent Beta - The Adversary ({DEFAULT_BETA_MODEL})]**\n> {beta_output}\n\n"
                f"**[Plano Estratégico Consolidado - Agent Gamma ({GEMINI_MODEL})]**\n\n"
                f"{final_plan}\n"
                f"---"
            )
            print(final_ui)
            append_to_log(LOG_FILE_COMPLETE, final_ui)
            save_key_round_summary(20, final_ui)
            print("\n✅ Simulação de 20 rodadas finalizada com sucesso. Logs e resumos salvos.")


if __name__ == "__main__":
    main()
