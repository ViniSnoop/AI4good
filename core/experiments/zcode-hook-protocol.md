# ZCode hook protocol
> Will ZCode execute this workspace's hook registration in `.zcode/config.json`, and what does a fired hook actually
> receive?

## Method

Register probe hooks in `.zcode/config.json` (`hooks.enabled: true`, all four usable events,
no matcher): `core/hooks/zcode/probe.sh` dumps stdin + filtered env + cwd + ppid to
`/tmp/zcode_probe/`; `probe-deny.sh` (plain-text stdout + exit 2) rides a sacrificial
`WebFetch` matcher. Run the battery in a fresh ZCode session: Read, Bash, Write, Edit, Agent
(Explore subagent), WebFetch, prompt submit. Measurement = dump files present per event +
verbatim block text for WebFetch. Re-run after any trust/config change; instruments stay in
`core/hooks/zcode/`.

## Results

| Date | Run | Hooks fired | WebFetch blocked | Verdict |
|---|---|---|---|---|
| 2026-08-21 | Sonda 1 — fresh scheduled session, config created mid-session of another | **0** (`/tmp/zcode_probe/` never created) | no (deny never ran) | config read + parsed, execution blocked by workspace-trust gate |

Run detail (2026-08-21, ZCode 3.8.1):

- Config accepted: diagnostics name `/mnt/workspace/.zcode/config.json`, scope `project`,
  path `hooks` — schema valid, `enabled: true` honored as a flag.
- Blocker, logged at every session event:
  `config.project_hooks.pending_trust` (adapters.config) — *"Project hooks are pending
  workspace trust and remain blocked"*. Not a matcher miss: nothing executed at all.
- Trust state is not agent-writable: absent from `~/.zcode/v2/setting.json`,
  `~/.zcode/v2/config.json`, and `~/.zcode/cli/db/db.sqlite` (`local_setting` holds only
  `permission.mode=yolo`, `model.reasoningLevel`; `permission` table empty). Client-UI
  acceptance, once per machine.
- Config is evaluated per fresh session, not per tool call, not mid-session (main session
  that authored the config never saw it; the scheduled session did; a user-scope config
  created mid-session was likewise ignored).
- `zcode` binary is the Electron desktop launcher — no headless session spawn from Bash.
- Doc discrepancy: zcode-plugin skill `diagnosing-hooks` claims non-plugin config hooks have
  "no trust gate … run unconditionally" — contradicted for project scope by this run. User
  scope untested (a user-scope probe config was created for a Sonda 2, then removed without
  running: its WebFetch-deny would block every workspace).

## What changed

- `.zcode/config.json` now carries the production registration (direct spawns of the
  canonical `core/hooks/*` scripts, absolute paths, mirroring `.claude/settings.json`) —
  **inert until the workspace is trusted**; one-time `agent: no` step recorded in
  `SETUP.md`.
- `core/hooks/zcode/` holds the probe instruments; `test_shim_paths.py` gained the `zcode`
  entry (path-resolution check passes).
- The adapter-vs-direct decision is deferred to the first post-trust run: if plain-text
  stdout on exit 2 does not reach the agent, `core/hooks/zcode/zcode-hook.py` replaces the
  direct registration.

## Limitations

- No hook has ever executed under ZCode on this machine — payload shape (stdin schema,
  `session_id` presence), exit-2 message fidelity, and `${CLAUDE_PROJECT_DIR}` expansion
  are all `—`, measured by nobody. The 2A direct registration rests on documentation plus
  Claude-Code symmetry, not on a fired hook.
- One machine, one ZCode version (3.8.1, Linux); the trust gate's UI wording/flow was not
  observed, only its log signature.
- Sonda 1 could not separate "config re-read at session start" from "diagnostics emitted per
  event" — both are consistent with the log.
