# RTK
> Tool-output compaction, and registering it with each agent runtime that hooks.
> feature: rtk-compaction

<!-- steps:start -->

## RTK
> feature: `rtk-compaction` · agent: yes

[rtk-ai/rtk](https://github.com/rtk-ai/rtk) — a Rust CLI proxy that filters and compresses dev-command
output (git, test runners, docker) before it reaches an agent's context: 60-90% token savings.
Complementary to caveman, which compresses the agent's *own* output, not tool output. Apache 2.0,
single static binary, no deps.

**Precondition**
```bash
rtk --version && rtk gain --help >/dev/null && echo "rtk present"
```

**Install**
```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh   # → ~/.local/bin/rtk
```

⚠ **Name collision.** If `rtk gain` reports an unknown subcommand, the installed binary is
reachingforthejack/rtk (Rust Type Kit), a different tool with the same name. Check `which rtk`.

**Verify**
```bash
rtk gain            # a savings table, not an error
```

## RTK — Claude Code registration
> feature: `rtk-compaction` · agent: yes

**One registration, and it must be the shim.** Claude Code merges hooks across settings scopes and
runs *all* matches, so a project entry does not replace a global one; it runs beside it. The
workspace registers the shim **globally** and holds no `Bash` compact entry of its own, which also
covers sessions started inside nested `code/*` repos — those have no project settings and would
otherwise get line-1-only compaction.

**Why a shim at all: `rtk hook` reads the first line only.** A multi-line Bash payload gets one shot
at rewriting, and if line 1 is not rewritable — `cd` opens 23.4% of this workspace's Bash calls —
the whole call runs raw. [`core/hooks/compact/`](core/hooks/compact/CONTEXT.md) patches that.

**Precondition**
```bash
python3 -c "import json,pathlib; d=json.loads((pathlib.Path.home()/'.claude/settings.json').read_text()); \
print([h['command'] for e in d.get('hooks',{}).get('PreToolUse',[]) if e.get('matcher')=='Bash' for h in e['hooks']])"
# Expected when done: one entry ending in core/hooks/compact/bash-compact-rewrite.py
```

**Install** — idempotent; replaces any existing `Bash` entry rather than appending:
```bash
python3 - <<'PATCH'
import json, pathlib
p = pathlib.Path.home() / '.claude' / 'settings.json'
d = json.loads(p.read_text())
shim = 'python3 /mnt/workspace/core/hooks/compact/bash-compact-rewrite.py'
pre = d.setdefault('hooks', {}).setdefault('PreToolUse', [])
entry = next((e for e in pre if e.get('matcher') == 'Bash'), None)
if entry is None:
    pre.append({'matcher': 'Bash', 'hooks': [{'type': 'command', 'command': shim}]})
else:
    entry['hooks'] = [{'type': 'command', 'command': shim}]
p.write_text(json.dumps(d, indent=2) + '\n')
PATCH
```

**Verify** — end to end. **Config alone proves nothing, and this is the step that taught the whole
file that rule**: the wiring looked correct for weeks while it was dropping every multi-line call.
```bash
printf '%s' '{"hook_event_name":"PreToolUse","tool_name":"Bash","session_id":"probe",
"tool_input":{"command":"cd core\ngit status\nls -la"}}' \
  | python3 core/hooks/compact/bash-compact-rewrite.py
# expect: cd core / rtk git status / rtk ls -la  — lines 2 and 3 are what raw rtk drops
```

⚠ **Do not run `rtk init --global --auto-patch` on this machine.** It overwrites that `Bash` entry
back to `rtk hook claude`, silently reverting multi-line compaction. `rtk init --show` cannot tell
the two apart either — it reports `settings.json: RTK hook configured` for both, so a green line
there is not evidence the shim is wired. Use the probe above.

## RTK — other agents
> feature: `rtk-compaction` · agent: yes

Skip whichever agents you do not use; each is independent.

**Precondition** — `ls ~/.config/opencode/plugins/rtk.ts ~/.pi/agent/extensions/rtk.ts 2>/dev/null`

**Install** — opencode (global plugin only, no project-scoped variant exists):
```bash
rtk init --global --opencode        # writes ~/.config/opencode/plugins/rtk.ts
```
Coexists with this workspace's own `.opencode/plugins/workspace-policy.js` — separate files, both
auto-load.

Pi needs a manual peer-dependency fix; the generated extension does not work out of the box:
```bash
rtk init --agent pi --global
mkdir -p ~/.pi/agent/extensions && cd ~/.pi/agent/extensions
echo '{"name":"pi-extensions-peer-deps","private":true}' > package.json
npm install @earendil-works/pi-coding-agent
```
Why: the generated `rtk.ts` does `import type { ExtensionAPI } from "@earendil-works/pi-coding-agent"`,
but Pi's loader resolves it as a real `require()` — type erasure does not happen — and Node resolves
`node_modules` relative to the extension file's own directory, not to wherever `pi` is installed.
Without the local `node_modules` it fails with `Cannot find module`, even with the package installed
globally.

[Feynman](https://www.feynman.is/) is not on rtk's supported list but is built directly on Pi, with
its own `PI_CODING_AGENT_DIR` pointing the loader at `~/.feynman/agent`. Wired by parity, same
peer-dep gotcha:
```bash
mkdir -p ~/.feynman/agent/extensions
cp ~/.pi/agent/extensions/rtk.ts ~/.feynman/agent/extensions/rtk.ts
cd ~/.feynman/agent/extensions
echo '{"name":"feynman-extensions-peer-deps","private":true}' > package.json
npm install @earendil-works/pi-coding-agent
```

**Verify**
```bash
pi -e ~/.pi/agent/extensions/rtk.ts --no-session     # silence and exit 0 means loaded
```
Feynman has no `-e`/dry-run flag, so its only signal is the **absence** of `[rtk] rtk binary not
found` or `Failed to load extension` on the first real session's startup. Treat it as unverified.

**Using it.** Everything is rewritten transparently at zero token cost — `git status` becomes
`rtk git status` without anyone asking. Four commands have to be typed: `rtk gain` (savings),
`rtk gain --history`, `rtk discover` (missed opportunities), `rtk proxy <cmd>` (run raw, for
debugging the proxy itself). **Uninstall** (any target):
`rtk init --uninstall [--global] [--copilot|--opencode|--agent pi]`.

<!-- steps:end -->
