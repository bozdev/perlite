"""Read-only health check for a Perlite vault.

Usage: python lint.py <vault-path>

Never writes, moves or deletes anything. Prints a plain-text report.
Exit codes: 0 = no findings, 1 = findings, 2 = not a Perlite vault.
Requires Python 3.8+ and nothing outside the standard library.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

RULES_FILE = "PERLITE.md"
SKIP_DIRS = {".obsidian", ".raw", ".trash", "inbox"}
REQUIRED = ("type", "title", "status", "created", "updated", "tags")
CORE_PAGES = {"wiki/index.md", "wiki/log.md", "wiki/hot.md", "wiki/overview.md", RULES_FILE}
TYPE_FOLDERS = {
    "source": "wiki/sources/",
    "entity": "wiki/entities/",
    "concept": "wiki/concepts/",
    "question": "wiki/questions/",
    "comparison": "wiki/questions/",
    "session": "wiki/sessions/",
}

FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
LINK_RE = re.compile(r"(!?)\[\[([^\]\n]+?)\]\]")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):", re.MULTILINE)
TYPE_RE = re.compile(r"^type:\s*[\"']?([\w-]+)[\"']?\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def rel(path: Path, vault: Path) -> str:
    return path.relative_to(vault).as_posix()


def collect(vault: Path) -> tuple[list[Path], list[Path]]:
    notes, files = [], []
    for path in vault.rglob("*"):
        parts = path.relative_to(vault).parts
        if not parts or parts[0] in SKIP_DIRS or not path.is_file():
            continue
        files.append(path)
        if path.suffix.lower() == ".md":
            notes.append(path)
    return notes, files


def strip_code(text: str) -> str:
    return INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))


def empty_sections(body: str) -> list[str]:
    # A fenced block counts as section content, so replace it with a placeholder.
    lines = FENCE_RE.sub("[code]", body).splitlines()
    headings = [(i, m) for i, line in enumerate(lines) if (m := HEADING_RE.match(line))]
    found = []
    for n, (i, match) in enumerate(headings):
        following = headings[n + 1] if n + 1 < len(headings) else None
        end = following[0] if following else len(lines)
        if any(line.strip() for line in lines[i + 1:end]):
            continue
        # A heading followed directly by a deeper subheading is a parent, not empty.
        if following and len(following[1].group(1)) > len(match.group(1)):
            continue
        found.append(match.group(2))
    return found


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) != 2:
        print("Usage: python lint.py <vault-path>")
        return 2
    vault = Path(sys.argv[1]).expanduser().resolve()
    if not (vault / RULES_FILE).is_file():
        print(f"ERROR: {vault} is not a Perlite vault ({RULES_FILE} not found).")
        return 2

    notes, files = collect(vault)
    by_stem = defaultdict(list)
    for path in notes:
        by_stem[path.stem.casefold()].append(path)
    by_path = {rel(p, vault).casefold()[:-3]: p for p in notes}
    by_name = defaultdict(list)
    for path in files:
        by_name[path.name.casefold()].append(path)

    findings = defaultdict(list)
    incoming = defaultdict(set)
    types = {}

    for path in notes:
        name = rel(path, vault)
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = FRONTMATTER_RE.match(text)
        body = text[fm.end():] if fm else text
        if not fm:
            findings["Missing frontmatter"].append(name)
        else:
            keys = set(KEY_RE.findall(fm.group(1)))
            missing = [k for k in REQUIRED if k not in keys]
            if missing:
                findings["Missing required property"].append(f"{name}: {', '.join(missing)}")
            type_match = TYPE_RE.search(fm.group(1))
            if type_match:
                page_type = type_match.group(1)
                types[path] = page_type
                folder = TYPE_FOLDERS.get(page_type)
                if folder and not name.startswith(folder):
                    findings["Type does not match folder"].append(
                        f"{name}: type={page_type}, expected {folder}"
                    )

        for heading in empty_sections(body):
            findings["Empty section"].append(f"{name}: '{heading}'")

        for embed, raw in LINK_RE.findall(strip_code(text)):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            suffix = Path(target).suffix.lower()
            if embed and suffix and suffix != ".md":
                if not by_name.get(Path(target).name.casefold()):
                    findings["Broken embed"].append(f"{name} -> ![[{target}]]")
                continue
            key = target.casefold()
            key = key[:-3] if key.endswith(".md") else key
            if "/" in key:
                hit = by_path.get(key)
                hits = [hit] if hit else []
            else:
                hits = by_stem.get(key, [])
            if not hits:
                findings["Broken link"].append(f"{name} -> [[{target}]]")
            elif len(hits) > 1:
                findings["Ambiguous link"].append(f"{name} -> [[{target}]]")
            elif hits[0] != path:
                incoming[hits[0]].add(path)

    for paths in by_stem.values():
        if len(paths) > 1:
            findings["Duplicate note names"].append(", ".join(rel(p, vault) for p in paths))

    index = vault / "wiki" / "index.md"
    for path in notes:
        name = rel(path, vault)
        if name in CORE_PAGES or not name.startswith("wiki/"):
            continue
        if not incoming.get(path):
            findings["Orphan note (nothing links to it)"].append(name)
        if types.get(path) in TYPE_FOLDERS and index not in incoming.get(path, set()):
            findings["Missing from index"].append(name)

    inbox = vault / "inbox"
    pending = sorted(p.name for p in inbox.iterdir() if p.is_file()) if inbox.is_dir() else []

    print(f"Vault: {vault}")
    print(f"Notes: {len(notes)}  ·  waiting in inbox: {len(pending)}")
    if pending:
        print("  " + ", ".join(pending))
    if not findings:
        print("\nNo issues found.")
        return 0
    total = sum(len(v) for v in findings.values())
    print(f"\n{total} finding(s):")
    for title, items in findings.items():
        print(f"\n## {title} ({len(items)})")
        for item in sorted(items):
            print(f"- {item}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
