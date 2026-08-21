# Exit-2 fidelity probe: block with a PLAIN-TEXT stdout reason, to learn whether ZCode shows a
# non-JSON block reason to the agent (the canonical core/hooks gates emit plain text on exit 2).
# Registered only on a matcher for a sacrificial tool. Temporary — see probe.sh.
echo "PROBE-DENY-PLAIN: a razão em texto puro deste block deve chegar ao agente (exit 2)"
exit 2
