# session_cost.py — the price of a turn. The one place rates live.
#
# Split out of `usage` on 2026-08-15 so `context` can rank sources by spend instead of by token
# count. The two are different rankings: a cache-read token is 0.1x a fresh input token, so a
# source that arrives once and is re-read for the rest of the session costs far less than its
# token share suggests.
#
# Rates come from the claude-api skill — update them there and here together.

# USD per million tokens: (input, output). Cache write is 1.25x input at the 5m TTL and 2x at 1h;
# cache read is 0.1x.
RATES = {
	'claude-fable-5': (10.0, 50.0),
	'claude-opus-5': (5.0, 25.0),
	'claude-opus-4-8': (5.0, 25.0),
	'claude-sonnet-5': (3.0, 15.0),
	'claude-haiku-4-5-20251001': (1.0, 5.0),
}


# The billed components, cheapest-to-read order. `output` is the only one the agent authors
# directly; the rest are what re-reading it costs, which is why the split is worth printing.
COMPONENTS = ('input', 'write_1h', 'write_5m', 'cache_read', 'output')


def turn_components(model: str, usage: dict) -> dict:
	"""What one turn cost, split by what was billed. turn_cost is the sum of this."""
	rate_in, rate_out = RATES.get(model, (5.0, 25.0))
	made = usage.get('cache_creation') or {}
	write_1h = made.get('ephemeral_1h_input_tokens', 0)
	write_5m = made.get('ephemeral_5m_input_tokens', 0)
	if not (write_1h or write_5m):
		write_5m = usage.get('cache_creation_input_tokens', 0)
	return {
		'input': usage.get('input_tokens', 0) * rate_in / 1e6,
		'write_1h': write_1h * rate_in * 2.0 / 1e6,
		'write_5m': write_5m * rate_in * 1.25 / 1e6,
		'cache_read': usage.get('cache_read_input_tokens', 0) * rate_in * 0.1 / 1e6,
		'output': usage.get('output_tokens', 0) * rate_out / 1e6,
	}


def turn_cost(model: str, usage: dict) -> float:
	return sum(turn_components(model, usage).values())
