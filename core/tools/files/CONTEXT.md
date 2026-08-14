# files
> Remote file storage: list, search, download, upload. Provider leaf: `gdrive`.

Auth is two tokens, not one: reads use the `drive` token (`drive.readonly`), and `mkdir` / `put`
use a separate `drive-write` one. A read re-consent therefore leaves the write token dead —
`gdrive auth <alias> --write --reauth` is a different command, and the recovery message says so.
Downloads land in `/mnt/workspace/Downloads/workspace-drive`.

`drive_migrate.py` is not part of the CLI — it is a standing account-to-account copy (`cin` →
`personal`), idempotent, run by path.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`drive_core.py`](drive_core.py) | [`drive_core.pyi`](drive_core.pyi) | `get_service`, `list_files`, `search_files`, `recent_files`, `download_file` | drive_core.py — Google Drive read+write seam (account-agnostic) for Core/tools/files/gdrive |
| [`drive_migrate.py`](drive_migrate.py) | [`drive_migrate.pyi`](drive_migrate.pyi) | `migrate_recursive`, `run` | ← add first-line comment |
| [`drive_migrate_core.py`](drive_migrate_core.py) | [`drive_migrate_core.pyi`](drive_migrate_core.pyi) | `get_cin_service`, `get_personal_service` | ← add first-line comment |
| [`gdrive`](gdrive) | — | — | Google Drive read+write CLI for workspace OS — commands: auth, recent, list, search, download, mkdir, put |
<!-- routing:end -->
