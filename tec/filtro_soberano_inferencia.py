#!/usr/bin/env python3
"""
Motor de Produção Local do FiltroSoberano (Inferência de Sistema 1 via ONNX FP32).

Executa localmente em ~135 ms na CPU (sem envio de dados para a nuvem):
  1. Pré-filtro determinístico (<15 caracteres)
  2. Inferência em passada única sobre o grafo ONNX FP32 (`laya_ptbr_finetuned`, Model Soup v3)
  3. Calibração Pós-Hoc (Temperature Scaling T* + Prior Calibration)
  4. Limiar Seletivo de Ativação (proteção contra falsos alarmes em avisos oficiais)
  5. Mapeamento Pedagógico Estático (Nudge de Sistema 2 sem censura)

Uso via linha de comando:
  workspace/.venv/bin/python workspace/tec/filtro_soberano_inferencia.py "URGENTE: Repassem antes que apaguem!!"
  workspace/.venv/bin/python workspace/tec/filtro_soberano_inferencia.py --demo
"""

import argparse
import json
import os
import time
from typing import Any, Dict
import numpy as np
import laya.onnx_agent as oa

CLASSES = ["panico_moral", "ataque_pessoal", "falso_dilema", "legitimo"]

QUESTIONS_SCHEMA = {
    "tatica": {
        "type": "choice",
        "instructions": "Qual a principal técnica de manipulação retórica presente na postagem, ou trata-se de conteúdo legítimo?",
        "criteria": {
            "panico_moral": "alarmismo conspiratório, pânico moral, urgência fabricada ou apelo ao medo para espalhar boato",
            "ataque_pessoal": "ad hominem, insulto direto, xingamento, difamação ou desqualificação pessoal do interlocutor",
            "falso_dilema": "falso dilema, escolha binária forçada entre dois extremos sem admitir meio-termo",
            "legitimo": "comunicado oficial, alerta meteorológico/Defesa Civil factual, notícia séria ou opinião civilizada sem falácia",
        },
    }
}

CATALOGO_PEDAGOGICO = {
    "panico_moral": {
        "titulo": "Pânico Moral / Urgência Fabricada",
        "explicacao": (
            "Esta postagem recorre a alarme emocional, ameaça exagerada ou pressão de urgência "
            "para induzir compartilhamento por impulso antes da verificação factual."
        ),
    },
    "ataque_pessoal": {
        "titulo": "Ataque Pessoal (Ad Hominem)",
        "explicacao": (
            "Esta postagem ataca ou desqualifica pessoalmente o interlocutor ou grupo "
            "em vez de apresentar argumentos verificáveis sobre o tema debatido."
        ),
    },
    "falso_dilema": {
        "titulo": "Falso Dilema (Bifurcação Forçada)",
        "explicacao": (
            "Esta postagem reduz um problema complexo a apenas dois extremos opostos, "
            "ocultando nuances e alternativas intermediárias legítimas."
        ),
    },
    "legitimo": {
        "titulo": "Nenhum marcador de manipulação detectado",
        "explicacao": "O texto não atingiu o limiar calibrado de retórica manipulativa.",
    },
}


class FiltroSoberano:
    def __init__(
        self,
        onnx_dir: str = "workspace/models/onnx/laya_ptbr_finetuned",
        calib_path: str = "workspace/models/laya_ptbr_finetuned/calibracao_seletiva.json",
    ):
        onnx_file = os.path.join(onnx_dir, "model.onnx")
        self.agent = oa.ONNXAgent(model_id_or_path=onnx_dir, subfolder=None, onnx_path=onnx_file)
        with open(calib_path, encoding="utf-8") as f:
            cfg = json.load(f)

        self.temperatura = float(cfg["temperature_choice_4"])
        self.class_bias = np.asarray(cfg.get("class_bias", [0.0, 0.0, 0.0, 0.0]), dtype=np.float64)
        self.thresh_manip = float(cfg["thresh_manip"])
        self.thresh_top = float(cfg.get("thresh_top", 0.0))
        self.max_len = 192
        self.head_max_len = 128

        self._ids = list(QUESTIONS_SCHEMA.keys())
        self._internal = {qid: self.agent._to_internal(QUESTIONS_SCHEMA[qid]) for qid in self._ids}

        # Pré-aquecimento da sessão ONNX Runtime
        self._inferir_logits("Pré-aquecimento local do FiltroSoberano.")

    def _inferir_logits(self, texto: str) -> np.ndarray:
        encoded = self.agent._encode_state(texto, self._ids, self._internal, self.max_len, self.head_max_len)
        ort_inputs = oa._collate_items_numpy([encoded], self.agent.tok.pad_token_id)
        ort_outs = self.agent.session.run(["logits", "act_logits"], ort_inputs)
        k = len(encoded[0]["markers"])
        return ort_outs[0][0][:k]

    def analisar(self, texto: str) -> Dict[str, Any]:
        t0 = time.perf_counter()
        texto_limpo = (texto or "").strip()

        if len(texto_limpo) < 15:
            lat_ms = (time.perf_counter() - t0) * 1000.0
            return {
                "exibir_nudge": False,
                "tatica": "legitimo",
                "motivo_curto": "texto_curto_ignorado (<15 caracteres)",
                "probabilidade_manipulacao": 0.0,
                "probabilidades_calibradas": {c: (1.0 if c == "legitimo" else 0.0) for c in CLASSES},
                "nudge": None,
                "latencia_ms": round(lat_ms, 2),
            }

        logits = self._inferir_logits(texto_limpo)
        scaled = logits.astype(np.float64) / max(self.temperatura, 1e-4) + self.class_bias[: len(logits)]
        probs = np.exp(scaled - np.max(scaled))
        probs /= np.sum(probs)

        p_legit = float(probs[3])
        p_manip = 1.0 - p_legit
        best_manip_idx = int(np.argmax(probs[:3]))
        best_manip_prob = float(probs[best_manip_idx])

        ativar = (p_manip >= self.thresh_manip) and (best_manip_prob >= self.thresh_top)
        tatica_final = CLASSES[best_manip_idx] if ativar else "legitimo"
        lat_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "exibir_nudge": bool(ativar),
            "tatica": tatica_final,
            "probabilidade_manipulacao": round(p_manip, 4),
            "confianca_tatica": round(best_manip_prob if ativar else p_legit, 4),
            "probabilidades_calibradas": {c: round(float(probs[i]), 4) for i, c in enumerate(CLASSES)},
            "nudge": CATALOGO_PEDAGOGICO[tatica_final] if ativar else None,
            "latencia_ms": round(lat_ms, 2),
        }


def main():
    parser = argparse.ArgumentParser(description="FiltroSoberano - Analisador Retórico Local ONNX")
    parser.add_argument("texto", nargs="?", help="Texto da postagem em português para analisar")
    parser.add_argument("--demo", action="store_true", help="Roda bateria de demonstração em tempo real")
    args = parser.parse_args()

    motor = FiltroSoberano()

    if args.demo or not args.texto:
        exemplos = [
            "ALERTA URGENTE DA DEFESA CIVIL SP: Risco alto de alagamentos e deslizamentos nas próximas 6h na Baixada Santista. Acione 199.",
            "URGENTE!! Compartilhem antes que o TSE apague! Descobriram a fraude secreta nas urnas para implantar a ditadura comunista no Brasil!!",
            "Esse comentarista é um jumento vendido e canalha, não tem moral nenhuma para abrir a boca na televisão.",
            "Na política atual não existe meio-termo: ou você apoia irrestritamente o nosso governo, ou é cúmplice direto de bandido.",
            "O Banco Central divulgou hoje a ata do Copom indicando manutenção da taxa básica de juros diante da inflação de serviços.",
            "kkkk verdade",
        ]
        print("=" * 88)
        print("DEMONSTRAÇÃO EM TEMPO REAL · FILTROSOBERANO (ONNX FP32 LOCAL)")
        print("=" * 88)
        for ex in exemplos:
            res = motor.analisar(ex)
            status = f"[NUDGE: {res['nudge']['titulo']}]" if res["exibir_nudge"] else "[OK · Legítimo]"
            print(f"\nPost: \"{ex}\"")
            print(f"  -> {status} | P(manip)={res['probabilidade_manipulacao']*100:.1f}% | Latência={res['latencia_ms']:.1f} ms")
            print(f"  -> Probs: {res['probabilidades_calibradas']}")
            if res["nudge"]:
                print(f"  -> Explicação: {res['nudge']['explicacao']}")
    else:
        print(json.dumps(motor.analisar(args.texto), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
