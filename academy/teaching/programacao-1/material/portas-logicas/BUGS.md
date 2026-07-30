# Known Bugs — Portas Lógicas Slidev Port

Presentation ID: `1QAMjplTVwzXOwL76JE3IfKNGdbtC8oYw9e3TfRR3jFg` (accessible via `personal` account)

## OR gate body missing

**Slide:** "portas lógicas : or" (slide 23 in API, ~slide 24 in deck)

**Symptom:** OR gate D-shaped body is absent. Only input/output arrows and LIGHTNING_BOLT decorations render.

**Investigation:** Slide 23 `pageElements` has 12 elements. The only candidate for a gate body is a `group()` at `l:0%;t:27.4%` containing:
- a `line` (sx=1, sy=1) — renders as the XOR arc line
- a `TEXT_BOX` (sx=0.32, sy=0.195, NOT_RENDERED) — ghost-filtered (scale < 0.4)

No `FLOW_CHART_DELAY` or custom path shape exists at the expected gate position (~50%;45%). The gate body is either:
1. Stored as a freeform/custom path shape our renderer doesn't handle, OR
2. Embedded in a way not exposed through `pageElements`

**AND gate works** because it uses explicit `solidFill` with `rgb(103,78,167)` — the OR gate likely has a different fill encoding.

**Next step:** Check if the OR gate body is a `CUSTOM` shape type or uses `shapeProperties.geometry` for its path. Inspect the group's child line transform to confirm it's the XOR arc, then look for any shape with `shapeType: CUSTOM` in that slide.

## XOR gate arc renders as straight diagonal

**Slide:** "portas lógicas : x or"

**Symptom:** The XOR gate's extra input-side arc (the bump that differentiates XOR from OR) renders as a straight purple diagonal line instead of a curve.

**Root cause:** `_render_line` uses SVG `<line>` (straight). The arc is a curved connector in Google Slides. Bend/curvature data is in the API's `lineProperties` but we don't extract it. Would need SVG `<path>` with cubic Bezier to fix.

Line endpoints: `(474.0, 249.5) → (506.8, 357.8)` stroke `rgb(103,78,167)` width 4pt.

## Signal value overlays absent on "soma com circuitos" slides

**Slides:** soma circuit slides (5 animation steps)

**Symptom:** Colored 0/1 signal values that should appear overlaid on circuit wire diagrams are absent. Circuit images are static (identical md5 across all 5 steps).

**Root cause:** These text overlays are Google Slides animation elements — they exist as part of the slide's animation timeline, NOT in `pageElements`. The Slides API only returns structural (final-state) elements; animation-hidden elements are inaccessible via this API endpoint.

**Cannot fix** without a different API approach (e.g., rendering each animation step via the Slides render API instead of parsing `pageElements`).

## Footer "LUCAS SILVA FIGUEIREDO" weight looks heavy

**Symptom:** Footer name uses `font-weight:900` (Raleway Black). This is what the API reports for those text runs (`weightedFontFamily.weight = 900`).

**Status:** Working as designed — 900 is what the designer set. If it looks too heavy, the original Google Slides font weight may have been set differently or the font was not Raleway Black in the original.
