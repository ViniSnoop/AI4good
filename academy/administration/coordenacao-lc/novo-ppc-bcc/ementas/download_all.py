#!/mnt/workspace/.venv/bin/python3
"""Download every source in inventory.json into fonte/<periodo>__<nome>.docx (gdoc->docx export; no-op for real docx)."""
import json, pathlib, sys
sys.path.insert(0, "/mnt/workspace/core/tools")
import drive_core

HERE = pathlib.Path(__file__).parent
inv = json.load(open(HERE / "inventory.json", encoding="utf-8"))
fonte = HERE / "fonte"
fonte.mkdir(exist_ok=True)

for item in inv:
    safe = f"{item['periodo']}__{item['nome']}".replace("/", "-")
    out = fonte / f"{safe}.docx"
    if out.exists():
        print("skip (exists):", safe)
        continue
    path = drive_core.download_file("ufrpe", item["id"], fonte, export_as="docx")
    pathlib.Path(path).rename(out)
    print("ok:", safe)
