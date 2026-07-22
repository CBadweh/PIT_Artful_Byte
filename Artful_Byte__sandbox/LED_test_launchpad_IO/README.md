# LED_test_launchpad_IO

**Lesson:** 12 — How I Program GPIOs in C
**Course:** Artful Byte — Bare-Metal Sumo Robot (MSP430G2553)
**Stage:** 5 of 6 — Hardware board validation

---

## Overview

This sandbox validates the IO driver against real hardware. Two test functions probe all 16 LaunchPad pins: an output sweep (toggles each pin sequentially — verify with a scope or LED probe) and an interactive input probe (configures all pins as pull-up inputs, waits for the user to ground each pin one at a time). The LED signals test progress during the input test. By default, only the output test runs; the input test is commented out in `main()`.

---

## What This Demonstrates

- **Output sweep (`test_launchpad_io_pins_output`)**: configures `IO_10`→`IO_27` as outputs, then toggles each `HIGH` → `LOW` with a 10 ms delay — allows a scope or LED probe to verify each pin physically drives
- **Interactive input probe (`test_launchpad_io_pins_input`)**: configures all pins as pull-up inputs (`IO_RESISTOR_ENABLED`, `IO_OUT_HIGH`), then loops through each pin waiting for the user to pull it low; the test LED turns on when the MCU is waiting on a specific pin, off when it detects the pin was pulled low
- **`SUPPRESS_UNUSED` attribute**: both test functions are marked `__attribute__((unused))` — one is always commented out in `main()`, so the compiler warning is suppressed intentionally
- **`led_init()` guard**: the input test calls `led_init()` first, which internally calls `io_config_compare()` to verify `io_init()` already ran correctly — the led driver won't proceed if the pin config doesn't match expectations
- **`io_get_input()`**: reads `PxIN` register for the given pin via the array-of-pointers pattern

---

## File Structure

```
LED_test_launchpad_IO/
├── src/
│   ├── main.c                    ← test_launchpad_io_pins_output() active; input test commented out
│   ├── common/
│   │   ├── defines.h             ← BUSY_WAIT_ms, SUPPRESS_UNUSED, ARRAY_SIZE macros
│   │   ├── assert_handler.h
│   │   └── assert_handler.c
│   └── drivers/
│       ├── io.h                  ← full API: io_init(), io_get_input(), io_config_compare()
│       ├── io.c                  ← io_initial_configs[], io_init(), io_get_current_config()
│       ├── led.h                 ← led_e, led_state_e, led_init(), led_set()
│       ├── led.c                 ← io_config_compare() guard, led_set() via io_set_out()
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

To switch between output and input test, edit `src/main.c`:
```c
// Output sweep (default — active):
test_launchpad_io_pins_output();

// Input probe (swap in by commenting out the line above):
// test_launchpad_io_pins_input();
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
| **5** | **LED_test_launchpad_IO** ← you are here | Hardware board validation, output sweep + input probe |
| 6 | LED_Final | Clean final form — `main()` only calls `io_set_out()` |

---

## Key Question This Sandbox Answers

> *How do you verify that the IO driver actually works on real hardware before building higher-level drivers on top of it?*

Answer: sweep every output pin with a scope or probe to confirm direction and toggling work, then interactively probe every input pin with a pull-up to confirm `io_get_input()` reads correctly. Hardware validation happens at the IO driver layer — before any higher-level driver depends on it.
