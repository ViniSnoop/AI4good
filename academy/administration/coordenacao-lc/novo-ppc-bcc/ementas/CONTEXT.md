# ementas
> Ementa pipeline for the new BCC PPC: download the sources, classify them, build one SIGAA-shaped `.docx` per
> discipline.

`fonte/` holds what was downloaded, `saida-docx/` what was generated — regenerate rather than
hand-edit either. Plan, status and the open upload step: [`../ROADMAP-ementas.md`](../ROADMAP-ementas.md).

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`build.py`](build.py) | [`build.pyi`](build.pyi) | `carga_breakdown_raw` | Build every [MODELO-SIGAA] <nome>.docx into saida-docx/, from whichever |
| [`classify.py`](classify.py) | [`classify.pyi`](classify.pyi) | `uniq_cells`, `classify` | Classify each fonte/<periodo>__<nome>.docx as new-filled / new-blank / old-schema. |
| [`download_all.py`](download_all.py) | [`download_all.pyi`](download_all.pyi) | — | Download every source in inventory.json into fonte/<periodo>__<nome>.docx (gdoc->docx export; no-op for real docx). |
| [`extract_old.py`](extract_old.py) | [`extract_old.pyi`](extract_old.pyi) | `uniq_cells`, `flatten_rows`, `extract` | Extract SIGAA-shaped fields from an old-schema ('PROGRAMA DA DISCIPLINA') source doc. |
| [`extract_single.py`](extract_single.py) | [`extract_single.pyi`](extract_single.pyi) | `extract` | Extract SIGAA fields from a standalone single-table new-schema doc (no |
| [`filler.py`](filler.py) | [`filler.pyi`](filler.pyi) | `cell_label`, `fill` | Fill MODELO EMENTA SIGAA.docx into one per-discipline doc. |
| [`gaps-derivados.md`](gaps-derivados.md) | — | — | Conteúdo reenumerado da ementa, carga vinda de créditos, fallbacks do modelo. |
| [`gaps-objetivos-1.md`](gaps-objetivos-1.md) | — | — | OBJETIVOS gerados pelo batch, primeira metade das disciplinas. |
| [`gaps-objetivos-2.md`](gaps-objetivos-2.md) | — | — | OBJETIVOS gerados pelo batch, segunda metade das disciplinas. |
| [`gaps.md`](gaps.md) | — | — | gaps.md -- auditoria do BATCH MODELO-SIGAA (gerado 2026-07-21) |
| [`hallucination_scan.py`](hallucination_scan.py) | [`hallucination_scan.pyi`](hallucination_scan.pyi) | — | Flag any token in a generated OBJETIVOS that doesn't appear in that same |
| [`port.py`](port.py) | [`port.pyi`](port.pyi) | `uniq_cells`, `match_label`, `extract`, `set_font`, `fill` | Port one discipline into a MODELO-SIGAA doc. |
| [`upload_all.py`](upload_all.py) | [`upload_all.pyi`](upload_all.pyi) | — | Upload every built [MODELO-SIGAA] doc to the Drive subfolder matching its |
| [`verify.py`](verify.py) | [`verify.pyi`](verify.pyi) | — | Round-trip verification: re-read every built [MODELO-SIGAA] doc and diff its |
<!-- routing:end -->
