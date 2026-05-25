# Plan: FastBit1 C Topics Needed for Artful Bytes Project

## Context

**Problem:** Students with Arduino-level C skills want to follow the Artful Bytes sumo robot course (bare-metal MSP430, register-level drivers, no HAL). They don't have time for the full FastBit1 C course (31 sections, 192 lessons). We need to identify which FastBit1 sections to study and rank them by impact.

**Approach:** I read the actual Artful Bytes nsumo source code (`io.c`, `uart.c`, `adc.c`, `pwm.c`, `state_machine.c`, `ring_buffer.h`, `assert_handler.c`, `defines.h`, `io.h`) and identified every C concept used. Then I mapped each concept back to the FastBit1 section that teaches it.

**What Arduino students already know:** `digitalWrite()`, `analogRead()`, basic `if/else`, `for` loops, `int`/`float` types, simple functions, `Serial.println()`. They do NOT know: register-level access, bitwise manipulation, pointers, volatile, structs, enums, preprocessor macros, or how a build process works.

---

## Pareto Ranking: FastBit1 Sections Needed (8 sections = 26% of course → covers ~90% of Artful Bytes C patterns)

### Tier 1 — MUST STUDY (without these, students cannot read a single driver file)

#### 1. S17 Bitwise Operators + S19 Bitwise Shift Operators

**FastBit1 Lessons:** S17 (L104–L112), S19 (L127–L132)

**Why needed:** Every single driver file in Artful Bytes uses bitwise ops for register manipulation. This is the #1 gap between Arduino and bare-metal.

**Concrete Artful Bytes examples:**


| Pattern                                 | Where in nsumo code   | What it does                                  |
| --------------------------------------- | --------------------- | --------------------------------------------- |
| `*port_dir_regs[port] |= pin`           | `io.c:269`            | Set bit → configure pin as output             |
| `*port_dir_regs[port] &= ~pin`          | `io.c:266`            | Clear bit → configure pin as input            |
| `P1OUT ^= BIT0`                         | `assert_handler.c:42` | Toggle bit → blink LED                        |
| `1 << io_pin_idx(io)`                   | `io.c:42`             | Shift to create pin bitmask                   |
| `(io & IO_PORT_MASK) >> IO_PORT_OFFSET` | `io.c:32`             | Mask + shift to extract port number from enum |
| `ADC10CTL0 |= ENC + ADC10SC`            | `adc.c:22`            | Set multiple control bits at once             |
| `IFG2 &= ~UCA0TXIFG`                    | `uart.c:39`           | Clear interrupt flag bit                      |


**Arduino equivalent they already know:** `digitalWrite(13, HIGH)` — but that hides the `PORTB \|= (1<<5)` happening underneath.

---

#### 2. S13 Pointers + S5 Address-of Operator

**FastBit1 Lessons:** S13 (L076–L082), S5 (L024–L030)

**Why needed:** Artful Bytes stores hardware register addresses in pointer arrays and dereferences them to control hardware. Without understanding pointers, students cannot read ANY driver code.

**Concrete Artful Bytes examples:**


| Pattern                                                          | Where in nsumo code | What it does                              |
| ---------------------------------------------------------------- | ------------------- | ----------------------------------------- |
| `volatile uint8_t *const port_dir_regs[] = { &P1DIR, &P2DIR }`   | `io.c:60`           | Array of pointers to hardware registers   |
| `*port_dir_regs[port] |= pin`                                    | `io.c:269`          | Dereference pointer to write to register  |
| `volatile unsigned int *const ccr`                               | `pwm.c:37`          | Pointer to timer capture/compare register |
| `*pwm_cfgs[pwm].ccr = duty_cycle`                                | `pwm.c:100`         | Dereference struct member pointer         |
| `const struct io_config *config`                                 | `io.c:209`          | Pointer to struct as function parameter   |
| `void ring_buffer_put(struct ring_buffer *rb, const void *data)` | `ring_buffer.h:33`  | Pointer to generic data (void pointer)    |


**Arduino equivalent:** Arduino hides all pointers behind library functions. Students have never seen `*ptr` or `&variable`.

---

#### 3. S24 Volatile Type Qualifier

**FastBit1 Lessons:** S24 (L146–L149)

**Why needed:** Every hardware register pointer in Artful Bytes is declared `volatile`. Without understanding why, students will write code that "works in debug but breaks in release" — the most confusing embedded bug.

**Concrete Artful Bytes examples:**


| Pattern                                              | Where in nsumo code | What it does                       |
| ---------------------------------------------------- | ------------------- | ---------------------------------- |
| `static volatile uint8_t *const port_dir_regs[]`     | `io.c:60`           | Register pointers MUST be volatile |
| `static volatile adc_channel_values_t adc_dtc_block` | `adc.c:14`          | DMA buffer modified by hardware    |
| `volatile unsigned int *const cctl`                  | `pwm.c:36`          | Timer control register pointer     |


**Why Arduino students don't know this:** Arduino IDE compiles with `-O0` (no optimization) by default, so the bug never appears. Artful Bytes uses `-Os` where the compiler WILL optimize away register reads without volatile.

---

#### 4. S14 Importance of `stdint.h`

**FastBit1 Lessons:** S14 (L083–L088)

**Why needed:** Artful Bytes uses `uint8_t`, `uint16_t` exclusively — never `int` or `unsigned int`. The MSP430 is 16-bit, so `int` = 16 bits (not 32 like Arduino's ARM-based boards). Wrong type = silent overflow bugs.

**Concrete Artful Bytes examples:**

- `uint8_t` for pin indices, port numbers, duty cycle percentages
- `uint16_t` for timer values, program counter in assert handler
- `static_assert(sizeof(io_generic_e) == 1, ...)` at `io.c:25` — the code literally ASSERTS on data size

**Why it matters:** Arduino `int` is 32-bit on ARM boards but 16-bit on MSP430. Code that "works" on Arduino breaks silently on MSP430 if you use `int` instead of `uint16_t`.

---

### Tier 2 — SHOULD STUDY (needed to understand architecture and write new modules)

#### 5. S25 Structures and Bit Fields

**FastBit1 Lessons:** S25 (L150–L163)

**Why needed:** Artful Bytes uses structs everywhere for organizing data — driver configs, state machine data, ring buffers. Students need structs to understand how modules pass data around.

**Concrete Artful Bytes examples:**


| Pattern                                                                                                        | Where in nsumo code     |
| -------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `struct io_config { io_select_e select; io_resistor_e resistor; io_dir_e dir; io_out_e out; }`                 | `io.h:106-112`          |
| `struct state_transition { state_e from; state_event_e event; state_e to; }`                                   | `state_machine.c:36-40` |
| `struct state_machine_data { state_e state; struct state_common_data common; ... }`                            | `state_machine.c:70-82` |
| `struct ring_buffer { uint8_t *buffer; uint8_t buffer_size; ... }`                                             | `ring_buffer.h:10-18`   |
| Designated initializers: `[IO_TEST_LED] = { IO_SELECT_GPIO, IO_RESISTOR_DISABLED, IO_DIR_OUTPUT, IO_OUT_LOW }` | `io.c:105`              |
| Struct member access via pointer: `config->select`, `data->state`                                              | Throughout              |


**Note:** Artful Bytes does NOT use bit fields for register overlays (it uses bitwise ops directly). But understanding structs is essential — bit fields from FastBit1 S27 can be skipped.

---

#### 6. S31 Pre-processor Directives

**FastBit1 Lessons:** S31 (L181–L192)

**Why needed:** Artful Bytes relies heavily on preprocessor for hardware abstraction, macros, and conditional compilation.

**Concrete Artful Bytes examples:**


| Pattern                                                                      | Where in nsumo code      | What it does                                     |
| ---------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------ |
| `#if defined(LAUNCHPAD)` / `#elif defined(NSUMO)`                            | `io.c:10`, `io.h:23`     | Compile different pin maps for different boards  |
| `#define ARRAY_SIZE(array) (sizeof(array) / sizeof(array[0]))`               | `defines.h:6`            | Utility macro                                    |
| `#define INTERRUPT_FUNCTION(vector) void __attribute__((interrupt(vector)))` | `defines.h:7`            | ISR declaration macro                            |
| Multi-line macro with `do { } while(0)`: `GPIO_OUTPUT_LOW`                   | `assert_handler.c:16-23` | Safe multi-statement macro                       |
| Token pasting `##`: `P##port##SEL &= ~(BIT##bit)`                            | `assert_handler.c:18`    | Generate port register names at compile time     |
| `#define STATIC_RING_BUFFER(name, size, type) ...`                           | `ring_buffer.h:20-28`    | Macro that declares both buffer array and struct |
| Include guards: `#ifndef IO_H` / `#define IO_H` / `#endif`                   | Every `.h` file          | Prevent double inclusion                         |


---

#### 7. S6 Storage Classes + S7 Functions

**FastBit1 Lessons:** S6 (L031–L038), S7 (L039–L048)

**Why needed:** Artful Bytes uses `static` extensively for encapsulation — the primary mechanism for "private" functions/variables in C. Every module has `static` internal functions and exposes only the API through the header.

**Concrete Artful Bytes examples:**


| Pattern                                                        | Where in nsumo code                   | What it does                     |
| -------------------------------------------------------------- | ------------------------------------- | -------------------------------- |
| `static uint8_t io_port(io_e io)`                              | `io.c:30`                             | Private helper — not in io.h     |
| `static inline uint8_t io_pin_idx(io_e io)`                    | `io.c:35`                             | Private + inline for performance |
| `static bool initialized = false`                              | `uart.c:101`, `adc.c:25`, `pwm.c:112` | File-scope state variable        |
| `static volatile uint8_t *const port_dir_regs[]`               | `io.c:60`                             | File-scope constant array        |
| `static const struct state_transition state_transitions[]`     | `state_machine.c:43`                  | File-scope lookup table          |
| Function pointer typedef: `typedef void (*isr_function)(void)` | `io.h:126`                            | Callback registration pattern    |


**Arduino gap:** Arduino sketches are single-file. Students have never used `static` for scope control or split code across `.c/.h` pairs.

---

### Tier 3 — NICE TO HAVE (helpful context, can learn on-the-fly)

#### 8. S21 `const` Type Qualifier

**FastBit1 Lessons:** S21 (L137–L141)

**Why needed:** Artful Bytes uses `const` for read-only data (config tables, string literals) and `const` pointers to prevent accidental register writes. Understanding `const` helps read function signatures.

**Examples:** `const struct io_config *config` (pointer to read-only struct), `volatile uint8_t *const` (pointer that can't be redirected).

#### 9. S9 Build Process

**FastBit1 Lessons:** S9 (L059–L065)

**Why needed:** Understanding preprocessor → compiler → assembler → linker helps students understand the Artful Bytes Makefile and why `make HW=LAUNCHPAD` produces different binaries than `make HW=NSUMO`. Also helps debug linker errors.

---

## Sections to SKIP (not needed for Artful Bytes)


| FastBit1 Section                       | Why Skip                                                                |
| -------------------------------------- | ----------------------------------------------------------------------- |
| S1-S3 (Intro, IDE, First Program)      | Students already write Arduino code                                     |
| S4 (Data Types basics)                 | Arduino students know int/float/char — S14 stdint.h covers the gap      |
| S8 (MCU Hello World, printf/ITM)       | Artful Bytes uses UART printf, not ITM/semihosting                      |
| S10-S12 (Code analysis, floats, scanf) | Not used in Artful Bytes                                                |
| S15-S16 (Operators, Decision Making)   | Arduino students already know +, -, if/else, switch                     |
| S20 (Looping)                          | Arduino students already know for/18while                               |
| S22 (Pin Read exercise)                | Artful Bytes teaches this with its own GPIO driver                      |
| S23 (Optimization)                     | Too advanced for now — volatile (S24) is the key takeaway               |
| S26 (Unions)                           | Not used in Artful Bytes nsumo code                                     |
| S27 (Bit Field register overlays)      | Artful Bytes uses bitwise ops, not bit field overlays                   |
| S28 (Keypad Interfacing)               | Different hardware                                                      |
| S29-S30 (Arrays, Strings)              | Arduino students know basic arrays; strings are minimal in Artful Bytes |


---

## Recommended Study Order (9 sections, ~65 lessons)

```
Week 1: The Foundation Gap
  S17 → S19 → S13 + S5 → S18     Bitwise ops + Pointers + LED exercise (capstone)
  (After this: students can READ io.c and understand what register manipulation does.
   S18 is where the full chain clicks: cast address → bitwise configure → hardware changes)

Week 2: Embedded-Specific C
  S24 → S14                        volatile + stdint.h
  (After this: students understand WHY the code uses volatile uint8_t instead of int)

Week 3: Code Organization
  S25 → S31 → S6 + S7             Structs + Preprocessor + static/functions
  (After this: students can understand multi-file architecture, macros, and module design)
```

**Total: ~65 lessons out of 192 (34%) → covers ~90% of the C patterns in the Artful Bytes codebase.**

---

## Verification

To confirm this mapping is complete, here's a checklist of every C concept found in the nsumo source code and which FastBit1 section teaches it:


| C Concept in nsumo                 | Used in                              | FastBit1 Section                                         | Tier |
| ---------------------------------- | ------------------------------------ | -------------------------------------------------------- | ---- |
| `|=`, `&= ~`, `^=`                 | Every driver                         | S17                                                      | 1    |
| `<<`, `>>`                         | Every driver                         | S19                                                      | 1    |
| Pointer declaration + dereference  | Every driver                         | S13 + S5                                                 | 1    |
| `volatile`                         | Every register pointer               | S24                                                      | 1    |
| `uint8_t`, `uint16_t`              | Every file                           | S14                                                      | 1    |
| `struct` + designated initializers | io.h, state_machine.c, ring_buffer.h | S25                                                      | 2    |
| `#define`, `#if defined`, `##`     | defines.h, every .h                  | S31                                                      | 2    |
| `static` functions/variables       | Every .c file                        | S6                                                       | 2    |
| Function pointers                  | io.h (isr_function)                  | S7 + S13                                                 | 2    |
| `const`                            | Config tables, function params       | S21                                                      | 3    |
| Build process (linker, .elf)       | Makefile                             | S9                                                       | 3    |
| `enum` (typedef)                   | io.h, state_machine.h                | S25 (partially)                                          | 2    |
| `static_assert`                    | io.c, uart.c, pwm.c                  | Not in FastBit1 — teach as "compile-time check"          | —    |
| `inline`                           | io.c, state_machine.c                | Not in FastBit1 — teach as "hint to compiler"            | —    |
| `__attribute_`_                    | defines.h (interrupt, unused)        | Not in FastBit1 — teach alongside Artful Bytes Lesson 17 | —    |


