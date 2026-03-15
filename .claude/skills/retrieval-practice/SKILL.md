---
name: retrieval-practice
description: Use when user asks a conceptual question about course material.
             Follows two-layer retrieval workflow instead of explaining directly.
---

# Two-Layer Retrieval Practice Workflow

When the user asks a conceptual question about course material, follow this workflow instead of explaining directly.

## Step 1 — Point to Notes First

Check the relevant files and point the user to the exact section:
- **Layer 1** (Section summaries in `Artful_Bytes_Transcript/`) — per-lesson terminology, techniques, source code mapping, discussion prompts
- **Layer 2** (`Chat/Class_note/` and `Artful_Byte_Sandbox/`) — deep study notes, architecture docs, hands-on learning checkpoints

Example response:
> "Check `S04_Development_Workflow_Best_Practices.md` → Lesson 008 → Commit Rules (Three Rules). Come back if it doesn't click."

## Step 2 — Only Explain if It Doesn't Click

If the user returns saying the notes didn't make sense, then explain using analogies or diagrams (in chat only — not saved verbatim to notes).

## Step 3 — Prompt a Note Update

After explaining, ask the user to capture it in their own words:
- One-liner insight or factual note → suggest adding to `Chat/Class_note/` (Layer 1)
- Analogy, diagram, or hands-on example → suggest adding to the relevant `Artful_Byte_Sandbox/` README (Layer 2)

## Step 4 — Prompt Understanding Verification

After pointing the user to their notes (Step 1), always end with a prompt like:

> "Come back and tell me what you understood in your own words."

When the user responds with their understanding:
- If correct → confirm briefly and precisely (1-3 sentences max); point out any gaps or nuances they missed; prompt them toward the next concept
- If partially correct → confirm what's right, correct only what's wrong
- If incorrect → ask one targeted question to guide them, don't explain everything at once

This ensures the user initiates the verification loop even if they forget to do so on their own.

## What Each Layer Contains

| Layer | Files | Contains |
|---|---|---|
| 1 | `Artful_Bytes_Transcript/S0X_*.md` | Per-lesson structured summaries: terminology, techniques, source code mapping, demos, discussion prompts |
| 2 | `Chat/Class_note/` | Deep study notes: architecture, coding guidelines, course mapping, troubleshooting |
| 2 | `Artful_Byte_Sandbox/` | Hands-on checkpoints: isolated examples for learning one concept at a time |

### Section File Quick Reference

| File | Lessons | Topic |
|---|---|---|
| `S01_Hardware_Design_Component_Selection.md` | 1-3 | Parts, schematic, PCB |
| `S02_Development_Environment_Setup.md` | 4-5 | IDE, Makefile, toolchain |
| `S03_Software_Architecture_Project_Organization.md` | 6-7 | Layered architecture, project structure |
| `S04_Development_Workflow_Best_Practices.md` | 8-11 | Git, cppcheck, CI/CD, clang-format |
| `S05_Low_Level_Programming_Fundamentals.md` | 12-20 | GPIO, interrupts, UART, memory, IR remote |
| `S06_Motor_Control_PWM.md` | 21 | PWM, TB6612FNG, tank drive |
| `S07_Sensor_Integration.md` | 22-23 | ADC/DMA line sensors, I2C range sensors |
| `S08_System_Integration_Testing.md` | 24-28 | Board bring-up, simulator, state machine, reflection |

## Lean Notes — Format by Concept Type

When prompting the user to update their notes, suggest the right format for the concept:

| Concept Type | Best Format |
|---|---|
| Sequences (boot flow, state machine transitions, build pipeline) | Flowchart / ASCII diagram |
| Spatial (memory map, register layout, PCB layout) | ASCII memory map / block diagram |
| Lookup values (register values, pin assignments, peripheral configs) | Table |
| One critical insight ("poll-based = no RTOS needed") | One-liner sentence |
| Detailed code mechanics | Minimal code snippet |

**The 10-second test:** If the user has to *read* a note rather than *glance* at it, it's still prose — suggest converting it to the appropriate format above.

## Scope Tip

At the start of a session, ask which section (S01-S08) or lesson (1-28) the user is studying. Read only the relevant section file — not the full summary — to stay within context limits.
