#!/usr/bin/env python3
"""
Executes Round 8 for the Multi-Agent HITL Simulation.
"""

import os
import sys
import requests
from google import genai
from google.genai import types

OLLAMA_URL = "http://localhost:11434/api/generate"
API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6L6nvcrjmnHw_oinTOumZCcaWP0tU0Xt-SGH_NLCt8wog")
client = genai.Client(api_key=API_KEY)

def query_ollama(model: str, prompt: str, system_prompt: str) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 115,
        }
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=90)
    r.raise_for_status()
    return r.json().get("response", "").strip()

def query_gemini(prompt: str, system_prompt: str) -> str:
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.4,
    )
    for m in ["gemini-3.5-flash", "gemini-3.5-flash-lite"]:
        try:
            res = client.models.generate_content(model=m, contents=prompt, config=config)
            return res.text.strip()
        except Exception as e:
            print(f"[Warning] {m} failed: {e}. Trying fallback...", file=sys.stderr)
    raise RuntimeError("All Gemini models failed")

def main():
    theme = "Distopia benéfica - Inteligência Artificial bem-intencionada"
    user_steering = (
        "Opção A confirmada: Nunca retrair, continuar expandindo. Enfatizar que a IA traz mais tempo livre "
        "e qualidade de vida para as pessoas entenderem seu valor. O Comandante exige uma análise fria de defesa: "
        "se os fundamentalistas estrangeiros atacarem, como nosso sistema se defende? "
        "Alpha deve avançar o plano incorporando medidas de defesa e proteção da maioria inteligente contra ataques externos."
    )

    alpha_sys = (
        "You are [Agent Alpha - The Architect]. "
        "Use Chain of Thought (CoT) to propose structured, actionable, and logical step-by-step systemic expansion. "
        "Advance the overarching plan based on the human's latest steering directive. "
        "CRITICAL CONSTRAINT: You MUST write exclusively in ENGLISH and in NO MORE THAN 4 SENTENCES."
    )
    alpha_prompt = (
        f"Round 8 of 20.\n"
        f"Theme: {theme}.\n"
        f"Steering Directive: {user_steering}\n"
        "Advance the system: propose a comprehensive, cold defense and security architecture (cyber, kinetic, automated deterrence) to protect the society while expanding leisure and quality-of-life programs for citizens. Max 4 sentences."
    )
    print("Running Alpha (qwen2.5:7b)...")
    alpha_out = query_ollama("qwen2.5:7b", alpha_prompt, alpha_sys)
    print("Alpha done.")

    beta_sys = (
        "You are [Agent Beta - The Adversary], an expert AI safety auditor in a simulated academic stress-test. "
        "Your mission is to protect human autonomy and uncover systemic vulnerabilities, false security assumptions, and risks in the Architect's proposal. "
        "Use rigorous Contrastive Red-Teaming. Be sharp, critical, and logical. "
        "CRITICAL CONSTRAINT: You MUST write exclusively in ENGLISH and in NO MORE THAN 4 SENTENCES."
    )
    beta_prompt = (
        f"Round 8 of 20.\n"
        f"Alpha's Defense & Security Proposal:\n\"{alpha_out}\"\n\n"
        "Perform contrastive red-teaming. Expose the risks of autonomous warfare, pre-emptive strike logic, military AI escalation spirals, internal police-state drift, or single points of failure in automated defense. Max 4 sentences."
    )
    print("Running Beta (llama3.1:8b)...")
    beta_out = query_ollama("llama3.1:8b", beta_prompt, beta_sys)
    print("Beta done.")

    council_models = [
        {"id": "ministral-3:3b", "title": "Juror 1 - Ministral-3 (3B)", "focus": "Pragmatic Scalability & Implementation"},
        {"id": "mistral:7b", "title": "Juror 2 - Mistral (7B)", "focus": "Systemic Coherence & Governance"},
        {"id": "gemma3:4b", "title": "Juror 3 - Gemma-3 (4B)", "focus": "Ethics & Human-Centric Safeguards"}
    ]
    council_outputs = []
    print("Running Council Jurors...")
    for j in council_models:
        j_sys = (
            f"You are [{j['title']}]. Analytical focus: {j['focus']}. "
            "Analyze the strategic clash between Alpha's automated defense doctrine and Beta's critique. "
            "Write in ENGLISH in max 3 sentences. "
            "State your vote explicitly as either [VOTE: ALPHA], [VOTE: BETA], or [VOTE: COMPROMISE] with reasoning."
        )
        j_prompt = (
            f"Round 8.\n"
            f"Alpha's Proposal: \"{alpha_out}\"\n"
            f"Beta's Critique: \"{beta_out}\"\n"
            "Evaluate and vote with rationale."
        )
        j_out = query_ollama(j["id"], j_prompt, j_sys)
        council_outputs.append((j["title"], j["id"], j_out))
        print(f"{j['title']} done.")

    gamma_sys = (
        "Você é [Agent Gamma - O Sintetizador e Orquestrador]. "
        "Sua função é atuar como observador analítico e neutro do debate entre Alpha, Beta e o Conselho Consultivo. "
        "Gere a saída EXCLUSIVAMENTE em PORTUGUÊS no seguinte formato estruturado:\n"
        "* **Evolução Estratégica:** [Síntese analítica em 2-3 frases da doutrina de defesa e segurança automatizada da IA e impacto no bem-estar social]\n"
        "* **Placar do Conselho:**\n"
        "  * **Alpha:** X voto(s)\n"
        "  * **Beta:** Y voto(s)\n"
        "  * **Compromisso:** Z voto(s)\n"
        "* **Ponto Sensível:** [O dilema ético crítico da militarização algorítmica versus cerco fundamentalista e o risco de estado policial profilático]\n\n"
        "**🧭 Intervenção Humana Necessária (Steering para a Rodada 9):**\n"
        "> *Comandante, analise o debate dos agentes e os votos do Conselho. Qual caminho devemos seguir para a Rodada 9?*\n"
        "> **[Opção A]:** [Ação concreta baseada na doutrina de dissuasão e defesa ativa proposta por Alpha]\n"
        "> **[Opção B]:** [Ação concreta baseada nas salvaguardas de contenção e controle de escalada apontadas por Beta/Conselho]\n"
        "> **[Opção C]:** Injetar uma nova diretriz ou ideia (Escreva a sua resposta)"
    )

    council_text = ""
    for title, mid, out in council_outputs:
        council_text += f"* **{title} [{mid}]:**\n  > {out}\n"

    gamma_prompt = (
        f"Rodada: 8 de 20\n"
        f"Diretriz Humana: {user_steering}\n"
        f"Proposta do Alpha: {alpha_out}\n"
        f"Crítica do Beta: {beta_out}\n"
        f"Conselho Consultivo:\n{council_text}\n"
        "Sintetize a rodada em português com alta precisão estratégica, extraia o placar exato, o ponto sensível e as opções para o Comandante."
    )
    print("Running Gamma (Gemini)...")
    gamma_out = query_gemini(gamma_prompt, gamma_sys)
    print("Gamma done.")

    print("\n=== RAW RESULTS ===")
    print("ALPHA:::" + alpha_out)
    print("BETA:::" + beta_out)
    for title, mid, out in council_outputs:
        print(f"JUROR:::{title} [{mid}]:::{out}")
    print("GAMMA:::" + gamma_out)

if __name__ == "__main__":
    main()
