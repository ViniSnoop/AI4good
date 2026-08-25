#!/usr/bin/env python3
# The entropy report: what the dashboard's findings look like on the page.
#
# Split from entropy-dashboard.py 2026-07-30, when that file crossed the 150-line warn.
# A tool that reports size signals is a poor place to ignore one.
#
# Since 2026-08-20 it renders a delimited BLOCK rather than a whole file: the measurements live
# inside ISSUES.md, under hand-written issues, because both answer the same question — what is
# currently untrue that we know about (core/SCHEMA.md § The `.md` type system).
from datetime import date

START = '<!-- entropy:start -->'
END = '<!-- entropy:end -->'

# Only used when ISSUES.md is missing entirely — a clone gets it from git. It carries the type's own
# head so the file is a legal ISSUES.md from its first line rather than from its first run.
SEED = ('# Workspace issues\n'
        '> What is currently untrue that we know about: hand-written issues first, every measured\n'
        '> number inside its own generated block.\n')


def local_seed(repo: str) -> str:
    """The same head, for a code repo's own ledger — created on the first scatter, then authored."""
    return (f'# {repo.split("/")[-1]} issues\n'
            '> What is currently untrue that we know about in this repo: hand-written issues\n'
            '> first, every measured number inside its own generated block.\n')


def _rel(path, root) -> str:
    return str(path).replace(f'{root}/', '')


SECTIONS = (
    ('types', 'Off-allowlist `.md` types', 'route via core/SCHEMA.md § four disposal routes'),
    ('inventories', 'CONTEXT.md hand-written inventories', 'the routing block owns inventory'),
    ('naming', 'Naming and placement', 'kebab-case ASCII, types where their scope allows'),
    ('goals', 'Projects not declaring their goal', 'line 3 of a code/ CONTEXT.md'),
    ('wiki', 'Wiki-links naming nothing', 'a [[slug]] is a goal file or an item in one'),
    ('retired', 'Retired tokens still alive', 'a rename is unfinished until these are zero'),
    ('citations', 'Roadmap item numbers cited outside a roadmap',
     'a closed item is deleted — cite the SPECS.md/SCHEMA.md section that owns the rule'),
    ('duplicates', 'Items claimed by two ledgers', 'v1 criterion 2 — an item lives in one place'),
    ('size', 'Size signals', 'a signal for review, never a cap — do not summarize to fit'),
    ('stubs', 'Source files with no interface stub',
     'the read gate only fires when a stub exists — a missing one turns it off silently'),
    ('fanout', 'Directories holding too many files',
     'splitting costs one hop — pay it only when it removes more table than it adds'),
    ('finished', 'Prose describing finished work',
     'git is the history — cut it, or rewrite it as present-tense state'),
    ('undescribed', 'Unanswered scaffold placeholders',
     'a generator asked a question — answer it at the source, never by cutting the marker'),
    ('stores', 'Doubt stores missing their own discipline',
     'an experiment states its Method, Results, What changed and Limitations; a judged reference '
     'carries a source tier'),
    ('vendor', 'Ledgers naming a model where they mean a tier',
     'which model fills a tier is data — core/flows/craft/routing.md'),
    ('fields', 'Header fields naming code that is not there',
     'a field naming our own tree is a claim, and it is checked before a later session inherits '
     'it as fact — core/SCHEMA-outgrowing.md § the field table'),
    ('truncated', 'Truncated routing descriptions',
     'the source wrote past the bound — shorten it there, never edit the table'),
    ('misplaced', 'Constraints trapped in a CONTEXT.md head',
     'the only enforced-read type — move the contract to a sibling SPECS.md'),
    ('branches', 'Repos on an unmerged feature branch',
     'promote when the work is green, or say which reason applies — /roundup Phase 5'),
    ('remotes', 'Remote branches already merged into their base',
     'safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas'),
)


def _index(counts: dict, here: int) -> list:
    """The root's index of the local ledgers, and the one collected number.

    The sum is computed from the counts the same run just wrote, so it cannot disagree with them.
    A repo may not write into it — that is the copied-count drift these checks exist to catch.
    """
    scattered = sum(counts.values())
    out = ['', '### Findings per code repo', '',
           '*Each repo keeps its own `ISSUES.md`; this table is the index and the sum. '
           'Open the repo to see what its findings are.*', '',
           '| Repo | Findings |', '|------|----------|']
    out += [f'| [`{repo}`]({repo}/ISSUES.md) | {counts[repo]} |' for repo in sorted(counts)]
    return out + [f'| **collected** | **{scattered + here}** |']


def render(findings: dict, scanned: int, root, name: str = '', index: dict = None,
           trend: str = '') -> str:
    total = sum(len(findings[key]) for key, _, _ in SECTIONS)
    scope = f'`{name}`' if name else 'the whole tree'
    collected = total + sum(index.values()) if index else total
    out = [START,
           '## Entropy',
           '',
           '> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans '
           f'{scope}. Never edit inside this block, and never copy a count out of it — a copied '
           'number is the drift these checks exist to catch.',
           '',
           f'{date.today().isoformat()} · {scanned} tracked files scanned · '
           f'**{collected} findings**{trend}'
           + (f', {total} of them here' if index else ''), '',
           '| Check | Findings |', '|-------|----------|']
    out += [f'| {title} | {len(findings[key])} |' for key, title, _ in SECTIONS]
    if index:
        out += _index(index, total)
    for key, title, note in SECTIONS:
        items = findings[key]
        out += ['', f'### {title}', '', f'*{note}*', '']
        out += ['Clean.'] if not items else [
            f'- {_rel(i.splitlines()[0], root)}' for i in sorted(items)]
    return '\n'.join(out + ['', END]) + '\n'
