---
name: query
description: "Answer a question from the Perlite vault's notes instead of general knowledge, citing the notes it used. Read-only: never changes the vault. Use when the user picks the vault as the source: ask my wiki, according to my notes, search the wiki, what does my vault say about, based on the wiki, perlite query."
argument-hint: "<question>"
---

# Answer from the vault

This skill **only reads**. Never create, edit or move a file in the vault.

## 1. Find the vault

A Perlite vault is a folder that contains `PERLITE.md`. Use the first that applies:

1. A path the user gave in the request.
2. The `PERLITE_VAULT` environment variable (PowerShell: `$env:PERLITE_VAULT`,
   Bash: `echo "$PERLITE_VAULT"`).
3. The current working directory or its nearest parent that contains `PERLITE.md`.

If none applies, ask the user for the vault path.

## 2. Gather evidence

1. Read `<vault>/PERLITE.md`, `<vault>/wiki/hot.md` and `<vault>/wiki/index.md`.
2. Pull the key terms and their synonyms from the question (`$ARGUMENTS`). Search
   `<vault>/wiki/` with Grep, and follow `[[links]]` from `index.md` and from the
   notes you find.
3. Read the most relevant notes, up to the per-query limit in `PERLITE.md`. If you
   need more, tell the user.
4. Read the linked source notes when a claim needs checking.

## 3. Answer

- Rely only on the vault. End each important sentence with the note it rests on,
  as `[[Note name]]`.
- State how settled the information is: settled (`evergreen`), provisional,
  contested, or unsourced.
- If notes disagree, show both sides. Never silently pick one.
- If the vault has no answer or only part of one, say so plainly. If you fill a gap
  from general knowledge, label that part clearly, for example "Not in the vault —
  general knowledge:".
- If you notice a gap worth filling, suggest it (for example "adding a source on X
  would strengthen this").
- Answer in the language the user asked in.

If the answer is worth keeping, offer to save it as a question note with
`/perlite:save`. Do not save unless the user asks.
