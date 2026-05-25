#!/usr/bin/env python
"""
parse_session.py

Parses one or more Claude Code JSONL session files and outputs clean
markdown for review. Uses parentUuid to reconstruct the full conversation
tree, correctly handling rewind, fork (esc-esc), and /branch.

Usage:
    py parse_session.py <file1.jsonl> [file2.jsonl ...] > output.md

Goal:
    Show every user prompt and AI response from a Claude Code session,
    organized for review. Multiple session files (from /branch) are
    merged into a single document with shared history printed once.
    Files from different conversations are auto-grouped by root UUID.

Architecture — why parentUuid, not UUID sets:
    v1 used UUID set-intersection across files to find shared history.
    This broke for chain branches (A->B->C), branches from different
    fork points, and couldn't detect esc-esc forks within a single file.

    v2 switched to parentUuid tree-walking because every JSONL record
    points to its parent, forming a linked list (tree at fork points).
    This naturally handles:

    /branch  — creates a NEW .jsonl file (copy of session).
               Detected by: branch's first UUID appears in a different
               file than the trunk.
    esc-esc  — creates a fork WITHIN the same file. A new child is
               appended to an earlier parent; the old child stays.
               Detected by: parent has multiple distinct children in
               the same file. Latest line position = active path.
    /resume  — reopens existing file; new records append linearly.
               No fork or branch — just extends the parentUuid chain.

    At each fork point (parent with N children in one file):
    - All N paths are preserved and printed (no dead branches dropped)
    - The path through the latest child (highest line position) is
      labeled "active path"; earlier paths are labeled "path 1", etc.

    Across files (multi-file /branch):
    - active_path() per file picks latest child at forks (for trunk
      detection via lockstep comparison)
    - Trunk = longest common prefix of all active paths
    - Branches = remaining tails after trunk divergence

    v3 added conversation grouping: files are grouped by root UUID
    so that files from different conversations are processed independently.
    Same root UUID = same conversation (/branch copies the root).

Output structure:
    # Session Metadata          — cwd, file IDs, session names
    # Conversation N            — (only when multiple conversations)
    ## Conversation Tree         — nested diagram: /branch vs fork,
                                   first user prompt per path
    (trunk records)              — shared history (all files)
    ## Branch: <name>            — per-branch content with fork markers
      #### Fork (esc-esc)        — marks where paths diverge
"""

import json, os, re, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

if len(sys.argv) < 2:
    print("Usage: py parse_session.py <file1.jsonl> [file2.jsonl ...]",
          file=sys.stderr)
    sys.exit(1)

paths   = sys.argv[1:]
n_files = len(paths)

# ── 1. Load all records, build per-file tree ─────────────────────────────────
# records        : uuid → record (first occurrence wins for dedup)
# file_children  : per file, {parent_uuid → {child_uuid → max_line_pos}}
# file_roots     : per file, [(uuid, line_pos)] for root nodes (no parent)

records        = {}
file_children  = []
file_roots     = []
session_names  = []
session_ids    = [os.path.splitext(os.path.basename(p))[0] for p in paths]
cwd            = ""

for i, path in enumerate(paths):
    fc   = defaultdict(dict)          # parent → {child → latest line pos}
    fr   = []
    name = ""
    with open(path, encoding="utf-8") as f:
        for j, line in enumerate(f):
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            uid = rec.get("uuid")
            if uid:
                if uid not in records:
                    records[uid] = rec
                parent = rec.get("parentUuid")
                if parent:
                    fc[parent][uid] = max(fc[parent].get(uid, -1), j)
                else:
                    fr.append((uid, j))
            if not name and rec.get("sessionName"):
                name = rec["sessionName"]
            if not cwd and rec.get("cwd"):
                cwd = rec["cwd"]
    file_children.append(fc)
    file_roots.append(fr)
    session_names.append(name)

# ── 1b. Group files by conversation (root UUID) ─────────────────────────────
# Files from the same /branch share the same root UUID.
# Different conversations have different roots.

conv_groups = defaultdict(list)
for i, fr in enumerate(file_roots):
    root_uid = min(fr, key=lambda x: x[1])[0] if fr else f"__empty_{i}__"
    conv_groups[root_uid].append(i)
conv_group_list = list(conv_groups.values())

# ── 2. Utility functions ────────────────────────────────────────────────────

def active_path(file_idx):
    """Return the active conversation path for one file as [uuid, ...]."""
    fr = file_roots[file_idx]
    if not fr:
        return []
    current = max(fr, key=lambda x: x[1])[0]   # latest root
    fc      = file_children[file_idx]
    path    = [current]
    while current in fc:
        kids    = fc[current]                   # {child_uuid → line_pos}
        current = max(kids, key=kids.get)       # latest child wins
        path.append(current)
    return path

def build_path_tree(file_idx, start_uid):
    """Build complete tree of all paths from start_uid (includes dead forks)."""
    fc      = file_children[file_idx]
    linear  = [start_uid]
    current = start_uid
    while current in fc:
        kids = fc[current]
        if len(kids) == 1:
            current = list(kids.keys())[0]
            linear.append(current)
        elif len(kids) > 1:
            sorted_kids = sorted(kids.items(), key=lambda x: x[1])
            forks = [build_path_tree(file_idx, uid) for uid, _ in sorted_kids]
            return {"linear": linear, "forks": forks}
        else:
            break
    return {"linear": linear, "forks": None}

def tree_count(tree):
    """Count total UUIDs across all paths in a tree."""
    n = len(tree["linear"])
    if tree["forks"]:
        for f in tree["forks"]:
            n += tree_count(f)
    return n

def first_user_prompt(uid_list, max_len=60):
    """Return truncated text of the first user message in uid_list."""
    for uid in uid_list:
        rec = records.get(uid)
        if not rec:
            continue
        msg = rec.get("message") or {}
        if msg.get("role") != "user":
            continue
        content = msg.get("content") or ""
        if isinstance(content, list):
            content = " ".join(
                c.get("text", "") for c in content if c.get("type") == "text")
        text = content.strip().replace("\n", " ")
        if text:
            return (text[:max_len] + "...") if len(text) > max_len else text
    return None

# ── 3. Format / print helpers ───────────────────────────────────────────────
tool_calls = {}                                  # tool_use id → (name, input)

def format_record(rec):
    """Return (role, content_str) or None if not a printable record."""
    msg  = rec.get("message") or {}
    role = msg.get("role")
    if role not in ("user", "assistant"):
        return None
    content = msg.get("content") or ""           # handles null
    if isinstance(content, list):
        parts = []
        for c in content:
            ctype = c.get("type")
            if ctype == "text" and c.get("text"):
                parts.append(c["text"])
            elif ctype == "tool_use":
                tool_calls[c["id"]] = (c["name"], c.get("input", {}))
            elif ctype == "tool_result":
                call = tool_calls.get(c.get("tool_use_id", ""))
                if call:
                    name, inp = call
                    cmd = (inp.get("command") or inp.get("file_path")
                           or inp.get("pattern") or str(inp))
                    parts.append(f"```\n[TOOL CALL]: {name}({cmd})\n```")
            elif ctype == "image":
                parts.append("[IMAGE]")
            # thinking blocks: skip silently
        content = "\n\n".join(parts)
    return role, content

def print_record(rec):
    result = format_record(rec)
    if not result:
        return
    role, content = result
    if not content.strip():
        return
    first_char = content.strip()[0]
    if role == "user" and first_char in ("<", "[", "`"):
        print(f"\n{content}")                    # command/tool/code lines — no header
        return
    if role == "assistant":
        lines   = content.split("\n")
        out     = []
        in_fence = False
        for line in lines:
            if line.strip().startswith("```"):
                in_fence = not in_fence
                out.append(line)
            elif not in_fence:
                out.append(re.sub(r'^#{1,6} ', '#### ', line))
            else:
                out.append(line)
        content = "\n".join(out)
    content = content.lstrip("\n")
    if role == "assistant":
        print(f"\n ASSISTANT\n{content}")
    else:
        split      = content.split("\n", 1)
        first_line = split[0]
        rest       = split[1] if len(split) > 1 else ""
        if rest.strip():
            print(f"\n## USER {first_line}\n{rest}")
        else:
            print(f"\n## USER {first_line}")

def print_records(uid_list):
    for uid in uid_list:
        rec = records.get(uid)
        if rec:
            print_record(rec)

def print_path_tree(tree, depth=0):
    """Print records from a path tree, showing fork markers."""
    print_records(tree["linear"])
    if tree["forks"]:
        for idx, fork in enumerate(tree["forks"]):
            is_last = idx == len(tree["forks"]) - 1
            prompt  = first_user_prompt(fork["linear"])
            ptext   = f" — \"{prompt}\"" if prompt else ""
            if is_last:
                print(f"\n\n{'#' * min(depth + 4, 6)} Fork (esc-esc) — active path{ptext}\n")
            else:
                print(f"\n\n{'#' * min(depth + 4, 6)} Fork (esc-esc) — path {idx + 1}{ptext}\n")
            print_path_tree(fork, depth + 1)

# ── 4. Session metadata ─────────────────────────────────────────────────────
print("# Session Metadata")
print(f"- **cwd:** {cwd or '(unknown)'}")
for i, (sid, name) in enumerate(zip(session_ids, session_names)):
    label = f" — {name}" if name else ""
    print(f"- **File {i + 1}:** {sid}{label}")

if len(conv_group_list) > 1:
    print(f"\n**{len(conv_group_list)} separate conversations detected.**")
    for g_idx, group in enumerate(conv_group_list):
        file_labels = ", ".join(f"File {i + 1}" for i in group)
        print(f"- Conversation {g_idx + 1}: {file_labels}")

# ── 5. Process one conversation group ────────────────────────────────────────

def process_group(file_indices):
    """Process and print one conversation group (files sharing a root UUID)."""
    n_group = len(file_indices)

    # ── 5a. Trunk / branch split ────────────────────────────────────────
    group_paths = [active_path(fi) for fi in file_indices]

    trunk    = []
    branches = {}                                # file_idx → [uuids]

    if n_group == 1:
        trunk = group_paths[0]
    else:
        min_len = min(len(p) for p in group_paths) if group_paths else 0
        for idx in range(min_len):
            if len({p[idx] for p in group_paths}) == 1:
                trunk.append(group_paths[0][idx])
            else:
                break
        for pos, p in enumerate(group_paths):
            tail = p[len(trunk):]
            if tail:
                branches[file_indices[pos]] = tail

    branch_trees = {i: build_path_tree(i, branches[i][0]) for i in branches}

    # Trunk forks (intra-file forks within trunk)
    trunk_forks = {}
    if trunk and file_indices:
        ref_fi = file_indices[0]
        for idx in range(len(trunk) - 1):
            uid      = trunk[idx]
            next_uid = trunk[idx + 1]
            kids     = file_children[ref_fi].get(uid, {})
            dead     = {k: v for k, v in kids.items() if k != next_uid}
            if dead:
                trunk_forks[uid] = [
                    build_path_tree(ref_fi, k)
                    for k in sorted(dead, key=dead.get)]

    # ── 5b. Conversation tree ───────────────────────────────────────────
    if n_group > 1:
        print("\n## Conversation Tree\n")

        trunk_prompts = [first_user_prompt([u]) for u in trunk]
        trunk_prompts = [p for p in trunk_prompts if p]

        print(f"Trunk — {len(trunk)} records")
        for tp in trunk_prompts:
            print(f'│ "{tp}"')

        # Classify branches: /branch vs fork (esc-esc)
        branch_info     = {}
        branch_parent   = {}
        branch_children = defaultdict(list)

        if trunk and branches:
            fork_point   = trunk[-1]
            branch_first = {branches[i][0]: i for i in branches}

            for fi in file_indices:
                kids = file_children[fi].get(fork_point, {})
                bk = {uid: kids[uid] for uid in kids if uid in branch_first}
                if len(bk) <= 1:
                    continue
                sorted_kids = sorted(bk.items(), key=lambda x: x[1])
                origin_branch = branch_first[sorted_kids[0][0]]
                for uid, _ in sorted_kids[1:]:
                    fork_branch = branch_first[uid]
                    branch_info[fork_branch] = {
                        "type": "fork", "origin": origin_branch}
                    branch_parent[fork_branch] = origin_branch
                    branch_children[origin_branch].append(fork_branch)

        for i in branches:
            if i not in branch_info:
                branch_info[i] = {"type": "branch", "origin": None}

        # Print intra-file fork tree
        def print_fork_tree(forks, prefix):
            for pos, fork in enumerate(forks):
                is_last   = pos == len(forks) - 1
                connector = "└── " if is_last else "├── "
                cont      = "    " if is_last else "│   "
                prompt    = first_user_prompt(fork["linear"])
                ptext     = f': "{prompt}"' if prompt else ""
                print(f"{prefix}{connector}fork (esc-esc){ptext}")
                if fork["forks"]:
                    print_fork_tree(fork["forks"], prefix + cont)

        # Print nested branch tree
        def print_tree(entries, prefix=""):
            for pos, (kind, fi) in enumerate(entries):
                is_last   = pos == len(entries) - 1
                connector = "└── " if is_last else "├── "
                cont      = "    " if is_last else "│   "

                if kind == "trunk_only":
                    name = session_names[fi] or session_ids[fi][:8]
                    print(f"{prefix}{connector}(trunk only): {name}")
                else:
                    info  = branch_info[fi]
                    name  = session_names[fi] or session_ids[fi][:8]
                    count = tree_count(branch_trees[fi])
                    label = ("fork (esc-esc)"
                             if info["type"] == "fork" else "/branch")
                    prompt = first_user_prompt(branches[fi])
                    kids   = branch_children.get(fi, [])
                    tree   = branch_trees[fi]

                    print(f"{prefix}{connector}{label}: {name}"
                          f" ({count} records)")

                    has_sub = kids or (tree and tree["forks"])
                    if prompt and has_sub:
                        print(f'{prefix}{cont}│ "{prompt}"')
                    elif prompt:
                        print(f'{prefix}{cont}  "{prompt}"')

                    if tree and tree["forks"]:
                        print(f"{prefix}{cont}│")
                        print_fork_tree(tree["forks"], prefix + cont)

                    if kids:
                        if not (tree and tree["forks"]):
                            print(f"{prefix}{cont}│")
                        child_entries = [
                            (branch_info[k]["type"], k) for k in kids]
                        print_tree(child_entries, prefix + cont)

                if not is_last:
                    print(f"{prefix}│")

        top = [("branch", i) for i in branches if i not in branch_parent]
        top += [("trunk_only", i)
                for i in file_indices if i not in branches]
        print("│")
        print_tree(top)

    # ── 5c. Body output ─────────────────────────────────────────────────
    if n_group == 1:
        fi = file_indices[0]
        root = max(file_roots[fi], key=lambda x: x[1])[0]
        single_tree = build_path_tree(fi, root)
        print_path_tree(single_tree)
    else:
        if trunk_forks:
            for uid in trunk:
                rec = records.get(uid)
                if rec:
                    print_record(rec)
                if uid in trunk_forks:
                    for dead_tree in trunk_forks[uid]:
                        prompt = first_user_prompt(dead_tree["linear"])
                        ptext  = f" — \"{prompt}\"" if prompt else ""
                        print(f"\n\n#### Fork (esc-esc)"
                              f" — abandoned path{ptext}\n")
                        print_path_tree(dead_tree, depth=1)
                        print(f"\n\n#### (continued on active path)\n")
        else:
            print_records(trunk)

        for fi in file_indices:
            if fi not in branches:
                continue
            name = session_names[fi] or session_ids[fi][:8]
            print(f"\n\n## Branch: {name}")
            print_path_tree(branch_trees[fi])

# ── 6. Main loop — process each conversation group ──────────────────────────

for g_idx, group in enumerate(conv_group_list):
    if len(conv_group_list) > 1:
        names = [session_names[i] for i in group if session_names[i]]
        group_name = (names[0] if names
                      else session_ids[group[0]][:8])
        print(f"\n\n---\n# Conversation {g_idx + 1}: {group_name}\n")
    process_group(group)
