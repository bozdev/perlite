---
name: lint
description: "Health check for the Perlite vault: broken links and embeds, orphan notes, missing frontmatter, notes missing from the index, type/folder mismatches, empty sections, duplicate names, and files waiting in the inbox. Reports only; fixes nothing without approval. Use for: check my wiki, vault health check, find broken links, lint the vault, perlite lint."
argument-hint: "[vault folder path]"
---

# Vault health check

## 1. Find the vault

A Perlite vault is a folder that contains `PERLITE.md`. Use the first that applies:

1. A path the user gave in the request (`$ARGUMENTS`).
2. The `PERLITE_VAULT` environment variable (PowerShell: `$env:PERLITE_VAULT`,
   Bash: `echo "$PERLITE_VAULT"`).
3. The current working directory or its nearest parent that contains `PERLITE.md`.

If none applies, ask the user for the vault path.

## 2. Run the checker

`${CLAUDE_SKILL_DIR}/lint.py` is a read-only script; it never changes a file. It
needs Python 3.8 or newer and nothing else.

```text
python "${CLAUDE_SKILL_DIR}/lint.py" "<vault>"
```

- On Windows, if `python` is not found, try `py -3` instead. Do not use `python3`
  on Windows: it is often a Microsoft Store shortcut, not a real interpreter.
- Exit code 0 means no findings, 1 means findings, 2 means the folder is not a
  Perlite vault.

**If Python is not available,** do the same checks by hand with Glob, Grep and
Read: notes without frontmatter or required properties, `[[links]]` that point to
no note, notes in `wiki/` that nothing links to, notes missing from
`wiki/index.md`, and files waiting in `inbox/`. Say that the manual check may miss
things the script would catch.

## 3. Explain the findings

- Double-check any surprising finding by reading the note (a link may point to a
  note the user plans to write).
- Give a short summary: how many findings, which matter, which can be ignored.
- If files are waiting in `inbox/`, suggest `/perlite:ingest`.

## 4. Fixes

This skill never fixes anything on its own. Propose fixes as a list (for example
"add these 3 notes to the index, fix this broken link"). If the user approves,
apply them with Edit following the rules in `<vault>/PERLITE.md`, then add a
`## YYYY-MM-DD · fix` entry to `wiki/log.md`.
