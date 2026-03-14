### Section 3: Software Architecture & Project Organization

---

### Lesson 006 --- How to Create a Software Architecture

**File Path:** [Lesson_006_transcript.txt](Artful_Bytes_Transcript/6%20How%20to%20Create%20a%20Software%20Architecture%20%20Embedded%20System%20Project%20Series%20%236.txt)

**Objective:** Presents the software architecture for the nsumo robot as a layered diagram of modules, explains why organizing software matters (readability, maintainability, portability, testability), and introduces key software design principles applied to embedded systems.

**Terminology & Key Concepts:**
- **Software Architecture**: The high-level organization of a software system into modules, their relationships, and the rules governing those relationships. For nsumo, a two-layer architecture: Drivers (hardware-dependent) and Application (hardware-independent).
- **Layered Architecture Pattern**: An architectural style where software is organized into horizontal layers of abstraction, with higher layers depending on lower layers but not vice versa. The most common and suitable pattern for embedded systems.
- **Driver Layer**: The bottom layer containing modules that directly interact with MCU hardware registers. Includes peripheral drivers (UART, I2C, PWM, ADC, IO, millis) and device drivers (VL53L0X, QRE1113, TB6612FNG, IR remote, LED).
- **Application Layer**: The top layer containing hardware-independent logic. Includes the state machine, enemy detection, line detection, drive control, timer, and trace/printf modules. Could theoretically run on any platform.
- **State Machine**: The central decision-making module at the top of the architecture. Takes abstracted sensor input (enemy position, line detection) and produces drive commands. States: WAIT -> SEARCH -> ATTACK -> RETREAT, plus MANUAL.
- **Separation of Concerns**: The principle that each module should encapsulate a single concept or responsibility. E.g., the UART module handles UART peripheral configuration; it should not contain I2C code.
- **Single Responsibility Principle (SRP)**: Each module has one reason to change. The enemy module translates raw sensor data into enemy position; it does not control motors.
- **Encapsulation / Information Hiding**: The driver layer hides hardware details from the application layer. Application modules don't know which registers are being written --- they call abstracted functions like `drive_forward()`.
- **Decoupling**: Minimizing dependencies between modules. The enemy module depends on the range sensor driver but has no connection to the PWM module. This is especially critical in embedded to separate hardware-dependent from hardware-independent code.
- **DRY (Don't Repeat Yourself)**: Putting shared code (like IO pin configuration) in a single common module rather than duplicating it across multiple drivers.
- **Cohesion**: Keeping related code close together. All ADC-related register manipulation lives in the `adc` module, not scattered across sensor modules.
- **Modularity**: Designing so individual modules can be replaced without affecting the rest. E.g., changing the MCU requires rewriting only the driver layer; the application layer remains unchanged.

**Techniques & Methods:**
- **Hardware Block Diagram as Architecture Guide**: Using the physical hardware block diagram as a natural starting point for the software architecture. Each hardware component maps to a software module; hardware interfaces map to module dependencies.
- **Input Simplification Modules**: Creating intermediate modules (enemy, line, drive) between the state machine and raw drivers to translate complex data into simplified representations. E.g., enemy module converts an array of distance integers into "enemy is close-left" or "enemy is far-front."
- **Platform Independence Strategy**: Explicitly separating platform-dependent code (driver layer) from platform-independent code (application layer) to enable: (1) MCU porting, (2) host-computer simulation, (3) unit testing of application logic in isolation.
- **Divide and Conquer Design**: Breaking the overall problem ("make robot find and push enemy while staying in ring") into sub-problems that map to individual modules.
- **Pragmatic Over Theoretical**: The instructor emphasizes striking a balance --- avoiding both "everything in one file" and excessive over-abstraction. The architecture should serve practical goals (easier to read, maintain, test, port) rather than theoretical purity.

**Source Code Mapping:**
- `main()`: `src/main.c:10-23` --- The entry point initializes all modules in dependency order, then runs the state machine.
  ```c
  int main(void)
  {
      mcu_init();        // Driver layer: MCU initialization
      trace_init();      // Common: logging over UART
      drive_init();      // App layer: motor control abstraction
      enemy_init();      // App layer: range sensor abstraction
      line_init();       // App layer: line sensor abstraction
      ir_remote_init();  // Driver: IR receiver setup
      state_machine_run(); // App layer: main control loop
      ASSERT(0);         // Should never reach here
      return 0;
  }
  ```
- Architecture reflected in directory structure (`src/app/`, `src/drivers/`, `src/common/`):
  - `src/app/state_machine.c` --- Top-level decision making (SEARCH, ATTACK, RETREAT states)
  - `src/app/enemy.c` --- Translates VL53L0X distances to enemy position
  - `src/app/line.c` --- Translates QRE1113 ADC values to line detection
  - `src/app/drive.c` --- Translates drive commands to PWM/direction signals
  - `src/drivers/uart.c`, `i2c.c`, `pwm.c`, `adc.c`, `io.c` --- Peripheral drivers
  - `src/drivers/vl53l0x.c`, `qre1113.c`, `tb6612fng.c` --- Device drivers
  - `src/common/defines.h`, `trace.c`, `ring_buffer.c` --- Shared utilities

**Demo / Example:**
- **Goal:** Present and explain the complete software architecture diagram for the nsumo robot.
- **Why Important:** This is the blueprint for all subsequent implementation videos. Understanding the module decomposition and their relationships guides where each piece of code should live and how modules should interact.
- **Demo Flow:**
  1. Why organize software: easier to read, implement, maintain, extend, collaborate, reuse, port, and test.
  2. Present the architecture diagram: modules arranged from low (hardware) to high (application).
  3. Application layer walkthrough: State machine (SEARCH/ATTACK/RETREAT) at top, fed by enemy and line modules, outputting to drive module. Trace/printf for logging. Timer for elapsed time tracking.
  4. Driver layer walkthrough: MCU init, UART, I2C + VL53L0X, ADC + QRE1113, PWM + TB6612FNG, IR remote, LED. IO module at the bottom shared by all drivers.
  5. Millis module: Repurposes the watchdog timer to provide millisecond timestamps (not used as a watchdog in this project).
  6. Dependency arrows: enemy -> VL53L0X -> I2C; line -> QRE1113 -> ADC; drive -> TB6612FNG -> PWM; trace -> printf -> UART.
  7. Discussion of design principles applied: layered architecture, separation of concerns, encapsulation, decoupling, DRY, cohesion, modularity.
  8. Pragmatic advice: don't over-theorize; logical reasoning about the problem naturally leads to many good design principles.

**Discussion Prompts:**
- **Q1: Why is decoupling from hardware the most important architectural concern in embedded?**
  - Hardware-coupled code cannot be tested on a host computer, cannot be ported to a new MCU (critical during chip shortages), and cannot be simulated. By isolating hardware interaction in the driver layer, the application layer becomes portable, testable, and simulatable --- which the instructor later uses when running the application on a 2D simulator.
- **Q2: How does the hardware block diagram guide the software architecture?**
  - Each physical component naturally maps to a software module. The range sensor (VL53L0X) becomes a driver module; the I2C bus it uses becomes another module. The motor driver IC (TB6612FNG) becomes a module that depends on the PWM module. This one-to-one mapping between hardware concepts and software modules is a strength of embedded systems design --- the real world provides a natural decomposition.
- **Q3: What is the role of the "intermediate" application modules (enemy, line, drive)?**
  - They simplify the interface for the state machine. Instead of the state machine dealing with raw distance arrays and ADC values, the enemy module provides "enemy is close-left" and the line module provides "line detected at front-right." This abstraction makes the state machine logic cleaner and more readable.

---

### Lesson 007 --- The BEST Project Structure for C/C++ MCU

**File Path:** [Lesson_007_transcript.txt](Artful_Bytes_Transcript/7%20The%20BEST%20Project%20Structure%20for%20CC++MCU%20%20Embedded%20System%20Project%20Series%20%237.txt)

**Objective:** Creates the physical directory structure for the nsumo project, mapping the software architecture from Lesson 6 into folders and files, and discusses naming conventions, directory best practices, and the role of each top-level file.

**Terminology & Key Concepts:**
- **Pitchfork Layout**: A community-proposed C/C++ project structure that formalizes common patterns observed in professional projects. The nsumo project uses a similar structure. Directories include: `src/`, `external/`, `docs/`, `tools/`, `build/`.
- **Canonical Project Structure**: Another proposed layout from the C++ committee tooling group, focused on packages. Referenced for inspiration but not directly followed.
- **Source Directory (`src/`)**: Contains all source and header files. Subdivided into `app/`, `drivers/`, `common/`, and `test/` to reflect the software architecture layers.
- **External Directory (`external/`)**: Holds third-party code included unchanged. In this project, only the stripped-down printf implementation, included as a git submodule.
- **Docs Directory (`docs/`)**: Contains documentation assets --- hardware block diagram, software architecture diagram, project photos. Most written documentation lives in the README.
- **Tools Directory (`tools/`)**: Holds build scripts, Docker files, and other development utilities.
- **Build Directory (`build/`)**: Generated during compilation, contains object files and the final binary. Excluded from git via `.gitignore`.
- **Git Submodule**: A way to include an external git repository within your own repository at a specific commit. Used for the printf library to track its origin and version.
- **`.clang-format`**: Configuration file for the clang-format auto-formatter. Defines the coding style (indentation, brace placement, column limit) enforced across the project.
- **`.gitignore`**: Lists files and directories that git should not track (e.g., `build/` directory with generated artifacts).

**Techniques & Methods:**
- **Architecture-Driven Directory Structure**: The `src/app/`, `src/drivers/`, `src/common/` subdivision directly mirrors the software architecture layers defined in Lesson 6.
- **Headers and Sources Together**: Keeping `.h` and `.c` files in the same directory (not separating headers into an `include/` directory) for simplicity and reduced navigation overhead. Separate header directories are justified for libraries but not for single-project codebases.
- **Clean Project Lobby**: Keeping the root directory minimal and navigable: `src/`, `external/`, `docs/`, `tools/`, `Makefile`, `README.md`, `LICENSE`, `.clang-format`, `.gitignore`.
- **Main File Visibility**: Placing `main.c` at the `src/` level (not inside `app/` or `drivers/`) makes the project entry point immediately discoverable.
- **Naming Conventions**: All lowercase, no spaces (underscores instead), no capitalization --- optimized for command-line tab completion and cross-platform compatibility.
- **Simplicity Over Perfection**: With only ~20 files, even a flat structure would work. The directories add mild organizational benefit and scratch the "order itch" but are not critical at this scale.

**Source Code Mapping:**
- Project directory structure as implemented:
  ```
  nsumo_video/
  +-- src/
  |   +-- main.c
  |   +-- app/           (state_machine, enemy, line, drive, timer, etc.)
  |   +-- drivers/       (uart, i2c, pwm, adc, io, led, millis, etc.)
  |   +-- common/        (defines.h, assert_handler, trace, ring_buffer, sleep)
  |   +-- test/           (test.c)
  +-- external/
  |   +-- printf/        (lightweight printf, git submodule)
  +-- docs/
  |   +-- coding_guidelines.md
  |   +-- nsumo.jpg, sw_arch.png, sysdiag.jpg, etc.
  +-- tools/
  |   +-- dockerfile, build_tests.sh
  +-- build/             (generated, gitignored)
  +-- Makefile
  +-- README.md
  +-- LICENSE
  +-- .clang-format
  +-- .gitignore
  +-- .gitmodules
  +-- .github/workflows/ci.yml
  ```
- `SOURCES_WITH_HEADERS` in `Makefile:55-84` --- Lists all source files with corresponding headers, reflecting the directory structure.

**Demo / Example:**
- **Goal:** Create and explain the complete project directory skeleton before any implementation code is written.
- **Why Important:** A clear directory structure makes projects navigable, sets expectations for where new code should go, and reflects the software architecture visually in the file system.
- **Demo Flow:**
  1. Discuss that there is no "best" directory structure --- it depends on project specifics and personal preference.
  2. Reference community examples: Pitchfork layout, Canonical Project Structure.
  3. Create the directory tree: `src/` with `app/`, `drivers/`, `common/`, `test/` subdirectories.
  4. Create `external/` for the printf submodule.
  5. Create `docs/` for images and documentation assets.
  6. Create `tools/` as a placeholder for future scripts.
  7. Explain top-level files: Makefile, README.md, LICENSE, .clang-format, .gitignore.
  8. Naming convention: all lowercase, underscores instead of spaces, no caps.
  9. Pragmatic conclusion: don't overthink it, keep it simple, let it evolve.

**Discussion Prompts:**
- **Q1: Why keep header and source files in the same directory?**
  - For a single-project codebase (not a library), separating headers into a dedicated `include/` directory adds navigational overhead without clear benefit. Finding the implementation file for a header is easier when they sit side-by-side. Separate header directories make sense when building a library where consumers need headers but not source files.
- **Q2: Why use placeholder files in empty directories?**
  - Git does not track empty directories. To commit the project skeleton with its directory structure intact, placeholder files (e.g., `.gitkeep` or similar) are needed in otherwise-empty directories. These are removed once real files are added.
