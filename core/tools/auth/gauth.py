#!/mnt/workspace/.venv/bin/python3
# gauth.py — Google's leaf of the auth family: shared OAuth2 for every Google-backed tool
import json, pathlib, sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

_GMAIL_CONFIG = pathlib.Path.home() / ".config" / "workspace-gmail"

# Services whose CLI already exposes `auth <alias> --reauth`. Anything absent here has no
# recovery flag yet, so its instruction is the manual equivalent: drop the token, re-run.
# When a CLI gains the flag, add it here and its message upgrades itself.
_REAUTH_CMD = {
    "drive": "core/tools/files/gdrive auth {alias} --reauth",
    "drive-write": "core/tools/files/gdrive auth {alias} --write --reauth",
    "gmail": "core/tools/mail/gmail auth {alias} --reauth",
    "calendar": "core/tools/calendar/gcalendar auth {alias} --reauth",
}


def config_dir(service: str) -> pathlib.Path:
    d = pathlib.Path.home() / ".config" / f"workspace-{service}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _credentials_file(service: str) -> pathlib.Path:
    """Find credentials.json: service dir first, then gmail dir (same GCP project)."""
    for d in (config_dir(service), _GMAIL_CONFIG):
        f = d / "credentials.json"
        if f.exists():
            return f
    raise FileNotFoundError(
        f"credentials.json not found. Place it in {config_dir(service)}/ "
        f"(download from GCP console → APIs & Services → Credentials)."
    )


def get_accounts() -> list:
    """Read accounts.json from gmail config (canonical source for all Google services)."""
    f = _GMAIL_CONFIG / "accounts.json"
    return json.loads(f.read_text()).get("accounts", []) if f.exists() else []


def primary_aliases() -> list:
    return [a["aliases"][0] for a in get_accounts() if a.get("aliases")]


def resolve_alias(alias: str) -> str:
    for acct in get_accounts():
        if alias in acct.get("aliases", []):
            return acct["aliases"][0]
    return alias


class AuthExpired(RuntimeError):
    """A token past recovery. Carries recovery text meant to be shown to Lucas verbatim."""


def account_email(alias: str) -> str:
    """The Google address an alias signs in as — the one thing the consent screen asks for."""
    primary = resolve_alias(alias)
    email = "unknown (check ~/.config/workspace-gmail/accounts.json)"
    for acct in get_accounts():
        if primary in acct.get("aliases", []):
            email = acct.get("email", email)
    return email


def recovery_text(alias: str, service: str, token_path: pathlib.Path) -> str:
    """The whole instruction: one command, and which account to sign in as."""
    template = _REAUTH_CMD.get(service)
    if template:
        step = template.format(alias=alias)
    else:
        step = f"rm {token_path}   # then re-run the command that just failed"
    lines = [
        f"GOOGLE AUTH EXPIRED — service '{service}', account '{alias}'.",
        "The stored token was revoked or expired. A refresh cannot recover it; only a new",
        "consent can.",
        "",
        "AGENT: run this yourself, do not hand it to Lucas as a chore. It opens a browser",
        "on his machine, so run it in the background and tell him the address below.",
        f"    {step}",
        "",
        f"LUCAS: a browser tab opens — sign in as:  {account_email(alias)}",
        "Signing in as a different Google account succeeds and then reads the wrong",
        "mailbox/drive, which is worse than failing. Check the address on the consent screen.",
    ]
    return "\n".join(lines)


def run(main_fn) -> None:
    """Entrypoint wrapper: a dead token prints its own fix instead of a traceback."""
    try:
        main_fn()
    except AuthExpired as exc:
        sys.exit(str(exc))


def auth(alias: str, service: str, scopes: list) -> Credentials:
    """OAuth2 flow for alias+service. Tokens stored per-service per-alias."""
    d = config_dir(service)
    token_path = d / f"{alias}.token.json"
    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # A revoked token raises RefreshError (invalid_grant) here and does NOT fall
            # through to consent, so this is the one place that can name the fix.
            try:
                creds.refresh(Request())
            except RefreshError as exc:
                raise AuthExpired(recovery_text(alias, service, token_path)) from exc
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(_credentials_file(service)), scopes
            )
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    return creds
