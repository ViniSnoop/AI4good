# ementas
> Ementa pipeline for the new BCC PPC: download the sources, classify them, build one SIGAA-shaped `.docx` per discipline.

`fonte/` holds what was downloaded, `saida-docx/` what was generated — regenerate rather than
hand-edit either. Plan, status and the open upload step: [`../ROADMAP-ementas.md`](../ROADMAP-ementas.md).

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`build.py`](build.py) | [`build.pyi`](build.pyi) | `carga_breakdown_raw` | ← add first-line comment |
| [`classify.py`](classify.py) | [`classify.pyi`](classify.pyi) | `uniq_cells`, `classify` | Classify each fonte/<periodo>__<nome>.docx as new-filled / new-blank / old-schema. |
| [`download_all.py`](download_all.py) | [`download_all.pyi`](download_all.pyi) | — | Download every source in inventory.json into fonte/<periodo>__<nome>.docx (gdoc->docx export; no-op for real docx). |
| [`extract_old.py`](extract_old.py) | [`extract_old.pyi`](extract_old.pyi) | `uniq_cells`, `flatten_rows`, `extract` | ← add first-line comment |
| [`extract_single.py`](extract_single.py) | [`extract_single.pyi`](extract_single.pyi) | `extract` | ← add first-line comment |
| [`filler.py`](filler.py) | [`filler.pyi`](filler.pyi) | `cell_label`, `fill` | ← add first-line comment |
| [`gaps.md`](gaps.md) | — | — | gaps.md -- auditoria do BATCH MODELO-SIGAA (gerado 2026-07-21) |
| [`hallucination_scan.py`](hallucination_scan.py) | [`hallucination_scan.pyi`](hallucination_scan.pyi) | — | ← add first-line comment |
| [`port.py`](port.py) | [`port.pyi`](port.pyi) | `uniq_cells`, `match_label`, `extract`, `set_font`, `fill` | ← add first-line comment |
| [`upload_all.py`](upload_all.py) | [`upload_all.pyi`](upload_all.pyi) | — | ← add first-line comment |
| [`verify.py`](verify.py) | [`verify.pyi`](verify.pyi) | — | ← add first-line comment |
<!-- routing:end -->
