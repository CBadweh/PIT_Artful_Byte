### Section 5: Low-Level Programming Fundamentals

---

### Lesson 012 -- How I Program GPIOs in C

**File Path:** [12 How I program GPIOs in C  Embedded System Project Series #12.txt](Artful_Bytes_Transcript/12%20How%20I%20program%20GPIOs%20in%20C%20%20Embedded%20System%20Project%20Series%20%2312.txt)

**Objective:** Teaches how to write a clean GPIO abstraction layer in C for the MSP430 microcontroller, translating a hardware schematic's pin assignments into software by wrapping TI's register defines behind a well-structured interface. This is the first real driver code in the project and establishes the pattern for all subsequent driver implementations.

**Terminology & Key Concepts:**
- **IO Pins (GPIO)**: General Purpose Input/Output -- the configurable metal pins on a microcontroller used to communicate with external hardware (sensors, motors, LEDs)
- **Pin Assignment / Pin Mapping**: The hardware-level decision of which microcontroller pin connects to which external component, determined during PCB design and documented in the schematic
- **Memory-Mapped Registers**: Hardware registers accessible at specific memory addresses; writing to or reading from these addresses configures or queries the hardware
- **Port**: A logical grouping of IO pins (8 pins per port on MSP430); each port has its own set of configuration registers
- **Pin Muxing (Select)**: Configuring a pin to serve either as GPIO or to connect to an internal peripheral (UART, I2C, Timer, ADC)
- **Pull-Up / Pull-Down Resistor**: Internal resistors that drive a floating input pin to a known state (high or low) to prevent unpredictable behavior and excess current consumption
- **Bit Banging**: Implementing a communication protocol purely in software using GPIO toggling, consuming more CPU cycles than using dedicated peripherals
- **Inline Function**: A function hint to the compiler to insert the function body at each call site, avoiding function call overhead at the cost of potentially larger code size

| Register | Purpose | Direction |
|---|---|---|
| PxSEL / PxSEL2 | Select pin function (GPIO vs. peripheral alt 1/2/3) | Write |
| PxDIR | Set pin direction (input or output) | Write |
| PxREN | Enable/disable internal pull-up or pull-down resistor | Write |
| PxOUT | Set output level (high/low) or select pull-up vs pull-down | Write |
| PxIN | Read digital input level of pin | Read |
| PxIFG / PxIE / PxIES | Interrupt flag, enable, and edge select (covered in later lesson) | Read/Write |

**Techniques & Methods:**
- **Bottom-Up Implementation**: Start driver code at the lowest layer of the software stack (closest to hardware) and build upward, allowing each layer to be tested before the next is added
- **Enum-Based Pin Naming**: Using a C enum (`io_e`) to give meaningful names to each pin drawn from the schematic, providing type-safe identifiers that can be passed as function arguments
- **Bitwise Port/Pin Extraction**: Encoding the port number and pin index into the enum value's bit pattern (`[zeros(3)|port(2)|pin(3)]`) so the port and pin can be extracted using shifts and masks without if/switch statements
- **Array-Indexed Register Access**: Storing register addresses in arrays indexed by port number to avoid verbose switch/if statements and reduce flash usage
- **Compile-Time Target Switching**: Using `#ifdef LAUNCHPAD` / `#ifdef NSUMO` preprocessor directives to maintain two pin assignment sets for the development board (16 pins) and robot PCB (24 pins)
- **Config Struct Pattern**: Defining a `struct io_config` that bundles all pin settings (select, direction, resistor, output), then passing it to a single `io_configure()` function
- **Init-Time Bulk Configuration**: Storing all pin configs in a const array indexed by pin name, then looping through it in `io_init()` to configure every pin at boot

**Source Code Mapping:**
- `io_port()`: `io.c:30` -- Extracts port number from an io_e enum value using bitwise shift and mask
  ```c
  static uint8_t io_port(io_e io)
  {
      return (io & IO_PORT_MASK) >> IO_PORT_OFFSET;
  }
  ```
- `io_pin_bit()`: `io.c:40` -- Converts pin index to a bitmask by shifting 1 left by the pin number
  ```c
  static uint8_t io_pin_bit(io_e io)
  {
      return 1 << io_pin_idx(io);
  }
  ```
- `io_set_select()`: `io.c:236` -- Writes to PxSEL and PxSEL2 registers to select GPIO or alternate peripheral function
- `io_set_direction()`: `io.c:260` -- Sets a pin as input or output by writing to the PxDIR register
- `io_set_resistor()`: `io.c:274` -- Enables or disables the internal pull-up/pull-down resistor via PxREN
- `io_set_out()`: `io.c:288` -- Sets the output level (high/low) or selects pull-up vs pull-down via PxOUT
- `io_get_input()`: `io.c:302` -- Reads the digital input level from PxIN
- `io_configure()`: `io.c:209` -- Calls all set functions to configure a pin from a single `struct io_config`
- `io_init()`: `io.c:195` -- Loops through the `io_initial_configs[]` array to configure every pin at startup
- Register address arrays: `io.c:59-73` -- `port_dir_regs[]`, `port_sel1_regs[]`, etc., storing volatile pointers to hardware registers indexed by port number
  ```c
  static volatile uint8_t *const port_dir_regs[IO_PORT_CNT] = { &P1DIR, &P2DIR };
  ```

**Demo / Example:**
- **Goal:** Verify all GPIO pins work as both outputs and inputs on the Launchpad development board
- **Why Important:** Validates the entire IO abstraction layer and confirms hardware connections are functional before building higher-level drivers
- **Demo Flow:**
  1. **Test 1 -- LED Blink**: Replace raw register writes with `io_configure()` and `io_set_out()` to blink the test LED, confirming basic output functionality
  2. **Test 2 -- All Pins Output**: Configure all pins as outputs and toggle them in a loop; verify with a logic analyzer (Sigrok) that signals appear on each pin
  3. **Test 3 -- All Pins Input**: Configure all pins as inputs with internal pull-up resistors except one LED pin; loop through each pin waiting for the operator to pull it low with an external resistor, using the LED as visual feedback
- **What Changed:**
  - `io.c` / `io.h`: Created with full pin abstraction -- enums, config struct, all register access functions, init array
  - `mcu_init.c` / `mcu_init.h`: Created to hold watchdog stop and future MCU initialization
  - `Makefile`: Updated to include new source files
  - `main.c`: Test functions added directly (marked as TODO to move later)
- **Related Code:**
  ```c
  // Unused pin config macro -- prevents floating inputs
  #define UNUSED_CONFIG { IO_SELECT_GPIO, IO_RESISTOR_ENABLED, IO_DIR_OUTPUT, IO_OUT_LOW }
  // Pin init array -- maps every pin to its boot configuration
  static const struct io_config io_initial_configs[IO_PORT_CNT * IO_PIN_CNT_PER_PORT] = {
      [IO_TEST_LED] = { IO_SELECT_GPIO, IO_RESISTOR_DISABLED, IO_DIR_OUTPUT, IO_OUT_LOW },
      [IO_UART_RXD] = { IO_SELECT_ALT3, IO_RESISTOR_DISABLED, IO_DIR_OUTPUT, IO_OUT_LOW },
      ...
  };
  ```

**Discussion Prompts:**
- **Q1: Why use array-indexed register access instead of switch/if statements?**
  - Array indexing produces smaller machine code on a flash-constrained MCU (16 KB on MSP430). A switch statement for each register access would duplicate branching logic across every function, wasting precious flash. Array indexing also makes the code cleaner -- each function body becomes just a few lines of bitwise operations on `*port_xxx_regs[port]`.
- **Q2: Why configure unused pins instead of leaving them at their default reset state?**
  - Unconfigured (floating) input pins have indeterminate voltage levels that fluctuate with noise, causing unpredictable and elevated current consumption. The MSP430 datasheet recommends configuring unused pins as outputs or as inputs with pull-up/pull-down resistors enabled. This is good practice on any microcontroller.
- **Q3: Why use `volatile` and `const` together on the register pointer arrays?**
  - `volatile` tells the compiler the memory at the pointed-to address can change outside the program's control (hardware registers), preventing the compiler from optimizing away reads/writes. `const` on the pointer itself means the address stored in the array never changes (register addresses are fixed). Together they ensure correct hardware access while preventing accidental pointer modification.

---

### Lesson 013 -- Handling Multiple Hardware Versions

**File Path:** [13 Handling multiple Hardware Versions  Embedded System Project Series #13.txt](Artful_Bytes_Transcript/13%20Handling%20multiple%20Hardware%20Versions%20%20Embedded%20System%20Project%20Series%20%2313.txt)

**Objective:** Demonstrates how to handle multiple hardware targets (Launchpad development board vs. nsumo robot PCB) both at compile time through Makefile arguments and at runtime through hardware version detection, a common practice in professional embedded projects with multiple board revisions.

**Terminology & Key Concepts:**
- **Hardware Versioning**: The practice of distinguishing between different physical board revisions or hardware targets in software, essential when supporting multiple PCB revisions in production
- **Compile-Time Target Selection**: Passing defines to the compiler via the build system to conditionally compile code for a specific hardware target
- **Runtime Hardware Detection**: Reading a physical characteristic of the board (e.g., a GPIO with a pull-up resistor) at boot to determine which hardware the code is running on
- **Board Revision Detection**: Using pull-up/pull-down resistors on GPIO pins to create a binary encoding that software can read to identify the hardware version

| Detection Method | GPIO Pins Needed | Versions Supported | Notes |
|---|---|---|---|
| 1 GPIO + pullup/pulldown | 1 | 2 | Simplest; used in this project |
| 2 GPIOs + resistors | 2 | 4 | Binary encoding |
| 3 GPIOs + resistors | 3 | 8 | Scales exponentially |
| 1 ADC + resistor network | 1 | Many | Distinct voltage per version; saves GPIOs |

**Techniques & Methods:**
- **Makefile HW Argument**: Adding `HW=LAUNCHPAD` or `HW=NSUMO` as a mandatory make argument that gets passed as a `-D` compiler define, replacing manual `#define` editing in source files
- **Separate Build Directories**: Creating subdirectories under `build/` for each target (e.g., `build/launchpad/`, `build/nsumo/`) to avoid having to clean between target switches
- **Error Checking in Makefile**: Using `$(error ...)` to report meaningful errors when required arguments are missing, and excluding non-target-dependent rules (clean, cppcheck, format) from the HW requirement
- **Physical Pull-Up for Detection**: Soldering a 100K ohm pull-up resistor on an unused GPIO (pin 3.4) on the robot PCB; reading that pin at boot returns HIGH on the robot and LOW on the Launchpad
- **CI Dual-Target Build**: Adding both `make HW=LAUNCHPAD` and `make HW=NSUMO` steps to the GitHub Actions workflow so every commit is validated against both targets

**Source Code Mapping:**
- `io_detect_hw_type()`: `io.c:184` -- Configures port 3 pin 4 as input (using raw TI registers since port 3 is not in the Launchpad enum) and reads its level to determine hardware type
  ```c
  static hw_type_e io_detect_hw_type(void)
  {
      P3SEL &= ~(BIT4);
      P3SEL2 &= ~(BIT4);
      P3DIR &= ~(BIT4);
      P3REN &= ~(BIT4);
      P3OUT &= ~(BIT4);
      return P3IN & BIT4 ? HW_TYPE_NSUMO : HW_TYPE_LAUNCHPAD;
  }
  ```
- `io_init()`: `io.c:195` -- Calls `io_detect_hw_type()` and asserts that the detected hardware matches the compile-time target
  ```c
  void io_init(void)
  {
  #if defined(NSUMO)
      ASSERT(io_detect_hw_type() == HW_TYPE_NSUMO);
  #elif defined(LAUNCHPAD)
      ASSERT(io_detect_hw_type() == HW_TYPE_LAUNCHPAD);
  #endif
      ...
  }
  ```
- Makefile target selection: `Makefile:6-13` -- Parses the `HW` argument and maps it to `TARGET_HW`

**Demo / Example:**
- **Goal:** Flash correct and incorrect firmware to both targets and verify the mismatch detection works
- **Why Important:** Prevents accidental damage from running firmware compiled for the wrong hardware, a real risk when the same debugger programs both boards
- **Demo Flow:**
  1. Build with `make HW=NSUMO`, flash to robot -- LED blinks (correct target, test passes)
  2. Build with `make HW=LAUNCHPAD`, flash to robot -- LED does not blink (assert fires, code hangs in while loop)
  3. Repeat for Launchpad: correct firmware blinks, wrong firmware hangs
  4. Verify `make clean` works without requiring the `HW` argument
- **What Changed:**
  - `Makefile`: Added HW argument parsing, separate build directories per target, error reporting for missing arguments, exclusion of non-target rules
  - `io.c`: Added `io_detect_hw_type()` and assert in `io_init()`
  - `.github/workflows/ci.yml`: Added both `HW=LAUNCHPAD` and `HW=NSUMO` build steps

**Discussion Prompts:**
- **Q1: Why not just rely on compile-time defines and skip runtime detection entirely?**
  - Compile-time defines protect against compiling the wrong code, but they cannot prevent the developer from flashing the wrong binary to the wrong board. Since the MSP430 on the Launchpad and robot are the same chip, the debugger cannot distinguish between them. Runtime detection catches this final failure mode.
- **Q2: When would you use an ADC-based version detection instead of GPIOs?**
  - When GPIO pins are scarce and many board versions exist. A single ADC pin with a resistor divider network can encode dozens of versions as distinct voltage levels, while GPIO-based detection requires one pin per bit (2^n versions per n pins). The trade-off is slightly more complex read logic and sensitivity to resistor tolerances.

---

### Lesson 014 -- Assert on a Microcontroller

**File Path:** [14 Assert on a Microcontroller  Embedded System Project Series #14.txt](Artful_Bytes_Transcript/14%20Assert%20on%20a%20Microcontroller%20%20Embedded%20System%20Project%20Series%20%2314.txt)

**Objective:** Implements a custom assert handler suitable for a bare-metal microcontroller that has no operating system to gracefully handle crashes, using software breakpoints, LED blinking, and (later) UART tracing to make programming errors detectable and localizable during development. Also introduces static_assert for compile-time validation and creates a dedicated LED driver.

**Terminology & Key Concepts:**
- **Runtime Assert**: A conditional check that halts execution when a programming assumption is violated; on a microcontroller without an OS, the developer must define what "halt" means
- **Software Breakpoint**: A special CPU instruction (opcode `0x4343` on MSP430, `CLR.B R3`) that causes the debugger to pause execution programmatically, as opposed to a manually-set IDE breakpoint
- **Static Assert (`static_assert`)**: A compile-time assertion that triggers a compiler error if its condition is false; catches mistakes before the code even runs
- **Assert Handler**: The function that executes when an assert fires -- in this project: stop motors, trigger breakpoint, trace to terminal, blink LED forever
- **`-fshort-enums` Flag**: A GCC compiler flag that makes enums use the smallest integer type that fits all values (1 byte instead of 2), saving flash on constrained MCUs

**Techniques & Methods:**
- **Macro-Wrapped Assert**: The `ASSERT()` macro wraps `assert_handler()`, enabling compile-time switching (e.g., disable in production), and uses `__FILE__` / `__LINE__` preprocessor directives to capture the location of the failure
- **Inline Assembly for Breakpoint**: Using `__asm volatile("CLR.B R3")` in GCC because the TI compiler's `__op_code()` intrinsic is not available in GCC
- **Isolated Assert Handler**: The assert handler avoids calling functions that themselves contain asserts (like the LED driver) to prevent recursive assert calls leading to stack overflow; instead it writes directly to IO registers
- **Dual-Target LED Blinking**: The assert handler configures the LED pin for both Launchpad and nsumo using raw register writes, so the LED blinks even if the wrong target was flashed
- **`BUSY_WAIT_ms()` Macro**: Wraps `__delay_cycles()` with millisecond conversion (`CYCLES_PER_MS * ms`) for more readable delay code
- **Static Assert for Enum Size**: Verifying `sizeof(io_generic_e) == 1` to confirm `-fshort-enums` is active, since the bitwise port/pin extraction logic depends on 1-byte enums

**Source Code Mapping:**
- `ASSERT()` macro: `assert_handler.h:8-15` -- Captures program counter via inline assembly and calls `assert_handler(pc)`
  ```c
  #define ASSERT(expression)                              \
      do {                                                \
          if (!(expression)) {                            \
              uint16_t pc;                                \
              asm volatile("mov pc, %0" : "=r"(pc));     \
              assert_handler(pc);                         \
          }                                               \
      } while (0)
  ```
- `assert_handler()`: `assert_handler.c:65` -- Main handler: stops motors, triggers breakpoint, traces PC, blinks LED forever
- `BREAKPOINT` macro: `assert_handler.c:11` -- `__asm volatile("CLR.B R3")` triggers MSP430 software breakpoint
- `assert_blink_led()`: `assert_handler.c:36` -- Configures LED pins via raw register writes and blinks in an infinite loop
- `assert_stop_motors()`: `assert_handler.c:49` -- Sets all motor-related GPIOs to output low to prevent uncontrolled motor operation
- `GPIO_OUTPUT_LOW()` macro: `assert_handler.c:16-23` -- Configures a pin as GPIO output low using token-pasting for the port/bit
  ```c
  #define GPIO_OUTPUT_LOW(port, bit)                     \
      do {                                               \
          P##port##SEL &= ~(BIT##bit);                   \
          P##port##SEL2 &= ~(BIT##bit);                  \
          P##port##DIR |= BIT##bit;                      \
          P##port##REN &= ~(BIT##bit);                   \
          P##port##OUT &= ~(BIT##bit);                   \
      } while (0)
  ```
- `led_init()`: `led.c:15` -- Asserts the LED pin has the expected config (validates `io_init()` was called) and prevents double-init
- `led_set()`: `led.c:24` -- Asserts initialization, then calls `io_set_out()` to turn the LED on or off
- `static_assert` usage: `io.c:25` -- Validates enum fits in 1 byte
  ```c
  static_assert(sizeof(io_generic_e) == 1, "Unexpected size, -fshort-enums missing?");
  ```
- `BUSY_WAIT_ms()`: `defines.h:17` -- Converts milliseconds to CPU cycles for `__delay_cycles()`
  ```c
  #define BUSY_WAIT_ms(ms) (__delay_cycles(ms_TO_CYCLES(ms)))
  ```

**Demo / Example:**
- **Goal:** Demonstrate the assert handler and LED driver working together, and show static_assert catching a compile-time error
- **Why Important:** Asserts are the primary defensive mechanism for catching logic errors during development on bare-metal systems
- **Demo Flow:**
  1. Call `led_init()` twice -- triggers "already initialized" assert, debugger breaks at correct call stack location
  2. Omit `io_init()` before `led_init()` -- triggers config mismatch assert
  3. Omit `led_init()` before `led_set()` -- triggers "not initialized" assert inside `led_set()`
  4. Run normally with no assertion violations -- LED blinks without interruption
  5. Remove `-fshort-enums` from Makefile -- static_assert fires at compile time showing "Unexpected size"
- **What Changed:**
  - `assert_handler.c` / `assert_handler.h`: Created with ASSERT macro, breakpoint, and LED blinking
  - `led.c` / `led.h`: Created as a thin wrapper around `io_set_out()` with sanity-check asserts
  - `defines.h`: Added `BUSY_WAIT_ms()`, `UNUSED()`, `SUPPRESS_UNUSED` macros
  - `io.c`: Added `io_get_current_config()` and `io_config_compare()` for config verification
  - `Makefile`: Added `-fshort-enums` compiler flag

**Discussion Prompts:**
- **Q1: Why not use the standard library `assert()` on a microcontroller?**
  - The standard `assert()` typically calls `abort()`, which on a microcontroller with no OS either does nothing useful or is undefined. A custom handler lets you define exactly what happens: stop motors (safety), trigger a debugger breakpoint, trace the location, and blink an LED as a visual indicator. This is far more useful for debugging than a silent hang.
- **Q2: Why does the assert handler avoid using the LED driver and instead writes registers directly?**
  - The LED driver itself contains asserts (e.g., checking that `led_init()` was called). If the assert handler called `led_set()` and that inner assert also failed, `assert_handler()` would be called recursively until the stack overflows. By using raw register writes, the assert handler has zero code dependencies and cannot trigger further asserts.

---

### Lesson 015 -- My Small Test Functions

**File Path:** [15 My Small Test Functions  Embedded System Project Series #15.txt](Artful_Bytes_Transcript/15%20My%20Small%20Test%20Functions%20%20Embedded%20System%20Project%20Series%20%2315.txt)

**Objective:** Improves the handling of ad-hoc test/scratch functions by moving them from `main.c` into a dedicated `test.c` file and making individual test functions selectable via a Makefile argument, eliminating the need to manually comment/uncomment code. Also adds a CI step that builds all test functions automatically.

**Terminology & Key Concepts:**
- **Test Functions (Scratch Functions)**: Quick, disposable functions written during development to verify isolated parts of the code; not formal unit tests but serve a similar purpose in bare-metal projects
- **Build-Time Test Selection**: Passing a test function name as a Makefile argument (`TEST=test_blink_led`) that gets defined as a preprocessor macro, allowing the test file's `main()` to call the correct function
- **`SUPPRESS_UNUSED` Attribute**: GCC's `__attribute__((unused))` applied to test functions to suppress "unused function" warnings, since only one test function is active per build
- **CI Test Matrix**: A build script that automatically discovers and compiles every test function, ensuring they all remain compilable as the codebase evolves

**Techniques & Methods:**
- **Separate Test Main**: The `test.c` file contains its own `main()` function; the Makefile switches between `src/main.c` (normal build) and `src/test/test.c` (test build) based on whether the `TEST` argument is provided
- **Preprocessor-Based Function Selection**: The `TEST` argument becomes a `-DTEST=test_blink_led` define, and inside `test.c` the macro `TEST()` expands to the function name, calling it at runtime
- **Forced Recompilation**: The Makefile uses `$(shell touch src/test/test.c)` to force `test.c` to recompile every time, since changing only the `TEST` define does not modify any source file and `make` would skip the rebuild
- **Regex-Based Test Discovery**: The `build_tests.sh` script uses `grep` with regex to extract all function names matching `void test_*` from `test.c`, then loops through them to build each one for both hardware targets
- **Test Function Naming Convention**: All test functions must be prefixed with `test_`; the Makefile validates this and errors if a non-conforming name is passed

**Source Code Mapping:**
- `test.c` main function: `test.c:464` -- Uses the `TEST()` macro to call whichever test function was selected at build time
  ```c
  int main()
  {
      TEST();
      ASSERT(0); // Should never return from test
  }
  ```
- `test_blink_led()`: `test.c:35` -- Example test function using the LED driver
- `test_setup()`: `test.c:22` -- Common initialization called by all test functions (calls `mcu_init()`)
- `SUPPRESS_UNUSED`: `defines.h:5` -- `__attribute__((unused))` prevents warnings on inactive test functions
  ```c
  #define SUPPRESS_UNUSED __attribute__((unused))
  ```
- Makefile test selection: `Makefile:17-23` -- Validates and passes the TEST argument as a compiler define
  ```makefile
  ifneq ($(TEST),)
  ifeq ($(findstring test_,$(TEST)),)
  $(error "TEST=$(TEST) is invalid (test function must start with test_)")
  else
  TARGET_NAME=$(TEST)
  endif
  endif
  ```
- Makefile main file switch: `Makefile:86-92` -- Selects test.c or main.c as the main file
  ```makefile
  ifndef TEST
  MAIN_FILE = src/main.c
  else
  MAIN_FILE = src/test/test.c
  $(shell touch src/test/test.c)
  endif
  ```

**Demo / Example:**
- **Goal:** Build and run individual test functions from the command line without editing source code
- **Why Important:** Eliminates manual commenting/uncommenting of test functions in main.c, reducing friction during development and preventing accidental code breakage
- **Demo Flow:**
  1. Run `make HW=LAUNCHPAD TEST=test_blink_led` -- builds binary named `test_blink_led` under `build/launchpad/bin/`
  2. Run `make HW=LAUNCHPAD TEST=test_io_pins_output` -- builds a different binary under the same directory
  3. Run `make HW=LAUNCHPAD TEST=nonexistent` -- Makefile errors because name does not start with `test_`
  4. Run `tools/build_tests.sh` -- discovers all test functions via regex and builds each for both targets
  5. Verify CI passes with the new `tests` step in GitHub Actions
- **What Changed:**
  - `test.c`: Created under `src/test/` with all test functions moved from `main.c`, own `main()` using `TEST()` macro
  - `main.c`: Cleaned up, test functions removed
  - `Makefile`: Added `TEST` argument handling, main file switching, forced recompile, test binary naming
  - `tools/build_tests.sh`: Created bash script that discovers and builds all test functions
  - `.github/workflows/ci.yml`: Added step to run `build_tests.sh`

**Discussion Prompts:**
- **Q1: Why use this approach instead of a proper unit testing framework?**
  - The author explicitly chose not to write formal unit tests for this project. These test functions are "scratch functions" -- quick validation that a specific driver or feature works on real hardware. They require physical interaction (pressing buttons, connecting logic analyzers) and cannot be automated in the traditional unit test sense. The Makefile-based selection is a pragmatic middle ground for a small embedded project.
- **Q2: Why force-touch test.c on every build instead of making make aware of the TEST define change?**
  - Make tracks file modification timestamps, not compiler flags. If only the `TEST=` argument changes but no source file is modified, make will reuse the old object file, linking the wrong test function. Touching `test.c` forces it to recompile, ensuring the new `TEST` define takes effect. This is an acknowledged workaround for a make limitation.

---

### Lesson 016 -- How Microcontroller Memory Works

**File Path:** [16 How Microcontroller Memory Works  Embedded System Project Series #16.txt](Artful_Bytes_Transcript/16%20How%20Microcontroller%20Memory%20Works%20%20Embedded%20System%20Project%20Series%20%2316.txt)

**Objective:** Explains the memory architecture of a microcontroller (Flash vs RAM), how different types of C variables map to different memory sections (.text, .data, .bss, .const, stack), and demonstrates tools (`msp430-elf-size`, `msp430-elf-readelf`) for analyzing flash and RAM usage -- a critical skill for resource-constrained embedded development.

**Terminology & Key Concepts:**
- **Flash Memory (Non-Volatile)**: Persistent storage that retains data after power-off; holds program code (.text) and constant data (.const). MSP430G2553 has 16 KB.
- **RAM (Volatile)**: Working memory that loses contents on power-off; holds global variables (.data, .bss) and the stack. MSP430G2553 has only 512 bytes.
- **EEPROM**: A smaller non-volatile memory for storing configuration data; not covered in depth here
- **Linker Script**: A file that tells the linker where each memory section starts, its size, and which sections map to Flash vs RAM
- **Startup Code (C Runtime Init / `__c_int00`)**: Code that runs before `main()` to initialize .data (copy from Flash to RAM), zero-fill .bss, and set the stack pointer
- **Stack Overflow**: When the stack grows large enough to collide with .data/.bss sections in RAM, corrupting variables

| Memory Section | Location | Contents | When Initialized |
|---|---|---|---|
| `.text` | Flash | Machine code (CPU instructions) | At flash programming time |
| `.const` / `.rodata` | Flash | Constant data, string literals, initial values for .data | At flash programming time |
| `.data` | RAM (+ copy in Flash) | Initialized global/static variables | By startup code before `main()` |
| `.bss` | RAM | Uninitialized (zero-initialized) global/static variables | By startup code before `main()` |
| Stack | RAM (grows downward) | Local variables, function call context, return addresses | At runtime as functions are called |

**Techniques & Methods:**
- **IDE Memory Browser**: Using CCS (Code Composer Studio) memory browser to inspect raw memory contents at any address, verifying where variables actually reside
- **Map File Analysis**: Reading the linker-generated `.map` file to find the start address and size of each memory section
- **`msp430-elf-size` Command**: Quickly reports .text, .data, and .bss sizes for the compiled binary, added as a Makefile rule
- **`msp430-elf-readelf -s` (Symbols)**: Lists every symbol (function, variable) with its size, sorted to identify the largest flash consumers
- **Compiler Optimization Awareness**: The compiler may store local variables in registers instead of on the stack; `volatile` forces stack allocation for demonstration
- **Avoiding Flash-Heavy Operations**: Float multiplication added ~300 bytes (no FPU on MSP430); `printf()` from stdlib added thousands of bytes; modulo and division operators also drag in large library code

**Source Code Mapping:**
- `BUSY_WAIT_ms()`: `defines.h:17` -- Added in a previous lesson, uses `__delay_cycles()` with 16 MHz cycle calculation
- Makefile `size` rule: `Makefile:166` -- Runs `msp430-elf-size` on the target binary
  ```makefile
  size: $(TARGET)
  	@$(SIZE) $(TARGET)
  ```
- Makefile `symbols` rule: `Makefile:169` -- Runs `msp430-elf-readelf -s` sorted by size to find largest symbols
  ```makefile
  symbols: $(TARGET)
  	@$(READELF) -s $(TARGET) | sort -n -k3
  ```

**Demo / Example:**
- **Goal:** Demonstrate where different C variable types end up in microcontroller memory and how to measure flash/RAM usage
- **Why Important:** Understanding memory layout is essential for avoiding out-of-memory situations on MCUs with 16 KB flash and 512 bytes RAM
- **Demo Flow:**
  1. Create five test variables: initialized global (`.data`), const global (`.const`), uninitialized global (`.bss`), local initialized (stack + `.const`), static initialized (`.data` + `.const`)
  2. Compile and run in CCS debugger; use Memory Browser to locate each variable
  3. Cross-reference addresses with the `.map` file to confirm section placement
  4. Step through code to watch startup code initialize `.data` and `.bss` before `main()`
  5. Demonstrate that removing `-fshort-enums` increases flash by ~100 bytes
  6. Show that adding float multiplication increases flash by ~300 bytes (no FPU)
  7. Show that adding `printf()` from stdlib increases flash by thousands of bytes
- **What Changed:**
  - `Makefile`: Added `size`, `symbols`, and `addr2line` rules for memory analysis
  - No permanent source code changes (demo used standalone blink examples in CCS)

**New Tools Introduced:**
- `msp430-elf-size` -- Reports .text, .data, .bss section sizes of the compiled ELF binary
- `msp430-elf-readelf` -- Lists symbols and their sizes for identifying the largest flash consumers
- CCS Memory Browser -- Inspects raw memory contents at arbitrary addresses during debug sessions

**Discussion Prompts:**
- **Q1: Why does the MSP430 have so much more Flash (16 KB) than RAM (512 bytes)?**
  - Flash stores the program code, which tends to be larger than the working data. Most embedded applications use relatively few global variables and keep function stacks shallow, but even a simple application requires thousands of bytes of machine instructions. This ratio (16:0.5 KB or 32:1) is typical for small microcontrollers.
- **Q2: What advice does the author give about choosing MCU memory size?**
  - Pick a microcontroller with more memory than you think you need, especially for hobby projects. The author admits that by the end of this project, the 16 KB flash was completely filled and he had to spend significant time optimizing code size. Doubling the flash would have saved hours of work. In production where unit cost matters, memory is chosen more carefully.

---

### Lesson 017 -- Microcontroller Interrupts

**File Path:** [17 Microcontroller Interrupts  Embedded System Project Series #17.txt](Artful_Bytes_Transcript/17%20Microcontroller%20Interrupts%20%20Embedded%20System%20Project%20Series%20%2317.txt)

**Objective:** Explains the fundamentals of interrupts on microcontrollers, demonstrates a ChatGPT-generated interrupt example for the MSP430, and implements a clean interrupt registration system in the IO driver that uses function pointers to decouple interrupt handlers from the port ISR, making it easy to add new interrupts in future drivers.

**Terminology & Key Concepts:**
- **Interrupt**: A hardware mechanism that pauses the CPU's current execution to run a special function (ISR) in response to an event, then returns to the original code
- **Interrupt Service Routine (ISR)**: The function that executes when an interrupt fires; should be kept short and fast to minimize disruption to main code
- **Interrupt Vector Table**: A table in memory mapping each interrupt source to its corresponding ISR address; defined in the linker script
- **Polling vs. Interrupts**: Polling continuously checks a condition in a loop (wastes CPU cycles); interrupts notify the CPU only when the event occurs (efficient but adds complexity)
- **Edge-Triggered Interrupt**: An interrupt that fires on a signal transition (rising edge: low-to-high, or falling edge: high-to-low)
- **Interrupt Flag (IFG)**: A register bit that gets set when an interrupt condition occurs; must be manually cleared in software on MSP430
- **Nested Interrupts**: When an interrupt fires during another ISR; on MSP430, interrupts are disabled during ISR execution by default (not nested)
- **`volatile` Keyword**: Required for variables shared between ISRs and main code to prevent the compiler from caching the value in a register

**Techniques & Methods:**
- **ChatGPT Code Generation**: The author uses ChatGPT to generate a basic MSP430 interrupt example (button toggles LED), demonstrating that LLMs can produce working embedded code with minor corrections
- **INTERRUPT_FUNCTION Macro**: Wrapping `__attribute__((interrupt(vector)))` in a readable macro (`INTERRUPT_FUNCTION`) defined in `defines.h`
  ```c
  #define INTERRUPT_FUNCTION(vector) void __attribute__((interrupt(vector)))
  ```
- **Function Pointer ISR Registration**: Storing ISR function pointers in a 2D array indexed by `[port][pin]`, allowing drivers to register their own ISR without modifying the port interrupt handler
- **Generic Port ISR with Loop**: The port ISR iterates over all 8 pins, checks each interrupt flag, and calls the registered function pointer if one exists -- a clean, extensible pattern
- **Interrupt Enable/Disable for Critical Sections**: Disabling interrupts (via register write or `_disable_interrupts()`) when accessing shared data structures to prevent race conditions

**Source Code Mapping:**
- `io_configure_interrupt()`: `io.c:353` -- Sets edge trigger, registers ISR function pointer, and configures the interrupt in one call
  ```c
  void io_configure_interrupt(io_e io, io_trigger_e trigger, isr_function isr)
  {
      io_set_interrupt_trigger(io, trigger);
      io_register_isr(io, isr);
  }
  ```
- `io_register_isr()`: `io.c:345` -- Stores a function pointer in the `isr_functions[port][pin]` array with an assert to prevent double-registration
- `isr_port_1()` / `isr_port_2()`: `io.c:396-408` -- Port ISR handlers that loop over all pins and dispatch to registered function pointers
  ```c
  INTERRUPT_FUNCTION(PORT1_VECTOR) isr_port_1(void)
  {
      for (io_generic_e io = IO_10; io <= IO_17; io++) {
          io_isr(io);
      }
  }
  ```
- `io_isr()`: `io.c:382` -- Checks the interrupt flag for a specific pin, calls the registered ISR if present, then clears the flag
- `io_set_interrupt_trigger()`: `io.c:327` -- Configures rising or falling edge trigger via PxIES register; disables interrupt first to prevent spurious triggers during configuration
- `io_enable_interrupt()` / `io_disable_interrupt()`: `io.c:372-380` -- Writes to PxIE register to enable or disable interrupt on a specific pin
- `io_deconfigure_interrupt()`: `io.c:366` -- Unregisters ISR and disables interrupt
- `isr_functions[][]`: `io.c:80` -- 2D array of function pointers for all interrupt-capable ports/pins, initialized to NULL

**Demo / Example:**
- **Goal:** Demonstrate interrupt-driven GPIO handling with two buttons controlling an LED
- **Why Important:** Interrupts are fundamental to embedded systems -- nearly every driver in the project (UART, IR remote, timer) depends on them
- **Demo Flow:**
  1. ChatGPT generates an MSP430 button interrupt example; author verifies it works with minor fixes
  2. In the project code, create a `test_io_interrupt` function that registers ISRs on two GPIO pins
  3. Pin IO_11 falling edge turns LED ON; pin IO_20 falling edge turns LED OFF
  4. Pull each pin low with a wire to trigger the interrupt and observe LED behavior
- **What Changed:**
  - `io.c`: Added interrupt-related register arrays, `isr_functions[][]` function pointer table, `io_configure_interrupt()`, `io_enable_interrupt()`, `io_disable_interrupt()`, port ISR handlers
  - `io.h`: Added `isr_function` typedef, `io_trigger_e` enum, interrupt function prototypes
  - `defines.h`: Added `INTERRUPT_FUNCTION` macro
  - `test.c`: Added `test_io_interrupt()` function
- **Related Code:**
  ```c
  // test.c -- test function demonstrating interrupt registration
  static void io_11_isr(void) { led_set(LED_TEST, LED_STATE_ON); }
  static void io_20_isr(void) { led_set(LED_TEST, LED_STATE_OFF); }
  static void test_io_interrupt(void)
  {
      test_setup();
      io_configure_interrupt(IO_11, IO_TRIGGER_FALLING, io_11_isr);
      io_configure_interrupt(IO_20, IO_TRIGGER_FALLING, io_20_isr);
      io_enable_interrupt(IO_11);
      io_enable_interrupt(IO_20);
      while(1);
  }
  ```

**Discussion Prompts:**
- **Q1: Why use function pointers for ISR registration instead of hardcoding the handler in the port ISR?**
  - Function pointers decouple the IO driver from the higher-level drivers. The IR remote, UART, and other drivers can register their own ISRs without modifying `io.c`. This makes the code modular and extensible -- adding a new interrupt-driven feature only requires calling `io_configure_interrupt()` from the new driver's init function.
- **Q2: Why must the interrupt flag be manually cleared in software on the MSP430?**
  - Unlike some microcontrollers that auto-clear flags on ISR entry, the MSP430 requires explicit clearing of PxIFG bits. If the flag is not cleared, the ISR will fire again immediately after returning, creating an infinite loop. The author clears it after calling the registered handler to avoid accidentally clearing a flag set by a new event during handler execution.

---

### Lesson 018 -- Write a UART Driver (Polling and Interrupt)

**File Path:** [18 Write a UART driver (Polling and Interrupt)  Embedded System Project Series #18.txt](Artful_Bytes_Transcript/18%20Write%20a%20UART%20driver%20%28Polling%20and%20Interrupt%29%20%20Embedded%20System%20Project%20Series%20%2318.txt)

**Objective:** Implements a UART driver for the MSP430 in two stages -- first a simple polling-based version, then an efficient interrupt-driven version with a ring buffer -- enabling serial communication between the microcontroller and a desktop terminal. This is a key debug facility for the rest of the project.

**Terminology & Key Concepts:**
- **UART (Universal Asynchronous Receiver/Transmitter)**: A serial communication protocol transmitting data one bit at a time with start/stop framing but no clock signal; widely used for MCU-to-PC debug communication
- **Baud Rate**: The number of signal transitions per second; set to 115200 in this project. Both transmitter and receiver must agree on the same rate.
- **Polling-Based TX**: Writing a byte to the TX buffer register, then busy-waiting (polling a flag) until the hardware finishes transmitting before sending the next byte. Simple but blocks the CPU.
- **Interrupt-Driven TX**: Loading a byte into the TX buffer and returning immediately; when the hardware finishes, it triggers an interrupt that loads the next byte from a ring buffer. CPU is free between bytes.
- **Ring Buffer (Circular Buffer / FIFO)**: A fixed-size array with head and tail pointers that wraps around, providing O(1) put/get operations without dynamic allocation
- **USCI (Universal Serial Communication Interface)**: MSP430's peripheral that can be configured for UART, SPI, or I2C mode
- **USB-to-UART Bridge**: An external board that converts UART signals to USB so the microcontroller can communicate with a PC's terminal emulator

| UART Config Parameter | Value | Register |
|---|---|---|
| Data bits | 8 | UCA0CTL0 (default) |
| Stop bits | 1 | UCA0CTL0 (default) |
| Parity | None | UCA0CTL0 (default) |
| Baud rate | 115200 | UCA0BR0, UCA0BR1, UCA0MCTL |
| Clock source | SMCLK (16 MHz) | UCA0CTL1 |
| Mode | Low-Frequency Baud Rate | UCA0MCTL |

**Techniques & Methods:**
- **Module Reset During Config**: Setting UCSWRST before configuring UART registers and clearing it after, as required by the MSP430 family user guide
- **Baud Rate Calculation with Defines**: Using preprocessor math to compute the integer and fractional parts of the clock divisor, with `static_assert` guards to validate the values fit in their registers
- **Critical Section in `_putchar()`**: Disabling the TX interrupt while modifying the ring buffer, then re-enabling it -- ensures the ISR does not read the buffer in an inconsistent state
- **Ring Buffer as Macro**: `STATIC_RING_BUFFER(tx_buffer, 16, uint8_t)` instantiates a statically-allocated ring buffer using a macro that generates the buffer array and struct
- **Carriage Return Handling**: Prepending `\r` before `\n` because some terminals (especially Windows) require `\r\n` for proper newline display
- **Separate Assert-Safe UART Functions**: `uart_init_assert()` and `uart_trace_assert()` use polling instead of interrupts, suitable for use inside the assert handler where interrupts may be unreliable

**Source Code Mapping:**
- `uart_init()`: `uart.c:102` -- Asserts not already initialized, calls `uart_configure()`, clears and enables TX interrupt
- `uart_configure()`: `uart.c:76` -- Sets USCI module into reset, configures clock source, baud rate divisor, modulation, then releases reset
  ```c
  static void uart_configure(void)
  {
      UCA0CTL1 &= UCSWRST;          // Hold in reset
      UCA0CTL0 = 0;                  // 8N1 default
      UCA0CTL1 |= UCSSEL_2;         // SMCLK
      UCA0BR0 = UART_DIVISOR_INT_LOW_BYTE;
      UCA0BR1 = UART_DIVISOR_INT_HIGH_BYTE;
      UCA0MCTL = (UART_UCBRF << 4) + (UART_UCBRS << 1) + UART_UC0S16;
      UCA0CTL1 &= ~UCSWRST;         // Release from reset
  }
  ```
- `_putchar()`: `uart.c:113` -- The function called by the external printf library; handles `\r\n`, polls if ring buffer full, adds character to buffer, starts TX if idle
  ```c
  void _putchar(char c)
  {
      if (c == '\n') { _putchar('\r'); }
      while (ring_buffer_full(&tx_buffer)) { }
      uart_tx_disable_interrupt();
      const bool tx_ongoing = !ring_buffer_empty(&tx_buffer);
      ring_buffer_put(&tx_buffer, &c);
      if (!tx_ongoing) { uart_tx_start(); }
      uart_tx_enable_interrupt();
  }
  ```
- `isr_uart_tx()`: `uart.c:61` -- TX complete ISR: removes transmitted byte from ring buffer, clears interrupt flag, starts next byte if buffer not empty
- `uart_tx_start()`: `uart.c:52` -- Peeks at the oldest byte in the ring buffer and writes it to `UCA0TXBUF` to initiate transmission
- `uart_init_assert()`: `uart.c:132` -- Assert-safe UART init that disables interrupts and reconfigures UART for polling mode
- `uart_trace_assert()`: `uart.c:147` -- Loops through a string and sends each character using polling (`uart_putchar_polling`)
- Ring buffer: `ring_buffer.c` / `ring_buffer.h` -- Generic circular buffer with `put`, `get`, `peek_tail`, `peek_head`, `count`, `empty`, `full` operations
  ```c
  // Macro to instantiate a static ring buffer
  #define STATIC_RING_BUFFER(name, size, type) RING_BUFFER(name, size, type, static)
  ```
- Baud rate calculation: `uart.c:22-35` -- Preprocessor defines compute divisor from SMCLK/baud_rate with static_assert validation

**Demo / Example:**
- **Goal:** Send characters from the MSP430 to a PC terminal via UART, first by polling, then by interrupt
- **Why Important:** UART tracing is the primary debugging mechanism for the rest of the project, equivalent to `printf` debugging on desktop systems
- **Demo Flow:**
  1. Connect MSP430 TX/RX pins to USB-to-UART bridge, connect bridge to PC
  2. **Stage 1 (Polling)**: Implement `uart_putchar_polling()` -- write byte to `UCA0TXBUF`, poll `UCA0TXIFG` until complete. Test by sending "ARTFUL" character-by-character; characters appear on terminal.
  3. **Stage 2 (Interrupt)**: Replace polling with ring buffer + interrupt. `_putchar()` adds to buffer and kicks off TX. ISR handles subsequent bytes. Same test, but CPU is now free between characters.
  4. Open `picocom` terminal at 115200 baud to view output
- **What Changed:**
  - `uart.c` / `uart.h`: Created with full UART driver -- polling and interrupt-driven TX, ring buffer integration, assert-safe functions
  - `ring_buffer.c` / `ring_buffer.h`: Created as a generic circular buffer (reused by IR remote driver later)
  - `test.c`: Added `test_uart()` function
  - `Makefile`: Added `terminal` rule for opening picocom

**Discussion Prompts:**
- **Q1: Why implement both polling and interrupt-driven versions?**
  - The polling version is simpler to understand and useful in the assert handler where interrupts may be disabled or unreliable. The interrupt-driven version is used for normal operation because it frees the CPU to do other work while bytes are being transmitted, which is essential for a robot that must simultaneously process sensors and control motors.
- **Q2: Why use a ring buffer instead of a simple array for the TX buffer?**
  - A ring buffer provides FIFO (first-in, first-out) behavior with O(1) put and get operations and fixed memory usage. It handles the producer-consumer pattern between `_putchar()` (producer, called from main code) and the TX ISR (consumer, called from interrupt context). A simple array would require shifting elements or tracking multiple indices, which is less efficient and more error-prone.

---

### Lesson 019 -- Printf on a Microcontroller

**File Path:** [19 Printf on a Microcontroller  Embedded System Project Series #19.txt](Artful_Bytes_Transcript/19%20Printf%20on%20a%20Microcontroller%20%20Embedded%20System%20Project%20Series%20%2319.txt)

**Objective:** Integrates an external lightweight printf implementation (mpaland/printf) into the project to enable formatted string output over UART, creates a `trace` module that prefixes every log with file name and line number, and adds a UART-based trace to the assert handler using the program counter and `addr2line` to locate the failing assert.

**Terminology & Key Concepts:**
- **Lightweight Printf**: A minimal printf implementation designed for embedded systems that is tiny and configurable, unlike the standard library printf which can consume thousands of bytes of flash
- **`_putchar()` Hook**: The single function that the external printf library requires the user to implement; each character output by printf is passed through this function, which sends it over UART
- **Trace Module**: A wrapper around printf that automatically prepends the source file name and line number using `__FILE__` and `__LINE__` preprocessor macros
- **`snprintf()`**: A printf variant that writes to a string buffer instead of a character output function, used in the assert handler to format the PC value
- **`addr2line`**: A toolchain utility that converts a program counter address to a source file name and line number using debug symbols
- **Variadic Function**: A function that accepts a variable number of arguments (like printf); implemented using `va_list`, `va_start`, `va_end`
- **Git Submodule**: An external Git repository embedded within the main repository; the printf library was added as a submodule under `external/printf/`

**Techniques & Methods:**
- **Printf Configuration Header**: Creating `external/printf_config.h` to disable unused formatting options (float, exponential, etc.), reducing flash usage
- **`TRACE()` Macro**: Wraps `trace()` with `__FILE__` and `__LINE__` automatically appended, plus a newline
  ```c
  #define TRACE(fmt, ...) trace("%s:%d: " fmt "\n", __FILE__, __LINE__, ##__VA_ARGS__)
  ```
- **Compile-Time Trace Disable**: The `DISABLE_TRACE` define replaces `trace_init()` and `trace()` with no-ops, saving flash when traces are not needed
- **Assert Trace via Program Counter**: Instead of passing `__FILE__` and `__LINE__` (which would waste flash per-assert), the assert handler captures the PC register and uses `snprintf()` to format it as a hex string; the developer then runs `make addr2line ADDR=0xXXXX` to get the exact source location
- **Isolated Assert UART**: The assert handler uses `uart_init_assert()` (disables interrupts, re-configures UART) and `uart_trace_assert()` (polling-based character send) to avoid depending on the interrupt-driven UART path that might itself have asserts
- **Makefile Filter for External Files**: Using `filter-out` to exclude `external/printf/printf.c` and `.h` from `clang-format` and `cppcheck` rules

**Source Code Mapping:**
- `TRACE()` macro: `trace.h:4` -- Wraps `trace()` with file/line prefix
  ```c
  #define TRACE(fmt, ...) trace("%s:%d: " fmt "\n", __FILE__, __LINE__, ##__VA_ARGS__)
  ```
- `trace_init()`: `trace.c:9` -- Asserts not double-initialized, calls `uart_init()`
- `trace()`: `trace.c:16` -- Variadic wrapper that calls `vprintf()` from the external printf library
  ```c
  void trace(const char *format, ...)
  {
      ASSERT(initialized);
      va_list args;
      va_start(args, format);
      vprintf(format, args);
      va_end(args);
  }
  ```
- `_putchar()`: `uart.c:113` -- The hook function that the external printf library calls for each character; routes to the interrupt-driven UART TX
- `assert_trace()`: `assert_handler.c:25` -- Configures UART TX pin, calls `uart_init_assert()`, formats PC as hex string via `snprintf()`, sends via `uart_trace_assert()`
  ```c
  static void assert_trace(uint16_t program_counter)
  {
      P1SEL |= BIT2;
      P1SEL2 |= BIT2;
      uart_init_assert();
      char assert_string[ASSERT_STRING_MAX_SIZE];
      snprintf(assert_string, sizeof(assert_string), "ASSERT 0x%x\n", program_counter);
      uart_trace_assert(assert_string);
  }
  ```
- `addr2line` Makefile rule: `Makefile:173` -- Maps a program counter value back to source file and line number
  ```makefile
  addr2line: $(TARGET)
  	@$(ADDR2LINE) -e $(TARGET) $(ADDR)
  ```
- Trace disable: `trace.h:9-12` -- When `DISABLE_TRACE` is defined, replaces functions with empty macros
- Printf config: `external/printf_config.h` -- Disables float, exponential, and other unused format specifiers to save flash

**Demo / Example:**
- **Goal:** Print formatted strings from the microcontroller to a PC terminal, and add trace output to the assert handler
- **Why Important:** Completes the debug facility trifecta (LED blink, breakpoint, serial trace) that will be used throughout the rest of development
- **Demo Flow:**
  1. Include external printf library, implement `_putchar()` to call UART, test with `test_uart()` function sending "ARTFUL"
  2. Create `test_trace()` function using `TRACE("Artful bytes %d", 2023)` -- terminal shows file, line, and formatted message
  3. Trigger `test_assert()` -- terminal shows "ASSERT 0xC0DE" (example PC value)
  4. Run `make addr2line ADDR=0xC0DE HW=LAUNCHPAD TEST=test_assert` -- output shows `test.c:20`, identifying the exact assert location
- **What Changed:**
  - `trace.c` / `trace.h`: Created with `trace_init()`, `trace()` function, `TRACE()` macro, `DISABLE_TRACE` support
  - `assert_handler.c`: Added `assert_trace()` using `snprintf()` and polling UART
  - `uart.c`: Added `uart_init_assert()` and `uart_trace_assert()` for assert-safe serial output; renamed `uart_putchar()` to `_putchar()` for printf library compatibility
  - `Makefile`: Added printf config define, external/printf source, `addr2line` rule, filter-out for external files
  - `.github/workflows/ci.yml`: Added `with: submodules: true` to clone the printf git submodule

**New Tools Introduced:**
- `msp430-elf-addr2line` -- Converts program counter hex value to source file and line number using debug symbols
- `picocom` -- Terminal emulator for viewing UART output at 115200 baud

**Discussion Prompts:**
- **Q1: Why use an external printf instead of implementing a custom one or using the standard library?**
  - The standard library printf is too large (thousands of bytes) for a 16 KB MCU. Writing a custom printf is tedious and error-prone. The external library (mpaland/printf) is specifically designed for embedded systems -- tiny, configurable, and well-tested. It only requires implementing `_putchar()`, making integration trivial.
- **Q2: Why trace the program counter in the assert handler instead of the file name and line number directly?**
  - Embedding `__FILE__` and `__LINE__` as string literals in every assert would consume significant flash space because each unique file path is stored as a constant string. By instead capturing the 2-byte program counter and using `addr2line` offline, the assert handler uses the same amount of flash regardless of how many asserts exist in the code. The trade-off is an extra manual step to resolve the address.

---

### Lesson 020 -- NEC Protocol Driver (Infrared Remote)

**File Path:** [20 NEC Protocol Driver (Infrared remote)  Embedded System Project Series #20.txt](Artful_Bytes_Transcript/20%20NEC%20Protocol%20Driver%20%28Infrared%20remote%29%20%20Embedded%20System%20Project%20Series%20%2320.txt)

**Objective:** Implements a driver to decode NEC infrared protocol signals from a remote control, using GPIO interrupts (falling edge) and the Timer A1 peripheral to measure pulse timing. This enables remote control of the robot during development and provides the start signal required by competition rules.

**Terminology & Key Concepts:**
- **NEC Protocol**: One of the most common infrared communication protocols; encodes a 32-bit message (8-bit address + inverse + 8-bit command + inverse) using pulse-distance modulation
- **Pulse-Distance Modulation**: Encoding bit values by varying the time between signal transitions -- a logical '1' has a longer gap (~2.25 ms) than a '0' (~1.12 ms) between falling edges
- **IR Receiver (Demodulator)**: An integrated component that receives the modulated IR signal, demodulates it, and outputs a clean digital signal on a GPIO pin
- **Timer Peripheral (Timer A1)**: A hardware counter configured to generate periodic interrupts (every 1 ms), used as a timebase to measure the duration between IR pulses
- **Repeat Code**: When a button is held down, the NEC protocol sends the full message once, then sends shorter repeat codes every 108 ms to indicate continued press
- **Union for Bit Reinterpretation**: A C `union` that allows the same memory to be interpreted as either a 32-bit raw integer (for bit shifting during decode) or a struct with individual 8-bit fields (for extracting the command)

| NEC Protocol Timing | Falling Edge Gap | Meaning |
|---|---|---|
| 9 ms low + 4.5 ms high | Pulse 1-2 | Start of transmission |
| ~1.12 ms | Pulse 3-34 (gap < 2 ms) | Bit value = 0 |
| ~2.25 ms | Pulse 3-34 (gap >= 2 ms) | Bit value = 1 |
| 108 ms interval | Pulse 35+ | Repeat code (button held) |

| IR Command | Hex Value | Button |
|---|---|---|
| IR_CMD_1 | 0xA2 | 1 |
| IR_CMD_2 | 0x62 | 2 |
| IR_CMD_UP | 0x18 | Up arrow |
| IR_CMD_DOWN | 0x4A | Down arrow |
| IR_CMD_OK | 0x38 | OK |
| IR_CMD_NONE | 0xFF | No command received |

**Techniques & Methods:**
- **Falling-Edge-Only Decoding**: Instead of tracking both rising and falling edges with a complex state machine, the simplified approach only triggers on falling edges and measures the time between them. This reduces code size and complexity.
- **Timer A1 as Millisecond Counter**: Configured with SMCLK (16 MHz) / prescaler (8) = 2 MHz tick rate; CCR0 set to 2000 ticks = 1 ms interrupt period. A `timer_ms` variable is incremented each interrupt.
- **Timer Start/Stop for Power Efficiency**: The timer is started when the first IR pulse arrives and stopped after decoding is complete or after a 150 ms timeout, avoiding continuous timer interrupts when no signal is present
- **Pulse Validity Checking**: `is_valid_pulse()` sanity-checks the timing of each pulse to detect transmission errors or unexpected new transmissions mid-decode
- **Union-Based Message Parsing**: The `ir_message` union allows building the 32-bit message by shifting bits into the `raw` field, then reading the `decoded.cmd` field to extract the 8-bit command
- **Ring Buffer for Command Queue**: Decoded commands are stored in a ring buffer, allowing multiple button presses to be queued and consumed by the application at its own pace
- **Critical Section for Shared Data**: `ir_remote_get_cmd()` disables the IO interrupt while reading from the ring buffer to prevent corruption from concurrent ISR writes
- **`IS_ODD()` Macro for Repeat Detection**: Uses `x & 1` instead of `x % 2` to check if a pulse count is odd, avoiding the expensive modulo operation on MSP430

**Source Code Mapping:**
- `ir_remote_init()`: `ir_remote.c:141` -- Registers the pulse ISR on the IR_REMOTE pin (falling edge), enables interrupt, initializes timer
  ```c
  void ir_remote_init(void)
  {
      io_configure_interrupt(IO_IR_REMOTE, IO_TRIGGER_RISING, isr_pulse);
      io_enable_interrupt(IO_IR_REMOTE);
      ir_timer_init();
  }
  ```
- `ir_timer_init()`: `ir_remote.c:37` -- Configures Timer A1 with SMCLK + divider 8, sets CCR0 for 1 ms interrupt, enables CCIE
  ```c
  static void ir_timer_init(void)
  {
      TA1CTL = TASSEL_2 + ID_3;
      TA1CCR0 = TIMER_INTERRUPT_TICKS;
      TA1CCTL0 = CCIE;
  }
  ```
- `ir_timer_start()` / `ir_timer_stop()`: `ir_remote.c:47-58` -- Start/stop timer by writing MC_1 or MC_0 to TA1CTL, clearing counter on start
- `isr_pulse()`: `ir_remote.c:92` -- Main decoding logic: stops timer, increments pulse count, validates timing, shifts bits for bit-pulses, stores message on pulse 34 or odd repeat pulses, restarts timer
  ```c
  static void isr_pulse(void)
  {
      ir_timer_stop();
      pulse_count++;
      if (!is_valid_pulse(pulse_count, timer_ms)) {
          pulse_count = 1;
          ir_message.raw = 0;
      } else if (is_bit_pulse(pulse_count)) {
          ir_message.raw <<= 1;
          ir_message.raw += (timer_ms >= 2) ? 1 : 0;
      }
      if (is_message_pulse(pulse_count)) {
          ring_buffer_put(&ir_cmd_buffer, &ir_message.decoded.cmd);
      }
      ir_timer_start();
  }
  ```
- `isr_timer_a0()`: `ir_remote.c:113` -- Timer ISR: increments `timer_ms` each millisecond; on timeout (150 ms), stops timer and resets state
- `is_bit_pulse()`: `ir_remote.c:82` -- Returns true for pulses 3-34 (the 32 data bits)
- `is_message_pulse()`: `ir_remote.c:87` -- Returns true on pulse 34 (initial message) or odd pulses after 36 (repeat codes)
- `is_valid_pulse()`: `ir_remote.c:60` -- Sanity-checks timing for each pulse number to detect errors
- `ir_remote_get_cmd()`: `ir_remote.c:126` -- Disables interrupt, reads from ring buffer, re-enables interrupt, returns command enum
- `ir_message` union: `ir_remote.c:20` -- Dual interpretation of the 32-bit NEC message
  ```c
  static union {
      struct {
          uint8_t cmd_inverted;
          uint8_t cmd;
          uint8_t addr_inverted;
          uint8_t addr;
      } decoded;
      uint32_t raw;
  } ir_message;
  ```
- `ir_cmd_e` enum: `ir_remote.h:6` -- Maps each button's command byte to a named constant (e.g., `IR_CMD_1 = 0xA2`)
- `IS_ODD()`: `defines.h:10` -- Bit-level odd check: `(x & 1)` avoids expensive modulo
- `TIMER_MC_MASK`: `defines.h:24` -- Mask for clearing MC bits in timer control register when starting/stopping

**Demo / Example:**
- **Goal:** Decode IR remote button presses and display the button name on the serial terminal
- **Why Important:** The IR remote enables manual robot control during development (tested in later motor/drive videos) and provides the start signal required by sumo competition rules
- **Demo Flow:**
  1. First implement in isolated CCS project to get the decoding working independently
  2. Connect IR receiver to development board, hook up oscilloscope to inspect raw NEC signal waveform
  3. Press each button and record the command byte values to populate the `ir_cmd_e` enum
  4. Move code to main project, using `io_configure_interrupt()` for clean ISR registration
  5. Create `test_ir_remote()` function that traces button names: `TRACE("Command %s", ir_remote_cmd_to_string(ir_remote_get_cmd()))`
  6. Hold button down to verify repeat code handling works
- **What Changed:**
  - `ir_remote.c` / `ir_remote.h`: Created with full NEC protocol decoder -- timer init, pulse ISR, timing validation, repeat code handling, ring buffer command queue
  - `defines.h`: Added `IS_ODD()`, `TIMER_MC_MASK`, `TIMER_INPUT_DIVIDER_3` defines
  - `test.c`: Added `test_ir_remote()` function
  - `uart.c`: Fixed carriage return / line feed ordering (`\r` before `\n`)
  - `Makefile`: Added ir_remote.c to source list

**Discussion Prompts:**
- **Q1: Why track only falling edges instead of both edges with a state machine?**
  - The author initially implemented a full rising+falling edge state machine but found it required significantly more code (wasting precious flash) and was harder to follow. The falling-edge-only approach works because the NEC protocol's bit values can be distinguished solely by the time between consecutive falling edges (< 2 ms = '0', >= 2 ms = '1'). This insight eliminates half the interrupt triggers and most of the state tracking.
- **Q2: Why use a ring buffer for IR commands instead of a simple variable?**
  - A ring buffer queues multiple commands, preventing lost button presses if the main loop is busy when an IR signal arrives. If the main loop processes commands slower than they arrive (e.g., during a trace output), the buffer holds up to 10 pending commands. A single variable would overwrite unprocessed commands. The ring buffer also enables mutual exclusion -- `ir_remote_get_cmd()` disables interrupts only briefly while reading, avoiding long critical sections.
- **Q3: How does the timer timeout prevent wasted CPU cycles?**
  - After 150 ms without a falling edge, the timer ISR stops the timer and resets the decoder state. Without this, the timer would continue generating interrupts indefinitely (every 1 ms) even when no IR signal is present, wasting power and CPU time on unnecessary ISR entries. The 150 ms threshold is chosen because the longest expected gap in normal NEC transmission is ~110 ms (between repeat codes).
