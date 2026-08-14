#!/mnt/workspace/.venv/bin/python3
# notion_auth.py — Notion's integration-token store, and the instructions a failure prints
import json, pathlib

SERVICE = "notion"
INTEGRATIONS = "https://www.notion.so/my-integrations"
CLI = "core/tools/notes/notion"


class AuthMissing(RuntimeError):
    """No usable token. Carries text written for Lucas — relay it unchanged."""


class NotShared(RuntimeError):
    """The token works; the target was never connected to the integration."""


def config_dir() -> pathlib.Path:
    d = pathlib.Path.home() / ".config" / f"workspace-{SERVICE}"
    d.mkdir(parents=True, exist_ok=True)
    d.chmod(0o700)
    return d


def token_path(alias: str) -> pathlib.Path:
    return config_dir() / f"{alias}.token.json"


def save_token(alias: str, token: str) -> pathlib.Path:
    """Store the secret readable by nobody else. This file is the only copy we keep."""
    path = token_path(alias)
    path.write_text(json.dumps({"token": token.strip()}, indent=2) + "\n")
    path.chmod(0o600)
    return path


def load_token(alias: str) -> str:
    path = token_path(alias)
    token = ""
    if path.exists():
        token = json.loads(path.read_text()).get("token", "").strip()
    if not token:
        raise AuthMissing(setup_text(alias))
    return token


def setup_text(alias: str) -> str:
    """What Lucas mints, where he pastes it, what the agent runs — the whole instruction."""
    return "\n".join([
        f"NOTION TOKEN MISSING — workspace '{alias}'.",
        "Notion has no headless consent flow: the secret is minted inside Lucas's account, so",
        "this is the one step an agent cannot absorb.",
        "",
        "LUCAS: three steps, once.",
        f"  1. {INTEGRATIONS} → New integration → name it 'WOS'.",
        "     Capabilities: Read content, Update content, Insert content.",
        "  2. Copy the Internal Integration Secret (it starts with 'ntn_').",
        "  3. Open the page in Notion → ⋯ → Connections → add 'WOS'. Connecting a parent covers",
        "     everything under it, so the class root is usually the only click.",
        "",
        "AGENT: run this and let him paste at the prompt — never take the secret as an argument,",
        "argv is readable by every process of this user.",
        f"    {CLI} auth {alias}",
        f"The token lands at {token_path(alias)}, mode 600.",
    ])


def revoked_text(alias: str) -> str:
    """401: the stored secret is not the live one. Nothing refreshes; only replacement works."""
    return "\n".join([
        f"NOTION REJECTED THE TOKEN (401) — workspace '{alias}'.",
        "The stored secret is wrong or was revoked. An integration token has no refresh step —",
        "a new secret is the only recovery.",
        "",
        f"LUCAS: {INTEGRATIONS} → the WOS integration → Secrets → show or regenerate it.",
        "",
        f"AGENT: {CLI} auth {alias}   (overwrites {token_path(alias)})",
    ])


def not_shared_text(alias: str, target: str) -> str:
    """404/403: almost always an unshared page, so say that before doubting the id."""
    return "\n".join([
        f"NOTION CANNOT SEE IT — '{target}' (workspace '{alias}').",
        "Notion answers the same code for 'not connected to this integration' and for 'no such",
        "id', and the first is far more common: content is invisible until shared, not forbidden.",
        "",
        "LUCAS: open it in Notion → ⋯ → Connections → add 'WOS'. A parent connection covers its",
        "children, so sharing the class root fixes every page under it at once.",
        "",
        f"AGENT: once he has, {CLI} list --account {alias} prints everything the token reaches.",
        "If the page is still absent from that list, then the id is the problem.",
    ])
