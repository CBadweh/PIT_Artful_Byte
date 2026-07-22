# LED_test_blink_led

**Lesson:** 12 — How I Program GPIOs in C
**Course:** Artful Byte — Bare-Metal Sumo Robot (MSP430G2553)
**Stage:** 3 of 6 — `mcu_init()` integration + assertions

---

## Overview

This sandbox integrates the IO driver with the MCU initialization layer. `mcu_init()` now owns watchdog disable, clock setup (16 MHz DCO), `io_init()`, and interrupt enable. `main()` calls one function and then runs the blink loop. `ASSERT(0)` is introduced as a tail after the infinite loop — the first use of the assertion system.

---

## What This Demonstrates

- **`mcu_init()`**: single entry point that runs: `watchdog_setup()` → `init_clocks()` (16 MHz DCO via `CALBC1_16MHZ`/`CALDCO_16MHZ`) → `io_init()` → `_enable_interrupts()`
- **`BUSY_WAIT_ms(ms)` macro**: defined in `common/defines.h` as `__delay_cycles(CYCLES_16MHZ / 1000 * ms)` — portable delay that scales with clock frequency
- **`ASSERT(0)` tail**: after an infinite loop that should never exit — captures the program counter via inline asm (`mov pc, %0`) and calls `assert_handler()`
- **`assert_handler()`**: hits a software breakpoint (`CLR.B R3` opcode = 0x4343), then blinks the LED via raw registers (bypasses the IO driver intentionally — must work even if io driver is broken)
- **NSUMO dual-target**: `io.h` now includes Port 3 pins under `#if defined(NSUMO)`, while `LAUNCHPAD` stays at 2 ports

---

## File Structure

```
LED_test_blink_led/
├── src/
│   ├── main.c                    ← mcu_init() + io_configure() + blink + ASSERT(0)
│   ├── common/
│   │   ├── defines.h             ← BUSY_WAIT_ms, ARRAY_SIZE, UNUSED macros
│   │   ├── assert_handler.h      ← ASSERT macro (captures PC on MCU, calls assert_handler)
│   │   └── assert_handler.c      ← BREAKPOINT + assert_blink_led() via raw registers
│   └── drivers/
│       ├── io.h                  ← dual-target io_e (LAUNCHPAD + NSUMO), full API
│       ├── io.c                  ← full IO driver with io_init(), io_get_input()
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

**Requires:** `msp430-elf-gcc` on PATH (`C:/ti/msp430-gcc/bin`), CCS installed at `C:/ti/ccs2041`

```bash
# Build
make

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
| **3** | **LED_test_blink_led** ← you are here | `mcu_init()` integration, `BUSY_WAIT_ms`, assertions |
| 4 | LED_init_pin | `io_init()` bulk table, `io_get_input()`, dual-target |
| 5 | LED_test_launchpad_IO | Hardware board validation, `led` driver layer |
| 6 | LED_Final | Clean final form — `main()` only calls `io_set_out()` |

---

## Key Question This Sandbox Answers

> *How does the MCU get set up before the application runs, and what happens when something goes wrong?*

Answer: `mcu_init()` is a single call that sequences every low-level setup step. `ASSERT()` provides a debug hook — when triggered it breaks into the debugger and then blinks the LED so the failure is visible even without a debug session.
