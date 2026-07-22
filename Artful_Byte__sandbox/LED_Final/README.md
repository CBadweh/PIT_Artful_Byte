# LED_Final

**Lesson:** 12 — How I Program GPIOs in C
**Course:** Artful Byte — Bare-Metal Sumo Robot (MSP430G2553)
**Stage:** 6 of 6 — Clean final form

---

## Overview

This is the endpoint of the Lesson 12 progression. The full IO driver and MCU initialization layer are in place, and `main()` is reduced to its simplest possible form: one `mcu_init()` call, then a blink loop using only `io_set_out()`. No manual `io_configure()`, no watchdog code, no clock setup — all owned by `mcu_init()`.

---

## What This Demonstrates

- **`mcu_init()` owns everything**: watchdog disable, 16 MHz DCO clock, `io_init()` bulk pin config, interrupt enable — `main()` does not touch any of this
- **`io_set_out()` only in main**: `IO_TEST_LED` is already configured as output by `io_init()` at boot; `main()` only toggles it
- **`BUSY_WAIT_ms(250)`**: 250 ms delay via `__delay_cycles` scaled to 16 MHz — readable and portable
- **`ASSERT(0)` tail**: after the infinite loop (unreachable) — marks the intent that `main()` must never return; if it somehow did, the assert would catch it
- **Minimal `main()`**: 6 lines — the result of every abstraction introduced across Stages 1–5

---

## File Structure

```
LED_Final/
├── src/
│   ├── main.c                    ← mcu_init() + io_set_out() blink loop + ASSERT(0)
│   ├── common/
│   │   ├── defines.h             ← BUSY_WAIT_ms, ARRAY_SIZE, UNUSED macros
│   │   ├── assert_handler.h
│   │   └── assert_handler.c
│   └── drivers/
│       ├── io.h                  ← full dual-target API (LAUNCHPAD + NSUMO)
│       ├── io.c                  ← io_initial_configs[], io_init(), full implementation
│       ├── mcu_init.h
│       └── mcu_init.c            ← watchdog + 16 MHz DCO + io_init + interrupts
├── build/
│   ├── bin/blink.elf             ← final binary (generated)
│   └── obj/                      ← compiled objects (generated)
├── msp430g2553.ccxml             ← DSLite debug configuration
├── Makefile
└── README.md
```

---

## Build & Flash

**Requires:** `msp430-elf-gcc` at `C:/ti/msp430-gcc`, CCS installed at `C:/ti/ccs2041`

```bash
# Build
make TOOLS_PATH=/c/ti

# Flash to LaunchPad via DSLite
make flash

# Clean build artifacts
make clean
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
| 3 | LED_test_blink_led | `mcu_init()` integration, `BUSY_WAIT_ms`, assertions |
| 4 | LED_init_pin | `io_init()` bulk table, `led` driver, `io_config_compare()` guard |
| 5 | LED_test_launchpad_IO | Hardware board validation, output sweep + input probe |
| **6** | **LED_Final** ← you are here | Clean final form — `main()` is 6 lines |

---

## Key Question This Sandbox Answers

> *What does the code look like when all the abstraction layers are correctly in place?*

Answer: `main()` becomes a policy file — it says *what* to do (`blink the LED every 250 ms`) without saying *how* (no register names, no pin numbers, no clock math). All the *how* is encapsulated in the driver and initialization layers built across Stages 1–5.
