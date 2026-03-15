# S04 Development Workflow (Lessons 8-11)

Checkpoint of the nsumo project skeleton with development workflow tooling in place — no application code yet. This is the outcome of **Section 4: Development Workflow & Best Practices**.

## What It Demonstrates

- Git best practices: `.gitignore`, `.gitmodules`, conventional commits (Lesson 8)
- Static analysis with `make cppcheck` integrated into the Makefile (Lesson 9)
- CI/CD pipeline with GitHub Actions and Docker (Lesson 10)
- Code formatting with `make format` and `.clang-format` (Lesson 11)
- Coding guidelines in `docs/coding_guidelines.md` (Lesson 11)

## Prerequisites

- `TOOLS_PATH` env var pointing to TI toolchain root (contains `msp430-gcc/` and `ccs1120/`)
- `cppcheck` installed (`sudo apt install cppcheck`)
- `clang-format-12` installed (or use the Docker container from Lesson 10)

## Commands

```bash
TOOLS_PATH=/path/to/tools make    # build → build/bin/nsumo
make cppcheck                     # run static analysis
make format                       # auto-format all sources
make flash                        # flash to LaunchPad via mspdebug
make clean                        # remove build artifacts
```

## Reference

Full lesson details: `Artful_Bytes_Transcript/S04_Development_Workflow_Best_Practices.md`
