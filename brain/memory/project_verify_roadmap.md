---
name: project-verify-roadmap
description: Workspace verification/enforcement roadmap lives at code/VERIFY.md — check status there before verification/testing/hooks work
metadata: 
  node_type: memory
  type: project
  originSessionId: a27f5989-708e-425f-951b-f6713daa6830
  modified: 2026-07-25T22:35:59.555Z
---

code/VERIFY.md is the canonical plan for agent self-verification +
enforcement. As of 2026-07-02, phases W1, W2, W3, I1, I2, I3 are DONE: context-gate
hook suite live (whole workspace, Copilot parity), jscpd + verify:fast + BUGS
gates in global pre-commit, isoroll has verify:fast/verify:full with unit+e2e+golden
tiers on branch `feature/verify-harness` (NOT merged — Lucas decides). B32 mechanically
verified; B33 open (xfail spec); B2 narrowed to GridConfig path. Remaining: I4 unit
coverage expansion, A1 apptime adoption, opencode shim wiring, tsc type gate.
Read code/VERIFY.md status log + open items before any work touching .hooks/, tests, or
verification.
