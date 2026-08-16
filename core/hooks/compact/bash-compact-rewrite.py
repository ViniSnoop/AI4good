#!/usr/bin/env python3
# PreToolUse: Bash — send every line of a multi-line command through rtk, not just the first.
# rtk parses line 1 only, so `cd x\ngit status` reaches the context uncompacted; measured at
# 23.4% of Bash calls (first line is `cd`) plus 1,249 rewritable commands stranded on lines 2+.
# Delegates verbatim to `rtk hook claude` for every shape it cannot split safely.
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hook_input import parse_stdin

# Bound the subprocess fan-out: one rtk call per line, so a huge payload delegates instead.
MAX_LINES = 30
# A line that opens a block, continues onto the next, or feeds a heredoc is not a standalone
# command, and splitting the payload around it would change what the shell runs.
BLOCK_KEYWORD = re.compile(r'^\s*(if|then|else|elif|fi|for|while|until|do|done|case|esac|select|function|\{|\}|\(|\))\b')
CONTINUES = re.compile(r'(\\|\||&&|;)\s*$')


def rtk_rewrite(command: str) -> str | None:
	"""How rtk would rewrite one command. None when it declines, errors, or is not installed."""
	payload = json.dumps({
		'hook_event_name': 'PreToolUse',
		'tool_name': 'Bash',
		'tool_input': {'command': command},
	})
	try:
		done = subprocess.run(
			['rtk', 'hook', 'claude'], input=payload,
			capture_output=True, text=True, timeout=10,
		)
	except (OSError, subprocess.SubprocessError):
		return None
	if not done.stdout.strip():
		return None
	try:
		got = json.loads(done.stdout)['hookSpecificOutput']['updatedInput']['command']
	except (ValueError, KeyError, TypeError):
		return None
	return got if isinstance(got, str) and got != command else None


def delegate(command: str) -> None:
	"""Hand the untouched payload to rtk and pass its verdict through unchanged."""
	payload = json.dumps({
		'hook_event_name': 'PreToolUse',
		'tool_name': 'Bash',
		'tool_input': {'command': command},
	})
	try:
		done = subprocess.run(
			['rtk', 'hook', 'claude'], input=payload,
			capture_output=True, text=True, timeout=10,
		)
	except (OSError, subprocess.SubprocessError):
		return
	if done.stdout.strip():
		sys.stdout.write(done.stdout)


def splittable(lines: list[str]) -> bool:
	"""True only when every line stands alone as a simple command. Anything else is rtk's to judge."""
	if len(lines) > MAX_LINES:
		return False
	for line in lines:
		if '<<' in line or BLOCK_KEYWORD.match(line) or CONTINUES.search(line):
			return False
		if line.count("'") % 2 or line.count('"') % 2:
			return False
	return True


def main() -> int:
	_raw, tool, tool_input, _session_id, _cwd = parse_stdin()
	if tool and tool != 'Bash':
		return 0
	command = str(tool_input.get('command', ''))
	if not command:
		return 0
	lines = command.split('\n')
	if len(lines) < 2 or not splittable(lines):
		delegate(command)
		return 0

	rewritten: list[str] = []
	changed = False
	for line in lines:
		stripped = line.strip()
		if not stripped or stripped.startswith('#'):
			rewritten.append(line)
			continue
		got = rtk_rewrite(stripped)
		if got is None:
			rewritten.append(line)
			continue
		# Keep the original indentation; rtk only ever prefixes the verb.
		rewritten.append(line[:len(line) - len(line.lstrip())] + got)
		changed = True
	if not changed:
		return 0

	updated = dict(tool_input)
	updated['command'] = '\n'.join(rewritten)
	print(json.dumps({'hookSpecificOutput': {
		'hookEventName': 'PreToolUse',
		'permissionDecisionReason': 'RTK auto-rewrite (multi-line)',
		'updatedInput': updated,
	}}))
	return 0


sys.exit(main())
