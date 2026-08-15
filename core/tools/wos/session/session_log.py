# session_log.py — replay a Claude Code transcript and attribute each turn's context growth.
#
# The reusable half of core/tools/wos/context. Sibling `usage` reads the same *.jsonl for cost and
# should adopt this walk rather than keeping its own loop.
#
# Two honesty rules, both load-bearing:
#   1. Per-turn context is exact (the usage fields); what *entered* is known only in characters. So
#      the chars-per-token ratio is measured per turn, never a global /4 constant. A measured ratio
#      well under ~3.5 means material enters that the transcript does not log, and the caller must
#      say so — see `context`'s header note, which prints it.
#   2. A blocking gate is a failed tool_result, never an attachment. Scanning only attachments
#      found 1 CONTEXT GATE firing where there are 518.
import json
from collections import defaultdict
from pathlib import Path


def label(att: dict) -> str:
	"""One source name per injected block. Hooks carry their event, so they can be told apart."""
	kind = att.get('type', '?')
	if kind.startswith('hook_'):
		return f"hook {att.get('hookName') or att.get('command', '')[:30]}"
	return kind.replace('_', ' ')


def blocks(message: dict) -> list:
	content = (message or {}).get('content')
	return content if isinstance(content, list) else [{'type': 'text', 'text': content or ''}]


def walk(path: Path) -> dict:
	"""Replay one transcript: what entered before each turn, and what that turn's context measured."""
	tool_of: dict = {}
	pending: dict = defaultdict(int)
	seen: set = set()
	turns: list = []
	reads = gates = prev = 0

	for line in path.open(errors='replace'):
		try:
			event = json.loads(line)
		except json.JSONDecodeError:
			continue
		if event.get('isSidechain'):
			continue
		kind = event.get('type')

		if kind == 'attachment':
			att = event.get('attachment') or {}
			pending[label(att)] += len(json.dumps(att))
		elif kind == 'user':
			for block in blocks(event.get('message')):
				if block.get('type') != 'tool_result':
					pending['user prompt'] += len(json.dumps(block))
					continue
				name = tool_of.get(block.get('tool_use_id'), '?')
				body = json.dumps(block.get('content'))
				pending[f'tool {name}'] += len(body)
				gates += block.get('is_error') is True and 'CONTEXT GATE' in body
		elif kind == 'assistant':
			message = event.get('message') or {}
			for block in blocks(message):
				if block.get('type') != 'tool_use':
					continue
				target = str((block.get('input') or {}).get('file_path', ''))
				is_ctx = block.get('name') == 'Read' and target.endswith('CONTEXT.md')
				tool_of[block.get('id')] = 'ctxread' if is_ctx else block.get('name', '?')
				reads += is_ctx
			usage = message.get('usage') or {}
			request = event.get('requestId')
			if not usage or (request and request in seen):
				continue
			seen.add(request)
			context = (usage.get('input_tokens', 0) + usage.get('cache_read_input_tokens', 0)
			           + usage.get('cache_creation_input_tokens', 0))
			turns.append((context - prev, dict(pending)))
			prev = context
			pending.clear()
			pending['assistant output'] = len(json.dumps(message.get('content')))

	return {'turns': turns, 'reads': reads, 'gates': gates, 'peak': prev}


def attribute(session: dict) -> tuple:
	"""Split turn 1 and the growth after it into tokens per source, self-calibrating per turn."""
	turns = session['turns']
	if not turns:
		return {}, {}, 0, 0.0
	body = [(d, p) for d, p in turns[1:] if d > 0 and sum(p.values())]
	chars = sum(sum(p.values()) for _d, p in body)
	tokens = sum(d for d, _p in body)
	if not tokens:
		return {}, {}, turns[0][0], 0.0
	per_token = chars / tokens

	start = {k: v / per_token for k, v in turns[0][1].items()}
	growth: dict = defaultdict(float)
	for delta, parts in body:
		ratio = delta / sum(parts.values())
		for name, size in parts.items():
			growth[name] += size * ratio
	return start, growth, turns[0][0], per_token


def median(values: list) -> float:
	ordered = sorted(values)
	return ordered[len(ordered) // 2] if ordered else 0.0
