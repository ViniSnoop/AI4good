---
name: project-isoroll-scene
description: "isoroll scene-creation program state — frozen renderer seam, MVP-first milestones, where the live plan lives"
metadata:
  node_type: memory
  type: project
  originSessionId: 330f2397-6922-4c4c-94e6-11c95c0fd1f2
  modified: 2026-07-30T02:47:01.321Z
---

Isoroll scene creation was REPLANNED 2026-07-29 (Lucas + inline) after stalling four review rounds deep in arm-A stair enclosure masks: a renderer seam is frozen (`DSL v2 → renderer → cell sprites + manifest → Foundry`) and the content strategy is now an A/B behind it (arm A kit-sprite / arm B scene-cell world-uv render / arm C NB-painted textures), never an architecture decision. Milestones SEAM → PLAYABLE → BAKEOFF → RICHNESS, MVP-first: ship playable-in-Foundry with deliberately ugly pixels and all 8+1 views BEFORE judging any look.

**Why:** the painter's ground truth is still the VOXEL GRID (Minecraft-underneath, layers 0-9, slice = source of truth) — Lucas's core design intent, do not regress to tile/sprite thinking. What changed is the *pixel source*: reusable sprite and true cross-tile continuity are mutually exclusive (proven from the code — world-absolute texcoords but module-local render origins), so continuity requires rendering each cell at its real world position. Look target is the Dead-Cells production model at Feather-3D / Tiny Glade level, NOT literal Hades (hand-painted, artist cost). Art cost is paid once at texture scale (~40 materials) and via meshes for props — never per tile. Anything that must rotate passes through geometry.

**How to apply:** ANY isoroll scene session reads `code/isoroll-content/ROADMAP.md` (the ONLY live-state file — strategy, decisions D1-D7, milestones) then `SCENE-CREATION.md` (status-free spec: seam, contract, kill-log) and `design/PAINTER-UX.md` (grammar rounds 1-19, frozen @ rig v16.2). Docs were restructured the same day: `ROADMAP-content-gen.md` and `SESSION-HANDOFF.md` are DELETED (absorbed into ROADMAP.md / HISTORY.md), `S4-REVIEW-ROUNDS.md` moved to `archive/` — do not look for them. Feel-rig artifact https://claude.ai/code/artifact/fce5e565-f376-4912-8ca7-7c19f6932ad4 (source `design/feel-rig/`, rebuild via build.py, republish SAME url). Gemini API key has NO image quota (limit:0) — web app or paid only. Related: [[project_hybrid_ideation]] [[fable_quota_strategy]] [[feedback_visual_eyeball_gate]]
