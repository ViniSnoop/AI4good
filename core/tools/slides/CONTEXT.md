# slides
> Presentations, read and edited in place. Provider leaf: `gslides` (Google Slides API).

```bash
core/tools/slides/gslides list  --account personal --name "AI4Good"
core/tools/slides/gslides read  --account personal <presentation_id>     # deck as navigable text
core/tools/slides/gslides new   --account personal "Aula 3"
core/tools/slides/gslides text  --account personal --slide <slide_id> <presentation_id> "título"
core/tools/slides/gslides apply --account personal <presentation_id> requests.json
```

**`read` prints element ids on purpose.** They are exactly what a `batchUpdate` request needs,
so reading a deck hands back the handles for editing it — no second raw-JSON fetch.

**`apply` is the real seam; the other write commands are conveniences over it.** The Slides API
is itself a list of typed requests, so the CLI wraps that list rather than inventing a DSL that
would go stale the moment Google adds a request type. `--json` on `read` gives the input side of
the same shape.

## Auth: two grants, and a read uses the strongest one it has

Tokens are `slides` (`presentations.readonly`) and `slides-write` (`presentations`), the same
split as [`../files/`](../files/CONTEXT.md). A read prefers the write token when the alias has
one — the edit consent already contains the read consent, so demanding a second browser trip
would buy no safety and just create two tokens that can die independently.

## Slidev is gone (2026-08-14)

This family used to be a Slidev CLI plus a Google-Slides→Slidev port pipeline (`slides_port`,
`slides_shapes`, `slides_style`, `slides_text`). Lucas ditched it once remote editing was
confirmed working: the reason to port decks out was that the source of truth could not be
edited from here, and it can. Do not resurrect a local presentation format without that
reason coming back.

What survived is the part that was never about Slidev: `slides_geom.py`, the Slides transform
algebra. The API's rendering facts live in [`SPECS.md`](SPECS.md).

## Motion is a generated slide sequence, not a player feature

Confirmed 2026-08-14: `duplicateObject` + `updatePageElementTransform` in one `batchUpdate`
authors per-frame motion, so position/velocity/acceleration sampled into frames survives PDF
export. Known wrinkle: duplicates land immediately after their source, so a run of frames comes
out reversed — reorder with `updateSlidesPosition` in the same batch.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | Google Slides API — facts worth not rediscovering |
| [`gslides`](gslides) | — | — | Google Slides CLI: auth, list, read, new, add, text, apply |
| [`slides_core.py`](slides_core.py) | [`slides_core.pyi`](slides_core.pyi) | `get_service`, `get_presentation`, `list_presentations`, `create`, `apply` | slides_core.py — Google Slides read+write seam (account-agnostic) for Core/tools/slides/gslides |
| [`slides_geom.py`](slides_geom.py) | [`slides_geom.pyi`](slides_geom.pyi) | `rotation_deg`, `eff_scale`, `compose_transforms`, `bounds` | slides_geom.py — Google Slides transform algebra: rotation, effective scale, composition, bounds |
| [`slides_outline.py`](slides_outline.py) | [`slides_outline.pyi`](slides_outline.pyi) | `element_text`, `kind`, `outline` | slides_outline.py — a deck as navigable text: slide index, element ids, and the words on them |
<!-- routing:end -->
