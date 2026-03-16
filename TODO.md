# Session Summary — 2026-03-15/16

## 1. Retrieval-Practice Skill Setup

### Tasks
- [x] Copied retrieval-practice skill from another course, updated for Artful_Byte
- [x] Updated Layer 1 references: `Artful_Bytes_Transcript/S0X_*.md` section files
- [x] Updated Layer 2 references: `Chat/Class_note/` and `Artful_Byte_Sandbox/`
- [x] Widened trigger: fires on ANY question where section files have relevant content (not just "conceptual questions")
- [x] Updated Step 2: first question always points to notes; only explain directly on 2nd/3rd follow-up

### Lesson Learned
- Retrieval practice should trigger on code/Makefile/tool questions too — not just "what is X?" conceptual questions. The section files already have source code mappings and demo flows.

---

## 2. Memory System Created

### Tasks
- [x] Created `feedback_commit_conventions.md` — all commits must follow Conventional Commits with WHY body
- [x] Created `feedback_append_to_section_files.md` — append diagrams/explanations to S0X_*.md, never create standalone files
- [x] Created `project_directory_philosophy.md` — Code vs Sandbox vs Transcript structure
- [x] Updated `MEMORY.md` index for all three

### Lesson Learned
- Standalone note files become orphans. Co-locating supplementary content (diagrams, code snippets) with the lesson in section files keeps everything in one retrieval point.

---

## 3. Lesson 8 Review — Git Best Practices

### Tasks
- [x] Reviewed Lesson 8 content from S04 section file
- [x] Created 3 ASCII diagrams from video screenshots (commit history, distributed backup, collaboration/branching)
- [x] Appended diagrams to S04 under Lesson 008
- [x] Deleted standalone `Chat/Class_note/8_Git_Best_Practices_Diagrams.md` (co-location principle)
- [x] Added "commit template" note from our discussion about Vim and `git commit` without `-m`

### Reviewed `Code/nsumo_video-feature_io_handling_2` against Lesson 8
- **PASS:** .gitignore, .gitmodules, .clang-format, CI, project structure
- **FAIL:** No Conventional Commits format, no commit bodies explaining WHY, some bundled commits
- Result: This is a **workflow habit change**, not a code fix

---

## 4. Lesson 9 Review — cppcheck / Static Analysis

### Tasks
- [x] Summarized essential topics
- [x] Verified cppcheck implementation in `Code/nsumo_video-feature_io_handling_2/Makefile:23,48-57,78,88-89`
- [x] Traced `make cppcheck` to the manual command it automates

---

## 5. S04 Sandbox Checkpoint Created

### Tasks
- [x] Copied `Code/nsumo_video-feature_io_handling_2/` → `Artful_Byte_Sandbox/S04_Development_Workflow/`
- [x] Removed Lesson 12-13 code (io.c, mcu_init.c, drive.c, enemy.c, test.c + headers)
- [x] Simplified main.c to minimal blink (Lesson 5 style)
- [x] Updated Makefile to remove deleted source references
- [x] Added PLACEHOLDER files for empty src/ directories
- [x] Rewrote README.md to match blink_example format (lean, with reference to S04 section file)
- [x] Verified: `make` builds, `make cppcheck` passes

### What Went Wrong
- `make format` failed — `clang-format-12` not installed locally (expected — it's in the Docker CI container from Lesson 10)

### Lesson Learned
- The `nsumo_video-feature_io_handling_2` directory is a Lesson 12-13 snapshot, not Lesson 9. Creating a clean checkpoint per section keeps the learning focused.

---

## 6. Lesson 10 — CI/CD with GitHub Actions and Docker

### Tasks
- [x] Read transcript and created 4 ASCII diagrams from video screenshots:
  1. Bringing It All Together (Makefile + Git + cppcheck → CI)
  2. CI/CD Developer Workflow (branch → push → PR → CI → merge/rework)
  3. CI as Protection Wall (firewall blocking broken code from main)
  4. GitHub Actions Architecture Stack (VM → Linux → Docker → Job)
- [x] Appended diagrams to S04 under Lesson 010's Objective
- [x] Appended exact terminal commands from video (Docker install, wget URLs, toolchain setup)
- [x] Appended Lesson 10 version of `ci.yml` (simpler than final version)

### Docker Hands-On
- [x] Built base image from `tools/dockerfile` (`docker build -t msp430-gcc .`)
- [x] Entered container (`docker run --interactive --tty`)
- [x] Attempted to download toolchain from TI — **404 error** (TI broke the URL, exactly as instructor warned)
- [x] Attempted to `docker cp` local Windows toolchain into Linux container — copied but **binaries are .exe** (won't run on Linux)
- [x] Pulled instructor's pre-built image: `docker pull artfulbytes/msp430-gcc-9.3.1.11:latest`
- [x] Verified Linux toolchain works inside container: `msp430-elf-gcc 9.3.1` runs correctly

### What Went Wrong
| Issue | Cause | Resolution |
|-------|-------|------------|
| `docker run ... /bin/bash` error | Git Bash converts `/bin/bash` to Windows path | Use `//bin/bash` (double slash) |
| 2 containers created from failed attempts | Every `docker run` creates a new container, even on failure | Delete unused containers |
| TI download URL 404 | TI updated their website (exactly the scenario Docker solves) | Used `docker cp` then switched to instructor's pre-built image |
| Windows toolchain in Linux container | `.exe` binaries don't run on Linux | Pulled `artfulbytes/msp430-gcc-9.3.1.11:latest` from Docker Hub |
| `docker cp` destination not found | Directory didn't exist inside container before copy | Must `mkdir -p` inside container first |

### Git/GitHub Workflow
- [x] Pushed `main` branch to remote (didn't exist on GitHub before)
- [x] Set up branch protection rules on `main` (require PR, require CI, no bypass)
- [x] Merged `fixed-Makefile` into `main` locally
- [x] Direct push to `main` blocked by branch protection — temporarily removed rule, pushed, re-added rule
- [x] CI triggered on push — **failed**: `"No targets specified and no makefile found"`

### What Went Wrong — CI
| Issue | Cause | Resolution |
|-------|-------|------------|
| CI can't find Makefile | `main.yml` runs `make` from repo root, but Makefile is in `Code/nsumo_video-feature_io_handling_2/` | Need to add `working-directory` to `main.yml` |

### Lessons Learned
- Docker Desktop on Windows = `docker.io` on Linux (same tool, different installer)
- `docker cp` bridges host ↔ container filesystems (`cp` can't cross the boundary)
- Image = class, Container = object (OOP analogy)
- `docker pull` replaces all of steps 2-6 (build, enter, install, commit, push) when the image already exists on Docker Hub
- Branch protection works! It blocked our direct push to `main` — had to temporarily disable to catch up, then re-enable
- TI download links break — this validates the Docker approach for CI

---

## 7. CLAUDE.md Updates

### Tasks
- [x] Added rule: provide clickable `file_path:line_number` links + code snippets when showing implementations
- [x] Added rule: ask questions when info is missing before writing/updating
- [x] Added S04_Development_Workflow sandbox to directory layout
- [x] Fixed summary filename reference (`ArtfulBytes_Claude_Summary.md` → `ArtfulBytes_ClaudeOpus_Summary.md`) — user fixed manually

---

## Remaining TODO

- [ ] **Fix CI working-directory**: Create branch `fix-ci-working-directory`, add `defaults.run.working-directory: Code/nsumo_video-feature_io_handling_2` to `main.yml`, push, PR, merge — this completes the Lesson 10 PR workflow exercise
- [ ] **Add `build_and_static_analysis` to branch protection**: After CI passes, add as required status check
- [ ] **Lesson 11**: Watch and study (clang-format, documentation, header dependency bug, cppcheck performance bug)
- [ ] **Clean up git branches**: `Artful-Byte-exp` and `PIT-progress` may be stale — merge or delete
