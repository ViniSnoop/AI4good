# The page's honesty block: what this picture covered, what it inferred, and where to change it.
#
# Split from diagram_page.py 2026-08-20, when the per-repo document arrived and the footer stopped
# being able to say one thing. Every line here is a claim ABOUT the document above it, and a claim
# that is right for the workspace is wrong for a repo — the old text told a repo's reader to edit
# core/features.txt for a matrix its page does not carry, and promised the nested repos would "earn
# their own document" after they already had one.
#
# So the split is by responsibility rather than by size: the shell renders, this states what the
# rendering is worth. A footer that hedges to stay true of both pages would say nothing.
from html import escape


def _coverage(coverage: dict) -> str:
    unparsed = coverage['unparsed']
    return (f'<b>coverage</b> parsed {coverage["parsed"]} of {coverage["total"]} routing blocks'
            + (f' · <b>{len(unparsed)} unparsed:</b> {escape(", ".join(unparsed))}'
               if unparsed else ' · none unparsed'))


def _scope(scope: dict, whole: bool) -> str:
    if whole:
        return (f'<p><b>scope</b> the workspace repository. {scope["nested"]} repositories nested '
                'inside it are drawn as directories and no deeper: each is its own repository and '
                'carries its own document, generated the same way — '
                '<code>architecture --repos</code>.</p>')
    return ('<p><b>scope</b> this repository alone. Four of the workspace document\'s drawings are '
            'absent because their source is: the enforcement matrix, the layer summary, the session '
            'lifecycle and the wiring fan-in all read <code>core/features.txt</code> and the hook '
            'registrations, which exist once, for the enforcement layer. That is the boundary '
            'between the two documents, not a gap in this one.</p>')


def _sources(whole: bool) -> str:
    return ('<p><b>how to change it</b> edit the source, not this file: '
            + ('<code>core/features.txt</code> for the matrix, a directory\'s ' if whole
               else 'a directory\'s ')
            + '<code>CONTEXT.md</code> for the spine'
            + ('' if whole else ', this repository\'s <code>ISSUES.md</code> for the findings')
            + '. Regenerated and committed by <code>/roundup</code> at every session close, so a '
            'stale picture is a bug in the close, not a fact of life.</p>')


def render(coverage: dict, scope: dict, whole: bool = True) -> str:
    return '\n'.join([
        '<footer>',
        f'<p>{_coverage(coverage)}</p>',
        _scope(scope, whole),
        '<p><b>what is inferred</b> nothing, as of 2026-08-18. Every edge above renders declared '
        'or generated data, the firing moment included: '
        '<code>core/hooks/trigger/trigger_law.py</code> reads it from the registrations, the '
        'pre-commit dispatcher\'s own stage order and the install steps. What the registrations '
        'cannot place is counted as a gap instead of guessed at.</p>',
        _sources(whole),
        '</footer>'])
