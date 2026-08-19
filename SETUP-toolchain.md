# Language toolchains
> Interface generators and linters: stubgen, tsc, ESLint/Prettier, LaTeX.
> feature: interface-stubs, lint-typescript, latex

<!-- steps:start -->

## Python interfaces — stubgen
> feature: `interface-stubs` · agent: yes

Generates the `.pyi` stubs the read gate hands an agent instead of a source file.

**Precondition**
```bash
.venv/bin/stubgen --version
```

**Install**
```bash
.venv/bin/pip install mypy
```

**Verify** — it must actually produce a stub, not merely answer `--version`:
```bash
.venv/bin/stubgen -o /tmp/stubprobe core/hooks/file_law.py && head -3 /tmp/stubprobe/file_law.pyi
```

## TypeScript interfaces — tsc
> feature: `interface-stubs` · agent: yes

**Precondition**
```bash
tsc --version || ~/.local/bin/tsc --version
```

**Install** — needs Node (`node --version`); install it with `nvm` if absent:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc && nvm install --lts
npm install -g typescript                    # if this needs sudo, use the prefix form:
npm install -g typescript --prefix ~/.local
```

**Verify**
```bash
tsc --version
```
The hook checks `tsc` on `PATH` first, then `~/.local/bin/tsc`, so either install location works.

## ESLint + Prettier for TypeScript projects
> feature: `lint-typescript` · agent: yes

Project-local, in every TS project carrying an `eslint.config.js`. Each imports the shared rules
from `code/eslint.shared.js` and runs from the project root via `node_modules/.bin/eslint` — no
global install.

**Precondition**
```bash
ls code/isoroll-module/node_modules/.bin/eslint code/voti/node_modules/.bin/eslint
```

**Install**
```bash
(cd code/isoroll-module && npm install)
(cd code/voti && npm install)
```

**Verify** — the gate must *bite*, not merely run:
```bash
printf '// test\nconst x = foo(bar());\n' > /tmp/test-lint.ts
(cd code/isoroll-module && node_modules/.bin/eslint /tmp/test-lint.ts)
# Expected: "2 calls in one statement"
```

## LaTeX toolchain
> feature: `latex` · agent: yes

For `academy/papers/`. The procedure lives in [`academy/SETUP.md`](academy/SETUP.md), which answers
a question no workspace-level install covers.

**Precondition**
```bash
pdflatex --version | head -1
```

**Install** — follow [`academy/SETUP.md`](academy/SETUP.md).

**Verify**
```bash
cd academy && make -n 2>/dev/null | head -3 || pdflatex --version | head -1
```

<!-- steps:end -->
