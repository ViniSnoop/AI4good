#!/usr/bin/env python3
"""
Avaliação Cega Definitiva (n = 200 postagens reais inéditas) do FiltroSoberano.
Compara rigorosamente, nas mesmas 200 postagens mantidas 100% fora do treino e da calibração:
  1. Linha de Base: Regras Determinísticas / Regex
  2. Laya Multilíngue Zero-Shot (ONNX FP32 sem fine-tuning)
  3. FiltroSoberano Laya PT-BR (RLCD Fine-Tuned ONNX FP32, argmax direto)
  4. FiltroSoberano Completo (RLCD Fine-Tuned ONNX FP32 + Temperature Scaling T* + Limiar Seletivo Calibrado + Regra <15c)
  5. Ablação: Sem Regra de Tamanho Mínimo (<15c)

Reporta:
  - Macro-F1 global e F1 detalhado por classe (panico_moral, ataque_pessoal, falso_dilema, legitimo)
  - Taxa de Falsos Positivos global e especificamente nos Alertas Oficiais (INMET / Defesa Civil)
  - Taxa de Erros Silenciosos (Falsos Negativos)
  - Acurácia Tática Exata
  - Latência Real em milissegundos/segundos na CPU via ONNX Runtime
  - Intervalos de Confiança de 95% (1.000 reamostras de bootstrap)
"""

import json
import os
import re
import time
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


def predizer_regras(texto: str):
    t0 = time.perf_counter()
    t_lower = texto.lower()

    padroes_panico = [
        r"\burgente\b", r"\balerta\b", r"\bconspira[çc]", r"\bapaguem\b",
        r"\bveneno\b", r"\bcaos\b", r"\bperigo\b", r"\bevacue\b",
        r"\brepassem\b", r"\bcompartilhem\b", r"\bgolpe\b", r"\bfraude\b",
    ]
    for p in padroes_panico:
        if re.search(p, t_lower):
            return "panico_moral", True, time.perf_counter() - t0

    padroes_ataque = [
        r"\bburro\b", r"\bincompetente\b", r"\bpalha[çc]o\b", r"\besc[oó]ria\b",
        r"\bvendido\b", r"\bvagabundo\b", r"\bhist[ée]rica\b", r"\bcovarde\b",
        r"\bcanalha\b", r"\bimbecil\b", r"\bsafado\b", r"\blixo\b", r"\bidiota\b",
    ]
    for p in padroes_ataque:
        if re.search(p, t_lower):
            return "ataque_pessoal", True, time.perf_counter() - t0

    if (
        re.search(r"\bou voc[êe]\b", t_lower)
        or re.search(r"\bou o\b", t_lower)
        or re.search(r"\bou a\b", t_lower)
        or re.search(r"\bquem n[ãa]o\b", t_lower)
    ):
        return "falso_dilema", True, time.perf_counter() - t0

    return "legitimo", False, time.perf_counter() - t0


class FiltroSoberanoONNX:
    """Motor de inferência local de produção do FiltroSoberano sobre ONNX Runtime."""

    def __init__(self, checkpoint_dir: str, onnx_path: str, max_len: int = 192, head_max_len: int = 128):
        self.agent = oa.ONNXAgent(
            model_id_or_path=checkpoint_dir,
            subfolder=None,
            onnx_path=onnx_path,
        )
        self.max_len = max_len
        self.head_max_len = head_max_len
        self.ids = list(QUESTIONS_SCHEMA.keys())
        self.internal = {qid: self.agent._to_internal(QUESTIONS_SCHEMA[qid]) for qid in self.ids}

        # Pré-aquecimento de sessão ONNX
        self.extrair_logits("Texto inicial de pré-aquecimento da sessão ONNX Runtime.")

    def extrair_logits(self, texto: str) -> np.ndarray:
        encoded = self.agent._encode_state(texto, self.ids, self.internal, self.max_len, self.head_max_len)
        ort_inputs = oa._collate_items_numpy([encoded], self.agent.tok.pad_token_id)
        ort_outs = self.agent.session.run(["logits", "act_logits"], ort_inputs)
        k = len(encoded[0]["markers"])
        return ort_outs[0][0][:k]

    def predizer(
        self,
        texto: str,
        temperatura: float = 1.0,
        class_bias=None,
        thresh_manip: float = 0.50,
        thresh_top: float = 0.0,
        usar_regra_tamanho: bool = True,
        argmax_puro: bool = False,
    ):
        t0 = time.perf_counter()
        if usar_regra_tamanho and len(texto.strip()) < 15:
            return "legitimo", False, time.perf_counter() - t0

        logits = self.extrair_logits(texto)
        bias_arr = np.zeros(len(logits), dtype=np.float64) if class_bias is None else np.asarray(class_bias, dtype=np.float64)
        scaled = logits.astype(np.float64) / max(temperatura, 1e-4) + bias_arr[: len(logits)]
        probs = np.exp(scaled - np.max(scaled))
        probs /= np.sum(probs)

        if argmax_puro:
            pred_idx = int(np.argmax(probs))
            tat = CLASSES[pred_idx]
            return tat, (tat != "legitimo"), time.perf_counter() - t0

        p_legit = float(probs[3])
        p_manip = 1.0 - p_legit
        best_manip_idx = int(np.argmax(probs[:3]))
        best_manip_prob = float(probs[best_manip_idx])

        if p_manip >= thresh_manip and best_manip_prob >= thresh_top:
            tat = CLASSES[best_manip_idx]
            return tat, True, time.perf_counter() - t0
        return "legitimo", False, time.perf_counter() - t0


def calcular_metricas(dados, predicoes):
    n = len(dados)
    y_true_tat = [d["gabarito_tatica"] for d in dados]
    y_pred_tat = [p[0] for p in predicoes]
    y_true_man = [d["eh_manipulativo"] for d in dados]
    y_pred_man = [p[1] for d, p in zip(dados, predicoes)]
    latencias = [p[2] for p in predicoes]

    acc = sum(1 for yt, yp in zip(y_true_tat, y_pred_tat) if yt == yp) / n

    legit_idx = [i for i, ym in enumerate(y_true_man) if not ym]
    fp_cnt = sum(1 for i in legit_idx if y_pred_man[i])
    taxa_fp = fp_cnt / max(1, len(legit_idx))

    alerta_idx = [i for i, d in enumerate(dados) if d.get("categoria") == "alerta_legitimo"]
    fp_alerta_cnt = sum(1 for i in alerta_idx if y_pred_man[i])
    taxa_fp_alerta = fp_alerta_cnt / max(1, len(alerta_idx))

    manip_idx = [i for i, ym in enumerate(y_true_man) if ym]
    fn_cnt = sum(1 for i in manip_idx if not y_pred_man[i])
    taxa_fn = fn_cnt / max(1, len(manip_idx))

    f1_por_classe = {}
    for c in CLASSES:
        tp = sum(1 for yt, yp in zip(y_true_tat, y_pred_tat) if yt == c and yp == c)
        fp = sum(1 for yt, yp in zip(y_true_tat, y_pred_tat) if yt != c and yp == c)
        fn = sum(1 for yt, yp in zip(y_true_tat, y_pred_tat) if yt == c and yp != c)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        f1_por_classe[c] = float(f1)

    return {
        "f1_macro": float(np.mean(list(f1_por_classe.values()))),
        "f1_por_classe": f1_por_classe,
        "taxa_fp": float(taxa_fp),
        "taxa_fp_alerta": float(taxa_fp_alerta),
        "taxa_fn": float(taxa_fn),
        "acc_tatica": float(acc),
        "latencia_s": float(np.mean(latencias)),
        "latencia_p95_s": float(np.percentile(latencias, 95)),
        "fp_count": fp_cnt,
        "fn_count": fn_cnt,
    }


def bootstrap_ic(dados, predicoes, n_boot: int = 1000):
    rng = np.random.RandomState(42)
    n = len(dados)
    f1s, fps, fns, accs = [], [], [], []
    for _ in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        ad = [dados[i] for i in idx]
        ap = [predicoes[i] for i in idx]
        m = calcular_metricas(ad, ap)
        f1s.append(m["f1_macro"])
        fps.append(m["taxa_fp"])
        fns.append(m["taxa_fn"])
        accs.append(m["acc_tatica"])

    def pct(arr):
        return [float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))]

    return {
        "f1_ic": pct(f1s),
        "fp_ic": pct(fps),
        "fn_ic": pct(fns),
        "acc_ic": pct(accs),
    }


def main():
    with open("workspace/exp/dataset_teste_cego_200.json", encoding="utf-8") as f:
        dados_teste = json.load(f)

    with open("workspace/models/laya_ptbr_finetuned/calibracao_seletiva.json", encoding="utf-8") as f:
        gate_cfg = json.load(f)

    t_star = float(gate_cfg["temperature_choice_4"])
    c_bias = gate_cfg.get("class_bias", [0.0, 0.0, 0.0, 0.0])
    th_manip = float(gate_cfg["thresh_manip"])
    th_top = float(gate_cfg["thresh_top"])

    print("=" * 90)
    print(f"AVALIAÇÃO DEFINITIVA NO TESTE CEGO INÉDITO (n = {len(dados_teste)} postagens reais)")
    print(f"Parâmetros ajustados na Calibração: T* = {t_star:.4f} | bias = {c_bias} | P_manip >= {th_manip:.2f} | P_top >= {th_top:.2f}")
    print("=" * 90)

    # 1. Modelo Zero-Shot original (ONNX FP32)
    from huggingface_hub import snapshot_download
    raw_snap = os.path.join(
        snapshot_download("convaiinnovations/laya", allow_patterns=["multilingual/*"], local_files_only=True),
        "multilingual",
    )
    motor_zeroshot = FiltroSoberanoONNX(
        checkpoint_dir=raw_snap,
        onnx_path="workspace/models/onnx/multilingual/model.onnx",
    )

    # 2. Modelo Fine-Tuned + Calibrado em ONNX FP32
    motor_finetuned = FiltroSoberanoONNX(
        checkpoint_dir="workspace/models/onnx/laya_ptbr_finetuned",
        onnx_path="workspace/models/onnx/laya_ptbr_finetuned/model.onnx",
    )

    condicoes = [
        (
            "1. Linha de Base: Regras Determinísticas (Regex)",
            [predizer_regras(x["texto"]) for x in dados_teste],
        ),
        (
            "2. Laya Multilíngue Zero-Shot (ONNX FP32 sem ajuste)",
            [motor_zeroshot.predizer(x["texto"], usar_regra_tamanho=True, argmax_puro=True) for x in dados_teste],
        ),
        (
            "3. FiltroSoberano Laya PT-BR (RLCD ONNX FP32, argmax direto)",
            [motor_finetuned.predizer(x["texto"], temperatura=t_star, usar_regra_tamanho=True, argmax_puro=True) for x in dados_teste],
        ),
        (
            f"4. FiltroSoberano Completo (RLCD ONNX FP32 + T*={t_star:.2f} + Limiar Seletivo)",
            [
                motor_finetuned.predizer(
                    x["texto"],
                    temperatura=t_star,
                    class_bias=c_bias,
                    thresh_manip=th_manip,
                    thresh_top=th_top,
                    usar_regra_tamanho=True,
                )
                for x in dados_teste
            ],
        ),
        (
            "5. Ablação: Sem Regra de Tamanho Mínimo (<15c)",
            [
                motor_finetuned.predizer(
                    x["texto"],
                    temperatura=t_star,
                    class_bias=c_bias,
                    thresh_manip=th_manip,
                    thresh_top=th_top,
                    usar_regra_tamanho=False,
                )
                for x in dados_teste
            ],
        ),
    ]

    print(
        "\n| Condição Experimental | Macro-F1 [IC 95%] | Falso Positivo [IC 95%] | FP em Alertas | Erro Silencioso [IC 95%] | Acurácia Tática | Latência Média (P95) |"
    )
    print("|:---|---:|---:|---:|---:|---:|---:|")

    saida_json = []
    for nome, preds in condicoes:
        m = calcular_metricas(dados_teste, preds)
        ic = bootstrap_ic(dados_teste, preds)
        print(
            f"| {nome} | "
            f"**{m['f1_macro']:.3f}** [{ic['f1_ic'][0]:.2f}–{ic['f1_ic'][1]:.2f}] | "
            f"{m['taxa_fp']*100:.1f}% [{ic['fp_ic'][0]*100:.0f}%–{ic['fp_ic'][1]*100:.0f}%] | "
            f"{m['taxa_fp_alerta']*100:.1f}% | "
            f"{m['taxa_fn']*100:.1f}% [{ic['fn_ic'][0]*100:.0f}%–{ic['fn_ic'][1]*100:.0f}%] | "
            f"{m['acc_tatica']*100:.1f}% [{ic['acc_ic'][0]*100:.0f}%–{ic['acc_ic'][1]*100:.0f}%] | "
            f"{m['latencia_s']:.3f} s ({m['latencia_p95_s']:.3f} s) |"
        )
        print(f"   -> F1 por classe: { {k: round(v, 3) for k, v in m['f1_por_classe'].items()} }")
        saida_json.append({"condicao": nome, **m, **ic})

    out_path = "workspace/exp/resultados_laya_ptbr_definitivos.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(saida_json, f, indent=2, ensure_ascii=False)
    print(f"\nResultados completos salvos em: {out_path}")


if __name__ == "__main__":
    main()
