# LED_Raw_Registers

**Lesson:** 12 — How I Program GPIOs in C
**Course:** Artful Byte — Bare-Metal Sumo Robot (MSP430G2553)
**Stage:** 1 of 6 — Starting point, zero abstraction. THIS IS THE FIRST BLINKY FROM THE VIDEO AT timestamp 9:00

---

## Overview

This sandbox is the baseline checkpoint for Lesson 12. It blinks the onboard LED on the MSP430G2553 LaunchPad using **direct register writes** — no drivers, no abstraction layer, no helper functions. The goal is to show what the hardware actually needs before any abstraction is introduced.

The entire program is 20 lines. Everything the MCU does maps directly to two register operations:

| Register | Operation | Effect |
|----------|-----------|--------|
| `P1DIR`  | `\|= BIT0` | Set P1.0 as output |
| `P1OUT`  | `^= BIT0`  | Toggle P1.0 (LED on/off) |

---

## What This Demonstrates

- **Memory-mapped I/O**: `P1DIR` and `P1OUT` are addresses in the MCU's address space — writing to them changes hardware state
- **Why abstraction exists**: This code only works for one pin on one port; any change requires knowing register names and bit positions throughout the codebase
- **Watchdog disable**: `WDTCTL = WDTPW + WDTHOLD` — required on MSP430 or the MCU resets every ~32 ms
- **Volatile loop delay**: `volatile unsigned int i` prevents the compiler from optimizing away the delay loop

---

## File Structure

```
LED_Raw_Registers/
├── src/
│   └── main.c            ← full program, 20 lines
├── build/
│   ├── bin/blink.elf     ← final binary (generated)
│   └── obj/              ← compiled objects (generated)
├── msp430g2553.ccxml     ← DSLite debug configuration
├── Makefile
└── README.md
```

---

## Build & Flash

```bash
# Build
make TOOLS_PATH=/c/ti

# Flash to LaunchPad via DSLite (MSP430G2553 / MSP430G2ET)
make flash

# Clean build artifacts
make clean
```

Output binary: `build/bin/blink.elf` (54 bytes flash, 0 bytes RAM)

> **Note:** `mspdebug` is not installed on this machine. Flash is handled by DSLite (`C:/ti/ccs2041/ccs/ccs_base/DebugServer/bin/DSLite.exe`) with `msp430g2553.ccxml`.
> If `mspdebug` is available, the equivalent command would be:
> `mspdebug rf2500 "prog build/bin/blink.elf"`

---

## Where This Fits in the Progression

| Stage | Sandbox | What changes |
|-------|---------|--------------|
| **1** | **LED_Raw_Registers** ← you are here | Direct `P1DIR`/`P1OUT` writes |
| 2 | LED_Intermerdiate | Bit-packing enum, array-of-pointers, `struct io_config` |
| 3 | LED_test_blink_led | `mcu_init()` integration, `BUSY_WAIT_ms`, assertions |
| 4 | LED_init_pin | `io_init()` bulk table, `io_get_input()`, dual-target |
| 5 | LED_test_launchpad_IO | Hardware board validation, `led` driver layer |
| 6 | LED_Final | Clean final form — `main()` only calls `io_set_out()` |

---

## Key Question This Sandbox Answers

> *What is the minimum code needed to toggle a GPIO pin on the MSP430?*

Answer: set direction, toggle output, loop. Two registers, three lines. Every abstraction layer in the later sandboxes exists to make that same operation safe, portable, and scalable across all pins and ports.
