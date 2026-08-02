# api
> The Google API seams each CLI calls: auth-bound fetch, download, upload, triage.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`calendar_fetch.py`](calendar_fetch.py) | [`calendar_fetch.pyi`](calendar_fetch.pyi) | `get_service`, `list_calendars`, `upcoming_events`, `events_in_range`, `fmt_events` | calendar_fetch.py — Google Calendar API auth and event fetch for Core/tools/google/calendar |
| [`drive_core.py`](drive_core.py) | [`drive_core.pyi`](drive_core.pyi) | `get_service`, `list_files`, `search_files`, `recent_files`, `download_file` | drive_core.py — Google Drive read+write seam (account-agnostic) for Core/tools/google/drive |
| [`drive_migrate.py`](drive_migrate.py) | [`drive_migrate.pyi`](drive_migrate.pyi) | `migrate_recursive`, `run` | ← add first-line comment |
| [`drive_migrate_core.py`](drive_migrate_core.py) | [`drive_migrate_core.pyi`](drive_migrate_core.pyi) | `get_cin_service`, `get_personal_service` | ← add first-line comment |
| [`gmail_attachments.py`](gmail_attachments.py) | [`gmail_attachments.pyi`](gmail_attachments.pyi) | `download` | gmail_attachments.py — download and summarize Gmail attachments for Core/tools/google/gmail |
| [`gmail_fetch.py`](gmail_fetch.py) | [`gmail_fetch.pyi`](gmail_fetch.pyi) | `auth`, `get_service`, `fetch`, `fetch_all` | gmail_fetch.py — Gmail API auth, fetch, and MIME parse for Core/tools/google/gmail |
| [`gmail_triage.py`](gmail_triage.py) | [`gmail_triage.pyi`](gmail_triage.pyi) | `classify` | gmail_triage.py — Claude API email classification for Core/tools/google/gmail |
<!-- routing:end -->
