#!/usr/bin/env python3
# PreToolUse: Bash — close the cat/head/grep bypass: extract workspace file paths from the
# command string and apply the same CONTEXT.md chain gate as context-gate.py.
# Known residual hole: dynamically constructed paths escape. See VERIFY.md W1.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chain import context_chain, paths_in
from hook_input import is_subagent, load_seen, parse_stdin


def main() -> int:
	raw, tool, tool_input, session_id, cwd = parse_stdin()
	if tool and tool != 'Bash':
		return 0
	if is_subagent(raw):
		return 0
	command = str(tool_input.get('command', ''))
	if not command:
		return 0
	seen = load_seen(session_id)
	unseen: list[str] = []
	for path in paths_in(command, cwd, files_only=True):
		for ctx in context_chain(path):
			if str(ctx) not in seen and str(ctx) not in unseen:
				unseen.append(str(ctx))
	if not unseen:
		return 0
	print('CONTEXT GATE (Bash) - command touches files in a subtree whose context', file=sys.stderr)
	print('is not loaded. Read these CONTEXT.md files with the Read tool, then retry:', file=sys.stderr)
	for ctx in sorted(unseen):
		print(f'   {ctx}', file=sys.stderr)
	return 2


sys.exit(main())
