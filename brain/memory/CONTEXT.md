# memory
> What the agent learned across sessions and nothing else records. Harness-written, workspace-owned.

**The harness path is a symlink into here** — `~/.claude/projects/<slug>/memory` →
`brain/memory/` — so every memory written by the agent lands in the workspace by construction,
shows up in `git status`, and can be trimmed like any other file. This gives both properties at
once: **locality** (the content is in the repo) and **control** (we can edit or delete
it). Per-file symlinks would have given only the first, leaving each *new* memory outside until
someone adopted it.

What cannot be controlled is the agent *deciding* to write one. That is fine — it lands in a diff.

| File | Role |
|------|------|
| `MEMORY.md` | The index. One line per memory; loaded into every session, so its length is a real cost (~1,198 tok — measured, see below). |
| `<slug>.md` | One fact each, with `name` / `description` / `metadata.type` frontmatter. |
| `user_profile.md` | A symlink to [`../USER.md`](../USER.md) — the profile is workspace content first and a memory second. |

Types are `user` · `feedback` · `project` · `reference`. Bodies link to each other with `[[name]]`,
and a `[[name]]` with no matching file is allowed on purpose: it marks a memory worth writing.
That is why `test_pointer_integrity` gates `](path)` links here but **not** `[[slug]]` ones.

**Known asymmetry, not yet fixed:** six `name:` fields use snake_case where the rest use kebab, and
`project_hybrid_ideation.md` declares `name: project-cria`, matching no filename. Harmless while
`[[slug]]` is ungated; it is what would have to be settled first to gate it.

**Cost, measured rather than assumed:** the index is ~1,198 tok of a ~27.6k session start, less than
half the skill listing. The long-standing suspicion that this store duplicates `USER.md` + `goals/`
enough to be worth folding was tested and **rejected on the numbers** —
[`core/experiments/context-window.md`](../../core/experiments/context-window.md).

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`MEMORY.md`](MEMORY.md) | Memory Index |
| [`fable_quota_strategy.md`](fable_quota_strategy.md) | How Lucas spends remaining Fable 5 quota (won't renew) — Fable decides, Opus… |
| [`feedback_agent_runs_auth.md`](feedback_agent_runs_auth.md) | Agent runs every auth command itself; Lucas only does what has no command form… |
| [`feedback_background_bash_reliability.md`](feedback_background_bash_reliability.md) | Backgrounded Bash tool calls (run_in_background) can die silently across a… |
| [`feedback_bug_tracking.md`](feedback_bug_tracking.md) | isoroll-module bugs go in BUGS.md, not memory |
| [`feedback_delete_weak_features.md`](feedback_delete_weak_features.md) | Lucas deletes a feature that only produces weak signal rather than keeping it as… |
| [`feedback_full_workflow_thinking.md`](feedback_full_workflow_thinking.md) | plan isoroll (and similar) work from the full user workflow, not from artifacts… |
| [`feedback_inbox_ref_task_pairing.md`](feedback_inbox_ref_task_pairing.md) | /inbox — an actionable ref must also spawn an assessment task, never land as… |
| [`feedback_parallel_sessions.md`](feedback_parallel_sessions.md) | How to work safely when multiple Claude/opencode sessions edit /mnt/workspace at… |
| [`feedback_plain_language.md`](feedback_plain_language.md) | Write WOS in plain words — Lucas loses the thread when jargon accumulates, and… |
| [`feedback_provider_agnostic_naming.md`](feedback_provider_agnostic_naming.md) | Never put provider/model names (NB, Gemini, etc.) in file names, verbs, or dirs… |
| [`feedback_visual_eyeball_gate.md`](feedback_visual_eyeball_gate.md) | Every image-producing pipeline step needs Lucas's visual review (artifact board)… |
| [`project_aiwbot.md`](project_aiwbot.md) | provider-agnostic bot to drive swappable coding agents (claude/opencode/copilot)… |
| [`project_casinhas.md`](project_casinhas.md) | Obra das casinhas (7 casas + 3 salas, Várzea/Recife, com o pai) — home em… |
| [`project_core_schema.md`](project_core_schema.md) | core/ agent-library soundness work — enforced frontmatter contract, tier… |
| [`project_dobra.md`](project_dobra.md) | Dobra — context folding + SLM runner project (code/dobra) with paper twin… |
| [`project_hybrid_ideation.md`](project_hybrid_ideation.md) | cria — workflow de ideação híbrida humano-IA como mechanism design; AI4Good… |
| [`project_instituto.md`](project_instituto.md) | Programa do instituto tem cockpit em branches/instituto/ — 5 núcleos de fluxo de… |
| [`project_isoroll_scene.md`](project_isoroll_scene.md) | isoroll scene-creation program state — frozen renderer seam, MVP-first… |
| [`project_spacemantics.md`](project_spacemantics.md) | spacemantics project — verifiable spatial DSL giving LLMs spatial capability; 4… |
| [`project_verify_roadmap.md`](project_verify_roadmap.md) | Workspace verification/enforcement roadmap lives at code/ROADMAP-verify.md … |
| [`project_wos_fanout_split.md`](project_wos_fanout_split.md) | core/hooks and core/tools split into families 2026-07-31 (every CLI path… |
| [`project_wos_zero_roadmap.md`](project_wos_zero_roadmap.md) | Zerar o ROADMAP do WOS = SHIPPAR tudo, não deletar — pós-v1 Lucas rejeitou… |
| [`reference_linuz90_bot.md`](reference_linuz90_bot.md) | linuz90/claude-telegram-bot source read — the reference design for aiwbot; how… |
| [`reference_texpace_is_spacemantics.md`](reference_texpace_is_spacemantics.md) | texpace" routes to the spacemantics project — same thing for /inbox routing |
| [`user_profile.md`](user_profile.md) | Lucas — read before any Brain task. |
<!-- routing:end -->
