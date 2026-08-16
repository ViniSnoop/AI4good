#!/usr/bin/env python3
# PreToolUse: Bash — a shell heredoc that writes a workspace file meets none of the file gates.
#
# `pre-edit.py`, `facade-gate.py`, `spec-read-gate.py` and `bugs-gate.py` are all
# `PreToolUse: Edit|Write`, so `cat > file << 'EOF'` walks past every one of them. Measured over
# this workspace's transcripts (2026-08-15): 128 such calls, 354,100 chars, and among them
# brain/INBOX.md, HISTORY.md and test_entropy_ledger.py — written past the 200-line size gate, the
# first-line-comment check and the CONTEXT.md description rule. ROADMAP Frente 4.6 predicted it.
#
# Warns, never blocks, and the reason is not politeness: a PreToolUse hook fires AFTER the model has
# emitted the payload. The tokens are already spent, and blocking only makes the turn re-emit them.
# This gate teaches turn N+1. It cannot recover turn N.
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hook_input import parse_stdin

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]

# A heredoc opener: `<< EOF`, `<<'EOF'`, `<<-"EOF"`. Not `<<<`, which is a here-string.
OPENER = re.compile(r'<<-?\s*(?![<])[\'"]?([A-Za-z_][A-Za-z0-9_]*)[\'"]?')
# An output redirect to a path. Excludes `2>`, `>&2` and friends — those go to a stream, not a file.
REDIRECT = re.compile(r'(?<![0-9&>])>>?\s*(?![&>])([^\s;|&<>()]+)')
# `tee out.txt`, `tee -a out.txt`. tee names its target as an argument, with no `>` to spot.
TEE = re.compile(r'\btee\b\s+((?:-\S+\s+)*)([^\s;|&<>()-][^\s;|&<>()]*)')


def targets(line: str) -> list:
	"""Every path this line would write. Empty for `python3 - <<'EOF'`, which writes nothing.

	That exclusion is the one this gate cannot get wrong: stdin-to-an-interpreter is 44% of all
	heredoc volume here and is throwaway analysis, including every script the cost measurements
	behind ROADMAP Frente 9 were run from. A gate firing on those is a gate that gets turned off.
	"""
	found = [match.group(1) for match in REDIRECT.finditer(line)]
	found += [match.group(2) for match in TEE.finditer(line)]
	return found


def in_workspace(target: str, cwd: str) -> Path | None:
	"""The path, if it lands inside the workspace. A write to /tmp is not this gate's business."""
	try:
		path = Path(target).expanduser()
		resolved = (path if path.is_absolute() else Path(cwd or '.') / path).resolve()
		resolved.relative_to(WORKSPACE_ROOT)
	except (ValueError, OSError, RuntimeError):
		return None
	return resolved


def written_paths(command: str, cwd: str) -> list:
	"""Scan a payload for heredoc writes, skipping heredoc bodies so their text is never parsed."""
	found: list = []
	delimiter = ''
	for line in command.split('\n'):
		if delimiter:
			if line.strip() == delimiter:
				delimiter = ''
			continue
		opener = OPENER.search(line)
		if not opener:
			continue
		delimiter = opener.group(1)
		for target in targets(line):
			path = in_workspace(target, cwd)
			if path and path not in found:
				found.append(path)
	return found


def main() -> int:
	_raw, tool, tool_input, _session, cwd = parse_stdin()
	if tool and tool != 'Bash':
		return 0
	paths = written_paths(str(tool_input.get('command', '')), cwd)
	if not paths:
		return 0
	names = ', '.join(str(p.relative_to(WORKSPACE_ROOT)) for p in paths[:3])
	print(json.dumps({'hookSpecificOutput': {
		'hookEventName': 'PreToolUse',
		'additionalContext': f'⚠ UNGATED WRITE — {names} was written by a shell heredoc, which '
		                     f'skips the size, first-line and CONTEXT.md checks. Use the Write tool '
		                     f'for workspace files.',
	}}))
	return 0


if __name__ == '__main__':
	sys.exit(main())
