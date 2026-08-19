# Portability and clonability
> A fresh clone gets every feature: declared deps, no undocumented hand-installs.
> priority: essential

## Front 10 — Portability & clonability — **v1 criterion 4**

> **Ruled 2026-08-16 (Lucas); every ruling is recorded where it is enforced, not here.** The harness
> is the installer and `SETUP.md` is the prose it executes — [`core/SCHEMA.md`](core/SCHEMA.md)
> § The `.md` type system. The registry's grouping, its columns, and the fact that `scope` **is** the
> general/Lucas-specific line (a column the sync reads, not a document) are declared in the header of
> [`core/features.txt`](core/features.txt) itself; the rule behind it is
> [`core/SPECS-features.md`](core/SPECS-features.md) § AD-14.

**Criterion 4 is met and the registry is live.** A feature whose `wired` column reads `-` cannot be
switched off, so **the ablation cannot report on it**. Wiring one is calling
`feature_law.is_enabled()` where the rule is enforced and naming that file in the column. Read the
count from `core/tools/wos/features --findings`, never from here — and the target is zero with **no
exceptions left**: the `n/a` column is empty, because the rows that carried it were category errors
rather than hard cases (`core/SPECS-features.md` § AD-14).

**The backlog is down to `telegram-capture`, and it is not mechanical** — it is item 6 below. Every
other row's guard was verified by running the feature both ways, never by grepping for the slug.

`skills` share one wiring point in the mirror, because a skill is markdown and the only real switch
is the mirror declining to publish it; a **tool** is a CLI this workspace writes, so it has a moment
of its own and guards at invocation, which buys a per-row behavioural answer instead of one answer
for the group.

**A feature that fires at two moments takes two paths, and the exception proves the rule.** Where the
two moments already share a program the guard goes in the program and one path is honest —
`routing-tables` is `context_synchronizer.py`, reached from both pre-commit and post-edit. Where they
do not, both fragments are named: `interface-stubs` and `lint-typescript` each keep a commit-time
half that stages or blocks and an edit-time half that keeps the artifact current, and guarding one
leaves the other writing. **`gates/project-contract.sh` hosts three features in one file**, so the
slug-names-the-file rule cannot apply there; that is a finding, not a rename to force.

**`norms` is live** — `core/norms/<slug>.md`, published into `AGENTS.md`'s generated rule block by
`core/hooks/routing/norms.py`, which is also the group's one switch. Rule order comes from the
registry, so moving a rule up the prompt means moving its row. Contract:
[`core/SCHEMA-layers.md`](core/SCHEMA-layers.md) § Layer: norm.

**`agents` and `flows` still have no rows**, and the seam is a *rendering* mirror rather than the
symlink one skills use. Ruled 2026-08-18 (Lucas): extend the mirror, not the read gate. Grounding
found the layer carries a **double asymmetry** the extension has to resolve first:

- `core/agents/` holds five research agents (`lead`, `researcher`, `writer`, `verifier`, `reviewer`)
  mirrored **nowhere** — they are file contents pasted as a system prompt, not spawnable agent types.
- `.claude/agents/craft-{high,medium,low}.md` and `.opencode/agents/craft-*.md` are hand-written
  **twice with no source in `core/`**, while [`core/SCHEMA-layers.md`](core/SCHEMA-layers.md) § Layer: agent calls
  them mirrors and states *"There is no generator, so keep each mirror's `model:` in sync with its
  source `tier:` by hand."*

**The two mirrors diverge on purpose**, which is why a symlink cannot serve: Claude Code's carries
`model: opus`, opencode's carries **no** `model:` line (stripped per the agnostic principle) plus
`mode: subagent`. So the work is one source per agent carrying `tier:`, and a generator resolving
`tier` → per-runtime frontmatter from [`core/flows/craft/routing.md`](core/flows/craft/routing.md) —
which deletes a documented hand-sync hazard as a side effect, and makes the five research agents
spawnable for the first time.

**Flows have no mirror location at all**, and that is the open question, not an oversight: a skill
names `core/flows/craft/*.md` by literal path, so publishing flows means moving where every skill
points. Decide that before building, because the pointer rewrite is the whole cost.

**Not built at the tail of the drain session it was scoped in** — it sits on `/craft`'s live spawn
path, and a frontmatter mistake breaks spawning until something catches it. → **tier: medium**,
agents first, flows after the pointer question is answered.

5. 🟡 **the public scaffold repo and its one-way sync.** A **separate public repository**, not a
   branch — personal history never leaves this repo, where a branch would carry every commit that
   ever touched `brain/`. That is what makes the general/Lucas-specific line checkable on every run
   instead of documented.

   **Ruled 2026-08-16 (Lucas), both open questions closed:**
   - **`brain/` crosses as empty structure** — `CONTEXT.md`, an empty `INBOX.md` and `GOALS.md`, one
     example goal file. No real goals, no `USER.md`, no attachments. The brain system is half the
     value of WOS; shipping `core/` alone hands someone an enforcement layer with nothing to enforce
     on. An example rich enough to look like real personal data is the thing to avoid.
   - **Sync is one-way, contributions land as INBOX entries.** The script pushes private → public
     and nothing auto-flows back. A useful PR is read and re-implemented here by hand, captured
     through `brain/INBOX.md` like every other input. The private repo stays the single source of
     truth, and contribution stays honest rather than blocked.
   - **The public checkout lives at `code/wos/`**, as a nested repo like every other project. Lucas:
     *"maybe a good idea is for us to have it here as a code repo under `code/wos/` so it is easy to
     monitor it. this workspace repo is private, mine and only I use it amongst my machines (two
     laptops), and the public is for my students and anyone else."* Still its own repository with its
     own history — that is what keeps personal commits from crossing — this only fixes where the
     working copy sits. It pays twice: the sync becomes an ordinary write into a tree that can be
     `git diff`ed **before** anything is pushed, so **the allowlist is reviewable as a diff rather
     than trusted as a script**; and the public repo inherits the gates, since `core/hooks` is wired
     globally and fires in every nested repo. Mechanically free — `code/wos` joins the `code/*`
     ignore list like `aiwbot` and `apptime`, so no gitlink forms.

   **It has real users now, and they change the shape** (Lucas, INBOX 2026-08-17): *"tive algumas
   reuniões com alunos hoje, quero que todos eles usem algum setup com HARNESS + uma versão desse
   workspace que contemple pelo menos o ramo da pesquisa e produção de artigos."* So the public repo
   stops being only the ablation's precondition and becomes a deliverable with a deadline shaped by
   his teaching. It also names the **minimum useful subset**: the research and paper-writing branch,
   not the whole scaffold. Second, separable deliverable: a **prompt in Portuguese** for students to
   paste into whichever harness they use, letting them and the harness decide what to adopt — his
   words, so it stays Portuguese, and it is the one artifact here that is not English by rule.

   The features file (step 4) ships as scaffold — it is the thing that makes a subset installable — with
   the profile replaced by a placeholder on the way out. **The sync's allowlist is the deliverable**,
   not the copy: a path that is not on it does not travel, so adding a new top-level directory fails
   closed.
   → **tier: medium**.

6. 🔴 **`code/aiwbot` lives in its own repo and that is why one feature cannot be switched off.**
   `telegram-capture` is the last row reading `-`, and every wiring available today is wrong rather
   than merely awkward: a `code/aiwbot/...` path in the column makes this repo's Tier 0 test assert
   on a nested repo's content, which Front 4 forbids for a reason this repo cannot fix; reopening
   `n/a` contradicts the ruling that the column is empty. So the row is blocked on a question about
   where the code lives, not on wiring effort. **`core/features.txt` now says exactly that in its
   own header** — it claimed the opposite for a day, and the page reading `1 of 69` beside a header
   claiming no exceptions left is what caught it.

   Lucas, 2026-08-18: *"aiwbot is part of WOS, it is deeply entangled, it is not meant for general
   purpose bots… maybe we could version it inside the WOS repo and delete the aiwbot repo."*

   **For absorbing it:** the seam becomes an ordinary in-process guard; the gates already fire there
   through the global `core.hooksPath`, so nothing is lost; one less repo to keep on a legal branch
   and pushed; and the registry reaches zero without an exception.
   **Against:** the public scaffold sync would have to exclude it by allowlist rather than by it
   living elsewhere, which moves a boundary that currently cannot be got wrong; a bot token and a
   systemd unit are machine state, and `SETUP.md` already carries them; and aiwbot has its own verify
   suite, its own history and its own `AgentBackend` seam, which is exactly the shape `code/*` is for.

   **The tie-breaker to settle first is the public repo**, not the wiring: if the scaffold ships the
   research and paper-writing subset, whether a Telegram bridge is inside the workspace or beside it
   is answered by what a student clones. Decide that, and this row decides itself.
   → **tier: high**, one sitting.

---
