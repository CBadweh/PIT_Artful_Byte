# S05 GPIO Hardware — Lesson 12: GPIO Abstraction Layer

Implementation of the GPIO driver (`io.c`/`io.h`) from Lesson 12 ("How I Program GPIOs in C"). This is the first real driver in the nsumo project — it translates the hardware schematic's pin assignments into a clean C abstraction layer.

## What's Implemented (Lesson 12)

- `src/drivers/io.h` / `io.c` — GPIO abstraction: enum-based pin naming, config struct, array-indexed register access, bulk init
- `src/drivers/mcu_init.h` / `mcu_init.c` — Watchdog stop, 16 MHz clock config, `io_init()` call
- `src/common/assert_handler.h` / `assert_handler.c` — MCU-safe assert with LED blink on failure
- `src/common/defines.h` — Utility macros (`BUSY_WAIT_ms`, `ARRAY_SIZE`, `INTERRUPT_FUNCTION`)
- `src/main.c` — LED blink test using IO abstraction
- `Makefile` — Updated with new sources, `-fshort-enums`, `-DLAUNCHPAD`

## Not Yet Implemented (Future Lessons)

- Lesson 13: Hardware versioning (`HW=LAUNCHPAD`/`NSUMO` Makefile arg, `io_detect_hw_type()`)
- Lesson 14: GPIO interrupts (`io_configure_interrupt`, ISR vectors)
- Lesson 15: Millisecond timer (watchdog repurposing for `millis.c`)
- Lesson 16: UART driver (`uart.c`, `trace.c`)

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

```bash
git clone --branch feature_io_handling https://github.com/artfulbytes/nsumo_video.git
```

This clones only the `feature_io_handling` branch. If you also want all other branches available locally, just clone normally and then checkout:

```bash
git clone https://github.com/artfulbytes/nsumo_video.git
cd nsumo_video
git checkout feature_io_handling
```