#!/usr/bin/env python3
# UserPromptSubmit — say what the next turn costs, once per threshold crossed.
#
# The session cannot see its own size, so the decision to hand off is made blind and
# usually made late. This reads the size the API already reported on the last assistant
# turn (input + cache read + cache write) and announces the two thresholds in limits.env.
# Zero model tokens until a threshold is crossed, and it never blocks a prompt.
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from file_law import load_limits  # noqa: E402
from hook_input import parse_stdin  # noqa: E402

TAIL_BYTES = 512 * 1024

# Where /handoff leaves the resume prompt. The meter only names it; core/skills/handoff.md
# writes it, and test_meter_and_skill_name_the_same_artifact keeps the two from drifting.
# Under outputs/ because it is session-local and gitignored — never an UPPERCASE type
# (`HANDOFF.md` is off the core/SCHEMA.md allowlist, which is why it never existed).
HANDOFF_ARTIFACT = 'outputs/handoff.md'


def state_file(session_id: str) -> str:
	return f'/tmp/claude_ctx_meter_{session_id}.txt'


def announced(session_id: str) -> int:
	try:
		with open(state_file(session_id)) as f:
			return int(f.read().strip() or 0)
	except (OSError, ValueError):
		return 0


def mark(session_id: str, threshold: int) -> None:
	try:
		with open(state_file(session_id), 'w') as f:
			f.write(str(threshold))
	except OSError:
		pass


def find_transcript(raw: dict, session_id: str, cwd: str) -> str:
	"""The payload names it when it can; otherwise it is <cwd-slug>/<session_id>.jsonl."""
	given = raw.get('transcript_path')
	if given and os.path.isfile(given):
		return given
	slug = cwd.replace('/', '-')
	candidate = Path.home() / '.claude' / 'projects' / slug / f'{session_id}.jsonl'
	return str(candidate) if candidate.is_file() else ''


def last_context(path: str) -> int:
	"""Context carried by the most recent main-chain assistant turn, in tokens."""
	try:
		with open(path, 'rb') as f:
			f.seek(0, os.SEEK_END)
			f.seek(max(0, f.tell() - TAIL_BYTES))
			chunk = f.read()
	except OSError:
		return 0
	for line in reversed(chunk.split(b'\n')):
		if b'"usage"' not in line:
			continue
		try:
			event = json.loads(line)
		except (json.JSONDecodeError, UnicodeDecodeError):
			continue
		if event.get('type') != 'assistant' or event.get('isSidechain'):
			continue
		usage = (event.get('message') or {}).get('usage') or {}
		if not usage:
			continue
		return (usage.get('input_tokens', 0)
		        + usage.get('cache_read_input_tokens', 0)
		        + usage.get('cache_creation_input_tokens', 0))
	return 0


def message(ctx: int, crossed: int, loud: int) -> str:
	size = f'{ctx // 1000}k'
	if crossed >= loud:
		return (f'CONTEXT {size} — past the hand-off mark. Every further turn re-reads all '
		        f'of it, so this thread now costs ~3x a fresh one for the same work. Run '
		        f'/handoff now: it writes {HANDOFF_ARTIFACT}, so a resume point exists even '
		        f'if this session dies. Then finish the current thread, run /roundup, and '
		        f'open the next window with: Read {HANDOFF_ARTIFACT} and continue.')
	return (f'CONTEXT {size} — past the point where turn cost starts climbing. Nothing is '
	        f'wrong; just pick a hand-off point while the work is still divisible, rather '
	        f'than mid-thread later.')


def main() -> None:
	raw, _tool, _tool_input, session_id, cwd = parse_stdin()
	path = find_transcript(raw, session_id, cwd)
	if not path:
		return
	ctx = last_context(path)
	limits = load_limits()
	warn, loud = limits.get('CTX_WARN', 0), limits.get('CTX_LOUD', 0)
	crossed = max((t for t in (warn, loud) if t and ctx >= t), default=0)
	if not crossed or crossed <= announced(session_id):
		return
	mark(session_id, crossed)
	print(message(ctx, crossed, loud))


if __name__ == '__main__':
	try:
		main()
	except Exception:
		pass  # a meter must never cost a prompt
	sys.exit(0)
