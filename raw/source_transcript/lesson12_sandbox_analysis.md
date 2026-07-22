# Lesson 12 Sandbox Analysis

## Summary Table

| Folder | Concept Demonstrated | Maps to Lesson 12? | Stage |
|--------|---------------------|-------------------|-------|
| LED_Raw_Registers | Direct register access: P1DIR, P1OUT, WDTCTL | Yes — GPIO register types, baseline | Stage 1: Raw registers |
| LED_Intermerdiate | io_generic_e bit-packing, array-of-pointers dispatch, struct io_config + io_configure() | Yes — core abstraction concepts | Stage 2: IO driver (LAUNCHPAD-only, trimmed) |
| LED_test_blink_led | io_configure() single-pin test via mcu_init() + assert_handler + defines | Yes — io_configure() + mcu_init integration | Stage 3: Test 1 (blink via full driver) |
| LED_init_pin | io_init() bulk init via io_initial_configs[] table, NSUMO + LAUNCHPAD target support | Yes — io_init() boot-time bulk init, dual-target | Stage 4: Full driver + io_init() |
| LED_test_launchpad_IO | io_get_input(), io_config_compare(), io_get_current_config(), led driver layer | Yes — IO input reading, config verification, LED abstraction | Stage 5: Test 2 & 3 (output sweep + input probe) |
| LED_Final | mcu_init() + io_init() + BUSY_WAIT_ms + ASSERT tail, minimal main | Yes — complete pattern, no manual pin setup in main | Stage 6: Final clean integration |

---

## Per-Folder Breakdown

### LED_Raw_Registers

**Files**
```
src/
  main.c
Makefile
```

**What it does**

`main.c` (19 lines) stops the watchdog with `WDTCTL = WDTPW + WDTHOLD`, then enters `test_blink_led()`. That function sets `P1DIR |= BIT0` to make P1.0 an output, then loops forever toggling `P1OUT ^= BIT0` with a software delay counter (`volatile unsigned int i`).

No abstraction exists. Registers are named directly as MSP430 macros from `<msp430.h>`.

**Lesson 12 mapping**

- Demonstrates: `PxDIR` (output direction), `PxOUT` (pin state), WDTCTL (watchdog stop)
- This is the motivating "before" state — the problem the IO driver solves
- No enum, no struct, no array-of-pointers

**Stage:** 1 — Raw registers, zero abstraction

---

### LED_Intermerdiate

**Files**
```
src/
  main.c
  drivers/
    io.c
    io.h
Makefile
```

Note: no `common/` directory. This is a trimmed build — LAUNCHPAD-only, no `assert_handler`, no `defines.h`.

**What it does**

`io.h` introduces:
- `io_generic_e` — flat enum `IO_10` through `IO_27`, one value per pin. The comment in `io.c` spells out the bit-packing: `sizeof(io_generic_e) == 1` (via `-fshort-enums`), encoding `[ zeros(3) | port(2) | pin(3) ]` in a single byte.
- `io_e` — named alias enum mapping logical names (`IO_TEST_LED = IO_10`) to `io_generic_e` values, gated by `#if defined(LAUNCHPAD)`.
- `struct io_config` with fields `select`, `resistor`, `dir`, `out` (each an enum).
- `io_configure()`, `io_set_select()`, `io_set_direction()`, `io_set_resistor()`, `io_set_out()`.

`io.c` implements the dispatch via five `static volatile uint8_t *const` arrays indexed by port:
```c
static volatile uint8_t *const port_dir_regs[IO_PORT_CNT] = { &P1DIR, &P2DIR };
static volatile uint8_t *const port_ren_regs[IO_PORT_CNT] = { &P1REN, &P2REN };
static volatile uint8_t *const port_out_regs[IO_PORT_CNT] = { &P1OUT, &P2OUT };
static volatile uint8_t *const port_sel1_regs[IO_PORT_CNT] = { &P1SEL, &P2SEL };
static volatile uint8_t *const port_sel2_regs[IO_PORT_CNT] = { &P1SEL2, &P2SEL2 };
```

The helper `io_port(io)` extracts bits [4:3] as the port index; `io_pin_bit(io)` extracts bits [2:0] and shifts `1 << idx` to produce the bitmask.

`main.c` manually stops the watchdog, fills a `struct io_config` with designated initializers, calls `io_configure(IO_TEST_LED, &led_config)`, then blinks by alternating `io_set_out()` calls with `__delay_cycles(250000)`.

**Lesson 12 mapping**

- Demonstrates: bit-packing trick (`io_generic_e` encoding port+pin), array-of-pointers for register dispatch, all five register types (PxSEL/PxSEL2 via `port_sel1_regs`/`port_sel2_regs`, PxDIR, PxREN, PxOUT), `struct io_config`, `io_configure()`
- This is the core abstraction lesson — all key mechanics introduced here
- `PxIN` and `io_init()` are absent (not yet added)

**Stage:** 2 — IO driver core (trimmed, LAUNCHPAD only, no mcu_init, no init table)

---

### LED_test_blink_led

**Files**
```
src/
  main.c
  drivers/
    io.c
    io.h
    mcu_init.c
    mcu_init.h
  common/
    assert_handler.c
    assert_handler.h
    defines.h
Makefile
```

**What it does**

`main.c` (32 lines) calls `mcu_init()` instead of manually stopping the watchdog, then runs `test_blink_led()`. That function creates a `struct io_config`, calls `io_configure(IO_TEST_LED, &led_config)` to set up the pin, then blinks with `io_set_out()` + `__delay_cycles(250000)`. The `ASSERT(0)` unreachable guard at the tail uses `assert_handler`.

`mcu_init.c` calls `watchdog_setup()`, `init_clocks()`, `io_init()`, and `_enable_interrupts()` — but the `io.c` in this folder does NOT yet include `io_init()` (compared to LED_init_pin). The `io.c` here matches the LED_Intermerdiate version (no init table).

`defines.h` provides `BUSY_WAIT_ms(ms)` macro expanding to `__delay_cycles(CYCLES_PER_MS * ms)` at 16 MHz.

**Lesson 12 mapping**

- Demonstrates: `io_configure()` as the entry point from a caller's perspective, `struct io_config` with designated initializers, `mcu_init()` integration pattern, `ASSERT` safety tail
- This is "Test 1" — the first hardware verification test described in lesson 12
- The blink logic is identical to LED_Intermerdiate's but now `mcu_init()` owns watchdog and clock setup

**Stage:** 3 — Test 1: io_configure() single-pin blink via full driver stack

---

### LED_init_pin

**Files**
```
src/
  main.c
  drivers/
    io.c
    io.h
    mcu_init.c
    mcu_init.h
  common/
    assert_handler.c
    assert_handler.h
    defines.h
Makefile
```

**What it does**

This is the fullest version of the IO driver. Key additions over LED_test_blink_led:

`io.h` adds:
- `IO_30`–`IO_37` range in `io_generic_e` (gated `#if defined(NSUMO)`) for Port 3 support
- Full NSUMO pin mapping in `io_e` (line sensors, range sensor shutdowns, motor PWM, etc.)
- `io_in_e` enum and `io_get_input()` function
- `io_get_current_config()` and `io_config_compare()` declarations
- `io_init()` declaration

`io.c` adds:
- `IO_PORT_CNT` set to 3 for NSUMO, 2 for LAUNCHPAD
- Three-entry register arrays for NSUMO: `{ &P1DIR, &P2DIR, &P3DIR }`, etc.
- `io_initial_configs[]` — a static const array of `struct io_config` indexed by `io_e` value, with designated initializer syntax `[IO_TEST_LED] = { ... }`, defining the boot-time state for every pin. Uses `UNUSED_CONFIG` and `ADC_CONFIG` macros for repeated patterns.
- `io_init()` — loops `for (io_e io = IO_10; io < ARRAY_SIZE(io_initial_configs); io++)` and calls `io_configure()` on each entry
- `io_get_current_config()` — reads live register values back into a `struct io_config`
- `io_config_compare()` — field-by-field struct comparison
- `io_get_input()` — reads `port_in_regs[port]` (PxIN)

`main.c` is nearly identical to LED_Final: `mcu_init()` then blink loop with `io_set_out()` + `BUSY_WAIT_ms(250)`. Comment confirms "io_init() calls through mcu_init()".

**Lesson 12 mapping**

- Demonstrates: `io_init()` bulk pin initialization, `io_initial_configs[]` designated-initializer table, `io_get_input()` using `PxIN`, `io_get_current_config()`, dual-target (LAUNCHPAD/NSUMO) compile-time selection
- This is the lesson's capstone on the IO driver implementation itself

**Stage:** 4 — Full IO driver with io_init(), PxIN, dual-target support

---

### LED_test_launchpad_IO

**Files**
```
src/
  main.c
  drivers/
    io.c
    io.h
    led.c
    led.h
    mcu_init.c
    mcu_init.h
  common/
    assert_handler.c
    assert_handler.h
    defines.h
Makefile
```

**What it does**

Adds a `led` driver layer on top of the IO driver.

`led.h` defines `led_e` (`LED_TEST`) and `led_state_e` (`LED_STATE_OFF`, `LED_STATE_ON`). Exposes `led_init()` and `led_set()`.

`led.c` holds a `static const struct io_config led_config` with GPIO output settings. `led_init()` asserts not already initialized, then calls `io_get_current_config(IO_TEST_LED, &current_config)` and `io_config_compare()` to verify `io_init()` already configured the pin correctly — it asserts if not. `led_set()` maps `LED_STATE_ON/OFF` to `IO_OUT_HIGH/LOW` and calls `io_set_out()`.

`main.c` contains two test functions (both `SUPPRESS_UNUSED`):
- `test_launchpad_io_pins_output()` — calls `mcu_init()`, sets all 16 pins (IO_10..IO_27) as GPIO outputs, sweeps each HIGH/LOW with `BUSY_WAIT_ms(10)` in a while(1). Used to probe with a multimeter.
- `test_launchpad_io_pins_input()` — calls `mcu_init()` + `led_init()`, sets all 16 pins as inputs with pull-up (`IO_OUT_HIGH` + `IO_RESISTOR_ENABLED`), then walks each pin waiting for the user to pull it LOW (via wire), using LED_TEST to signal "ready for next pin".

`main()` calls `test_launchpad_io_pins_output()` (the input test is commented out).

**Lesson 12 mapping**

- Demonstrates: `io_get_input()` / `PxIN`, `io_config_compare()` / `io_get_current_config()` for boot verification, `io_e` walking with `io_generic_e` loop, `led` driver as a thin wrapper over `io`, pull-up resistor config (`IO_RESISTOR_ENABLED` + `IO_OUT_HIGH`)
- This is "Test 2 and Test 3" from Lesson 12 — hardware board validation tests
- Introduces the `led` driver separation-of-concerns pattern

**Stage:** 5 — Test 2 & 3: board IO validation (output sweep + input probe with LED feedback)

---

### LED_Final

**Files**
```
src/
  main.c
  drivers/
    io.c
    io.h
    mcu_init.c
    mcu_init.h
  common/
    assert_handler.c
    assert_handler.h
    defines.h
Makefile
```

**What it does**

`main.c` (21 lines) is the cleanest version. It calls `mcu_init()` (which internally calls `io_init()` to configure all pins), enters a `while(1)` blink loop using `io_set_out(IO_TEST_LED, IO_OUT_HIGH/LOW)` with `BUSY_WAIT_ms(250)`, and has an `ASSERT(0)` at the unreachable tail.

No manual pin setup in `main()`. All GPIO initialization is handled by `io_init()` called from `mcu_init()`. The `main.c` comment reads: "final: mcu_init, full io_init, BUSY_WAIT_ms, ASSERT tail."

The `io.c` and `io.h` in this folder match the LED_init_pin versions (full driver with `io_init()`, dual-target, `io_get_input()`, `io_config_compare()`). The difference from LED_init_pin is that `main.c` here does not contain any `io_configure()` call — it trusts `mcu_init()` fully.

**Lesson 12 mapping**

- Demonstrates: the complete final pattern — `mcu_init()` → `io_init()` → blink with just `io_set_out()`, no manual config in application code
- `BUSY_WAIT_ms` macro from `defines.h` replaces raw `__delay_cycles`
- `ASSERT(0)` tail is the defensive programming pattern introduced in this lesson

**Stage:** 6 — Final integration: mcu_init absorbs all init, main is application-only

---

## Progression Story

These six folders are a deliberate step-by-step construction of the Lesson 12 GPIO driver, from bare metal to a clean abstracted API. Each stage adds exactly one concept.

```
Stage 1: LED_Raw_Registers
  └─ Direct P1DIR/P1OUT register writes. No abstraction.
     Problem: not portable, not readable, not testable.

Stage 2: LED_Intermerdiate
  └─ IO driver introduced. Key ideas all appear here:
       - io_generic_e bit-packing (port in bits[4:3], pin in bits[2:0])
       - array-of-pointers to register arrays (port_dir_regs[], port_out_regs[], etc.)
       - struct io_config (select, dir, resistor, out fields)
       - io_configure() as single-call pin setup
     Limitation: LAUNCHPAD-only, no mcu_init, no io_init, no PxIN.

Stage 3: LED_test_blink_led
  └─ io.c from Stage 2 + mcu_init.c + assert_handler + defines.h added.
       - mcu_init() owns watchdog + clock init
       - BUSY_WAIT_ms macro replaces raw __delay_cycles
       - ASSERT(0) tail introduced
     Still: main() calls io_configure() manually for the LED pin.

Stage 4: LED_init_pin
  └─ Full IO driver. Three new capabilities:
       - io_initial_configs[] table — static array of struct io_config,
         indexed by io_e value with designated initializers [IO_TEST_LED] = {...}
       - io_init() — boot-time loop that calls io_configure() on every pin
       - io_get_input() using PxIN register array
       - io_get_current_config() + io_config_compare() for runtime inspection
       - NSUMO target added (Port 3, different pin map)
     main() no longer calls io_configure() — mcu_init() → io_init() handles all pins.

Stage 5: LED_test_launchpad_IO
  └─ Hardware board validation tests using the full driver:
       - test_launchpad_io_pins_output(): sweep every pin HIGH/LOW (scope/meter check)
       - test_launchpad_io_pins_input(): walk every pin as pull-up input, wait for
         user to pull each LOW (continuity check)
       - led driver introduced as thin wrapper: led_init() verifies io_init() already
         configured the pin correctly via io_config_compare()
     Demonstrates io_get_input() (PxIN) and pull-up config in practice.

Stage 6: LED_Final
  └─ Minimal clean main — the "shipped" pattern:
       mcu_init() → while(1) { io_set_out(...HIGH); BUSY_WAIT_ms(250);
                               io_set_out(...LOW);  BUSY_WAIT_ms(250); }
       ASSERT(0);
     Application code calls zero configuration functions.
     All GPIO init is owned by the driver layer via mcu_init() → io_init().
```

**The central lesson arc:** The course moves from "write to registers by name" (Stage 1) to "describe what you want in a struct and let the driver figure out which register to touch" (Stage 6). The bit-packing trick (Stage 2) is the enabling mechanism — it lets a single `io_e` value carry enough information to index into the correct port register array without any lookup table or switch statement.
