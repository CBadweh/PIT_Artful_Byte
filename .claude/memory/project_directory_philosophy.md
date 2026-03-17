---
name: Directory Organization Philosophy
description: CBadweh's workspace design — two phases (Learning/Referencing), two layers (Overview/Detail), and how each directory serves them. Blueprint for new course workspaces.
type: project
---

## Two Phases

### Phase 1 — Learning
Actively following the course. `Code/` has working implementations that get modified lesson by lesson. As concepts are learned, notes get appended directly to `S0X_*.md` section files under the specific lesson. At section or milestone boundaries, working code moves from `Code/` to `*_Sandbox/` as a checkpoint.

### Phase 2 — Referencing
Looking up what was learned. The reference system is Layer 1 (course summary for overview) and Layer 2 (section files + sandbox READMEs for detail).

## Two Layers (by detail level)

| Layer | Files | Purpose |
|-------|-------|---------|
| 1 — Overview | `*_Transcript/XXX_ClaudeOpus_Summary.md` | Full course summary. First place to check for big-picture questions. |
| 2 — Detail | `*_Transcript/S0X_*.md` | Per-section depth: terminology, techniques, code snippets, CBadweh's appended notes. |
| 2 — Detail | `*_Sandbox/` | Hands-on checkpoints with READMEs: isolated examples created at learning milestones. |
| Source of truth | `Code/source_code/` | The actual codebase. Reference when Layers 1–2 don't suffice. |

## Directory → Phase/Layer Mapping

- **`Code/source_code/`** — Read-only upstream reference. Source of truth for both phases. Never modify.
- **`Code/` (other folders)** — Active during Phase 1. Working implementations that get modified as lessons progress. At milestones, code moves to Sandbox.
- **`*_Transcript/XXX_ClaudeOpus_Summary.md`** — Layer 1. AI-generated course overview for big-picture questions.
- **`*_Transcript/S0X_*.md`** — Layer 2. Per-section detail. Notes from learning get appended here under specific lessons — this is where "chat" insights are captured (no separate Chat/ directory).
- **`*_Sandbox/`** — Layer 2. Created at milestones during Phase 1 (code moves from Code/). Referenced during Phase 2 via READMEs. Each checkpoint isolates one concept without full-project complexity.

### Why Sandbox Exists
The completed source code has many integrated dependencies. When exploring a basic concept (e.g., how a Makefile works), the full project's Makefile is overwhelming because it includes CI targets, conditional compilation, multi-hardware support, etc. A Sandbox checkpoint contains only the bare essentials.

**How to apply:** When creating a new course workspace, follow these conventions. Working code goes in `Code/`, milestone checkpoints go in `*_Sandbox/`, transcripts and notes go in `*_Transcript/`. All learning notes get appended to section files — no separate Chat/ directory.
