# Workspace verification contract — see core/tools/verify/CONTEXT.md.
# The global pre-commit gate (core/hooks/pre-commit § 1a) discovers `verify-fast:` by
# convention and blocks the commit if it is red. Keep it under ~5s: it runs on every
# commit that stages a .py/.ts/.js/.dart file anywhere in the workspace repo.

PYTEST := .venv/bin/pytest

.PHONY: verify-fast verify-full entropy

# T0 static + T1 unit. No network, no model downloads, no browser.
verify-fast:
	@bash -n core/hooks/*.sh core/hooks/*/*.sh
	@$(PYTEST) core/tools/test/ -m "not network" -q

# The entropy dashboard: every Tier 0 check over the workspace AND its 24 nested repos,
# written to entropy.md. Read the report; never re-scan the tree by hand. Not part of
# verify-fast — it writes a file, and a verification step must not have side effects.
entropy:
	@python3 core/hooks/entropy/entropy-dashboard.py

# T2: adds the network-marked tests (live yt-dlp against real URLs — needs cookies
# for the Instagram cases, see core/tools/video/SETUP.md).
verify-full:
	@bash -n core/hooks/*.sh core/hooks/*/*.sh
	@$(PYTEST) core/tools/test/ -q
