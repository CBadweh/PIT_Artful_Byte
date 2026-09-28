# LED_test_blink_led

**Lesson:** 12 — How I Program GPIOs in C
**Course:** Artful Byte — Bare-Metal Sumo Robot (MSP430G2553)
**Stage:** 3 of 6 — `mcu_init()` + `io_init()` + `io_configure()` blink test
**Target:** LaunchPad only

---

## Overview

This sandbox runs the lesson 12 `test_blink_led` test: the IO driver configures P1.0 with `io_configure()` and toggles it with `io_set_out()`. `mcu_init()` stops the watchdog and calls `io_init()`, which applies a default configuration to all 16 LaunchPad pins.

Trimmed to lesson 12 scope — later-lesson code was removed (see below).

---

## What This Demonstrates

- **`mcu_init()`**: stops the watchdog, then calls `io_init()`
- **`io_init()`**: loops over `io_initial_configs[]` and calls `io_configure()` on every pin (`ARRAY_SIZE` from `common/defines.h`)
- **`UNUSED_CONFIG` / `ADC_CONFIG`**: shared default configs for unused pins and the line-detect ADC pin
- **`io_configure()`**: applies a `struct io_config` (select, resistor, direction, out) with one call
- **`__delay_cycles(250000)`**: compiler intrinsic delay — ~250 ms at the default ~1 MHz clock

---

## Removed (later lessons)

| Removed | Comes back in |
|---------|---------------|
| `NSUMO` target + `#if defined(LAUNCHPAD)` guards, `-DLAUNCHPAD` | Lesson 12/13 (dual target, `make HW=...`) |
| `ASSERT()`, `assert_handler.c/.h` | Lesson 14 |
| `io_get_current_config()`, `io_config_compare()` | Lesson 14 |
| 16 MHz clock setup (`init_clocks()`) | Lesson 17/18 |
| `_enable_interrupts()` | Lesson 17 |
| Extra macros in `defines.h` (`BUSY_WAIT_ms`, `CYCLES_16MHZ`, `UNUSED`, ...) | Later lessons |

Kept: `static_assert` in `io.c` — standard C compile-time check that `-fshort-enums` is set.

---

## File Structure

```
LED_test_blink_led/
├── src/
│   ├── main.c                    ← mcu_init() + test_blink_led()
│   ├── common/
│   │   └── defines.h             ← ARRAY_SIZE
│   └── drivers/
│       ├── io.h                  ← LaunchPad io_e pin map, io API
│       ├── io.c                  ← IO driver: register tables, io_init(), io_configure()
│       ├── mcu_init.h
│       └── mcu_init.c            ← watchdog stop + io_init()
├── build/                        ← generated (bin/blink.elf, obj/)
├── msp430g2553.ccxml             ← DSLite debug configuration
├── Makefile
└── README.md
```

---

## Build & Flash

**Requires:** `msp430-elf-gcc` on PATH (`C:/ti/msp430-gcc/bin`), CCS installed at `C:/ti/ccs2041`

```bash
make          # build
make flash    # flash to LaunchPad via DSLite
make clean    # remove build/
```

> **Note:** `mspdebug` is not installed on this machine. Flash is handled by DSLite with `msp430g2553.ccxml`.
> If `mspdebug` is available, the equivalent command would be:
> `mspdebug rf2500 "prog build/bin/blink.elf"`

---

## Where This Fits in the Progression

| Stage | Sandbox | What changes |
|-------|---------|--------------|
| 1 | LED_Raw_Registers | Direct `P1DIR`/`P1OUT` writes |
| 2 | LED_Intermerdiate | Bit-packing enum, array-of-pointers, `struct io_config`, `io_configure()` |
| **3** | **LED_test_blink_led** ← you are here | `mcu_init()`, `io_init()` default pin table, blink test |
| 4 | LED_init_pin | `io_init()` bulk table, `io_get_input()`, dual-target |
| 5 | LED_test_launchpad_IO | Hardware board validation, `led` driver layer |
| 6 | LED_Final | Clean final form — `main()` only calls `io_set_out()` |

---

## Key Question This Sandbox Answers

> *How does the MCU get set up before the application runs?*

Answer: `mcu_init()` is a single call that stops the watchdog and puts every pin into a known default state via `io_init()`. The test then configures the LED pin with `io_configure()` and toggles it.
