# The page the three drawings live in: one self-contained HTML file, no script, no asset it does
# not carry. It opens from a file:// path on a machine with no network and under any provider,
# which is what "an asset inside the workspace" has to mean to be worth committing.
#
# Tabs are radio inputs and CSS sibling selectors rather than JavaScript — one less thing that can
# fail silently in a viewer, and the file stays readable as text.
from html import escape

STYLE = """
:root { --bg:#fbfbf9; --fg:#1b1b1a; --dim:#6b6b66; --line:#dcdcd6; --card:#fff; --accent:#2b6cb0; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#16171a; --fg:#e6e6e2; --dim:#9a9a94; --line:#2e3034; --card:#1c1e22; --accent:#7cb2e8; }
}
* { box-sizing: border-box; }
body { margin:0; padding:28px 26px 60px; background:var(--bg); color:var(--fg); max-width:1180px;
  font:15px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif; }
h1 { font-size:20px; margin:0 0 6px; letter-spacing:-.01em; }
h2 { font-size:15px; margin:26px 0 8px; }
.lede { color:var(--dim); margin:0 0 22px; max-width:70ch; }
code { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.92em; }
.tabs input { position:absolute; opacity:0; pointer-events:none; }
.tabs label { display:inline-block; padding:6px 13px; margin:0 6px 14px 0; cursor:pointer;
  border:1px solid var(--line); border-radius:999px; color:var(--dim); background:var(--card); }
.tabs input:checked + label { color:var(--bg); background:var(--fg); border-color:var(--fg); }
.panel { display:none; }
#t-matrix:checked ~ .p-matrix, #t-spine:checked ~ .p-spine, #t-mass:checked ~ .p-mass { display:block; }
.scroll { overflow-x:auto; border:1px solid var(--line); border-radius:10px; background:var(--card);
  padding:12px; }
table.matrix { border-collapse:collapse; font-size:12px; }
table.matrix th, table.matrix td { border:1px solid var(--line); padding:2px 5px; text-align:center; }
table.matrix th.rowhead { text-align:left; white-space:nowrap; font-weight:500;
  position:sticky; left:0; background:var(--card); z-index:1; }
table.matrix tbody tr:nth-child(even) td { background:rgba(128,128,128,.06); }
table.matrix thead th { vertical-align:bottom; padding:6px 3px; font-weight:500; color:var(--dim); }
.vert { writing-mode:vertical-rl; transform:rotate(180deg); white-space:nowrap; }
.grouprow td, table.matrix tbody tr.grouprow:nth-child(even) td { text-align:left;
  background:var(--bg); color:var(--dim); font-size:11px;
  letter-spacing:.08em; text-transform:uppercase; padding:6px; }
td.blocks { color:#c0392b; } td.warns { color:#b7791f; } td.generates { color:var(--accent); }
td.advises { color:var(--dim); } td.none { color:var(--dim); opacity:.6; }
.empty { background:transparent; }
.unwired { color:#c0392b; font-size:10px; letter-spacing:.04em; }
.inf { color:var(--dim); font-size:9px; letter-spacing:.04em; }
.legend { color:var(--dim); font-size:12px; margin:10px 0 4px; }
.key { margin-right:16px; white-space:nowrap; }
.note { color:var(--dim); font-size:12px; max-width:80ch; margin:8px 0 0; }
svg.spine text { font-size:12px; fill:var(--fg); }
svg.spine circle { fill:var(--accent); }
svg.spine .d0 circle, svg.spine .d1 circle { fill:var(--fg); }
svg.spine .link { fill:none; stroke:var(--line); stroke-width:1.2; }
svg.treemap text { font-size:12px; fill:#fff; font-weight:500; }
svg.treemap text.sub { font-size:10px; font-weight:400; opacity:.8; }
svg.treemap rect { stroke:var(--bg); stroke-width:1; }
.c0 rect{fill:#2b6cb0} .c1 rect{fill:#2f855a} .c2 rect{fill:#975a16} .c3 rect{fill:#805ad5}
.c4 rect{fill:#c05621} .c5 rect{fill:#2c7a7b} .c6 rect{fill:#b83280} .c7 rect{fill:#4a5568}
footer { margin-top:34px; padding-top:14px; border-top:1px solid var(--line); color:var(--dim);
  font-size:12px; }
footer b { color:var(--fg); font-weight:600; }
"""

TABS = (('matrix', 'enforcement', 'what is wired where'),
        ('spine', 'routing', 'how an agent walks the tree'),
        ('mass', 'mass', 'how much of it there is'))


def _tab_inputs() -> str:
    out = []
    for i, (key, label, hint) in enumerate(TABS):
        checked = ' checked' if i == 0 else ''
        out.append(f'<input type="radio" name="tab" id="t-{key}"{checked}>'
                   f'<label for="t-{key}" title="{escape(hint)}">{escape(label)}</label>')
    return '\n'.join(out)


def _panel(key: str, heading: str, body: str) -> str:
    return (f'<section class="panel p-{key}"><h2>{escape(heading)}</h2>'
            f'<div class="scroll">{body}</div>')


def render(panels: dict, coverage: dict, scope: dict) -> str:
    """One page, three drawings of the same workspace. `panels` maps a tab key to its rendered
    body plus the prose under it; nothing here computes anything about the workspace."""
    body = [_tab_inputs()]
    for key, _label, _hint in TABS:
        drawing, prose = panels[key]
        heading = {'matrix': 'features against the sites that enforce them',
                   'spine': 'the routing chain, three levels deep',
                   'mass': 'tracked bytes per directory'}[key]
        body.append(_panel(key, heading, drawing) + prose + '</section>')

    return '\n'.join([
        '<!-- ARCHITECTURE.html — generated by core/tools/wos/diagram/architecture from '
        'core/features.txt and the generated routing blocks. Do not edit: run the tool. -->',
        '<!doctype html>',
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        '<title>workspace architecture</title>',
        f'<style>{STYLE}</style></head><body>',
        '<h1>the workspace as it is</h1>',
        '<p class="lede">Three drawings of one workspace, generated from the files that already '
        'declare it. Nothing here is drawn by hand — a hand-drawn map is the rot the routing '
        'tables exist to prevent, and it goes stale the day after it is drawn.</p>',
        '<div class="tabs">',
        '\n'.join(body),
        '</div>',
        _footer(coverage, scope),
        '</body></html>', ''])


def _footer(coverage: dict, scope: dict) -> str:
    unparsed = coverage['unparsed']
    line = (f'<b>coverage</b> parsed {coverage["parsed"]} of {coverage["total"]} routing blocks'
            + (f' · <b>{len(unparsed)} unparsed:</b> {escape(", ".join(unparsed))}'
               if unparsed else ' · none unparsed'))
    return '\n'.join([
        '<footer>',
        f'<p>{line}</p>',
        f'<p><b>scope</b> the workspace repository. {scope["nested"]} repositories nested inside '
        'it are drawn as directories and no deeper: each is its own repository and will earn its '
        'own document.</p>',
        '<p><b>what is inferred</b> every edge above renders declared or generated data except '
        'the firing moment of a hook, which is inferred from directory convention. No '
        'machine-readable hook-trigger registry exists yet, and until it does this page marks '
        'those and claims nothing more.</p>',
        '<p><b>how to change it</b> edit the source, not this file: '
        '<code>core/features.txt</code> for the matrix, a directory\'s <code>CONTEXT.md</code> '
        'for the spine. Regenerated and committed by <code>/roundup</code> at every session '
        'close, so a stale picture is a bug in the close, not a fact of life.</p>',
        '</footer>'])
