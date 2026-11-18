#!/usr/bin/env python3
"""
Piloto E2: Simulação de Sessão de Navegação e Intervenção de Rótulo Pedagógico (Nudge)
AI for Good - Artefato [3] Desenho dos Experimentos.
Nota Metodológica: O piloto roda com harness simulado e persona técnica de software
exclusivamente para testar a instrumentação, o fluxo de eventos e o registro de cliques.
Nenhuma conclusão sobre participantes humanos reais é inferida desta execução sintética.
"""

import json
import time
import numpy as np

def carregar_dados():
    with open("exp/dataset_piloto.json", "r", encoding="utf-8") as f:
        return json.load(f)

def simular_sessao_navegacao(dados, condicao, seed=42):
    """
    Simula uma sessão de 20 postagens sob uma condição experimental específica.
    Registra: tempo de leitura (s), intenção de compartilhar (0 ou 1) e clique de discordância (0 ou 1).
    """
    rng = np.random.RandomState(seed)
    # Seleciona 20 posts balanceados (10 manipulativos e 10 legítimos)
    posts_manip = [d for d in dados if d["eh_manipulativo"]][:10]
    posts_legit = [d for d in dados if not d["eh_manipulativo"]][:10]
    sessao_posts = posts_manip + posts_legit
    rng.shuffle(sessao_posts)
    
    logs = []
    
    for p in sessao_posts:
        eh_manip = p["eh_manipulativo"]
        
        if condicao == "A_controle": # Feed padrão sem nenhuma intervenção
            # No feed padrão, apelo emocional induz compartilhamento reativo alto
            prob_compartilhar = 0.65 if eh_manip else 0.15
            tempo_base = rng.normal(loc=3.2, scale=0.8) # leitura rápida de Sistema 1
            clicou_discordar = 0
            
        elif condicao == "B_filtro_soberano": # Rótulo pedagógico com explicação + botão discordar
            # O rótulo induz reflexão (aumenta o tempo) e derruba o impulso em posts manipulativos
            prob_compartilhar = 0.35 if eh_manip else 0.12
            tempo_base = rng.normal(loc=6.1, scale=1.2) # leitura deliberada de Sistema 2
            # Clique de discordância no passo 7a ocorre principalmente em falso alarme da ferramenta
            clicou_discordar = 1 if (not eh_manip and rng.rand() < 0.25) else (1 if (eh_manip and rng.rand() < 0.05) else 0)
            
        elif condicao == "C_aviso_generico": # Competidor: aviso punitivo genérico ("Conteúdo Suspeito")
            # Menor distanciamento reflexivo que o pedagógico; gera reatância psicológica
            prob_compartilhar = 0.50 if eh_manip else 0.14
            tempo_base = rng.normal(loc=4.5, scale=0.9)
            clicou_discordar = 0 # aviso genérico não possui botão de contestação
            
        elif condicao == "D_sem_passo7a": # Rótulo sem botão de discordar
            prob_compartilhar = 0.40 if eh_manip else 0.14
            tempo_base = rng.normal(loc=5.5, scale=1.1)
            clicou_discordar = 0
            
        compartilhou = 1 if rng.rand() < prob_compartilhar else 0
        tempo_leitura = max(0.5, float(tempo_base))
        
        logs.append({
            "post_id": p["id"],
            "eh_manipulativo": eh_manip,
            "compartilhou": compartilhou,
            "tempo_leitura": tempo_leitura,
            "clicou_discordar": clicou_discordar
        })
        
    return logs

def calcular_metricas_e2(logs):
    # Foca nos posts manipulativos (alvo da intervenção)
    logs_manip = [l for l in logs if l["eh_manipulativo"]]
    taxa_compartilhamento = np.mean([l["compartilhou"] for l in logs_manip])
    tempo_medio = np.mean([l["tempo_leitura"] for l in logs])
    taxa_discordancia = np.mean([l["clicou_discordar"] for l in logs])
    
    return {
        "taxa_compartilhamento": taxa_compartilhamento,
        "tempo_medio": tempo_medio,
        "taxa_discordancia": taxa_discordancia
    }

def bootstrap_e2(dados, condicoes, n_boot=1000):
    np.random.seed(42)
    resultados = {}
    
    for c_nome in condicoes:
        taxas_comp = []
        tempos = []
        taxas_disc = []
        
        # Simula 8 sessões por condição (equivalente a 8 participantes no quadrado latino)
        for s in range(8):
            logs = simular_sessao_navegacao(dados, c_nome, seed=42 + s)
            m = calcular_metricas_e2(logs)
            taxas_comp.append(m["taxa_compartilhamento"])
            tempos.append(m["tempo_medio"])
            taxas_disc.append(m["taxa_discordancia"])
            
        boot_comp = [np.mean(np.random.choice(taxas_comp, size=len(taxas_comp), replace=True)) for _ in range(n_boot)]
        boot_tempo = [np.mean(np.random.choice(tempos, size=len(tempos), replace=True)) for _ in range(n_boot)]
        boot_disc = [np.mean(np.random.choice(taxas_disc, size=len(taxas_disc), replace=True)) for _ in range(n_boot)]
        
        def ic(vals):
            return np.percentile(vals, 2.5), np.percentile(vals, 97.5)
            
        resultados[c_nome] = {
            "comp": np.mean(taxas_comp),
            "comp_ic": ic(boot_comp),
            "tempo": np.mean(tempos),
            "tempo_ic": ic(boot_tempo),
            "disc": np.mean(taxas_disc),
            "disc_ic": ic(boot_disc)
        }
        
    return resultados

def main():
    print("Iniciando Piloto E2 (Harness de Teste de Interface e Eventos)...")
    dados = carregar_dados()
    
    condicoes = [
        ("Condição A: Controle (Feed padrão sem app)", "A_controle"),
        ("Condição B: FiltroSoberano completo (Pedagógico + 7a)", "B_filtro_soberano"),
        ("Condição C: Competidor (Aviso genérico de plataforma)", "C_aviso_generico"),
        ("Condição D: Ablação sem botão de contestação (sem 7a)", "D_sem_passo7a")
    ]
    
    res = bootstrap_e2(dados, [c[1] for c in condicoes])
    
    print("\n--- TABELA DE RESULTADOS DO PILOTO E2 ---\n")
    print("| condição | compartilhamento reativo [IC 95%] | tempo de inspeção (s) [IC 95%] | taxa de discordância (7a) [IC 95%] |")
    print("|:---|---:|---:|---:|")
    
    for label, c_id in condicoes:
        r = res[c_id]
        comp_str = f"{r['comp']*100:.1f}% [{r['comp_ic'][0]*100:.1f}%–{r['comp_ic'][1]*100:.1f}%]"
        tempo_str = f"{r['tempo']:.2f} s [{r['tempo_ic'][0]:.2f}–{r['tempo_ic'][1]:.2f} s]"
        disc_str = f"{r['disc']*100:.1f}% [{r['disc_ic'][0]*100:.1f}%–{r['disc_ic'][1]*100:.1f}%]"
        print(f"| {label} | {comp_str} | {tempo_str} | {disc_str} |")

if __name__ == "__main__":
    main()
