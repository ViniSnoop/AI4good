#!/usr/bin/env python3
# PreToolUse: Bash — send every line of a multi-line command through rtk, not just the first.
# rtk parses line 1 only, so `cd x\ngit status` reaches the context uncompacted; measured at
# 23.4% of Bash calls (first line is `cd`) plus 1,249 rewritable commands stranded on lines 2+.
# Delegates verbatim to `rtk hook claude` for every shape it cannot split safely.
import json
import os
import re
import shutil
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


def delegate(command: str) -> str:
	"""Hand the untouched payload to rtk and pass its verdict through unchanged.
	Returns the verdict for the counter; the caller has nothing else to do with it."""
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
		return 'no-rtk'
	if not done.stdout.strip():
		return 'delegated-noop'
	sys.stdout.write(done.stdout)
	try:
		json.loads(done.stdout)['hookSpecificOutput']['updatedInput']['command']
	except (ValueError, KeyError, TypeError):
		return 'delegated-noop'
	return 'delegated-rewrote'


def record(session_id: str, verdict: str, lines: int) -> None:
	"""One row per Bash call, so adoption is a number instead of a belief. This exact bug read as a
	flat zero for weeks with nothing watching — a lever with no standing metric is a lever nobody
	can tell is broken. Same store convention as hook_input.seen_file(): per session, in /tmp.
	Ephemeral on purpose; the trend belongs in core/experiments/, not in a file that churns git."""
	if not session_id:
		return
	# Overridable so the suite can assert on an isolated dir instead of the shared /tmp path,
	# and so a harness that owns its own state directory can point this at it.
	directory = os.environ.get('RTK_COMPACT_DIR', '/tmp')
	try:
		with open(f'{directory}/claude_rtk_compact_{session_id}.tsv', 'a') as handle:
			handle.write(f'{verdict}\t{lines}\n')
	except OSError:
		pass  # counting must never be able to break the command being counted


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
	_raw, tool, tool_input, session_id, _cwd = parse_stdin()
	if tool and tool != 'Bash':
		return 0
	command = str(tool_input.get('command', ''))
	if not command:
		return 0
	lines = command.split('\n')
	# Checked once, up front: rtk_rewrite() cannot tell "declined" from "not installed", so
	# without this the split path files a missing binary as `split-noop` — an idle shim and an
	# absent one would read identically, which is the exact ambiguity the counter exists to kill.
	if shutil.which('rtk') is None:
		record(session_id, 'no-rtk', len(lines))
		return 0
	if len(lines) < 2 or not splittable(lines):
		record(session_id, delegate(command), len(lines))
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
		record(session_id, 'split-noop', len(lines))
		return 0

	record(session_id, 'split-rewrote', len(lines))
	updated = dict(tool_input)
	updated['command'] = '\n'.join(rewritten)
	print(json.dumps({'hookSpecificOutput': {
		'hookEventName': 'PreToolUse',
		'permissionDecisionReason': 'RTK auto-rewrite (multi-line)',
		'updatedInput': updated,
	}}))
	return 0


sys.exit(main())
