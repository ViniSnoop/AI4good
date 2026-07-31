# slides
> Slidev presentations: auth, scaffold, serve, build, and port from Google Slides.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`slides`](slides) | — | — | Slidev presentation CLI: auth, new, serve, build, port |
| [`slides_fetch.py`](slides_fetch.py) | [`slides_fetch.pyi`](slides_fetch.pyi) | `get_service`, `get_presentation`, `list_presentations` | slides_fetch.py — Google Slides API read-only for workspace OS |
| [`slides_port.py`](slides_port.py) | [`slides_port.pyi`](slides_port.pyi) | `convert` | slides_port.py — Convert Google Slides API JSON to Slidev markdown |
| [`slides_shapes.py`](slides_shapes.py) | [`slides_shapes.pyi`](slides_shapes.pyi) | `render_element` | slides_shapes.py — Element rendering (shapes, lines, tables, images, groups) for slides_port |
| [`slides_style.py`](slides_style.py) | [`slides_style.pyi`](slides_style.pyi) | `set_theme_colors`, `rotation_deg`, `eff_scale`, `compose_transforms` | slides_style.py — CSS helpers: colors, gradients, rotation, geometry, download |
| [`slides_text.py`](slides_text.py) | [`slides_text.pyi`](slides_text.pyi) | `text_html`, `has_content` | slides_text.py — Text extraction + HTML rendering for Google Slides elements |
<!-- routing:end -->
