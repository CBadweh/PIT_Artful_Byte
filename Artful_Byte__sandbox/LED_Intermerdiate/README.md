# LED_Intermerdiate

**Lesson:** 12 — How I Program GPIOs in C
**Course:** Artful Byte — Bare-Metal Sumo Robot (MSP430G2553)
**Stage:** 2 of 6 — First IO abstraction layer, THIS IS THE 2ND BLINK TEST FROM THE VIDEO timestamp 20:00
**CBadweh Note** LAUNCHPAD-only sandbox. Guards and assert removed — enum and io_e are unconditional.

---

## Overview

This sandbox introduces the IO driver that replaces the raw register writes from Stage 1. Instead of `P1DIR |= BIT0`, the code uses a typed enum API (`IO_TEST_LED`), a config struct, and `io_configure()`. The watchdog disable is still in `main()` — `mcu_init()` has not been introduced yet.

This is where the lesson's hardest concepts live. The bit-packing trick and array-of-pointers dispatch are both implemented here.

---

## What This Demonstrates

- **Bit-packing enum (`io_generic_e`)**: each value encodes `[ zeros(3) | port(2) | pin(3) ]` in a single byte — `IO_10` = port 1 pin 0, `IO_27` = port 2 pin 7
- **`-fshort-enums` compiler flag**: required so the enum fits in 1 byte; the bit-packing math relies on `io_generic_e` being exactly 1 byte
- **Array-of-pointers dispatch**: `port_dir_regs[]`, `port_out_regs[]`, etc. — port index extracted via mask+shift, no switch statement needed
- **`struct io_config`**: groups select, direction, resistor, out into one call to `io_configure()`
- **Abstraction benefit**: `main()` refers only to `IO_TEST_LED` — changing the pin only requires updating the enum, not hunting through `P1DIR`/`P1OUT` calls

---

## File Structure

```
LED_Intermerdiate/
├── src/
│   ├── main.c               ← io_configure() + io_set_out() blink loop
│   └── drivers/
│       ├── io.h             ← io_generic_e, io_e, struct io_config, API declarations
│       └── io.c             ← bit-packing helpers, register arrays, io_configure() impl
├── build/
│   ├── bin/blink.elf        ← final binary (generated)
│   └── obj/                 ← compiled objects (generated)
├── msp430g2553.ccxml        ← DSLite debug configuration
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
| **2** | **LED_Intermerdiate** ← you are here | Bit-packing enum, array-of-pointers, `struct io_config`, `io_configure()` |
| 3 | LED_test_blink_led | `mcu_init()` integration, `BUSY_WAIT_ms`, assertions |
| 4 | LED_init_pin | `io_init()` bulk table, `io_get_input()`, dual-target |
| 5 | LED_test_launchpad_IO | Hardware board validation, `led` driver layer |
| 6 | LED_Final | Clean final form — `main()` only calls `io_set_out()` |

---

## Key Question This Sandbox Answers

> *How do you write an IO driver that works for any pin on any port without a switch statement per register?*

Answer: encode port+pin into the enum value itself, then use that value as an index into an array of register pointers. The bit-packing trick turns a symbolic name (`IO_TEST_LED`) into a port index (0 or 1) and a pin bitmask — no per-port branching needed.
