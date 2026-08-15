# chain.py — the CONTEXT.md chain of a path, and the workspace paths named in a blob of text.
#
# One definition, three callers. It was two copies before (context-gate and bash-context-gate each
# carried a `context_chain`, and they had already drifted on whether to start at the target or its
# parent) — the same duplication the file-law module exists to prevent.
import re
from pathlib import Path

WORKSPACE = Path('/mnt/workspace')
# Freely readable: the deadlock guard, plus the docs that ARE the context.
EXEMPT_NAMES = {'CONTEXT.md', 'AGENTS.md', 'CLAUDE.md', 'MEMORY.md'}
SKIP_PARTS = {'.git', 'node_modules', 'dist', '.codegraph', '__pycache__', '.vscode', '.hooks'}
TOKEN_RE = re.compile(r'''[^\s'"`;|&<>()=]+''')


def context_chain(target: Path) -> list[Path]:
	"""CONTEXT.md files from the target's directory up to (excluding) the workspace root."""
	chain: list[Path] = []
	current = target if target.is_dir() else target.parent
	while current != WORKSPACE and current != current.parent:
		ctx = current / 'CONTEXT.md'
		if ctx.is_file():
			chain.append(ctx)
		current = current.parent
	return chain


def paths_in(text: str, cwd: str, files_only: bool = False) -> set[Path]:
	"""Every existing workspace path named in a blob of text — a command line, or an agent prompt.

	`files_only` keeps the Bash gate exactly as narrow as it was: a command merely *mentioning* a
	directory has never been gated, and widening that is a separate decision from sharing this code.
	An agent prompt is the opposite case — "work in core/flows/" is precisely the pointer a worker
	should be briefed on — so the collector leaves it off.
	"""
	found: set[Path] = set()
	for token in TOKEN_RE.findall(text):
		if '/' not in token:
			continue
		# Prose ends a path with punctuation — "...edit foo/bar.py." — and the trailing period made
		# every sentence-final path invisible. It cost a live probe to catch, because the unit test
		# happened to put a space after the path. A path never legitimately ends in these.
		raw = token.strip('\'"`,:;!?()[]{}<>').rstrip('.')
		if raw.startswith('~') or raw.startswith('-'):
			continue
		path = Path(raw) if raw.startswith('/') else Path(cwd) / raw
		try:
			path = path.resolve()
		except OSError:
			continue
		if not (path.is_file() if files_only else path.exists()):
			continue
		if not str(path).startswith(str(WORKSPACE) + '/'):
			continue
		if path.name in EXEMPT_NAMES or SKIP_PARTS.intersection(path.parts):
			continue
		found.add(path)
	return found


def summary_of(ctx: Path) -> str:
	"""A CONTEXT.md's one-line self-description — its `> ` line, which is line 2 by convention.

	The head is what a session pays for; the `>` line is what a *worker* needs. Handing a subagent
	the full head would recreate the cost the exemption exists to avoid.
	"""
	try:
		for line in ctx.read_text(encoding='utf-8', errors='replace').splitlines()[:6]:
			if line.startswith('> '):
				return line[2:].strip()
	except OSError:
		pass
	return ''
