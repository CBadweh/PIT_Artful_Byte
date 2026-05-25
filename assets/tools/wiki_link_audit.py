"""
Wiki Link Audit — Obsidian [[wikilink]] health checker

Pseudocode approach:
    1. Glob all .md files in wiki/  ->  set of valid page names (filename minus .md)
    2. For each .md file, regex out every [[target]] and [[target#heading]] link
    3. Cross-reference with set operations:
         broken   = link_targets - valid_pages    (links pointing to nothing)
         orphans  = valid_pages  - all_targets     (pages nobody links to)
         missing  = valid_pages  - index_entries   (pages not listed in index.md)
    4. Check for malformed filenames (double dots, double extensions)
    5. Print report to console

What this approach catches:
    - Broken [[wikilinks]] where the target .md file does not exist
    - Orphan pages with zero inbound links from other wiki pages
    - Pages missing from index.md
    - Malformed filenames (double dots, double extensions)
    - Links inside headings (bad Obsidian practice)

What this approach misses:
    - [[page#heading]] anchor validation — checks if page.md exists, but does NOT
      verify that the ## heading actually exists inside the file
    - Obsidian aliases — if a page has `aliases: [gcov]` in frontmatter,
      [[gcov]] resolves in Obsidian but this script flags it as broken
    - Embeds ![[image.png]] — embedded images/files are not checked
    - Markdown-style links [text](path.md) — only [[wikilink]] syntax is scanned
    - Tag consistency (#tag usage across files)
    - Renamed headings silently breaking existing [[page#old-heading]] links

Better ways:
    - Obsidian graph view: natively shows broken links in a different color,
      handles aliases, anchors, and embeds because it IS the resolver
    - Obsidian Linter plugin: automated rules for anchors, broken links,
      frontmatter consistency — runs inside Obsidian
    - CLI tools (obsidian-export, markdownlint with link plugins): parse full
      Obsidian resolution logic (aliases, case-insensitive, shortest-path)
    - For a small wiki (<50 pages), Obsidian graph view + this script covers ~95%

Run:
    python tools/wiki_link_audit.py
    python tools/wiki_link_audit.py --wiki-dir path/to/wiki
"""

import re
import sys
from pathlib import Path


# --- config ---
STRUCTURAL_PAGES = {"index", "log"}  # never flagged as orphans
SKIP_PREFIX = "_"  # utility files (_link_audit, _ref_*) excluded from orphan/index checks
LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")  # matches [[target]] or [[target#heading]]


def get_valid_pages(wiki_dir: Path) -> set[str]:
    """Return set of valid page names (stem of each .md file)."""
    return {f.stem for f in wiki_dir.glob("*.md")}


def extract_links(filepath: Path) -> list[dict]:
    """Extract all [[wikilinks]] from a file with line numbers."""
    links = []
    for i, line in enumerate(filepath.read_text(encoding="utf-8").splitlines(), 1):
        for match in LINK_PATTERN.finditer(line):
            raw = match.group(1)
            target = raw.split("|")[0].split("#")[0].strip()  # [[page|alias]] or [[page#heading]] -> page
            links.append({
                "source": filepath.stem,
                "target": target,
                "raw": raw,
                "line": i,
                "has_anchor": "#" in raw,
            })
    return links


def check_malformed_filenames(wiki_dir: Path) -> list[dict]:
    """Flag filenames with double dots, double extensions, etc."""
    issues = []
    for f in wiki_dir.glob("*.md"):
        name = f.name
        if name.count(".md") > 1:
            issues.append({"file": name, "problem": "double .md extension"})
        elif name.replace(".md", "").endswith("."):
            issues.append({"file": name, "problem": "trailing dot before .md"})
    return issues


def check_links_in_headings(wiki_dir: Path) -> list[dict]:
    """Find [[links]] used inside markdown headings (bad Obsidian practice)."""
    heading_pattern = re.compile(r"^#{1,6}\s+.*\[\[")
    issues = []
    for f in wiki_dir.glob("*.md"):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if heading_pattern.match(line):
                issues.append({"file": f.stem, "line": i, "heading": line.strip()})
    return issues


def get_index_entries(wiki_dir: Path) -> set[str]:
    """Extract page names referenced in index.md."""
    index_file = wiki_dir / "index.md"
    if not index_file.exists():
        return set()
    text = index_file.read_text(encoding="utf-8")
    return {m.group(1).split("#")[0] for m in LINK_PATTERN.finditer(text)}


def run_audit(wiki_dir: Path) -> None:
    valid_pages = get_valid_pages(wiki_dir)
    index_entries = get_index_entries(wiki_dir)

    # collect all links from all files
    all_links = []
    for f in wiki_dir.glob("*.md"):
        all_links.extend(extract_links(f))

    # --- broken links ---
    all_targets = {link["target"] for link in all_links if link["target"]}
    broken = [link for link in all_links if link["target"] and link["target"] not in valid_pages]

    # --- orphans (no inbound links, excluding structural and utility pages) ---
    inbound_targets = {link["target"] for link in all_links}
    orphans = {p for p in valid_pages if not p.startswith(SKIP_PREFIX)} - inbound_targets - STRUCTURAL_PAGES

    # --- missing from index ---
    indexable_pages = {p for p in valid_pages if not p.startswith(SKIP_PREFIX)} - STRUCTURAL_PAGES
    missing_from_index = indexable_pages - index_entries

    # --- malformed filenames ---
    malformed = check_malformed_filenames(wiki_dir)

    # --- links in headings ---
    heading_links = check_links_in_headings(wiki_dir)

    # --- duplicate links (same target 3+ times in one file) ---
    from collections import Counter
    per_file_counts: dict[str, Counter] = {}
    for link in all_links:
        per_file_counts.setdefault(link["source"], Counter())[link["target"]] += 1
    duplicates = [
        {"source": src, "target": tgt, "count": cnt}
        for src, counter in per_file_counts.items()
        for tgt, cnt in counter.items()
        if cnt >= 3
    ]

    # --- print report ---
    print("=" * 60)
    print("  Wiki Link Audit Report")
    print(f"  Directory: {wiki_dir}")
    print(f"  Pages scanned: {len(valid_pages)}")
    print("=" * 60)

    print(f"\n## Summary\n")
    print(f"  Total pages:           {len(valid_pages)}")
    print(f"  Total unique targets:  {len(all_targets)}")
    print(f"  Broken links:          {len(broken)}")
    print(f"  Orphan pages:          {len(orphans)}")
    print(f"  Missing from index:    {len(missing_from_index)}")
    print(f"  Malformed filenames:   {len(malformed)}")
    print(f"  Links in headings:     {len(heading_links)}")
    print(f"  Duplicate links (3+):  {len(duplicates)}")

    if broken:
        print(f"\n## Broken Links ({len(broken)})\n")
        for link in sorted(broken, key=lambda x: (x["source"], x["line"])):
            anchor = f"  (anchor: #{link['raw'].split('#', 1)[1]})" if link["has_anchor"] else ""
            print(f"  {link['source']}:{link['line']}  ->  [[{link['target']}]]{anchor}")

    if orphans:
        print(f"\n## Orphan Pages ({len(orphans)})\n")
        for page in sorted(orphans):
            in_idx = "in index" if page in index_entries else "NOT in index"
            print(f"  {page}.md  ({in_idx})")

    if missing_from_index:
        print(f"\n## Missing from index.md ({len(missing_from_index)})\n")
        for page in sorted(missing_from_index):
            print(f"  {page}.md")

    if malformed:
        print(f"\n## Malformed Filenames ({len(malformed)})\n")
        for issue in malformed:
            print(f"  {issue['file']}  ->  {issue['problem']}")

    if heading_links:
        print(f"\n## Links in Headings ({len(heading_links)})\n")
        for issue in heading_links:
            print(f"  {issue['file']}:{issue['line']}  {issue['heading']}")

    if duplicates:
        print(f"\n## Duplicate Links (3+ in same file)\n")
        for dup in sorted(duplicates, key=lambda x: (x["source"], -x["count"])):
            print(f"  {dup['source']}  ->  [[{dup['target']}]]  x{dup['count']}")

    # exit code: 1 if any broken links or malformed filenames
    if broken or malformed:
        print(f"\n{'=' * 60}")
        print(f"  ISSUES FOUND — {len(broken)} broken links, {len(malformed)} malformed files")
        print(f"{'=' * 60}")
        sys.exit(1)
    else:
        print(f"\n{'=' * 60}")
        print(f"  ALL CLEAR — no broken links or malformed filenames")
        print(f"{'=' * 60}")


def main():
    """Entry point — resolve wiki directory and run audit."""
    # default: wiki/ relative to this script's repo root
    if len(sys.argv) > 2 and sys.argv[1] == "--wiki-dir":
        wiki_dir = Path(sys.argv[2])
    else:
        wiki_dir = Path(__file__).resolve().parent.parent / "wiki"

    if not wiki_dir.is_dir():
        print(f"Error: wiki directory not found: {wiki_dir}", file=sys.stderr)
        sys.exit(2)

    run_audit(wiki_dir)


if __name__ == "__main__":
    main()
