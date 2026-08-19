# Caveman
> The compression mode and the shell helper that switches it per session.
> feature: caveman

<!-- steps:start -->

## Caveman
> feature: `caveman` · agent: yes

Output compression (~65% saving on the agent's own output). **Vendored** into this workspace since
2026-07-23 — source of truth [`core/skills/caveman/`](core/skills/caveman/CONTEXT.md), upstream
credit [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). **Do not run the upstream
installer**: it overwrites the links with copies and re-forks the two installs. Needs Node ≥ 18.

**Precondition**
```bash
core/tools/wos/sync-global-skills --check
```

**Install**
```bash
core/tools/wos/sync-global-skills            # links ~/.agents/skills/caveman + ~/.claude/hooks/caveman-*
mkdir -p ~/.config/caveman && echo '{"defaultMode": "full"}' > ~/.config/caveman/config.json
```
On Windows the config half is:
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\caveman" | Out-Null
'{"defaultMode": "full"}' | Set-Content "$env:USERPROFILE\.config\caveman\config.json"
```

Then, if `~/.claude/settings.json` did not come across from the old machine, add its three entries:
`SessionStart` → `caveman-activate.js`, `UserPromptSubmit` → `caveman-mode-tracker.js`,
`statusLine` → `caveman-statusline.sh`. Values for the default mode: `lite`, `full`, `ultra`, `off`.

**Verify** — open a Claude Code session; the `[CAVEMAN] ⛏` badge appears in the statusline.

**Wiring a new agent.** Two mechanisms, and every agent uses one: **installed**, where session-start
hooks call `caveman-activate.js` (Claude Code), or **induced**, where a session-start shim reads
`~/.config/caveman/config.json` and injects the rules as context (Copilot, via
`core/hooks/copilot/copilot-session-start.py`). Both read the same config file, so one toggle
controls every agent. Follow the induced pattern by hand — upstream's
[INSTALL.md](https://github.com/JuliusBrussee/caveman/blob/main/INSTALL.md) is still the reference
for what a given agent needs, but never let its generator write into this workspace.

## Caveman shell helper
> feature: `caveman` · agent: yes

**Precondition**
```bash
grep -q "caveman-compress()" ~/.bashrc && echo "already appended"
```

**Install** — guarded by the precondition above; appending twice defines the function twice.
```bash
cat >> ~/.bashrc << 'EOF'

# caveman-compress shortcut
caveman-compress() {
  local CLAUDE_BIN
  CLAUDE_BIN="$(dirname "$CLAUDE_CODE_EXECPATH")"
  (cd /mnt/workspace/core/skills/caveman && PATH="$CLAUDE_BIN:$PATH" python3 -m scripts "$1")
}
EOF
source ~/.bashrc
```
```powershell
Add-Content $PROFILE @'

# caveman-compress shortcut
function caveman-compress {
    param([string]$File)
    $claudeBin = Split-Path $env:CLAUDE_CODE_EXECPATH
    Push-Location "$env:USERPROFILE\.claude\skills\caveman"
    $env:PATH = "$claudeBin;$env:PATH"
    python3 -m scripts $File
    Pop-Location
}
'@
```

**Verify**
```bash
type caveman-compress        # Expected: "caveman-compress is a function"
```

<!-- steps:end -->
