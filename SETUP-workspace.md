# Workspace substrate
> The path, the venv, the declared deps, the git hook and the executable bits. Nothing else runs
> until these do: the first two steps install what every feature RUNS ON and so join to no registry
> row, which is what `> substrate: yes` declares.
> feature: declared-deps, git-hooks

<!-- steps:start -->

## Workspace path
> substrate: yes · agent: yes

Every tool under `core/tools/` runs on `#!/mnt/workspace/.venv/bin/python3`, because the venv holds
the declared dependencies and the system interpreter holds none of them. A shebang cannot resolve a
relative path, so that prefix is absolute — and a clone living anywhere else must rewrite it. **Run
this step first**: every later Verify probe calls a tool.

**Precondition** — if the workspace is at `/mnt/workspace`, this step is already done, permanently:
```bash
test "$PWD" = /mnt/workspace && echo "already correct"
```

**Install** — rewrite the shebangs to this clone's own path. Idempotent: re-running rewrites the
same line to the same value.
```bash
grep -rl '^#!.*/\.venv/bin/python3$' core/tools | \
  xargs sed -i "1s|^#!.*/\.venv/bin/python3$|#!$PWD/.venv/bin/python3|"
```

**Verify** — no tool points anywhere but this clone:
```bash
for f in $(find core/tools -type f ! -name "*.*"); do head -1 "$f"; done | sort -u
# Expected: only "#!/usr/bin/env bash" and "#!$PWD/.venv/bin/python3"
```

Substitute your real path for `/mnt/workspace` in every command below, too.

## The venv
> substrate: yes · agent: yes

One virtualenv at the workspace root, shared by every tool and the test suite. Nothing here is
per-project — `code/*` repos own their own environments.

**Precondition**
```bash
.venv/bin/python3 --version        # a version line means the venv exists
```

**Install**
```bash
python3 -m venv .venv              # no-op if .venv already exists
.venv/bin/pip install --upgrade pip
```

**Verify**
```bash
.venv/bin/python3 -c "import sys; print(sys.prefix)"
# Expected: the workspace's own .venv path, not /usr
```

## Declared dependencies
> feature: `declared-deps` · agent: yes

Every external dependency the tool surface needs is declared in
[`core/tools/deps.txt`](core/tools/deps.txt) with its install command, its probe, and **what its
absence looks like**. That last column exists because these were found the expensive way: four
were installed by hand into `.venv` and never written down, so a fresh clone lost the feature
*silently* — the tool returned a worse answer instead of an error. One cost a full session.

**Precondition** — this is the whole step's precondition, install plan, and probe in one command:
```bash
core/tools/wos/deps            # every dep, ok/MISSING, with the install line for each miss
```

**Install** — run what it printed. Rows marked `apt` need `sudo`; if you cannot get it, that is the
one part to hand to Lucas, naming the package and the `breaks` line the tool printed beside it.

**Verify**
```bash
core/tools/wos/deps --check    # exit 0 = nothing missing
```

Adding a tool with a new third-party import fails `make verify-fast` until it is declared here.
The rule and its stated limit: [`core/tools/SPECS.md`](core/tools/SPECS.md) § Declared dependencies.

## Git hook
> feature: `git-hooks` · agent: yes

Applies `core/hooks/pre-commit` to **every** git repo on the machine — that global reach is the
point, since projects under `code/` are their own repos.

**Precondition**
```bash
git config --global core.hooksPath        # already-set means done; expected: <workspace>/core/hooks
```

**Install**
```bash
git config --global core.hooksPath "$PWD/core/hooks"
```

**Verify** — the path resolves to a real dispatcher, not just a string:
```bash
test -f "$(git config --global core.hooksPath)/pre-commit" && echo "hook reachable"
```

## Executable bits
> feature: `git-hooks` · agent: yes

Git carries the execute bit, so a normal clone arrives correct. This step exists for the cases that
do not: an archive export, a copy across a filesystem that drops modes, or a `umask` that strips it.

**Precondition**
```bash
test -x core/hooks/pre-commit && test -x core/hooks/post-edit.sh && echo "bits already set"
```

**Install** — idempotent by nature:
```bash
chmod +x core/hooks/post-edit.sh core/hooks/read/pre-read.sh core/hooks/pre-commit \
         core/hooks/checks/check-line-counts.sh core/hooks/copilot/copilot-agent.sh \
         core/hooks/session/start-session.sh core/tools/wos/deps
```

**Verify**
```bash
find core/hooks core/tools -type f \( -name "*.sh" -o ! -name "*.*" \) ! -perm -u+x
# Expected: no output. Any line is a file that will fail to run.
```

The `.py` hooks are invoked through `python3` and need no execute bit.

<!-- steps:end -->
