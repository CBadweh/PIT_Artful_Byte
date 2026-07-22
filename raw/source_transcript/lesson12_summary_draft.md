# Lesson 12 Summary — How I Program GPIOs in C

---

## Transcript Key Points

### 1. Context and Motivation (00:00–03:20)

The lesson marks the first time actual hardware-control code is written. Previous lessons covered software design, Makefile-based build system, Git workflow, and CI. The lesson explains why GPIO is the right starting point:

- GPIO code sits at the **bottom of the software stack** — the convention is to build a stack bottom-up so each layer is verified before the one above it is built on top.
- Getting GPIO working early **verifies the hardware** — in a real project this matters because hardware bugs need to be caught early so a new PCB revision can be spun.
- GPIO enables **debug infrastructure**: blinking an LED is the simplest "is my code running?" check. UART tracing (next video) also depends on pin configuration.

The MSP430G2553 has 24 configurable IO pins (PCB package) / 16 (Launchpad package). Pin assignment was already fixed at PCB design time. The lesson's goal is to **implement that pin assignment in software**.

### 2. What a GPIO Pin Is (03:20–07:30)

A pin can serve one of several roles:
- **GPIO** — general purpose digital input or output.
- **Peripheral function** — the pin is muxed to an internal hardware block (UART, I2C, ADC, timer). The pin effectively bypasses the GPIO circuitry.

The MSP430 allows each pin to select from up to 4 functions (GPIO + 3 alternatives). Which peripheral maps to which alternative number is pin-specific and must be looked up in the datasheet.

Pins are grouped into **ports** (8 pins per port on MSP430). This matches the 8-bit data bus, so an entire port can be read/written in one operation.

### 3. Memory-Mapped Registers — The Core Mental Model (07:30–09:15)

Key insight stated in the transcript:

> "Simply speaking, all code on a microcontroller comes down to writing a value to a register or reading a value from a register. That's how you configure a pin, that's how you configure a peripheral, that's how you disable the Watchdog, that's how you change the clock rate — that's practically how you do anything involving the hardware."

Every port is represented as a set of memory-mapped registers. From the software's perspective these are just memory addresses. Writing to the right address at the right bit position is pin configuration. Texas Instruments provides a vendor header (`msp430.h`) that names these addresses as C variables — so code writes `P1DIR |= BIT0` rather than dereferencing a raw hex address.

The MSP430 GPIO port registers covered:

| Register | Direction | Purpose |
|----------|-----------|---------|
| `PxSEL` / `PxSEL2` | Write | Select GPIO vs. alternative peripheral function (2-bit field per pin) |
| `PxDIR` | Write | Set pin as output (1) or input (0) |
| `PxREN` | Write | Enable/disable internal pull-up/pull-down resistor |
| `PxOUT` | Write | Output level (also selects pull direction when resistor is enabled) |
| `PxIN` | Read | Current digital input level of pin |

Interrupt registers (`PxIE`, `PxIES`, `PxIFG`) are deferred to a later video.

### 4. Design Philosophy: Abstraction Layer Over Vendor Defines (09:15–10:15)

The raw blink example uses TI defines directly:
```c
P1DIR |= BIT0;
P1OUT |= BIT0;
```

The lesson argues this is "crude." The goal is an abstraction that lets you write:
```c
io_set_direction(IO_TEST_LED, IO_DIR_OUTPUT);
io_set_out(IO_TEST_LED, IO_OUT_HIGH);
```

Rules of the abstraction:
- TI defines are **hidden inside the `.c` file** (implementation detail).
- The public interface (`io.h`) uses enums for pin names and configuration values.
- The pin name enum (`io_e`) uses the **exact names from the schematic** as identifiers.

### 5. The Bit-Packing Trick for Port/Pin Extraction (15:35–17:30)

The naive approach to translating a pin name enum to a register is a big `switch` or `if` chain — verbose and wastes flash (the MSP430 only has 16 KB of flash).

The smarter approach: structure the `io_generic_e` enum values so the port number and pin index are **encoded directly in the bit pattern**:

```
[ 0000 0000 000 | PP | ppp ]
                  ^     ^
                port   pin index (0-7)
                (2 bits) (3 bits)
```

- Pins 0–7 are `IO_10`–`IO_17` (port 0, i.e. P1)
- Pins 8–15 are `IO_20`–`IO_27` (port 1, i.e. P2)
- Pins 16–23 are `IO_30`–`IO_37` (port 2, i.e. P3)

Extract port: `(io & 0x18) >> 3`
Extract pin bit: `1 << (io & 0x07)`

These are written as `static inline` functions rather than macros because the author found that inline functions produced better-optimized output than `#define` macros for this particular case.

### 6. Array Indexing Instead of Switch Statements for Registers (17:30–19:20)

Once the port number is extracted, another switch would be needed to map port 0 → `P1DIR`, port 1 → `P2DIR`, etc. Instead, the register addresses are stored in arrays:

```c
static volatile uint8_t *const port_dir_regs[] = { &P1DIR, &P2DIR };
```

Then access is: `*port_dir_regs[port] |= pin_bit`

This array-of-pointers pattern is used for all six register types (DIR, REN, OUT, IN, SEL, SEL2). Key qualifiers on these arrays:
- `static` — file-scoped only, not visible outside `io.c`
- `volatile` — prevents compiler from optimizing away register accesses
- `const` — the addresses themselves never change

### 7. The `io_configure` Struct and One-Call Init (19:20–20:00)

A `struct io_config` groups all four configuration fields (select, resistor, dir, out) for one pin. The function `io_configure(io_e io, const struct io_config *config)` calls all four setters in sequence — one call to fully configure a pin.

### 8. Testing Strategy (20:00–22:30)

Three progressive test functions written in `main.c`:

1. **`test_blink_led`** — single LED, verifies GPIO output direction and output level API.
2. **`test_launchpad_io_pins_output`** — configure all pins as output, toggle them one by one in a loop. Verified with a **logic analyzer** (Sigrok software).
3. **`test_launchpad_io_pins_input`** — configure all pins as input with pull-up. Use one LED pin as indicator. Loop through each pin, wait for it to be pulled low by an **external pull-down resistor** held by the operator. LED goes off when the tested pin goes low, blinks when all pins pass.

The author acknowledges test coverage is incomplete but acceptable as a first pass.

### 9. `io_init` and Default Pin Configuration (22:45–28:20)

All pins are configured at boot in `io_init()`. Rationale:
- Most pins have a fixed role throughout program execution.
- Explicitly configuring all pins (even unused ones) prevents floating-pin current consumption issues.

Unused pin policy (per MSP430 datasheet section 2.5):
- Input with pull-up or pull-down, OR output. Never leave floating.
- Author chose **input with pull-down** to reduce risk of accidental short-circuit.

Pin-by-pin configuration decisions are walked through in the transcript (see Section: Connection Transcript → Code below for the table).

### 10. Dual-Target Compilation (04:40–05:10)

The Launchpad has 16 pins (2 ports), the robot PCB has 24 pins (3 ports). Two separate `io_e` enum bodies are selected at compile time via `#if defined(LAUNCHPAD)` / `#elif defined(NSUMO)`. The `#define LAUNCHPAD` is in `io.h` (marked as TODO to improve).

### 11. Workflow Reminders

- New feature branch created at the start (`feature_io_handling`).
- Commits made at each logical checkpoint (skeleton, implementation, tests, init).
- `clang-format`, `cppcheck`, and a compile check precede every commit.
- Pull request opened on GitHub; CI passes checked before merging.

---

## Source Code Overview

### File List

| File | Role |
|------|------|
| `src/drivers/io.h` | Public interface: enums for pin names and config values, `struct io_config`, function prototypes |
| `src/drivers/io.c` | Implementation: register arrays, bit-extraction inlines, all `io_*` functions, `io_initial_configs` array |
| `src/drivers/mcu_init.h` | Public interface: single `mcu_init()` prototype |
| `src/drivers/mcu_init.c` | Calls `watchdog_stop()` then `io_init()` — the MCU startup sequence |
| `src/main.c` | Three test functions (two commented out), `main()` calls the active one |
| `src/test/test.c` | Empty placeholder (1 line) — tests not yet moved here, marked TODO |
| `src/common/defines.h` | Two utility macros: `UNUSED(x)` and `ARRAY_SIZE(array)` |
| `src/app/drive.c/.h` | Stub files for drive application layer (not relevant to this lesson) |
| `src/app/enemy.c/.h` | Stub files for enemy detection layer (not relevant to this lesson) |
| `Makefile` | Builds with `msp430-elf-gcc`, lists all source files, runs cppcheck and clang-format |
| `.github/workflows/ci.yml` | CI pipeline (not read — out of scope for this lesson) |
| `docs/schematic.png` | PCB schematic — source of truth for pin assignments |

### Key Functions

#### `io.h` — Public API

| Function | Signature | What it does |
|----------|-----------|--------------|
| `io_init` | `void io_init(void)` | Loops over `io_initial_configs[]` and calls `io_configure` for every pin |
| `io_configure` | `void io_configure(io_e, const struct io_config *)` | Calls all four setters in one shot |
| `io_set_select` | `void io_set_select(io_e, io_select_e)` | Writes `PxSEL` and `PxSEL2` to select GPIO or alt function |
| `io_set_direction` | `void io_set_direction(io_e, io_dir_e)` | Writes `PxDIR` bit |
| `io_set_resistor` | `void io_set_resistor(io_e, io_resistor_e)` | Writes `PxREN` bit |
| `io_set_out` | `void io_set_out(io_e, io_out_e)` | Writes `PxOUT` bit (level or pull direction) |
| `io_get_input` | `io_in_e io_get_input(io_e)` | Reads `PxIN` bit, returns `IO_IN_HIGH` or `IO_IN_LOW` |

#### `io.c` — Internal helpers (static inline)

| Function | What it does |
|----------|--------------|
| `io_port(io_e io)` | Returns 0-based port index: `(io & 0x18) >> 3` |
| `io_pin_idx(io_e io)` | Returns 0-based pin index within port: `io & 0x07` |
| `io_pin_bit(io_e io)` | Returns bitmask for the pin: `1 << io_pin_idx(io)` |

#### Registers accessed (via array-of-pointers)

| Array variable | Registers |
|----------------|-----------|
| `port_dir_regs` | `P1DIR`, `P2DIR` [, `P3DIR`] |
| `port_ren_regs` | `P1REN`, `P2REN` [, `P3REN`] |
| `port_out_regs` | `P1OUT`, `P2OUT` [, `P3OUT`] |
| `port_in_regs` | `P1IN`, `P2IN` [, `P3IN`] |
| `port_sel1_regs` | `P1SEL`, `P2SEL` [, `P3SEL`] |
| `port_sel2_regs` | `P1SEL2`, `P2SEL2` [, `P3SEL2`] |

Arrays have 2 entries for `LAUNCHPAD`, 3 entries for `NSUMO`.

#### `mcu_init.c`

`mcu_init()` → `watchdog_stop()` → `io_init()`

`watchdog_stop()` writes `WDTCTL = WDTPW + WDTHOLD` — the standard MSP430 pattern to stop the watchdog timer, which would otherwise reset the MCU in a loop.

#### `main.c`

Holds three test functions. All called `test_setup()` first (which calls `mcu_init()`). Only `test_launchpad_io_pins_input` is active at the end of the lesson. The other two are commented with `// TODO: Move to test file`.

#### `common/defines.h`

- `UNUSED(x)` — suppresses unused-variable compiler warnings during development.
- `ARRAY_SIZE(array)` — `sizeof(array) / sizeof(array[0])` — used in `io_init` loop bound.

---

## Connection: Transcript → Code

### Teaching Point → Code Artifact

| Transcript Teaching | Code Location | How it appears |
|---------------------|---------------|---------------|
| Pin names from schematic → enum | `io.h: io_e` | `IO_TEST_LED`, `IO_UART_RXD`, `IO_MOTORS_LEFT_CC_1`, etc. |
| Dual-target compile-time switch | `io.h` + `io.c` | `#if defined(LAUNCHPAD)` / `#elif defined(NSUMO)` blocks |
| GPIO vs. alternative function selection | `io.h: io_select_e`, `io.c: io_set_select()` | `IO_SELECT_GPIO`, `IO_SELECT_ALT1`–`ALT3`; writes both `PxSEL` and `PxSEL2` |
| Direction register | `io.h: io_dir_e`, `io.c: io_set_direction()` | `IO_DIR_OUTPUT` / `IO_DIR_INPUT` → set/clear bit in `port_dir_regs[port]` |
| Pull-up/pull-down resistor (REN + OUT) | `io.h: io_resistor_e, io_out_e`, `io.c: io_set_resistor()` + `io_set_out()` | Separate enable (`PxREN`) and direction (`PxOUT`) registers |
| Input reading | `io.h: io_in_e`, `io.c: io_get_input()` | Reads `PxIN` bit, returns typed enum |
| Bit-packing trick | `io.c: io_generic_e` layout + `io_port()`, `io_pin_bit()` | Enum values encode port (bits 4:3) and pin (bits 2:0) |
| Array-of-pointers instead of switch | `io.c: port_*_regs[]` arrays | `*port_dir_regs[port] |= pin` replaces `if (port == 0) P1DIR |= pin; else ...` |
| `struct io_config` + `io_configure` | `io.h: struct io_config`, `io.c: io_configure()` | Groups select/resistor/dir/out; `io_init` stores array of these structs indexed by pin name |
| Unused pins should not float | `io.c: UNUSED_CONFIG` macro, `io_initial_configs[]` | `{ IO_SELECT_GPIO, IO_RESISTOR_ENABLED, IO_DIR_OUTPUT, IO_OUT_LOW }` |
| UART pin needs only select set | `io.c: io_initial_configs[]` | `[IO_UART_RXD] = { IO_SELECT_ALT3, IO_RESISTOR_DISABLED, ... }` |
| Timer PWM exception: direction must also be set | `io.c: io_initial_configs[]` | `[IO_PWM_MOTORS_LEFT] = { IO_SELECT_ALT1, IO_RESISTOR_DISABLED, IO_DIR_OUTPUT, ... }` |
| PCB mistake: missing pull-up on range sensor | `io.c: io_initial_configs[]` | `[IO_RANGE_SENSOR_FRONT_INT] = { ..., IO_DIR_INPUT, IO_OUT_HIGH }` — `IO_OUT_HIGH` activates internal pull-up |
| ADC pins: function fully overridden by ADC peripheral | `io.c: io_initial_configs[]` | `[IO_LINE_DETECT_*] = { IO_SELECT_GPIO, IO_RESISTOR_DISABLED, IO_DIR_INPUT, IO_OUT_LOW }` (left floating, ADC config deferred) |
| Test: logic analyzer for output verification | `main.c: test_launchpad_io_pins_output` | Toggles all pins in loop; confirmed externally with Sigrok |
| Test: pull-down resistor + LED for input verification | `main.c: test_launchpad_io_pins_input` | Waits for `io_get_input(io) == IO_IN_LOW` while operator applies external pull-down |
| Watchdog must be stopped first | `mcu_init.c: watchdog_stop()` | `WDTCTL = WDTPW + WDTHOLD` before `io_init()` |

### Call Chain at Boot

```
main()
  └── test_launchpad_io_pins_input()
        └── test_setup()
              └── mcu_init()
                    ├── watchdog_stop()   [writes WDTCTL]
                    └── io_init()
                          └── io_configure(io, &io_initial_configs[io])  [for each pin]
                                ├── io_set_select()    [writes PxSEL, PxSEL2]
                                ├── io_set_direction() [writes PxDIR]
                                ├── io_set_out()       [writes PxOUT]
                                └── io_set_resistor()  [writes PxREN]
```

### Pin Configuration Summary (NSUMO target)

| Pin Name | Select | Resistor | Dir | Out | Reasoning |
|----------|--------|----------|-----|-----|-----------|
| `IO_TEST_LED` | GPIO | Disabled | Output | Low | Drives LED directly |
| `IO_UART_RXD/TXD` | ALT3 | Disabled | — | — | UART peripheral owns the pin |
| `IO_IR_REMOTE` | GPIO | Disabled | Input | — | IR receiver has its own resistor |
| `IO_I2C_SCL/SDA` | ALT3 | Disabled | — | — | External pull-ups on board |
| `IO_MOTORS_*_CC_*` | GPIO | Disabled | Output | Low | Motor direction control |
| `IO_PWM_MOTORS_*` | ALT1 | Disabled | Output | Low | Timer peripheral, direction must still be set |
| `IO_RANGE_SENSOR_FRONT_INT` | GPIO | Disabled | Input | High | Internal pull-up compensates for missing PCB resistor |
| `IO_XSHUT_*` | GPIO | Disabled | Output | Low | Range sensor boot mode control |
| `IO_LINE_DETECT_*` | GPIO | Disabled | Input | Low | ADC overrides fully; left floating for now |
| `IO_UNUSED_*` | GPIO | Enabled | Output | Low | Per datasheet: no floating unused pins |

---

## Notes and Open Questions

- `test.c` and `test.h` are empty stubs. The author marks all test functions in `main.c` with `// TODO: Move to test file` — a dedicated test infrastructure is planned for a later video.
- `#define LAUNCHPAD` is hardcoded at the top of `io.h`. The author calls this "ugly" and marks it `// TODO: Improve multiple HW targets handling`. The intent is to pass the target as a Makefile flag (`-DLAUNCHPAD` / `-DNSUMO`) rather than hardcoding it in the header.
- The `io_configure` call order in `io.c` is: select → direction → out → resistor. The REN register write comes last, after `PxOUT` is set. This ordering matters: `PxOUT` determines pull-up vs. pull-down direction when the resistor is subsequently enabled.
- `io_generic_e` and `io_e` are separate enums. `io_generic_e` defines the raw port/pin layout. `io_e` assigns human-readable names to those values. Functions in `io.c` accept `io_e` but the internal helpers (`io_port`, `io_pin_bit`) work on the underlying integer value of the enum, which is why the bit-extraction trick works transparently.
