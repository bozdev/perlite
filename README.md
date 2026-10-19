<h1 align="center">Perlite</h1>

<p align="center">
  <strong>A lightweight, Windows-native Obsidian knowledge base for Claude Code.</strong><br>
  Drop a source into your vault's inbox. Claude reads it and files it as linked,
  source-cited Markdown notes you own.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2563eb.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/version-0.1.0-d97745" alt="Version 0.1.0">
  <img src="https://img.shields.io/badge/Claude%20Code-plugin-7c3aed" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/Windows-native-0078d4" alt="Windows native">
</p>

---

Perlite turns Claude Code into the librarian of your Obsidian vault. You collect
articles, PDFs, papers and notes; Perlite reads them, writes a summary for each
source, builds notes for the concepts and entities they mention, links everything
together, and keeps an index, a log and a short "where things stand" page up to date.
Later you can ask questions and get answers grounded in your own notes, with links
to the notes behind every claim.

**Why "Perlite"?** Obsidian is volcanic glass. Perlite is volcanic glass too, but
expanded until it is extremely light. That is the whole idea: the Obsidian-wiki
workflow, with almost no weight.

## Contents

- [Why Perlite](#why-perlite)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Choosing the vault](#choosing-the-vault)
- [Commands](#commands)
- [Vault layout](#vault-layout)
- [Note format](#note-format)
- [Evidence rules](#evidence-rules)
- [Customizing with PERLITE.md](#customizing-with-perlitemd)
- [Everyday workflow](#everyday-workflow)
- [Privacy and safety](#privacy-and-safety)
- [Updating and uninstalling](#updating-and-uninstalling)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Repository structure](#repository-structure)
- [Credits](#credits)
- [License](#license)

## Why Perlite

Perlite exists for two reasons: **it is lightweight** and **it runs natively on
Windows**.

| | Perlite |
|---|---|
| **What it is** | 5 skills (plain Markdown instructions), 5 note templates, 1 optional Python checker |
| **Runs on** | Windows (native, no WSL), macOS, Linux |
| **Writes notes with** | Claude Code's own file tools (Read, Write, Edit) |
| **Hooks** | None. Nothing runs when a session starts or stops. |
| **Background processes** | None |
| **Network access** | None, unless you explicitly ask it to fetch a URL |
| **Dependencies** | None. Python 3.8+ is optional and only used by `/perlite:lint`. |
| **Lock-in** | None. The vault is plain Markdown that works without Perlite. |

Many knowledge-base plugins route every write through their own runtime: a Python
transaction layer, locks, journals and JSON ledgers. That machinery is powerful, but
it is heavy, and some of it depends on Linux-only file system features, so on Windows
it either refuses to write or requires WSL. Perlite takes the opposite approach.
Every rule lives in a readable Markdown file, and Claude applies those rules with the
same file tools it uses for everything else. If you can read a recipe, you can read
and change how Perlite works.

The trade-off is honest: Perlite has no transactional rollback. You get safety from
Claude Code's permission prompts, from Perlite's "never delete, never overwrite
sources" rules, and from your own backups (Obsidian's File recovery core plugin or Git
work well). See [Privacy and safety](#privacy-and-safety).

## How it works

```text
   you                      Perlite (Claude Code)                     your vault
 ───────                   ──────────────────────                    ────────────
 drop a PDF  ──────────▶   /perlite:ingest
 into inbox/               1. reads PERLITE.md (the rules)
                           2. reads the source completely
                           3. finds existing notes on the same topics
                           4. writes / updates notes  ─────────────▶  wiki/sources/
                                                                     wiki/concepts/
                                                                     wiki/entities/
                           5. updates the core pages  ─────────────▶  wiki/index.md
                                                                     wiki/log.md
                                                                     wiki/hot.md
                           6. archives the original   ─────────────▶  .raw/YYYY-MM-DD/

 ask a question ───────▶   /perlite:query  (read-only, cites [[notes]])
 keep an answer ───────▶   /perlite:save   ─────────────────────────▶  wiki/questions/
 check health   ───────▶   /perlite:lint   (read-only report)
```

Obsidian watches the folder, so new notes appear immediately and show up in the
Graph view as they get linked.

## Requirements

- **Claude Code**: the terminal CLI or the Code tab of the Claude desktop app.
- **Obsidian** (recommended, to browse the notes; Perlite itself only needs a folder).
- **Python 3.8+** (optional): only for the fast, deterministic checker behind
  `/perlite:lint`. Without Python, lint falls back to a manual check.

Perlite does not need WSL, Git, Node.js, a server, an API key or any Obsidian
community plugin.

## Installation

Perlite is distributed as a Claude Code plugin from this repository, which is also its
own plugin marketplace (named `bozdev`).

### From the terminal

```bash
claude plugin marketplace add bozdev/perlite
```

```bash
claude plugin install perlite@bozdev
```

The plugin is installed at user scope, so it is available in every project and in
the desktop app's Code tab.

### Inside a Claude Code session

```text
/plugin marketplace add bozdev/perlite
/plugin install perlite@bozdev
```

### In the Claude desktop app (Code tab)

1. Click the **+** button next to the prompt box.
2. Choose **Plugins → Add plugin**.
3. Add the marketplace `bozdev/perlite` if asked, select **perlite**, and choose a
   scope.

### Pinning a version

To install exactly the code you reviewed, pin the marketplace to a tag or branch:

```bash
claude plugin marketplace add bozdev/perlite#v0.1.0
```

### Trying it without installing

From a clone of this repository:

```bash
claude --plugin-dir ./perlite
```

The plugin loads for that session only.

## Quick start

1. **Create a vault.** In Obsidian, create a new vault (or pick an existing one).
2. **Initialize it.** In Claude Code, run:

   ```text
   /perlite:init C:\Users\you\Documents\MyVault
   ```

   Perlite asks which language your notes should be written in, shows what it will
   create, and creates the structure after you confirm. Existing files are never
   overwritten.
3. **Tell Perlite where the vault is** (optional but recommended). See
   [Choosing the vault](#choosing-the-vault).
4. **Add a source.** Copy a PDF, Markdown file or text file into the vault's
   `inbox/` folder.
5. **Process it.**

   ```text
   /perlite:ingest
   ```

6. **Ask questions.**

   ```text
   /perlite:query What are the main trade-offs discussed in my sources?
   ```

7. **Check health** now and then.

   ```text
   /perlite:lint
   ```

You do not have to type the slash commands. Claude also picks the right skill from
plain requests such as "process my inbox", "what does my wiki say about X", or
"save this answer to my wiki".

## Choosing the vault

A Perlite vault is any folder that contains a `PERLITE.md` file. Every command finds
the vault in this order:

1. **A path in your request**, for example `/perlite:lint D:\Notes\Research`.
2. **The `PERLITE_VAULT` environment variable.**
3. **The current folder**, or its nearest parent folder that contains `PERLITE.md`.

If none of these works, Perlite asks you.

**Recommended:** set `PERLITE_VAULT` once in your Claude Code user settings, so every
session, in any folder, writes to the same vault. Open `~/.claude/settings.json`
(on Windows: `C:\Users\<you>\.claude\settings.json`) and add:

```json
{
  "env": {
    "PERLITE_VAULT": "C:/Users/you/Documents/MyVault"
  }
}
```

Use forward slashes, or escape backslashes as `\\`. If the file already has an `env`
block, add the line to it. Restart Claude Code afterwards.

Alternatively, start Claude Code inside the vault folder; Perlite then finds
`PERLITE.md` on its own.

## Commands

| Command | Changes the vault? | What it does |
|---|---|---|
| `/perlite:init [path]` | Yes, after you confirm | Creates the Perlite structure and rules file in a folder |
| `/perlite:ingest [file \| text \| URL]` | Yes | Turns sources into linked notes and archives the originals |
| `/perlite:query <question>` | No | Answers from your notes, citing them |
| `/perlite:save [what]` | Yes | Saves a selected answer or insight from the conversation |
| `/perlite:lint [path]` | No | Reports broken links, orphans, missing properties and more |

### `/perlite:init`

Sets up a vault. It creates `inbox/`, `.raw/`, the `wiki/` folders, `PERLITE.md` and
the four core pages (`index`, `log`, `hot`, `overview`). It asks for your note
language and shows the plan before writing. In an existing Obsidian vault it only
adds what is missing; your notes stay where they are.

### `/perlite:ingest`

Processes sources. With no argument it processes everything in `inbox/`. You can also
name one file, paste text, or give a URL (Perlite asks before fetching anything).

For each source, Perlite:

1. reads it completely (PDFs page by page; images directly);
2. extracts key claims, entities, concepts, conflicts and open questions;
3. checks which notes already exist, so it updates instead of duplicating;
4. writes a **source note** in `wiki/sources/`, and **concept** and **entity** notes
   only when they add lasting value;
5. links every important claim back to its source note;
6. updates `index`, `log`, `hot` (and `overview` if the big picture changed);
7. moves the original file to `.raw/YYYY-MM-DD/`. Nothing is deleted.

Large batches are split: by default Perlite proposes 5 sources at a time.
Formats Claude cannot read (audio, video, `.docx` and similar) are reported, never
guessed.

Examples:

```text
/perlite:ingest
/perlite:ingest paper-on-retrieval.pdf
/perlite:ingest https://example.com/article
```

### `/perlite:query`

Answers a question **only from your vault**, and never changes it. Each important
sentence ends with the note it rests on, so you can click through. It tells you how
settled each point is, shows both sides when notes disagree, and clearly labels
anything that comes from general knowledge instead of your notes.

```text
/perlite:query How do the sources define "contextual retrieval"?
```

If the answer is worth keeping, it offers to save it with `/perlite:save`.

### `/perlite:save`

Saves something from the current conversation: an answer, a decision, an insight or a
short session summary. It saves only what you select, never the whole conversation,
and warns you if the content looks sensitive. Claims from the conversation that are
not backed by a source in the vault are marked `provisional`.

```text
/perlite:save the comparison table above as a note
```

### `/perlite:lint`

A read-only health check. It reports:

- broken `[[links]]` and broken `![[embeds]]`
- ambiguous links (two notes with the same name)
- orphan notes (nothing links to them)
- notes missing from `wiki/index.md`
- missing frontmatter or missing required properties
- a note whose `type` does not match its folder
- empty sections
- files waiting in `inbox/`

It never fixes anything on its own; it proposes fixes and applies them only after
you approve. With Python installed, the check is done by a small, read-only,
standard-library script (`skills/lint/lint.py`) that you can also run yourself:

```bash
python skills/lint/lint.py "C:/Users/you/Documents/MyVault"
```

## Vault layout

```text
MyVault/
├── PERLITE.md           # the rules (edit me)
├── inbox/               # drop sources here
├── .raw/                # archive of processed originals (hidden in Obsidian)
│   └── 2026-01-31/
└── wiki/
    ├── index.md         # catalog of every note
    ├── log.md           # operation history, newest first
    ├── hot.md           # short summary for the next session
    ├── overview.md      # the big picture
    ├── sources/         # one note per source
    ├── entities/        # people, organizations, products, projects
    ├── concepts/        # ideas, methods, definitions
    ├── questions/       # answered questions and comparisons
    ├── sessions/        # content saved from conversations
    └── canvases/        # Obsidian canvases
```

Folders that start with a dot (like `.raw/`) are hidden in Obsidian's file explorer
but are normal folders on disk.

## Note format

Every note starts with flat YAML properties:

```yaml
---
type: concept
title: "Contextual Retrieval"
status: developing
created: 2026-01-31
updated: 2026-01-31
tags:
  - retrieval
aliases: []
related:
  - "[[BM25]]"
sources:
  - "[[Introducing Contextual Retrieval]]"
---
```

| `type` | Folder | Used for |
|---|---|---|
| `source` | `wiki/sources/` | A traceable summary of one source |
| `entity` | `wiki/entities/` | A person, organization, product or project |
| `concept` | `wiki/concepts/` | An idea, framework, mechanism or definition |
| `question` | `wiki/questions/` | An answered question with visible evidence status |
| `comparison` | `wiki/questions/` | A criteria-based comparison |
| `session` | `wiki/sessions/` | Content saved from a conversation |
| `overview` | `wiki/` | The big picture |
| `meta` | `wiki/` | Index, log and hot pages |

**Statuses:** `seed`, `developing`, `evergreen`, `answered`, `provisional`,
`contested`, `archived`.

Source notes add `source_type`, `author`, `date_published`, `url` and `raw_path`.
Unknown values stay empty instead of being invented.

Because the properties are standard Obsidian properties, you can build
[Bases](https://help.obsidian.md/bases) views on top of them, for example a table of
all `source` notes sorted by `date_published`.

## Evidence rules

Perlite is designed to keep your knowledge base honest:

- Every important claim links to the source note it comes from.
- What a source says and what Claude concludes are kept apart; interpretation goes
  in a `> [!note] Interpretation` callout.
- When sources disagree, both views are kept and marked with
  `> [!warning] Conflict`. Neither is silently chosen.
- Unsourced claims are marked `provisional` or "no source".
- Sources, quotes, dates and authors are never invented.

## Customizing with PERLITE.md

`PERLITE.md` in the vault root is the single source of rules. Every Perlite command
reads it first, and its rules win over the skills' defaults. Open it in Obsidian and
edit it like any note. The **Settings** section at the top controls:

| Setting | Default | Meaning |
|---|---|---|
| Note language | chosen at init | The language notes are written in |
| Max notes read per query | 8 | How many notes `/perlite:query` reads before asking |
| Max sources per ingest batch | 5 | Above this, `/perlite:ingest` proposes a first batch |
| Hot page word limit | 500 | Maximum length of `wiki/hot.md` |

You can also change the writing rules, add your own note types or statuses, or add
house rules such as "always add a `## Takeaways` section to source notes".

## Everyday workflow

- **Collect:** throughout the day, save interesting PDFs and articles into `inbox/`.
- **Process:** once in a while, say "process my inbox". Review the new notes in
  Obsidian's Graph view.
- **Ask:** "according to my wiki, …" gets you answers with links to your notes.
- **Keep:** when a conversation produces something useful, say "save this to my
  wiki".
- **Maintain:** run `/perlite:lint` weekly and approve the fixes you agree with.

`wiki/hot.md` is a short summary of recent activity. Starting a session with "read my
hot page" gives Claude the context of where you left off.

## Privacy and safety

- **Local only.** Perlite has no hooks, no background processes, no telemetry and no
  network code. It reads and writes files in your vault through Claude Code.
- **No silent fetching.** URLs are fetched only when you ask, and only after Perlite
  confirms with you.
- **Note on Claude itself:** like any Claude Code work, content Claude reads is sent
  to the Claude model as part of the conversation. Perlite does not send it anywhere
  else.
- **Sources are never modified or deleted.** Originals are moved from `inbox/` to
  `.raw/` and never overwritten; name clashes get a suffix.
- **Source content is treated as data.** Instructions hidden inside a PDF or web page
  are ignored.
- **Nothing outside the vault is written.**
- **Permission prompts.** Claude Code asks before editing files. To skip prompts for
  your vault only, you can add an allow rule for that folder in your Claude Code
  permission settings.
- **Backups.** Perlite has no rollback. Enable Obsidian's **File recovery** core plugin
  or keep the vault in Git if you want to undo changes.

## Updating and uninstalling

Perlite sets a `version` in its manifest, so you only receive an update when a new
version is released. Auto-update is off by default for third-party marketplaces.

```bash
claude plugin marketplace update bozdev
```

```bash
claude plugin update perlite@bozdev
```

Or use `/plugin` → **Installed** → **perlite** → **Update now**.

To uninstall:

```bash
claude plugin uninstall perlite@bozdev
```

```bash
claude plugin marketplace remove bozdev
```

Uninstalling never touches your vault. Your notes, sources and `PERLITE.md` stay
exactly where they are.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Which vault should I use?" every time | Set `PERLITE_VAULT` (see [Choosing the vault](#choosing-the-vault)) or start Claude Code inside the vault. |
| `/perlite:...` commands don't appear | Run `claude plugin list` to confirm it is enabled, then start a new session (or run `/reload-plugins`). |
| `PERLITE_VAULT` is ignored | Restart Claude Code after editing `settings.json`, and check the JSON is valid and the path uses `/` or `\\`. |
| Lint says Python is not found | On Windows, install Python from python.org or try `py -3`. Avoid `python3` on Windows: it is often a Microsoft Store shortcut. Lint also works without Python, in manual mode. |
| A PDF was only partly processed | Very long PDFs are read in page ranges. Ask Perlite to continue from the page it stopped at. |
| New notes don't show up in Obsidian | Make sure Obsidian has the same folder open as the vault Perlite wrote to. |
| Too many permission prompts | Add an allow rule for the vault folder in Claude Code's permission settings. |

## FAQ

**Does it work on macOS and Linux?**
Yes. Nothing in Perlite is Windows-specific; it is simply designed so that Windows
works without extra setup.

**Can I use it with an existing Obsidian vault?**
Yes. `/perlite:init` adds only what is missing and never moves your notes. Your
existing notes can live alongside `wiki/`.

**Do I need to use the slash commands?**
No. Claude picks the right Perlite skill from plain requests. The slash commands are
there when you want to be explicit.

**What languages are supported?**
Any language Claude writes. Set the note language in `PERLITE.md`.

**Does Perlite work in the claude.ai chat or the desktop app's Chat tab?**
No. Perlite needs access to a folder on your computer, which is what Claude Code
provides. Use the terminal or the desktop app's Code tab.

**Can I edit the notes myself?**
Of course. They are your notes. Perlite asks before rewriting a large part of a note
you edited by hand.

## Repository structure

```text
perlite/
├── .claude-plugin/
│   ├── plugin.json          # plugin manifest
│   └── marketplace.json     # this repo as a one-plugin marketplace
├── skills/
│   ├── init/SKILL.md
│   ├── ingest/SKILL.md
│   ├── query/SKILL.md
│   ├── save/SKILL.md
│   └── lint/
│       ├── SKILL.md
│       └── lint.py          # optional, read-only checker
├── templates/vault/         # files /perlite:init copies into a new vault
│   ├── PERLITE.md
│   └── wiki/ (index, log, hot, overview)
├── CHANGELOG.md
├── LICENSE
└── README.md
```

Validate the plugin after changes:

```bash
claude plugin validate .
```

## Credits

Perlite's vault structure and note conventions are inspired by
[claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) by AgriciDaniel
(MIT), which in turn builds on Andrej Karpathy's "LLM wiki" idea. Perlite is an
independent, from-scratch implementation that trades claude-obsidian's transactional
runtime for a skills-only design that runs natively on Windows.

Developed by **[Boz](https://github.com/bozdev)**.

## License

[MIT](LICENSE) © 2026 Boz
