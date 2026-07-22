# LED_init_pin

**Lesson:** 12 — How I Program GPIOs in C
**Course:** Artful Byte — Bare-Metal Sumo Robot (MSP430G2553)
**Stage:** 4 of 6 — Bulk pin initialization + `led` driver layer

---

## Overview

This sandbox introduces `io_init()` — a function that configures every pin at boot from a single designated-initializer table (`io_initial_configs[]`). It also introduces the `led` driver layer, which wraps `io_set_out()` behind `led_set()` and uses `io_config_compare()` to assert that `io_init()` already ran before the LED driver is used. `main()` now contains zero manual `io_configure()` calls.

---

## What This Demonstrates

- **`io_initial_configs[]` designated-initializer table**: a `const struct io_config` array indexed by `io_e`, with `UNUSED_CONFIG` and `ADC_CONFIG` macros for repeated patterns — every pin is accounted for at compile time
- **`io_init()` bulk loop**: iterates `io_e io = IO_10` to `ARRAY_SIZE(io_initial_configs)`, calling `io_configure()` for each pin — one function configures all 16 (LAUNCHPAD) or 24 (NSUMO) pins
- **`io_get_current_config()`**: reads back live register state into a `struct io_config`
- **`io_config_compare()`**: compares two `struct io_config` structs field-by-field — used by `led_init()` to assert the expected config is already in hardware before the LED driver proceeds
- **`led` driver layer** (`led.c`/`led.h`): `led_init()` verifies hardware state via `io_config_compare()`; `led_set()` maps `LED_STATE_ON/OFF` → `IO_OUT_HIGH/LOW` via `io_set_out()`

---

## File Structure

```
LED_init_pin/
├── src/
│   ├── main.c                    ← mcu_init() + io_set_out() loop only, no manual io_configure()
│   ├── common/
│   │   ├── defines.h             ← BUSY_WAIT_ms, ARRAY_SIZE, UNUSED macros
│   │   ├── assert_handler.h
│   │   └── assert_handler.c
│   └── drivers/
│       ├── io.h                  ← full API including io_init(), io_get_input(), io_config_compare()
│       ├── io.c                  ← io_initial_configs[] table, io_init() bulk loop, io_get_current_config()
│       ├── led.h                 ← led_e, led_state_e, led_init(), led_set()
│       ├── led.c                 ← io_config_compare() guard in led_init(), io_set_out() in led_set()
│       ├── mcu_init.h
│       └── mcu_init.c
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
| 3 | LED_test_blink_led | `mcu_init()` integration, `BUSY_WAIT_ms`, assertions |
| **4** | **LED_init_pin** ← you are here | `io_init()` bulk table, `led` driver, `io_config_compare()` guard |
| 5 | LED_test_launchpad_IO | Hardware board validation, `led` driver layer |
| 6 | LED_Final | Clean final form — `main()` only calls `io_set_out()` |

---

## Key Question This Sandbox Answers

> *How do you configure all pins at boot without scattering `io_configure()` calls throughout the codebase?*

Answer: one designated-initializer table (`io_initial_configs[]`) holds every pin's config. `io_init()` loops through it at boot. Each driver layer (`led`, UART, I2C, etc.) then asserts the config it expects is already in hardware — catching any mismatch between the table and what the driver needs.
