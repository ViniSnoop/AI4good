# T1 auth recovery: a dead Google token must hand Lucas a runnable fix, not a traceback.
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import google_auth


ACCOUNTS = [
    {"aliases": ["personal", "pessoal"], "email": "lsf.cin@gmail.com"},
    {"aliases": ["cin", "voxar"], "email": "lsf@cin.ufpe.br"},
]


@pytest.fixture
def accounts(monkeypatch):
    monkeypatch.setattr(google_auth, "get_accounts", lambda: ACCOUNTS)


def test_secondary_alias_resolves_to_its_account_address(accounts):
    """Lucas types 'pessoal'; the consent screen still has to name the primary address."""
    assert google_auth.account_email("pessoal") == "lsf.cin@gmail.com"
    assert google_auth.account_email("voxar") == "lsf@cin.ufpe.br"


def test_unknown_alias_says_where_to_look_rather_than_guessing(accounts):
    email = google_auth.account_email("nope")
    assert "accounts.json" in email


def test_recovery_names_the_command_and_the_account(accounts):
    """The two things the message exists to carry. Four accounts make the address load-bearing."""
    text = google_auth.recovery_text("personal", "drive", pathlib.Path("/tmp/t.json"))
    assert "core/tools/google/drive auth personal --reauth" in text
    assert "lsf.cin@gmail.com" in text


def test_drive_write_recovers_with_the_write_flag(accounts):
    """A read re-consent leaves the write token dead, so the flag cannot be dropped."""
    text = google_auth.recovery_text("cin", "drive-write", pathlib.Path("/tmp/t.json"))
    assert "--write --reauth" in text


def test_service_without_a_reauth_flag_still_gets_a_runnable_step(accounts):
    """gmail/calendar/slides have no --reauth yet; the fallback must name the real token path."""
    token = pathlib.Path("/home/x/.config/workspace-calendar/cin.token.json")
    text = google_auth.recovery_text("cin", "calendar", token)
    assert str(token) in text
    assert "lsf@cin.ufpe.br" in text


def test_run_prints_the_instruction_instead_of_raising(accounts, capsys):
    """Entrypoints wrap main() in run(); a traceback here is the bug this guards."""
    def boom():
        raise google_auth.AuthExpired("SIGN IN AS: lsf.cin@gmail.com")

    with pytest.raises(SystemExit) as exit_info:
        google_auth.run(boom)
    assert "lsf.cin@gmail.com" in str(exit_info.value)


def test_every_google_cli_routes_its_entrypoint_through_run():
    """A CLI calling main() directly would print a traceback and lose the instruction."""
    tools_root = pathlib.Path(__file__).resolve().parents[1]
    clis = [
        tools_root / "google" / "drive",
        tools_root / "google" / "gmail",
        tools_root / "google" / "calendar",
        tools_root / "slides" / "slides",
    ]
    for cli in clis:
        body = cli.read_text(encoding="utf-8")
        assert "google_auth.run(main)" in body, f"{cli.name} bypasses the auth guard"
