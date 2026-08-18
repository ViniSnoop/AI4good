# The summary layer: the two questions answered before any detail arrives.
#
# Lucas, on the first version of the page: "I am not confident it helps me to understand... it is
# not visually informative yet." The diagnosis was never the data — it was that the page OPENS on
# maximum detail, so both of his reads are hunts. This module draws what he asked for instead:
# (1) is the workspace well tied, where is it loose, what is noise; (2) what is missing.
#
# Three encodings were built and shown at real scale; Lucas picked the heat grid on 2026-08-18 and
# the other two are gone rather than kept as options. What it won on is compression: the whole
# workspace is 30 cells, so the shape arrives before any reading does, and a layer that was declared
# and never built is a row of dots nobody has to hunt for.
#
# It wins that DESPITE the encoding hierarchy rather than because of it — colour and density are
# the weakest channels for judging quantity (Cleveland & McGill, core/refs/REFS.md § The health
# shelf), which is why every cell also carries its number. Density gets the eye to the region;
# the numeral answers once it is there.
from html import escape

# Hardest first. The order is the reading: a bar that starts red is a wall, one that is all grey is
# advice, and the difference lands before a label is read. Same order and same meaning as MARKS in
# diagram_matrix, because two orders for one idea is the asymmetry this workspace exists to catch.
STRENGTHS = ('blocks', 'warns', 'generates', 'advises', 'none')

STYLE = """
.ov { margin:0 0 26px; }
.ov h2 { margin:0 0 4px; }
.ov .q { color:var(--dim); font-size:12.5px; margin:0 0 12px; }
.finds { list-style:none; margin:0; padding:0; }
.finds li { display:grid; grid-template-columns:82px 1fr; gap:11px; padding:5px 0;
  border-top:1px solid var(--line); font-size:13px; }
.finds li:first-child { border-top:none; }
.finds .cnt { text-align:right; font-variant-numeric:tabular-nums; font-weight:600; }
.finds .of { color:var(--dim); font-weight:400; font-size:11.5px; }
.finds .zero .cnt, .finds .zero .txt { color:var(--dim); opacity:.65; font-weight:400; }
.finds .txt small { color:var(--dim); display:block; font-size:11px; margin-top:1px; }
table.heat { border-collapse:collapse; font-size:12px; font-variant-numeric:tabular-nums; }
table.heat th { color:var(--dim); font-weight:500; padding:4px 9px; }
table.heat th.l { text-align:right; }
table.heat td { border:1px solid var(--line); padding:5px 11px; text-align:center; min-width:52px; }
table.heat td.z { color:var(--dim); opacity:.4; }
"""


def _findings(items: list) -> str:
    """The gaps, as sentences with a magnitude — never as absences to be spotted.

    A count with no denominator is a number; `28 of 68` is a proportion a reader can judge without
    knowing this workspace. A finding at zero stays on the list, dimmed: a list that hides its
    clean rows cannot be read as coverage.
    """
    out = ['<ul class="finds">']
    for f in items:
        of = f'<span class="of"> of {f["of"]}</span>' if f['of'] is not None else ''
        inf = ' <span class="inf">inferred</span>' if f['inferred'] else ''
        out.append(f'<li class="{"zero" if not f["count"] else ""}">'
                   f'<span class="cnt">{f["count"]}{of}</span>'
                   f'<span class="txt">{escape(f["text"])}{inf}'
                   f'<small>{escape(f["where"])}</small></span></li>')
    return '\n'.join(out + ['</ul>'])


def _grid(layers: list) -> str:
    """Every declared layer against every enforcement strength: the workspace in thirty cells.

    Density is computed against the single busiest cell rather than per row. A per-row scale would
    make every layer look equally enforced — `norms` is ten out of ten `advises` and would render
    as solid as the sixteen commit-blocking hooks, which is the opposite of the truth.
    """
    peak = max((max(s.values(), default=0) for _l, s, _t in layers), default=1) or 1
    head = ''.join(f'<th>{escape(k)}</th>' for k in STRENGTHS)
    body = []
    for layer, strength, total in layers:
        cells = ''.join(
            f'<td class="{"z" if not strength.get(k) else ""}" '
            f'style="background:rgba(192,57,43,{strength.get(k, 0) / peak * 0.72:.3f})" '
            f'title="{strength.get(k, 0)} {escape(layer)} {escape(k)}">'
            f'{strength.get(k, 0) or "·"}</td>' for k in STRENGTHS)
        body.append(f'<tr><th class="l">{escape(layer)}</th>{cells}'
                    f'<th class="l">{total or "nothing"}</th></tr>')
    return f'<table class="heat"><tr><th></th>{head}<th></th></tr>{"".join(body)}</table>'


def render(layers: list, items: list) -> str:
    """The summary layer: how the workspace is tied, then what is loose or missing."""
    return (f'<section class="ov"><h2>how it is tied</h2>'
            f'<p class="q">every declared layer against how hard its features push. Darkness is '
            f'how many; a row of dots is a layer that was declared and never built. The '
            f'<b>none</b> column is not a failure — it is the half of this workspace that serves '
            f'when called instead of pushing on its own.</p>{_grid(layers)}</section>'
            f'<section class="ov"><h2>what is loose or missing</h2>'
            f'<p class="q">derived from the same declarations, so every row is a fact about the '
            f'workspace rather than a judgement about it</p>{_findings(items)}</section>')
