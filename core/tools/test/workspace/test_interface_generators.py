# T0 interface-generator invariants: a generated stub must land beside its source, and a
# jsconfig.json must never pretend to be a build config. Both bugs this guards were silent —
# the JS declaration path exited 0 and emitted nothing for years (ROADMAP Batch B item 6).
import json
import re
import subprocess
from pathlib import Path

from conftest import WORKSPACE_ROOT

POSTEDIT = WORKSPACE_ROOT / "core/hooks/postedit/interfaces.sh"
PRECOMMIT = WORKSPACE_ROOT / "core/hooks/generators/interfaces.sh"

# Keys tsc silently ignores in a file NAMED jsconfig.json: the name implies noEmit:true.
# Carrying them is how the workspace convinced itself declarations were being generated.
EMIT_KEYS = {"declaration", "emitDeclarationOnly", "outDir", "declarationDir"}


def _tracked(*patterns: str) -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "-z", *patterns],
        cwd=WORKSPACE_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return [WORKSPACE_ROOT / p for p in out.split("\0") if p]


def _templates(script: Path, name: str) -> list[str]:
    """Heredoc bodies the script scaffolds into <dir>/<name>."""
    body = script.read_text(encoding="utf-8")
    pattern = re.compile(
        r'cat > "\$dir/' + re.escape(name) + r'" << \'EOF\'\n(.*?)\nEOF', re.DOTALL
    )
    return pattern.findall(body)


def test_jsconfig_template_carries_no_emit_keys() -> None:
    templates = _templates(POSTEDIT, "jsconfig.json")
    assert templates, "postedit/interfaces.sh no longer scaffolds a jsconfig.json"
    for raw in templates:
        opts = json.loads(raw).get("compilerOptions", {})
        offenders = EMIT_KEYS & set(opts)
        assert not offenders, (
            f"jsconfig.json template declares {sorted(offenders)}, which tsc ignores "
            "because the file name implies noEmit:true. jsconfig is an editor aid; "
            "declarations are emitted per file by the tsc call above it."
        )


def test_tracked_jsconfigs_carry_no_emit_keys() -> None:
    for cfg in _tracked("*jsconfig.json"):
        opts = json.loads(cfg.read_text(encoding="utf-8")).get("compilerOptions", {})
        offenders = EMIT_KEYS & set(opts)
        assert not offenders, (
            f"{cfg.relative_to(WORKSPACE_ROOT)} declares {sorted(offenders)} — "
            "silently ignored, see the jsconfig template in postedit/interfaces.sh"
        )


def test_scaffolded_tsconfig_with_dot_outdir_declares_exclude() -> None:
    """tsc appends outDir to the DEFAULT exclude list, so `"outDir": "."` excludes the
    config's own directory unless exclude is stated — TS18003, zero inputs, no output."""
    for raw in _templates(POSTEDIT, "tsconfig.json"):
        cfg = json.loads(raw)
        if cfg.get("compilerOptions", {}).get("outDir") not in (".", "./"):
            continue
        assert "exclude" in cfg, (
            'tsconfig template sets "outDir": "." without an explicit "exclude". '
            "tsc adds outDir to the default exclude list, so the config excludes "
            "the very directory it is meant to compile (TS18003)."
        )


def test_js_declarations_are_generated_per_file_not_per_project() -> None:
    """`tsc -p <config>` reads its own previous output: our .d.ts sit beside their
    sources, so a project build resolves them as inputs and dies with TS5055."""
    body = PRECOMMIT.read_text(encoding="utf-8")
    section = body.split("# ── 7.")[1].split("# ── 8.")[0]
    # Comments in this section explain the defect by naming it — match code only.
    js_section = "\n".join(
        l for l in section.splitlines() if not l.lstrip().startswith("#")
    )
    assert "-p " not in js_section, (
        "the JS declaration step uses a tsc project build again — it must emit per "
        "file (--declarationDir), the same call post-edit makes"
    )
    assert "--declarationDir" in js_section


def _stub_out_dir(path: str, cwd: Path) -> str:
    return subprocess.run(
        ["bash", "-c",
         f'source "{WORKSPACE_ROOT}/core/hooks/stubgen/stub_paths.sh"; stub_out_dir "{path}"'],
        cwd=cwd, capture_output=True, text=True, check=True,
    ).stdout.strip()


def test_stub_output_root_climbs_out_of_the_package(tmp_path: Path) -> None:
    """stubgen mirrors package structure under -o, so passing the file's OWN directory
    wrote `pkg/pkg/*.pyi`. The output root must be the directory above the package root."""
    pkg = tmp_path / "outer" / "pkg" / "sub"
    pkg.mkdir(parents=True)
    for d in (tmp_path / "outer" / "pkg", pkg):
        (d / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "mod.py").write_text("# mod\n", encoding="utf-8")
    assert _stub_out_dir("outer/pkg/sub/mod.py", tmp_path) == "outer"


def test_stub_output_root_is_unchanged_outside_a_package(tmp_path: Path) -> None:
    plain = tmp_path / "plain"
    plain.mkdir()
    (plain / "mod.py").write_text("# mod\n", encoding="utf-8")
    assert _stub_out_dir("plain/mod.py", tmp_path) == "plain"


def test_both_hooks_use_the_shared_output_root_helper() -> None:
    for script in (POSTEDIT, PRECOMMIT):
        body = script.read_text(encoding="utf-8")
        assert "stub_out_dir" in body, f"{script.name} computes the stubgen -o path itself"
        assert '-o "$dir"' not in body, (
            f"{script.name} passes the file's own directory to stubgen again — that is "
            "what wrote a mirror of the path inside itself"
        )


def _repeated_run(parts: tuple[str, ...]) -> str | None:
    """Detect a path that mirrors part of itself: `a/a` or `a/b/a/b` — the signature of a
    generator resolving its output root against the wrong anchor."""
    for width in (1, 2):
        for i in range(len(parts) - 2 * width + 1):
            run = parts[i:i + width]
            if run == parts[i + width:i + 2 * width]:
                return "/".join(run * 2)
    return None


def test_no_generated_stub_sits_in_a_doubled_path() -> None:
    offenders = []
    for stub in _tracked("*.pyi", "*.d.ts", "*.dart.api"):
        rel = stub.relative_to(WORKSPACE_ROOT)
        doubled = _repeated_run(rel.parts[:-1])
        if doubled:
            offenders.append(f"{rel} (mirrors '{doubled}')")
    assert not offenders, (
        "generated stubs sit inside a mirror of their own path — the output root was "
        "resolved against the wrong anchor:\n  " + "\n  ".join(offenders)
    )
