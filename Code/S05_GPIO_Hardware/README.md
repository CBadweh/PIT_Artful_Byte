# S05 GPIO Hardware — Starting Point for Lesson 12

Pre-lesson-12 baseline of the nsumo project. Contains the full project skeleton and development tooling from Sections 4-5, but **no GPIO driver code yet**. This is the starting point for implementing the IO abstraction layer taught in Lesson 12.

## Current State (Pre-Lesson 12)

- `src/main.c` — Raw blink using direct register writes (`P1DIR`, `P1OUT`)
- `src/common/defines.h` — `UNUSED()` and `ARRAY_SIZE()` macros
- `src/drivers/` — Empty (PLACEHOLDER only)
- `src/app/` — Empty (PLACEHOLDER only)
- `Makefile` — Full build system ready for new source files

## What Lesson 12 Will Add

- `src/drivers/io.h` / `io.c` — GPIO abstraction layer (enum-based pin naming, config struct, register arrays, bulk init)
- `src/drivers/mcu_init.h` / `mcu_init.c` — Watchdog stop, clock config (16 MHz), `io_init()` call
- `src/main.c` — Updated to call `mcu_init()` + test functions (LED blink, all-pin output, all-pin input)
- `Makefile` — Updated `SOURCES_WITH_HEADERS` to include new driver files

## Prerequisites

- `TOOLS_PATH` env var pointing to TI toolchain root (contains `msp430-gcc/` and `ccs1120/`)
- `cppcheck` installed
- `clang-format-12` installed

## Commands

```bash
TOOLS_PATH=/path/to/tools make    # build → build/bin/nsumo
make cppcheck                     # run static analysis
make format                       # auto-format all sources
make flash                        # flash to LaunchPad via mspdebug
make clean                        # remove build artifacts
```

## Reference

- Lesson 12 notes: `Artful_Bytes_Transcript/S05_Low_Level_Programming_Fundamentals.md`
- Upstream reference: `Code/source_code/nsumo_video/src/drivers/io.c`
