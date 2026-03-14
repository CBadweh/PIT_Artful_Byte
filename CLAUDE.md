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

| Path | Contents |
|------|----------|
| `nsumo/` | Full nsumo codebase (from lesson 9 onward) |
| `nsumo_video/` | Snapshot of upstream `nsumo_video` repo |
| `nsumo_video-feature_io_handling_2/` | Feature branch snapshot |
| `Code/blink_example/` | Custom Makefile blink project (lesson 5) |
| `Code/Blink LED/` | IDE-generated blink project |
| `Artful_Bytes_Transcript/` | 28 lesson transcripts (`.txt`) |
| `Chat/` | AI conversation logs and troubleshooting notes |
| `nsumo/docs/` | Architecture docs, coding guidelines, class notes |
| `Artful_Byte_Sandbox/` | MBC sandbox experiments |

---

## Multiple nsumo Copies

The repo contains three copies of nsumo firmware at different stages. `nsumo/` is the primary working copy. `nsumo_video/` and `nsumo_video-feature_io_handling_2/` are reference snapshots from the upstream Artful Bytes repo. When making changes, work in `nsumo/` unless specifically asked to modify a snapshot.

---

## Branches

- `main` — primary branch
- `fixed-Makefile` — Makefile fixes for Windows/local toolchain paths
- `PIT-progress` — course progress tracking
- `Artful-Byte-exp` — experimental work
