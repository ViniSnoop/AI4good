# forms
> Surveys and their answers: a form written as a versioned spec, applied in one call. Provider leaf: `gforms`.

```bash
core/tools/forms/gforms new       --account personal --folder <drive_folder_id> spec.json
core/tools/forms/gforms read      --account personal <form_id>     # outline + responder link
core/tools/forms/gforms apply     --account personal <form_id> requests.json
core/tools/forms/gforms responses --account personal <form_id>     # answers as text
```

The spec format, the two auth grants, why `SERVICE_DISABLED` is not a permission bug, and what
`responses` returns: [`SPECS.md`](SPECS.md). The specs Lucas actually applies live with the course
material, in [`academy/teaching/forms/`](../../../academy/teaching/forms/CONTEXT.md).

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | The spec format a form is written in, the two grants it authenticates with, and… |
| [`forms_core.py`](forms_core.py) | [`forms_core.pyi`](forms_core.pyi) | `get_service`, `get_drive`, `edit_url`, `create`, `get_form` | forms_core.py — Google Forms read+write seam (account-agnostic) for Core/tools/forms/gforms |
| [`forms_spec.py`](forms_spec.py) | [`forms_spec.pyi`](forms_spec.pyi) | `requests` | forms_spec.py — a form written as JSON: compact spec → Forms API batchUpdate requests |
| [`gforms`](gforms) | — | — | Google Forms CLI: auth, new, read, apply, responses |
<!-- routing:end -->
