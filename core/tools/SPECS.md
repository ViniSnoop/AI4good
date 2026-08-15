# Tools — Specs
> What must be true of a `core/tools/` capability, and why: how a family is named, what a
> failure has to hand back, and what work is the agent's rather than Lucas's.

Companion to [`CONTEXT.md`](CONTEXT.md), which says what this directory *is* and routes into it.
These are the constraints. They live here rather than in the head because `CONTEXT.md` is the only
enforced-read type — every session touching this subtree pays for its head, while this file is read
on demand (core/SCHEMA.md § Placement).

## Naming: the directory is the capability, the file is the provider

**A family directory is a capability; the tool inside it is the provider.** `mail/gmail`,
`calendar/gcalendar`, `files/gdrive` — swapping a provider changes a leaf, never a family. This is
the workspace's provider-agnostic rule applied to the path: function in the directory, vendor at the
file.

Two sweeps have already renamed every tool path here, so **a third is not free** — check
[`ROADMAP.md`](../ROADMAP.md) before proposing one.

`auth/` is a family because it is shared across families rather than owned by any. A module imported
by more than one family belongs at this root; a module imported by exactly one belongs beside its
tool. That rule is why exactly one file sits at the root.

## An auth failure names its own fix — relay it verbatim

A dead token makes `gauth.auth()` raise `AuthExpired`, and every CLI entrypoint prints it through
`gauth.run()` instead of a traceback. That message is written **for Lucas** and already carries the
exact command *and* the address to sign in as. **Show it to him unchanged — do not paraphrase it,
and never say "you need to re-auth" on its own.**

Why the address is in the message and not in this file: Lucas has several Google accounts, so
"re-authenticate" without one is an instruction he cannot act on, and a wrong account is worse than a
failure — it authenticates fine and then reads the wrong mailbox or drive. The address is read at
runtime from `accounts.json`, so it cannot go stale here.

**Run the re-auth command yourself** — backgrounded, since it blocks until consent lands. It opens a
browser on Lucas's machine, so the only part that is his is picking the account on the consent
screen. Handing him the command to type is a chore the agent could have absorbed.

**That rule is provider-agnostic, and every new tool inherits it without asking again.** Lucas does
*only* what cannot be done from here — a click inside the provider's own UI, a consent screen, a
secret minted inside his account. Everything with a command form is the agent's, and a secret he
pastes into the conversation is stored through a builtin pipe so it never reaches argv:

```bash
printf '%s\n' '<secret>' | core/tools/<family>/<tool> auth <alias>
```

`notes/notion` is the non-OAuth shape of the same split. Tokens are per `(service, alias)` at
`~/.config/workspace-<service>/<alias>.token.json`; Drive writes (`mkdir`, `put`) use a separate
`drive-write` token from the read one.

## Adding a tool

1. Name the file for its **provider**, and put it in the directory named for the **capability** it
   delivers. Never a file at this root.
2. Create the family directory only when the tool actually lands in it — no empty `sheets/`,
   `docs/`, `maps/` waiting for a someday tool.
3. Give a family its own `CONTEXT.md` only once it holds more than one file. A one-tool family folds
   into the parent's routing table: one path hop, zero extra rows. Declaring itself early costs the
   reader a routing table that says nothing — `auth/` is the live example of the cheap side.
4. Add `# Usage: core/tools/<family>/<name> <args> — <description>` as the first comment line, after
   the shebang.
5. Save — the routing block regenerates automatically.
