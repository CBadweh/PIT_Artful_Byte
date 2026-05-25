"""lint_md.py — Auto-fix markdown files pasted from Claude Code sessions.

Problem this solves
-------------------
Pasting Claude Code terminal output into .md files leaves Unicode artifacts that
cost tokens and context to fix manually:
  - ╌╌╌╌  separators (terminal rendering of horizontal rules)
  - ▎      blockquote sidebar markers
  - ●      Claude response bullet
  - ❯      user prompt marker
  - ASCII box-drawing tables  (┌─┬│├┼└)
  - 2-space leading indent on every body paragraph

This script fixes all of them deterministically — no LLM needed.

Pipeline (order matters)
------------------------
Pre-scans (run first, no output changes):
  1. fence_regions()           → set of line indices inside ``` blocks
  2. find_ascii_table_spans()  → list of (start, end) index ranges for box tables

Fix passes (in this order — dependencies explained inline):
  3. fix_ascii_tables()          tables first, before whitespace strip touches them
  4. fix_unicode_separators()    ╌╌╌╌ → ---
  5. fix_blockquote_markers()    ▎ → >
  6. fix_chat_markers()          ● → **Claude:**
  7. fix_prompt_markers()        ❯ → **CBadweh:**
  8. strip_leading_whitespace()  lstrip() body lines; skip fences + list continuations
  9. strip_trailing_whitespace() rstrip() every line (always last)

Flag passes (read-only, never modify):
  10. flag_plain_text_headings() short lines with no punctuation end — may be headers
  11. flag_bare_code_blocks()    lines matching C/shell patterns outside fences

Pseudocode: leading whitespace strip
-------------------------------------
  in_fence = False
  prev_was_list = False
  for each line:
      if line starts with ```:
          toggle in_fence
      if in_fence or in table span:
          keep line as-is              ← never touch code blocks or tables
      else:
          stripped = line.lstrip()
          if line had indent AND prev line was a list item AND stripped is not a new item:
              keep line as-is          ← preserve markdown list continuation indent
          else:
              emit stripped            ← remove all leading whitespace
          prev_was_list = stripped starts with  -  *  or  1.

Pseudocode: ASCII table conversion
------------------------------------
  for each line in block:
      if line starts with ┌ ├ └  → border row → skip
      if line starts with │      → data row   → split on │, strip each cell
  first data row  → emit as markdown header  | col | col |
                    emit separator            |-----|-----|
  remaining rows  → emit as                  | val | val |

Usage:
    python lint_md.py <file>            fix in-place + print summary
    python lint_md.py <file> --dry-run  unified diff to stdout, no write
    python lint_md.py <file> --report   summary only, no write
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

# Box-drawing character sets used to detect ASCII table lines.
# BOX_BORDER covers every character that can appear in a border-only row.
# Data rows (│ cell │ cell │) are detected separately in is_box_line().
BOX_TOP    = set('┌┬┐')          # top border corners and junctions
BOX_MID    = set('├┼┤')          # mid-row dividers
BOX_BOT    = set('└┴┘')          # bottom border corners and junctions
BOX_BORDER = BOX_TOP | BOX_MID | BOX_BOT | {'─', '│'}

# Matches the opening of any fenced code block (``` or ```` etc.)
FENCE_RE   = re.compile(r'^(`{3,})')

# Heading flag heuristic: short line, no trailing punctuation, no inline markup.
# Conservative — only flags, never modifies.
_HEADING_PUNCT = set('.,:;?!)"\u2019')
_HEADING_MD    = re.compile(r'\*\*|\*|`|\[')

# Bare code heuristics — patterns that look like code but aren't inside fences.
# Inline backtick spans (e.g. `func()`) are stripped before matching to avoid
# flagging function names mentioned in prose.
_CODE_HINTS = re.compile(
    r'(\w+\([^)]*\);)'          # function call ending with semicolon: foo(x);
    r'|(->\w)'                  # C pointer dereference with no space: ptr->field
    r'|(^\s{4,}\S)'             # 4+ space indent (traditional Markdown code block)
    r'|(^\s*\$\s)'              # shell prompt line: $ command
    r'|(#include|#define|uint\d+_t)',  # C preprocessor directives or fixed-width types
    re.MULTILINE
)


# ── Detection helpers ──────────────────────────────────────────────────────────

def fence_regions(lines):
    """Return (fenced_set, unclosed_line) where fenced_set is the set of line indices
    inside ``` fences and unclosed_line is the 1-based line number of an unclosed opening
    fence (or None if all fences are balanced).

    An unclosed fence means everything after it would be wrongly treated as code.
    We detect it and exclude those lines from the fenced set so the content can
    still be processed — then warn the caller via the returned line number.
    """
    fenced = set()
    in_fence = False
    last_open_idx = None  # line index of the most recent unmatched ``` open

    for i, line in enumerate(lines):
        if FENCE_RE.match(line.lstrip()):
            in_fence = not in_fence
            fenced.add(i)
            if in_fence:
                last_open_idx = i   # record where this fence opened
            else:
                last_open_idx = None  # fence was closed — clear it
        elif in_fence:
            fenced.add(i)

    if in_fence and last_open_idx is not None:
        # Unclosed fence — remove everything from the opening ``` onward
        # so the content is still processed, then return the line number as a warning
        for j in range(last_open_idx, len(lines)):
            fenced.discard(j)
        return fenced, last_open_idx + 1  # 1-based for display

    return fenced, None


def is_box_line(line):
    """True if the line is part of an ASCII table (border row or data row starting with │)."""
    s = line.strip()
    if not s:
        return False
    # Pure border line (all box-drawing characters)
    if all(ch in BOX_BORDER for ch in s):
        return True
    # Data row: starts and ends with │ and contains at least one more │
    if s.startswith('│') and s.endswith('│') and s.count('│') >= 2:
        return True
    return False


def find_ascii_table_spans(lines, fenced):
    """Return list of (start, end) half-open index ranges for contiguous box-drawing blocks."""
    spans = []
    i = 0
    while i < len(lines):
        if i not in fenced and is_box_line(lines[i]):
            start = i
            while i < len(lines) and i not in fenced and is_box_line(lines[i]):
                i += 1
            spans.append((start, i))
        else:
            i += 1
    return spans


def _span_set(spans):
    """Expand list of (start, end) spans into a flat set of indices."""
    result = set()
    for s, e in spans:
        result.update(range(s, e))
    return result


# ── ASCII Table Conversion ────────────────────────────────────────────────────

def _parse_cells(line):
    """Split a │-delimited data row into a list of stripped cell strings."""
    s = line.strip()
    parts = s.split('│')
    # Drop the first and last empty tokens produced by leading/trailing │
    return [p.strip() for p in parts[1:-1]]


def _row_to_md(cells, widths=None):
    if widths:
        padded = [c.ljust(w) for c, w in zip(cells, widths)]
    else:
        padded = cells
    return '| ' + ' | '.join(padded) + ' |'


def _sep_row(widths):
    return '| ' + ' | '.join('-' * max(w, 3) for w in widths) + ' |'


def convert_ascii_table(block_lines):
    """Convert a list of box-drawing lines to markdown table lines."""
    data_rows = []
    for line in block_lines:
        s = line.strip()
        if not s:
            continue
        first = s[0]
        if first in BOX_TOP or first in BOX_MID or first in BOX_BOT:
            continue  # border line — skip
        if first == '│':
            cells = _parse_cells(s)
            if cells:
                data_rows.append(cells)

    if not data_rows:
        return block_lines  # nothing parseable — leave as-is

    # Normalise column count
    col_count = max(len(r) for r in data_rows)
    data_rows = [r + [''] * (col_count - len(r)) for r in data_rows]

    # Column widths
    widths = [max(len(row[c]) for row in data_rows) for c in range(col_count)]

    out = []
    out.append(_row_to_md(data_rows[0], widths) + '\n')  # header
    out.append(_sep_row(widths) + '\n')                   # separator
    for row in data_rows[1:]:
        out.append(_row_to_md(row, widths) + '\n')

    return out


# ── Fix passes ────────────────────────────────────────────────────────────────

def fix_ascii_tables(lines, spans):
    """Replace ASCII table blocks with markdown tables. Returns (new_lines, count)."""
    if not spans:
        return list(lines), 0

    out = []
    count = 0
    span_map = {s: e for s, e in spans}
    i = 0
    while i < len(lines):
        if i in span_map:
            end = span_map[i]
            block = lines[i:end]
            out.extend(convert_ascii_table(block))
            count += 1
            i = end
        else:
            out.append(lines[i])
            i += 1
    return out, count


def fix_unicode_separators(lines, fenced, skip):
    """Replace lines consisting entirely of ╌ characters with ---."""
    out = []
    count = 0
    for i, line in enumerate(lines):
        if i not in fenced and i not in skip:
            stripped = line.strip()
            if stripped and all(ch in '╌╍' for ch in stripped):
                ending = '\n' if line.endswith('\n') else ''
                out.append('---' + ending)
                count += 1
                continue
        out.append(line)
    return out, count


def fix_blockquote_markers(lines, fenced, skip):
    """Replace ▎ at line start with >."""
    out = []
    count = 0
    pattern = re.compile(r'^(\s*)▎\s?')
    for i, line in enumerate(lines):
        if i not in fenced and i not in skip:
            new, n = pattern.subn(r'\1> ', line)
            if n:
                out.append(new)
                count += n
                continue
        out.append(line)
    return out, count


def fix_chat_markers(lines, fenced):
    """Replace ● at line start with **Claude:**."""
    out = []
    count = 0
    pattern = re.compile(r'^●\s*')
    for i, line in enumerate(lines):
        if i not in fenced:
            new, n = pattern.subn('**Claude:** ', line)
            if n:
                out.append(new)
                count += n
                continue
        out.append(line)
    return out, count


def fix_prompt_markers(lines, fenced):
    """Replace ❯ at line start with **CBadweh:**."""
    out = []
    count = 0
    pattern = re.compile(r'^❯\s*')
    for i, line in enumerate(lines):
        if i not in fenced:
            new, n = pattern.subn('**CBadweh:** ', line)
            if n:
                out.append(new)
                count += n
                continue
        out.append(line)
    return out, count


def strip_leading_whitespace(lines, fenced, skip):
    """Strip leading whitespace from body lines; preserve list continuations."""
    out = []
    count = 0
    prev_was_list = False
    in_fence = False

    for i, line in enumerate(lines):
        if FENCE_RE.match(line.lstrip()):
            in_fence = not in_fence

        if i in fenced or i in skip:
            out.append(line)
            prev_was_list = False
            continue

        stripped = line.lstrip()
        has_indent = line != stripped and stripped  # non-empty, had leading space

        if has_indent:
            is_continuation = (
                prev_was_list
                and not stripped.startswith(('-', '*', '>', '#', '|'))
                and not re.match(r'^\d+\.', stripped)
            )
            if is_continuation:
                out.append(line)  # preserve intentional list continuation
            else:
                out.append(stripped)
                count += 1
        else:
            out.append(line)

        # Track list state for next iteration
        prev_was_list = bool(re.match(r'^[-*]|\d+\.', stripped or line.lstrip()))

    return out, count


def strip_trailing_whitespace(lines):
    """Strip trailing whitespace from every line."""
    out = []
    count = 0
    for line in lines:
        new = line.rstrip(' \t')  # preserve \n
        if new != line:
            count += 1
        out.append(new)
    return out, count


# ── Flag passes (read-only) ───────────────────────────────────────────────────

def flag_plain_text_headings(lines, fenced):
    """Flag lines that look like unformatted headings."""
    flags = []
    for i, line in enumerate(lines):
        if i in fenced:
            continue
        s = line.strip()
        if not s:
            continue
        if s[0] in ('#', '-', '*', '>', '|', '`'):
            continue
        if re.match(r'^\d+\.', s):
            continue
        if _HEADING_MD.search(s):
            continue
        words = s.split()
        if 2 <= len(words) <= 7 and s[-1] not in _HEADING_PUNCT:
            flags.append((i + 1, s))
    return flags


def flag_bare_code_blocks(lines, fenced, skip):
    """Flag lines outside fences that look like code but aren't fenced."""
    _backtick_span = re.compile(r'`[^`]+`')
    flags = []
    for i, line in enumerate(lines):
        if i in fenced or i in skip:
            continue
        s = line.strip()
        if not s or s.startswith(('`', '#', '|', '>', '-', '*')):
            continue
        # Remove inline code spans before checking — function() in prose is fine
        bare = _backtick_span.sub('', s)
        if _CODE_HINTS.search(bare):
            flags.append((i + 1, s))
    return flags


# ── Pipeline ──────────────────────────────────────────────────────────────────

def pipeline(lines):
    """Run all fix and flag passes. Returns (fixed_lines, stats, flags)."""
    stats = {}

    # Pre-scans (use original line list)
    fenced, unclosed = fence_regions(lines)
    spans  = find_ascii_table_spans(lines, fenced)
    skip   = _span_set(spans)

    # Fix passes (order matters — see plan)
    lines, stats['ascii_tables']       = fix_ascii_tables(lines, spans)
    # Recompute fenced/skip after table conversion (line count unchanged, content changed)
    fenced, unclosed = fence_regions(lines)
    skip   = _span_set(find_ascii_table_spans(lines, fenced))  # should be 0 now

    lines, stats['unicode_separators'] = fix_unicode_separators(lines, fenced, skip)
    lines, stats['blockquote_markers'] = fix_blockquote_markers(lines, fenced, skip)
    lines, stats['chat_markers']       = fix_chat_markers(lines, fenced)
    lines, stats['prompt_markers']     = fix_prompt_markers(lines, fenced)
    lines, stats['leading_indents']    = strip_leading_whitespace(lines, fenced, skip)
    lines, stats['trailing_ws']        = strip_trailing_whitespace(lines)

    # Recompute fenced after all fixes for flag passes
    fenced, unclosed = fence_regions(lines)
    skip   = _span_set(find_ascii_table_spans(lines, fenced))

    flags = {
        'headings':   flag_plain_text_headings(lines, fenced),
        'bare_code':  flag_bare_code_blocks(lines, fenced, skip),
        'unclosed_fence': [unclosed] if unclosed else [],
    }

    return lines, stats, flags


# ── Output helpers ────────────────────────────────────────────────────────────

def build_diff(orig, fixed, filename):
    return ''.join(difflib.unified_diff(orig, fixed, fromfile=filename, tofile=filename))


def print_summary(filename, stats, flags):
    labels = {
        'unicode_separators': 'unicode separators',
        'ascii_tables':       'ASCII tables',
        'blockquote_markers': 'blockquote markers',
        'chat_markers':       'chat markers (●)',
        'prompt_markers':     'prompt markers (❯)',
        'leading_indents':    'leading indents',
        'trailing_ws':        'trailing whitespace',
    }
    print(f'lint_md: {filename}')
    for key, label in labels.items():
        n = stats.get(key, 0)
        if n:
            print(f'  fixed  {n} {label}')

    unclosed_flags = flags.get('unclosed_fence', [])
    heading_flags  = flags.get('headings', [])
    code_flags     = flags.get('bare_code', [])

    if unclosed_flags:
        print(f'  warn   unclosed ``` fence at line {unclosed_flags[0]} — content below was processed anyway')

    if heading_flags:
        linenos = ', '.join(str(ln) for ln, _ in heading_flags)
        print(f'  flag   {len(heading_flags)} possible plain-text headings (lines {linenos})')

    if code_flags:
        linenos = ', '.join(str(ln) for ln, _ in code_flags)
        print(f'  flag   {len(code_flags)} possible bare code blocks (lines {linenos})')

    total_fixed = sum(stats.values())
    if total_fixed == 0 and not unclosed_flags and not heading_flags and not code_flags:
        print('  ok     nothing to fix')


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description='Auto-fix markdown files pasted from Claude Code sessions.'
    )
    p.add_argument('file', type=Path, help='Markdown file to lint')
    p.add_argument('--dry-run', action='store_true',
                   help='Print unified diff; do not write')
    p.add_argument('--report', action='store_true',
                   help='Print summary only; do not write')
    return p.parse_args()


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    args = parse_args()

    if not args.file.exists():
        print(f'lint_md: error: {args.file} not found', file=sys.stderr)
        return 1

    text  = args.file.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)

    fixed, stats, flags = pipeline(lines)

    if args.dry_run:
        diff = build_diff(lines, fixed, args.file.name)
        if diff:
            print(diff, end='')
        else:
            print(f'lint_md: {args.file.name} — no changes')
        return 0

    if not args.report:
        args.file.write_text(''.join(fixed), encoding='utf-8')

    print_summary(args.file.name, stats, flags)
    return 0


if __name__ == '__main__':
    sys.exit(main())
