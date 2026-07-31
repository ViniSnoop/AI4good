# google
> Google service CLIs — calendar, drive, gmail. Auth is shared: google_auth.py at the core/tools root.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`api/`](api/CONTEXT.md) | The Google API seams each CLI calls: auth-bound fetch, download, upload, triage. |

| File | Description |
|------|-------------|
| [`calendar`](calendar) | Google Calendar read-only CLI for workspace OS — commands: auth, upcoming, range, calendars |
| [`drive`](drive) | Google Drive read+write CLI for workspace OS — commands: auth, recent, list, search, download, mkdir, put |
| [`gmail`](gmail) | read-only Gmail integration for workspace OS |
<!-- routing:end -->
