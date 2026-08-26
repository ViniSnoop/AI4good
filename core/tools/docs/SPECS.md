# Google Docs API — facts worth not rediscovering
> What the API actually returns, learned the expensive way — read alongside `CONTEXT.md`.

## Indices, and why they are not object ids

A Slides element has an `objectId` that survives every edit. **A Docs element has an integer index
into the body, and nothing else.** There is no handle, no name, no anchor an edit can address — only
"the 141st character position". So:

- **Every insert or delete shifts every index after it.** `batchUpdate` applies requests in
  sequence against a body that is moving as it goes, so a batch measured against one `documents.get`
  is only self-consistent if it runs **highest index first**.
- **The API does not complain.** A front-to-back batch is accepted, applies, and puts the second
  edit somewhere nobody chose. That silence is why `docs_core.check_order` refuses the batch
  locally instead of trusting the round trip to fail.
- `check_order` only guards requests in `LENGTH_CHANGING`. A `updateTextStyle` or
  `updateParagraphStyle` batch may run in any order, because it moves nothing.
- `--force` exists for the one honest case: the caller already computed the shifts. It is not a way
  past a failing batch.

**`request_index` reads four different spellings**, because Docs says "where" four ways —
`location.index`, `insertionIndex`, `range.startIndex`, `tableRange`/`textRange.startIndex` — plus
`endOfSegmentLocation`, which means "the end" and carries no index at all.

## Revisions are the only real concurrency defence

`documents.get` returns a `revisionId`; handing it back as `writeControl.requiredRevisionId` makes
the API reject the batch if the document moved in between. Without it, indices measured before
somebody else's paragraph landed are applied after it — a corruption that looks like a typo.

**An empty `requiredRevisionId` is not the same as omitting the key** — the API rejects the empty
string, so `batch_body` leaves `writeControl` out entirely rather than sending `""`.

## Markdown is the good read, and Drive owns both directions

`documents.get` returns the words buried in several kilobytes of style objects per paragraph.
Drive's exporter already renders them, so `export_md` costs one call and no parser. Import works the
same way: uploading Markdown against `application/vnd.google-apps.document` converts it.

**`push` replaces the entire body.** Google's words: *"When you upload and convert media during an
update request to a Docs, Sheets, or Slides file, the full contents of the document are replaced."*
The id, URL and sharing survive — which is what makes a repo `.md` and the live Doc the same
document — but **anything anchored to text that goes away goes with it.** Read `gdocs comments`
before pushing over a document somebody has reviewed.

## Comments are not in the Docs API

They are Drive resources. A `documents.get` never mentions them, so a document can read as finished
while carrying twenty open objections. `gdocs comments` hides resolved threads by default and prints
`quotedFileContent` — the text each thread is anchored to — because a comment without its anchor is
usually unreadable.

## Auth

Two grants, `docs` (`documents.readonly`) and `docs-write` (`documents`), the same split as
[`../slides/`](../slides/CONTEXT.md) and [`../files/`](../files/CONTEXT.md). A read prefers the write
token when the alias has one: the edit consent already contains the read consent, so a second
browser trip would buy no safety and create two tokens that die independently.

**The grant name IS the config directory suffix** — a write token is
`~/.config/workspace-**docs-write**/<alias>.token.json`, and checking the read directory to see
whether a write grant landed answers *no* forever. `gdocs auth` prints the real path on its last
line; read that, not a directory you inferred the name of.

`list`, `read`, `push`, `new --from` and `comments` all ride the **existing** `drive` /
`drive-write` tokens rather than minting a third and fourth grant, since discovery, export and
comments are Drive endpoints.

## A 403 naming a project is not a permission bug

Confirmed the expensive way on 2026-08-25, after a successful consent:

```
Google Docs API has not been used in project 1048141740528 before or it is disabled.
```

The token was fine — the **API** was off. `gdocs` has no `credentials.json` of its own, so
`gauth._credentials_file` falls back to `~/.config/workspace-gmail/`, which is project
`workspace-gmail-499605`. `SETUP-accounts.md` records that `workspace-os-506016` has docs switched
on; that is the **forms** project, reached only by the second credential in `workspace-forms/`, and
it is not the project `gdocs` authenticates against.

**So the split matters:** everything Drive-backed (`list`, `read`, `push`, `new --from`,
`comments`) worked immediately, because the Drive API was already on. Only the Docs API half
(`read --outline`, `read --json`, `apply`, `text`, `replace`) was refused. A family half-working
this way is the signature of a disabled API, not of a bad grant — do not spend a re-auth on it.
