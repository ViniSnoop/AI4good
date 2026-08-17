# SPEC-DRIVE — Spec-Driven Development Rollout
> Enforcement rollout making the spec the contract for `code/` modules: verifiable inputs/outputs/invariants that precede and govern the code. Goal: [spec-driven-development](../brain/goals/spec-driven-development.md).

**Lifecycle: transient initiative doc** (ROADMAP-verify.md species — lives beside `code/CONTEXT.md`, not
workspace structure). Endstate: once the ratchet has converted the modules that matter and the
convention is durable in `code/SPECS.md` + `_templates/`, the surviving rules stay there and this file
is deleted (git keeps it). Sibling: [`ROADMAP-verify.md`](ROADMAP-verify.md) (the test-discipline rollout this extends).

**Origin:** assessment session 2026-07-17. The workspace had ~80% of the machinery (working `exit 2`
hook culture, mandatory `verify:fast`, spec-shaped Loop-0/3 artifacts, per-module contract idioms) but
**zero gated spec artifacts** — nothing forced spec-before-code. User's constraint: *"if not enforced it
will simply not happen"* = the workspace's own Principle 1 (ROADMAP-verify.md): **gate-or-injection, never
induction.** So the spine is a hard-blocking hook, not a convention doc.

---

## Principles (inherited from ROADMAP-verify.md + SDD-specific)

1. **Gate or injection — never induction.** The spec contract is enforced by `exit 2`, not advice.
2. **Spec precedes code.** A spec-locked module's SPEC.md is read before its code is edited; loop runs
   read the spec as pre-set criteria (Loop 0) and promote outcomes back into it (Loop 6).
3. **Ratchet, not big-bang.** Legacy modules are grandfathered; coverage grows as modules are touched.
   No wall of blocked commits.
4. **The spec is the contract.** `## Invariants` are the properties code may never violate; `## Examples`
   are the executable conformance cases, checked by the module's existing `verify:fast`.
5. **Per-module-directory granularity.** A module = a directory with a `CONTEXT.md`. Specs live beside it
   (`SPEC.md`), matching the existing idiom (`spacemantics/dsl/SPEC.md`, `isoroll-content/SCENE-CREATION.md`).

## The contract (SPEC v0)

`code/<project>/<module>/SPEC.md`, machine-parseable header + five sections. Skeleton:
[`_templates/module.SPEC.md`](_templates/module.SPEC.md). Documented in [`SPECS.md`](SPECS.md#module-spec-contract-spec-driven-development).

| Header key | Values | Effect |
|---|---|---|
| `status:` | `draft` \| `locked` | `locked` arms the read-gate for the module |
| `verify:` | `none` \| `make verify-fast` \| `npm run verify:fast` | how `## Examples` are mechanically checked |

A module is **spec-locked** when its `CONTEXT.md` carries `> spec: <path>` and the SPEC is `status: locked`.

## Enforcement surfaces

| Surface | Fires on | Behavior | Impl |
|---|---|---|---|
| `spec-read-gate.py` | Edit/Write of a spec-locked module's files | **exit 2** unless its SPEC.md was Read this session (nudge on new files in spec-less `code/` modules) | clone of `context-gate.py`; reuses `context-tracker.py` marker |
| pre-commit block **1d** | commit adding a new `CONTEXT.md` under `code/` | **exit 1** unless it declares `> spec: <existing file>` or `> spec: none` | clone of block 1c + known-bugs glob |
| `verify:fast` (block 1a) | commit with staged code | conformance rides it — a broken `## Examples` case is a red test = blocked | existing gate, unchanged |

Parity: wired in all three runtimes — Claude Code (`.claude/settings.json`), opencode
(`.opencode/plugins/workspace-policy.js`), Copilot (`.hooks/copilot-pre-tool.py`). Coverage rows in
[`core/hooks/SPECS.md`](../core/hooks/SPECS.md).

## The authoring side — the loop tree (2026-07-18)

The gates above guard the *output*. The *authoring workflow* that produces spec-first code is the
**`feature` subtree of the loop tree** ([core/flows/craft/tree.md](../core/flows/craft/tree.md),
[route.md](../core/flows/craft/route.md)). Its **Loop 3.5 Contract Layout** lays out every module's
`SPEC.md` + interface stubs + a type-matched connection graph *before* any code (checked by
`core/tools/spec-contract-check`), with an optional human sign-off configured in the Loop 0 permission
panel. A `feature` run is therefore what *fills the ratchet* — each shipped module leaves a locked spec.
Git Flow is enforced alongside (`.hooks/gitflow-gate.sh`, pre-commit 1e; see `SPECS.md` § Git Flow).

## Phases

### P0 — Format + pilot ✅ 2026-07-17
- `_templates/module.SPEC.md` v0 skeleton.
- `SPECS.md` § Module Spec Contract.
- Pilot: `spacemantics/dsl/SPEC.md` reshaped to v0 (`status: locked`, `verify: make verify-fast`); the
  rich language spec is preserved below as normative reference. `dsl/CONTEXT.md` carries `> spec: SPEC.md`.
  `make verify-fast` green (39 passed).

### P1 — The gates (enforcement) ✅ 2026-07-17
- `.hooks/spec-read-gate.py` + pre-commit block 1d + settings.json wiring; opencode + Copilot parity.
- Behavior-tested: block-when-unread, allow-after-read, exempt SPEC itself, out-of-scope pass, new-file
  nudge, and all four 1d branches (no-spec / optout / declared-missing / ok).

### P2 — Conformance rides verify:fast ◐ 2026-07-17 (convention set; extractor deferred)
- **Convention (done):** `## Examples` binds conformance in one of two modes — (a) *reference* existing
  test cases (the pilot does this: examples point at `tests/test_direction.py` etc., already run by
  `verify:fast`), or (b) *embed* literal input→output pairs for a future extractor to run.
- **Extractor (deferred):** `core/tools/spec-examples` (parse embedded `## Examples` → test cases) is
  **not built** — no spec embeds literal pairs yet, so it would have no consumer to test against (YAGNI).
  Build it when the first embedded-example spec lands; until then mode (a) already gives full conformance
  via the existing gate.

### P3 — Loop integration ✅ 2026-07-17
- `core/flows/craft/craft.md`: Loop 0 reads a spec-locked target module's SPEC.md and folds its
  `## Invariants` into `criteria:` (spec precedes). Loop 6 promotes the shipped chain's criteria/seams
  into the module's SPEC.md and sets `status: locked` before deleting `.loop/` (durable per-module
  contract). Loop 3's second-opinion verifier already audits criteria-coverage.

### P4 — Ratchet propagation + ledger ✅ 2026-07-17
- `_templates/CONTEXT.md` ships `> spec:` (default `none`, opt-in lock) so new projects are born aware.
- `core/tools/spec-scan` — the coverage ledger (`locked|draft|MISSING|optout|none` per module). Baseline
  at rollout: **1/88 locked** (spacemantics/dsl), 87 grandfathered.
- Hook table + coverage table rows (ENFORCED) — now `core/hooks/SPECS.md`.

## Open items

- Run `core/tools/spec-scan` in `/roundup` so coverage is visible each session.
- P2 extractor (`core/tools/spec-examples`) when a spec first embeds literal example pairs.
- Next lock candidates (highest signal): `isoroll-content` (has a Current-Workflow-Contract already),
  `spacemantics/checker` (once built — the natural home for the DSL's executable conformance).
- Consider extending the model to `core/flows` module dirs (SDD goal names them) — deferred: they have
  no `verify:fast` concept, so the conformance half needs separate design.

## Status log

| Date | Event |
|------|-------|
| 2026-07-17 | Plan approved (ratchet enforcement, spacemantics/dsl pilot). P0+P1+P3+P4 shipped; P2 convention set, extractor deferred. Gates live + tested in 3 runtimes. Baseline coverage 1/88. |
