# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository Purpose

Study repository for the **Artful Bytes "Embedded System Project Series"** — a 28-lesson YouTube course on building an MSP430-based sumo robot (nsumo). Contains course transcripts, the nsumo firmware at various stages, a custom blink example project, and AI-generated study notes.

---

## Build Commands

There is no unified top-level build. Each firmware directory has its own Makefile targeting MSP430G2553.

### nsumo firmware (`nsumo/` or `nsumo_video/`)

Requires `TOOLS_PATH` env var pointing to the TI toolchain root (contains `msp430-gcc/` and `ccs1120/`).

```bash
TOOLS_PATH=/path/to/tools make          # build (output: build/bin/nsumo)
make clean                               # remove build artifacts
make cppcheck                            # static analysis
make format                              # clang-format-12 all sources
make flash                               # program device via mspdebug
```

### blink example (`Code/blink_example/`)

Expects `msp430-elf-gcc` on PATH and TI toolchain at `C:/ti/msp430-gcc`.

```bash
make                                     # build (output: bin/blink.elf)
make flash                               # flash via DSLite
make clean
```

### CI (GitHub Actions)

Runs on push via `.github/workflows/main.yml`. Uses Docker image `artfulbytes/msp430-gcc-9.3.1.11:latest` to build the `nsumo/` Makefile and run cppcheck. There is no test runner in CI — only compile + static analysis.

---

## Architecture (nsumo firmware)

**MCU:** MSP430G2553 (16 KB flash, 512 B RAM) — Texas Instruments LaunchPad
**Compiler:** msp430-elf-gcc 9.3.1.11
**Pattern:** Poll-based state machine (no RTOS), 1 ms loop

### Three-layer source layout (`src/`)

| Layer | Dir | Role |
|-------|-----|------|
| Application | `src/app/` | State machine (`state_machine.c`), per-state handlers (`state_attack.c`, `state_retreat.c`, `state_search.c`, `state_wait.c`, `state_manual.c`), sensor processing (`enemy.c`, `line.c`), motor control (`drive.c`) |
| Drivers | `src/drivers/` | Peripheral drivers: `uart.c`, `i2c.c`, `pwm.c`, `adc.c`, `io.c`, `led.c`, `millis.c`, plus device drivers: `vl53l0x.c` (ToF), `qre1113.c` (reflectance), `tb6612fng.c` (motor H-bridge), `ir_remote.c` |
| Common | `src/common/` | Utilities: `ring_buffer.c`, `assert_handler.c`, `trace.c`, `sleep.c`, `defines.h` |

External dependency: `external/printf/` (lightweight printf, git submodule).

### State machine flow

`WAIT` → (IR command) → `SEARCH` → (enemy detected) → `ATTACK` → (line detected) → `RETREAT` → back to `SEARCH`. `MANUAL` state reachable from any state via IR remote.

---

## Coding Conventions (from `docs/coding_guidelines.md`)

- **snake_case** everywhere (files, functions, variables); **UPPER_CASE** for defines
- Prefix functions with module name: `uart_init()`, `i2c_read()`
- One module = one `.c/.h` pair
- 4-space indent, no tabs
- Always use `{ }` for if/else, even single statements
- Use `void` in empty parameter lists: `void foo(void)`
- Internal-only functions must be `static`
- Use fixed-width integers (`uint8_t`, `uint16_t`, etc.)
- Typedef enums with `_e` suffix; do NOT typedef structs or use `_t` suffix
- Wrap define constants in parentheses: `#define FOO (42)`
- Include order: local → project → system

---

## Directory Layout

```
Artful_Byte/
├── .github/workflows/          ← CI config (GitHub Actions)
├── Artful_Byte_Sandbox/        ← Checkpoints: minimal, isolated examples for learning one concept at a time
│   ├── Blink LED/              ← Lesson 4 checkpoint: CCS IDE blink project
│   └── blink_example/          ← Lesson 5 checkpoint: Makefile blink project
├── Artful_Bytes_Transcript/    ← 28 lesson transcripts (.txt) + course summary files
├── Chat/                       ← AI conversation logs and class notes
├── Code/
│   ├── nsumo_video-feature_io_handling_2/  ← IO driver implementation (lesson 12-13)
│   └── source_code/
│       └── nsumo_video/        ← Complete upstream reference (NEVER MODIFY)
│           ├── src/app/        ← Application layer (state machine, drive, enemy, line)
│           ├── src/drivers/    ← Peripheral + device drivers (uart, i2c, pwm, adc, io)
│           ├── src/common/     ← Shared utilities (assert, ring_buffer, trace)
│           ├── src/test/       ← On-target test functions
│           ├── external/       ← Lightweight printf (git submodule)
│           ├── docs/           ← Architecture diagrams, coding guidelines
│           ├── tools/          ← Dockerfile, build scripts
│           └── Makefile        ← Main build system
├── CLAUDE.md
└── README.md                   ← Course section mapping (lessons → topics)
```

---

## Directory Roles

| Directory | Role | What goes here |
|-----------|------|----------------|
| `Code/source_code/` | **Unmodified upstream reference** | Git-cloned project. Never modify. Read-only reference for the complete finished codebase. |
| `Code/` | **Implementations with real code** | Feature branches, CBadweh experiments, anything with actual working implementations. |
| `Artful_Byte_Sandbox/` | **Learning checkpoints** | Minimal, isolated examples stripped of dependencies. For exploring one concept at a time without the complexity of the full project (e.g., `blink_example/` for understanding Makefiles without the full nsumo build system). |
| `Artful_Bytes_Transcript/` | **Course content** | Lesson transcripts + AI-generated summaries and section files. |

---

## Course Summary

The full course summary lives in `Artful_Bytes_Transcript/ArtfulBytes_ClaudeOpus_Summary.md` (3,154 lines, all 10 sections + Pareto appendix). Per-section files for quick navigation:

| File | Lessons | Topic |
|------|---------|-------|
| `Artful_Bytes_Transcript/S01_Hardware_Design_Component_Selection.md` | 1-3 | Parts, schematic, PCB |
| `Artful_Bytes_Transcript/S02_Development_Environment_Setup.md` | 4-5 | IDE, Makefile, toolchain |
| `Artful_Bytes_Transcript/S03_Software_Architecture_Project_Organization.md` | 6-7 | Layered architecture, project structure |
| `Artful_Bytes_Transcript/S04_Development_Workflow_Best_Practices.md` | 8-11 | Git, cppcheck, CI/CD, clang-format |
| `Artful_Bytes_Transcript/S05_Low_Level_Programming_Fundamentals.md` | 12-20 | GPIO, interrupts, UART, memory, IR remote |
| `Artful_Bytes_Transcript/S06_Motor_Control_PWM.md` | 21 | PWM, TB6612FNG, tank drive |
| `Artful_Bytes_Transcript/S07_Sensor_Integration.md` | 22-23 | ADC/DMA line sensors, I2C range sensors |
| `Artful_Bytes_Transcript/S08_System_Integration_Testing.md` | 24-28 | Board bring-up, simulator, state machine, reflection |

When answering questions about course content, lessons, or concepts — read the relevant section file rather than the full summary.

---

## Branches

- `main` — primary branch
- `fixed-Makefile` — Makefile fixes for Windows/local toolchain paths
- `PIT-progress` — course progress tracking
- `Artful-Byte-exp` — experimental work
