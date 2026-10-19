---
name: init
description: "Set up a Perlite knowledge vault in an Obsidian folder: creates the inbox, archive and wiki structure, the PERLITE.md rules file and the core pages. Works on a new empty folder or an existing Obsidian vault without touching existing notes. Use for: set up perlite, initialize vault, create knowledge base, perlite init, adopt this vault, second brain setup."
argument-hint: "[vault folder path]"
---

# Initialize a Perlite vault

Create the Perlite structure in an Obsidian vault folder. Use only Claude's own
file tools (Read, Glob, Write) plus a shell command to create folders. This skill
never edits, moves or deletes an existing file.

Templates for the files live in `${CLAUDE_PLUGIN_ROOT}/templates/vault/`.

## 1. Choose the folder

1. If the user gave a path (`$ARGUMENTS` or in the request), use it.
2. Otherwise check the `PERLITE_VAULT` environment variable (PowerShell:
   `$env:PERLITE_VAULT`, Bash: `echo "$PERLITE_VAULT"`).
3. Otherwise ask which folder to use. Suggest an Obsidian vault folder; the
   current working directory is only a suggestion, never assumed.

If the folder already contains `PERLITE.md`, it is already a Perlite vault.
Report that and stop.

## 2. Ask for the note language

Ask which language notes should be written in (for example English, Turkish,
German). Default to the language the user is writing in.

## 3. Show the plan

List the folder and the files that will be created. Mention that existing files
are never overwritten and existing notes are not moved. Wait for the user's
go-ahead before writing.

Folders to create (only if missing):

```text
inbox/
.raw/
wiki/sources/
wiki/entities/
wiki/concepts/
wiki/questions/
wiki/sessions/
wiki/canvases/
```

Files to create (only if missing), from the templates:

```text
PERLITE.md
wiki/index.md
wiki/log.md
wiki/hot.md
wiki/overview.md
```

## 4. Create

1. Create the missing folders. PowerShell:
   `New-Item -ItemType Directory -Force -Path "<vault>\inbox"` (and so on). Bash:
   `mkdir -p "<vault>/inbox"` (and so on).
2. For each template file, check with Glob whether the target exists. If it
   exists, skip it and tell the user. If not, Read the template, replace
   `{{date}}` with today's date (`YYYY-MM-DD`) and `{{language}}` with the chosen
   language, then Write it to the vault.
3. If the note language is not English, translate the headings and placeholder
   lines of the core pages (`wiki/index.md`, `wiki/log.md`, `wiki/hot.md`,
   `wiki/overview.md`) into that language. Keep `PERLITE.md` in English unless
   the user asks otherwise; its rules apply in any language.

## 5. Existing vaults

If the folder already holds notes, leave them where they are. Offer, as a
separate optional step, to run `/perlite:lint` and then add existing notes to
`wiki/index.md`. Never move or rewrite existing notes without explicit approval.

## 6. Finish

Tell the user:

- which folders and files were created and which were skipped;
- that they can open the folder in Obsidian;
- how to make Perlite always use this vault from any folder: set
  `PERLITE_VAULT` (for example in `~/.claude/settings.json` under `"env"`), or
  start Claude Code inside the vault folder;
- the next step: drop a file into `inbox/` and run `/perlite:ingest`.
