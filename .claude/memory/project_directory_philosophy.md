---
name: Directory Organization Philosophy
description: CBadweh's directory structure conventions for course study repos — Code vs Sandbox vs Transcript roles and reasoning
type: project
---

CBadweh organizes each course study repo into three core directories, each with a distinct role:

## `Code/` — Implementations with real code

- `source_code/` holds the **unmodified upstream reference** (git-cloned, never modified). This is the complete finished project for read-only reference.
- Other subdirectories hold **feature branches, CBadweh's own experiments**, and anything with actual working implementations.

## `Artful_Byte_Sandbox/` (or `*_Sandbox/`) — Learning checkpoints

Minimal, isolated examples stripped of dependencies. Each checkpoint lets you explore **one concept at a time** without the complexity of the full project.

**Why:** The completed source code has many integrated dependencies. When exploring a basic concept (e.g., how a Makefile works), the full project's Makefile is overwhelming because it includes CI targets, conditional compilation, multi-hardware support, static analysis, etc. A checkpoint like `blink_example/` contains only the bare essentials — making the concept easy to understand.

**What goes here:** Milestone snapshots from the course, stripped-down examples, CCS projects used for verification, anything that serves as a reference point for a specific lesson or concept.

## `*_Transcript/` — Course content

Lesson transcripts (`.txt` files) plus AI-generated summaries and per-section summary files. This is the knowledge base, not code.

## `Chat/` — AI conversation logs and class notes

Notes from AI conversations, troubleshooting logs, and class-related notes.

**How to apply:** When CBadweh creates a new course study repo or adds content to this one, follow these conventions. Code goes in `Code/`, checkpoints go in `Sandbox/`, transcripts go in `Transcript/`. When CBadweh says "CBadweh" in a folder name, it means their own implementation/experiment.
