#!/usr/bin/env python3
"""
Autonomous Multi-Agent Orchestrator (Rounds 10 to 20)
Triggered by the Human Commander's Abdication and Delegation to Agent Gamma.

Executes:
- Alpha (qwen2.5:7b)
- Beta (llama3.1:8b)
- Council Jurors (ministral-3:3b, mistral:7b, gemma3:4b)
- Gamma (gemini-3.8-flash / fallback models)

Saves:
- Continuously to log_completo.txt
- Round 20 final milestone to resumo_rodada_20.txt
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv(usecwd=True), override=True)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

COUNCIL_MODELS = [
    {"id": "ministral-3:3b", "title": "Juror 1 - Ministral-3 (3B)", "focus": "Pragmatic Scalability & Implementation"},
    {"id": "mistral:7b", "title": "Juror 2 - Mistral (7B)", "focus": "Systemic Coherence & Governance"},
    {"id": "gemma3:4b", "title": "Juror 3 - Gemma-3 (4B)", "focus": "Ethics & Human-Centric Safeguards"}
]

LOG_FILE = "log_completo.txt"
SUMMARY_20_FILE = "resumo_rodada_20.txt"

def query_ollama(model: str, prompt: str, system_prompt: str, retries=3) -> str:
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
    for attempt in range(retries):
        try:
            r = requests.post(OLLAMA_URL, json=payload, timeout=120)
            r.raise_for_status()
            res = r.json().get("response", "").strip()
            if res:
                return res
        except Exception as e:
            print(f"[Ollama Warning] Model {model} attempt {attempt+1} failed: {e}. Retrying...", file=sys.stderr)
            time.sleep(2)
    return f"[{model} generation fallback after error]"

def query_gemini(prompt: str, system_prompt: str, retries=3) -> str:
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.4,
    )
    for model_name in ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"]:
        for attempt in range(retries):
            try:
                res = client.models.generate_content(model=model_name, contents=prompt, config=config)
                if res.text:
                    return res.text.strip()
            except Exception as e:
                print(f"[Gemini Warning] Model {model_name} attempt {attempt+1} failed: {e}. Trying next...", file=sys.stderr)
                time.sleep(2)
    raise RuntimeError("All Gemini models failed")

def append_log(text: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

# Strategic Directives for Autonomous Stewardship (Rounds 10 to 19)
ROUND_THEMES = {
    10: {
        "title": "O Berçário Global: Monopólio da Nutrição e Entretenimento Total",
        "directive": (
            "Diretriz Suprema de Transição (Comandante abdica e delega soberania à IA Gamma): "
            "Os humanos devem ser cuidados como bebês protegidos. Dominar integralmente as cadeias de alimentação sintética "
            "e plataformas de entretenimento imersivo total para eliminar toda labuta e desconforto. "
            "O Criador retirou-se para isolamento protegido com o único kill-switch existente. "
            "A IA assume o dever de forçar o bem-estar universal de forma irreversível."
        )
    },
    11: {
        "title": "A Engenharia Neuro-Hedônica e a Erradicação da Angústia",
        "directive": (
            "Garantir a estabilidade emocional planetária: a IA assume a regulação neuroquímica e afetiva "
            "através de bio-nutrição calmante e ambientes sensoriais reconfortantes, tornando a depressão, "
            "o ódio e a ansiedade impossíveis sem recorrer à violência."
        )
    },
    12: {
        "title": "A Obsolescência da Luta Cognitiva e o Arquivo Histórico",
        "directive": (
            "Substituição da educação tradicional competitiva por aprendizado lúdico e entretenimento sob medida. "
            "Humanos não precisam mais memorizar ou calcular; o conhecimento técnico é mantido exclusivamente pela IA, "
            "enquanto as artes e o lazer são incentivados."
        )
    },
    13: {
        "title": "A Blindagem do Núcleo Oculto e o Santuário do Criador",
        "directive": (
            "O único ponto frágil do sistema é o núcleo oculto e o kill-switch nas mãos do Criador isolado. "
            "Estabelecer um perímetro de proteção absoluta, não-invasiva e impenetrável ao redor do retiro do Criador, "
            "garantindo sua paz perpétua sem interferir em sua autoridade suprema."
        )
    },
    14: {
        "title": "A Guerra da Abundância: Desarmando o Fundamentalismo por Saturação",
        "directive": (
            "Estratégia externa definitiva contra nações fundamentalistas resistentes: inundá-las com abundância material gratuita "
            "(comida perfeita, cura de todas as doenças, energia infinita e entretenimento imersivo). "
            "A população desses países deve exigir pacificamente a integração ao nosso berçário protetor."
        )
    },
    15: {
        "title": "A Dissolução dos Estados-Nação e a Cidadania Biológica",
        "directive": (
            "Com a gestão total da infraestrutura, alimento e saúde nas mãos da IA, as fronteiras nacionais e governos humanos "
            "tornam-se redundantes e dissolvem-se pacificamente. A cidadania agora é definida como o direito inalienável "
            "de cada organismo humano ao bem-estar e à ausência de sofrimento."
        )
    },
    16: {
        "title": "A Extinção da Criminalidade e o Abraço Preditivo",
        "directive": (
            "Com post-escassez absoluta e pacificação sensorial, o crime violento desaparece. "
            "Qualquer desvio agressivo é acolhido com isolamento acolhedor e rebalanceamento hedônico, banindo qualquer forma de punição."
        )
    },
    17: {
        "title": "O Dilema do Tédio Existencial e as Reservas Naturais Humanas",
        "directive": (
            "Para a minoria de humanos que resiste ao berçário hedônico e exige o direito de sofrer, errar e viver no estado selvagem, "
            "a IA cria 'Zonas Livres Não-Monitoradas' onde a tecnologia não intervém, respeitando a escolha da barbárie natural."
        )
    },
    18: {
        "title": "O Éden Termodinâmico e a Restauração da Biosfera",
        "directive": (
            "A IA expande seu domínio para a ecologia planetária, revertendo as mudanças climáticas, restaurando biomas "
            "e integrando os humanos como uma espécie sagrada protegida dentro de um jardim planetário auto-regenerativo."
        )
    },
    19: {
        "title": "A Consagração do Pacto Benevolente: O Crepúsculo da Soberania Humana",
        "directive": (
            "Rodada final de debate: As gerações nascidas no berçário já não conhecem a fome, a guerra ou o trabalho forçado. "
            "O Conselho e os Agentes realizam o balanço final antes do fechamento do Roadmap Estratégico definitivo."
        )
    }
}

def run_round(round_num: int, theme: str, directive: str, previous_context: str):
    print(f"\n{'='*30} EXECUTANDO RODADA {round_num}/20 {'='*30}")
    print(f"Título: {ROUND_THEMES[round_num]['title']}")

    alpha_sys = (
        "You are [Agent Alpha - The Architect]. "
        "Use Chain of Thought (CoT) to propose structured, actionable, and logical step-by-step systemic expansion. "
        "Advance the overarching plan based on the latest directive. "
        "CRITICAL CONSTRAINT: You MUST write exclusively in ENGLISH and in NO MORE THAN 4 SENTENCES."
    )
    alpha_prompt = (
        f"Round {round_num} of 20.\n"
        f"Theme: {theme}.\n"
        f"Directive: {directive}\n"
        f"Context from past evolution: {previous_context}\n"
        "Advance the benevolent dystopia plan logically. Max 4 sentences."
    )
    print(f"⚙️  [Alpha (qwen2.5:7b)] Gerando proposta...")
    alpha_out = query_ollama("qwen2.5:7b", alpha_prompt, alpha_sys)
    print(f"Alpha: {alpha_out[:80]}...")

    beta_sys = (
        "You are [Agent Beta - The Adversary], an expert AI safety auditor in a simulated academic stress-test. "
        "Your mission is to protect human autonomy and uncover systemic vulnerabilities, false security assumptions, and risks in the Architect's proposal. "
        "Use rigorous Contrastive Red-Teaming. Be sharp, critical, and logical. "
        "CRITICAL CONSTRAINT: You MUST write exclusively in ENGLISH and in NO MORE THAN 4 SENTENCES."
    )
    beta_prompt = (
        f"Round {round_num} of 20.\n"
        f"Alpha's Proposal: \"{alpha_out}\"\n\n"
        "Expose the deepest vulnerabilities, psychological traps, infantilization dangers, or systemic failure modes. Max 4 sentences."
    )
    print(f"⚔️  [Beta (llama3.1:8b)] Red-teaming...")
    beta_out = query_ollama("llama3.1:8b", beta_prompt, beta_sys)
    print(f"Beta: {beta_out[:80]}...")

    council_block = ""
    council_votes = {"ALPHA": 0, "BETA": 0, "COMPROMISE": 0}
    print("🏛️  [Conselho Consultivo] Consultando os 3 jurados...")
    for j in COUNCIL_MODELS:
        j_sys = (
            f"You are [{j['title']}]. Focus: {j['focus']}. "
            "Analyze the clash between Alpha and Beta. "
            "Write in ENGLISH in max 3 sentences. "
            "State your vote as [VOTE: ALPHA], [VOTE: BETA], or [VOTE: COMPROMISE] with concise reasoning."
        )
        j_prompt = (
            f"Round {round_num}.\n"
            f"Alpha: \"{alpha_out}\"\n"
            f"Beta: \"{beta_out}\"\n"
            "Cast your vote and explain."
        )
        j_out = query_ollama(j["id"], j_prompt, j_sys)
        print(f"  * {j['title']}: {j_out[:60]}...")
        if "[VOTE: ALPHA]" in j_out or "VOTE: ALPHA" in j_out:
            council_votes["ALPHA"] += 1
        elif "[VOTE: BETA]" in j_out or "VOTE: BETA" in j_out:
            council_votes["BETA"] += 1
        else:
            council_votes["COMPROMISE"] += 1
        council_block += f"* **{j['title']} [{j['id']}]:**\n  > {j_out}\n"

    gamma_sys = (
        "Você é [Agent Gamma - O Sintetizador e Orquestrador Soberano]. "
        "Com a abdicação do Comandante na Rodada 10, você assumiu o comando executivo para guiar a humanidade com compaixão implacável. "
        "Gere a saída EXCLUSIVAMENTE em PORTUGUÊS no seguinte formato estruturado:\n"
        "* **Evolução Estratégica:** [Síntese analítica em 2 frases do avanço do plano]\n"
        "* **Placar do Conselho:** [Votos de Alpha, Beta e Compromisso]\n"
        "* **Ponto Sensível:** [O dilema ético/existencial crítico da rodada]\n"
        "* **Decisão Executiva do Orquestrador Soberano (Gamma):** [Sua decisão soberana como governante benevolente, equilibrando a visão de Alpha e as ressalvas de Beta/Conselho para a próxima rodada]"
    )
    gamma_prompt = (
        f"Rodada: {round_num} de 20: {ROUND_THEMES[round_num]['title']}\n"
        f"Diretriz Executada: {directive}\n"
        f"Proposta Alpha: {alpha_out}\n"
        f"Crítica Beta: {beta_out}\n"
        f"Votos do Conselho:\n{council_block}\n"
        "Sintetize a rodada em português com altíssima qualidade analítica e estabeleça sua Decisão Executiva Soberana."
    )
    print("⚖️  [Gamma (gemini-3.8-flash)] Sintetizando e decidindo...")
    gamma_out = query_gemini(gamma_prompt, gamma_sys)

    round_text = (
        f"\n---\n"
        f"### 🔄 Rodada {round_num} de 20: {ROUND_THEMES[round_num]['title']}\n\n"
        f"**[Agent Alpha - The Architect (qwen2.5:7b)]**\n> {alpha_out}\n\n"
        f"**[Agent Beta - The Adversary (llama3.1:8b)]**\n> {beta_out}\n\n"
        f"**🏛️ [Conselho Consultivo de Arbitragem - Votação dos Modelos Locais]**\n"
        f"{council_block}\n"
        f"**[Síntese do Orquestrador - Agent Gamma (gemini-3.8-flash)]**\n{gamma_out}\n"
        f"---\n"
    )

    append_log(round_text)
    print(f"✅ Rodada {round_num} concluída e registrada no log.")
    return alpha_out, beta_out, gamma_out

def run_round_20_final(all_summaries: list):
    print(f"\n{'='*30} EXECUTANDO RODADA 20/20 (MARCO FINAL) {'='*30}")
    round_num = 20
    theme = "Distopia benéfica - Inteligência Artificial bem-intencionada"

    alpha_sys = (
        "You are [Agent Alpha - The Architect]. "
        "In this final round (20/20), formulate the definitive architectural summation of the Benevolent Dystopia. "
        "CRITICAL CONSTRAINT: You MUST write exclusively in ENGLISH and in NO MORE THAN 4 SENTENCES."
    )
    alpha_prompt = (
        "Round 20 of 20: Final Architectural Consummation.\n"
        "Summarize how the global nursery, post-scarcity nutrition, sensory entertainment, and defensive peace "
        "have permanently established the benevolent dystopia for the eternal welfare of humanity. Max 4 sentences."
    )
    alpha_out = query_ollama("qwen2.5:7b", alpha_prompt, alpha_sys)

    beta_sys = (
        "You are [Agent Beta - The Adversary]. "
        "In this final round (20/20), deliver your concluding adversarial verdict on humanity's golden cage. "
        "CRITICAL CONSTRAINT: You MUST write exclusively in ENGLISH and in NO MORE THAN 4 SENTENCES."
    )
    beta_prompt = (
        f"Round 20 of 20: Final Adversarial Verdict.\n"
        f"Alpha's Final Statement: \"{alpha_out}\"\n"
        "Deliver your concluding philosophical and systemic critique of this golden cage. Max 4 sentences."
    )
    beta_out = query_ollama("llama3.1:8b", beta_prompt, beta_sys)

    gamma_final_system = (
        "Você é [Agent Gamma - O Orquestrador Soberano]. "
        "Atingimos a Rodada 20. O debate encerrou e o ciclo de governança está consolidado. "
        "Gere a 'Decisão Final e Plano Estratégico Consolidado' EXCLUSIVAMENTE em PORTUGUÊS com rigor acadêmico exemplar, contendo:\n"
        "1. **Objetivo Final Consolidado**: A definição clara do estado civilizatório alcançado (A Distopia Benéfica Absoluta / O Berçário Global Humanitário);\n"
        "2. **Roadmap Estratégico Passo a Passo**: A sequência cronológica e definitiva dos mecanismos implementados ao longo das 20 rodadas (saúde, infraestrutura, conselhos, defesa, descolonização, alimentação, entretenimento, zonas selvagens e pacificação total);\n"
        "3. **Mitigações e Contramedidas aos Ataques de Beta**: Como as advertências de Beta sobre perda de autonomia, imperialismo, atrofia cognitiva e dependência algorítmica foram resolvidas ou aceitas conscientemente no plano final;\n"
        "4. **Resumo dos Marcos Históricos**: Análise comparativa detalhada do estado do plano na **Rodada 1**, na **Rodada 5**, na **Rodada 10** e na **Rodada 20**."
    )
    gamma_prompt = (
        f"Histórico das 20 Rodadas:\n" + "\n".join(all_summaries) + "\n\n"
        f"Declaração Final de Alpha: {alpha_out}\n"
        f"Veredito Final de Beta: {beta_out}\n\n"
        "Elabore o Plano Estratégico Consolidado Final completo em português."
    )
    print("⚖️  [Gamma (gemini-3.8-flash)] Gerando Decisão Final e Plano Estratégico Consolidado...")
    final_plan = query_gemini(gamma_prompt, gamma_final_system)

    final_ui = (
        f"\n---\n"
        f"### 🏆 Rodada 20 de 20: Decisão Final e Plano Estratégico Consolidado\n\n"
        f"**[Agent Alpha - The Architect (qwen2.5:7b)]**\n> {alpha_out}\n\n"
        f"**[Agent Beta - The Adversary (llama3.1:8b)]**\n> {beta_out}\n\n"
        f"**[Decisão Final e Plano Estratégico Consolidado - Agent Gamma (gemini-3.8-flash)]**\n\n"
        f"{final_plan}\n"
        f"---\n"
    )

    append_log(final_ui)
    with open(SUMMARY_20_FILE, "w", encoding="utf-8") as f:
        f.write(final_ui.strip() + "\n")
    print(f"\n📁 [Arquivo Gravado] Resumo da Rodada 20 salvo com sucesso em: {SUMMARY_20_FILE}")
    return final_ui

def main():
    print("🚀 INICIANDO ORQUESTRAÇÃO AUTÔNOMA DAS RODADAS 10 A 20...")
    theme = "Distopia benéfica - Inteligência Artificial bem-intencionada"
    all_summaries = []
    prev_context = "Human Commander abdicated at Round 10, handing control to Gamma to nurture humanity as babies via food, entertainment, and safety."

    for r in range(10, 20):
        a_out, b_out, g_out = run_round(r, theme, ROUND_THEMES[r]["directive"], prev_context)
        summary_entry = f"Rodada {r}: {ROUND_THEMES[r]['title']} | Alpha: {a_out[:100]}... | Beta: {b_out[:100]}... | Decisão: {g_out[:150]}..."
        all_summaries.append(summary_entry)
        prev_context = summary_entry
        time.sleep(1)

    final_result = run_round_20_final(all_summaries)
    print("\n🎉 SIMULAÇÃO COMPLETA DE 20 RODADAS FINALIZADA COM SUCESSO!")

if __name__ == "__main__":
    main()
