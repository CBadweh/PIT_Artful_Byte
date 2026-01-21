# NSUMO Codebase Architecture Documentation

Prompt

    Thoroughly explore the codebase at C:\Users\Sheen\Desktop\Embedded_System\Artful_Byte\nsumo_video-main

    I need you to understand and document:
    1. All folders and files in the codebase
    2. The directory structure and layers
    3. The purpose of each major directory
    4. Key configuration files
    5. How the different parts relate to each other

    Let me know if you have any questions

    save the file as Codebase_Archiecture.md in C:\Users\Sheen\Desktop\Embedded_System\Artful_Byte\Class_note


## Project Overview

**Project Name:** Nsumo (500g 10x10cm Sumobot)
**Type:** Embedded Systems - Microcontroller-Based Robotics
**Target MCU:** MSP430G2553 (Texas Instruments)
**Language:** C (embedded C for microcontroller)
**Total Files:** 79
**Total Lines of Code:** ~5,008
**Directory Layout:** Pitchfork Layout

---

## Complete Directory Structure

```
nsumo_video-main/
│
├── ROOT CONFIGURATION FILES
│   ├── .clang-format          - Code formatting rules (WebKit-based style)
│   ├── .clangd/               - Language server configuration
│   ├── .gitignore             - Git ignore rules
│   ├── .gitmodules            - Git submodule configuration
│   ├── .github/               - GitHub automation
│   ├── LICENSE                - Project license
│   ├── Makefile               - Build system configuration
│   └── README.md              - Project documentation
│
├── .github/
│   └── workflows/
│       └── ci.yml             - GitHub Actions CI/CD pipeline
│
├── docs/                      - Documentation and Diagrams
│   ├── coding_guidelines.md   - Detailed coding style guide
│   ├── nsumo.jpg              - Robot hardware image
│   ├── retreat_state.png      - State diagram image
│   ├── retreat_state.uml      - PlantUML diagram source
│   ├── schematic.png          - Hardware schematic
│   ├── state_machine.png      - State machine diagram
│   ├── state_machine.uml      - PlantUML diagram source
│   ├── sw_arch.png            - Software architecture diagram
│   └── sysdiag.jpg            - System block diagram
│
├── external/                  - External Dependencies
│   ├── printf_config.h        - Printf configuration header
│   └── printf/                - Git Submodule (mpaland/printf)
│
├── src/                       - All Source Code
│   ├── main.c                 - Main entry point
│   │
│   ├── app/                   - Application Layer
│   │   ├── drive.c/h          - Motor drive control
│   │   ├── enemy.c/h          - Enemy detection and tracking
│   │   ├── input_history.c/h  - Input history buffer
│   │   ├── line.c/h           - Line sensor handling
│   │   ├── timer.c/h          - Application timing
│   │   ├── state_machine.c/h  - Main state machine
│   │   ├── state_attack.c/h   - Attack state behavior
│   │   ├── state_retreat.c/h  - Retreat state behavior
│   │   ├── state_search.c/h   - Search state behavior
│   │   ├── state_wait.c/h     - Wait state behavior
│   │   ├── state_manual.c/h   - Manual control state
│   │   └── state_common.h     - Common state definitions
│   │
│   ├── common/                - Shared/Utility Code
│   │   ├── assert_handler.c/h - Assertion handling
│   │   ├── defines.h          - Global defines and constants
│   │   ├── enum_to_string.c/h - Enum debugging utilities
│   │   ├── ring_buffer.c/h    - Circular buffer implementation
│   │   ├── sleep.c/h          - Sleep/delay functionality
│   │   └── trace.c/h          - Debug tracing
│   │
│   ├── drivers/               - Hardware Driver Layer
│   │   ├── mcu_init.c/h       - MCU initialization
│   │   ├── io.c/h             - GPIO I/O control
│   │   ├── led.c/h            - LED control
│   │   ├── uart.c/h           - Serial UART communication
│   │   ├── pwm.c/h            - PWM generation
│   │   ├── millis.c/h         - Millisecond timer
│   │   ├── i2c.c/h            - I2C communication protocol
│   │   ├── adc.c/h            - Analog-to-Digital Converter
│   │   ├── tb6612fng.c/h      - Motor driver IC control
│   │   ├── qre1113.c/h        - Reflectance sensor driver
│   │   ├── ir_remote.c/h      - Infrared remote receiver
│   │   └── vl53l0x.c/h        - Time-of-Flight distance sensor
│   │
│   └── test/                  - Testing Code
│       └── test.c             - Unit and integration tests
│
└── tools/                     - Build and CI/CD tools
    ├── build_tests.sh         - Test build script
    └── dockerfile             - Docker container definition
```

---

## Directory Purposes

| Directory | Purpose | File Count |
|-----------|---------|------------|
| **src/** | All source code | 78 files |
| **src/app/** | Application logic (state machine, behavior) | 18 files |
| **src/drivers/** | Hardware drivers and peripheral control | 18 files |
| **src/common/** | Shared utilities and helper code | 12 files |
| **src/test/** | Unit/integration test functions | 1 file |
| **external/** | Third-party dependencies (printf library) | 2 files |
| **docs/** | Documentation, diagrams, and images | 8 files |
| **tools/** | Build scripts and Docker configuration | 2 files |
| **.github/** | GitHub Actions CI/CD configuration | 1 file |

---

## Key Configuration Files

| File | Type | Purpose |
|------|------|---------|
| `Makefile` | Build System | Cross-compilation for MSP430, testing, formatting, analysis |
| `.clang-format` | Code Style | Enforces consistent code formatting (100 col limit, WebKit style) |
| `.github/workflows/ci.yml` | CI/CD Pipeline | Automated build, format check, static analysis |
| `tools/dockerfile` | Container Config | Docker image for CI with MSP430-GCC 9.3.1.11 |
| `tools/build_tests.sh` | Test Builder | Bash script to build all test functions |
| `.gitmodules` | Git Submodules | External printf library as submodule |
| `.gitignore` | Git Rules | Ignores build/, .clangd/, compile_commands.json |
| `docs/coding_guidelines.md` | Code Standards | Comprehensive coding guidelines document |
| `external/printf_config.h` | Printf Config | Configures lightweight printf for embedded use |

---

## Software Architecture Layers

The codebase follows a **3-layer architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│                      (src/app/)                              │
│   State Machine, Drive Control, Enemy Detection, Line       │
│   Detection, Input History, Timer                           │
├─────────────────────────────────────────────────────────────┤
│                     DRIVER LAYER                             │
│                    (src/drivers/)                            │
│   MCU Init, GPIO, UART, PWM, I2C, ADC, Motor Driver,        │
│   Line Sensors, Distance Sensors, IR Remote                 │
├─────────────────────────────────────────────────────────────┤
│                    COMMON LAYER                              │
│                    (src/common/)                             │
│   Assert Handler, Ring Buffer, Trace, Sleep, Defines,       │
│   Enum-to-String Utilities                                  │
├─────────────────────────────────────────────────────────────┤
│                   EXTERNAL LAYER                             │
│                    (external/)                               │
│   Lightweight printf implementation (mpaland/printf)        │
└─────────────────────────────────────────────────────────────┘
```

---

## Main Entry Point

**File:** `src/main.c`

```c
int main(void) {
    mcu_init();           // Initialize microcontroller peripherals
    trace_init();         // Initialize debug tracing
    drive_init();         // Initialize motor control
    enemy_init();         // Initialize distance sensors
    line_init();          // Initialize line sensors
    ir_remote_init();     // Initialize IR remote control
    state_machine_run();  // Enter infinite state machine loop
    ASSERT(0);            // Should never reach here
}
```

---

## State Machine Architecture

The robot uses a **non-blocking, poll-based state machine** with 5 core states:

```
                    ┌──────────────┐
                    │  STATE_WAIT  │
                    │   (idle)     │
                    └──────┬───────┘
                           │ IR Command
                           ▼
                    ┌──────────────┐
         ┌─────────│ STATE_SEARCH │◄────────┐
         │         │  (find enemy) │         │
         │         └──────┬───────┘         │
         │                │ Enemy Detected   │ Timeout/Enemy Lost
         │                ▼                  │
         │         ┌──────────────┐         │
         │         │ STATE_ATTACK │─────────┘
         │         │  (engage)    │
         │         └──────┬───────┘
         │                │ Line Detected
         │                ▼
         │         ┌──────────────┐
         └─────────│STATE_RETREAT │
   Line Detected   │  (back away) │
                   └──────────────┘

         ┌──────────────┐
         │ STATE_MANUAL │ (IR Remote Control - any state)
         └──────────────┘
```

### State Transitions

| Current State | Event | Next State |
|--------------|-------|------------|
| WAIT | IR Command | SEARCH |
| SEARCH | Enemy Detected | ATTACK |
| SEARCH | Line Detected | RETREAT |
| ATTACK | Line Detected | RETREAT |
| ATTACK | Timeout (5s) | SEARCH |
| RETREAT | Finished | SEARCH |
| Any | IR Manual Command | MANUAL |

---

## Hardware Components & Drivers

### Sensors

| Component | Driver File | Purpose |
|-----------|-------------|---------|
| **VL53L0X** (x5) | `vl53l0x.c/h` | Time-of-Flight distance sensors for enemy detection |
| **QRE1113** (x4) | `qre1113.c/h` | Reflectance sensors for line/edge detection |
| **IR Receiver** | `ir_remote.c/h` | Infrared remote control input |

### Actuators

| Component | Driver File | Purpose |
|-----------|-------------|---------|
| **TB6612FNG** | `tb6612fng.c/h` | Dual motor H-bridge driver |
| **LED** | `led.c/h` | Status indicator |

### Communication

| Protocol | Driver File | Purpose |
|----------|-------------|---------|
| **I2C** | `i2c.c/h` | Communication with VL53L0X sensors |
| **UART** | `uart.c/h` | Debug output (115200 baud) |
| **ADC** | `adc.c/h` | Read QRE1113 analog values |
| **PWM** | `pwm.c/h` | Motor speed control |

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────┐
│         STATE MACHINE (Main Loop)           │
│         - Polls every 1ms                   │
│         - Non-blocking                      │
└────────────┬────────────────────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
 [INPUT]  [EVENT]   [STATE]
    │      PROCESS   DISPATCH
    │        │        │
    └─┬──────┤────────┘
      │      │
      │      ▼
  SENSORS  STATE_HANDLERS
  ├─ Enemy   ├─ Wait
  │  (VL53L0X) ├─ Search
  ├─ Line     ├─ Attack
  │  (QRE1113) ├─ Retreat
  └─ IR Remote └─ Manual
      │
      ▼
  HARDWARE DRIVERS
  ├─ I2C (VL53L0X)
  ├─ ADC (QRE1113)
  ├─ PWM (Motors)
  ├─ GPIO (IR receiver)
  └─ Timer (Clocks)
      │
      ▼
  MOTOR OUTPUT (TB6612FNG)
  ├─ Left motor
  └─ Right motor
```

---

## Application Modules

### Drive Module (`src/app/drive.c/h`)

Controls robot movement with predefined directions and speeds:

**Directions:**
- Forward, Reverse
- Rotate Left/Right (spin in place)
- ArcTurn Sharp/Mid/Wide Left/Right (curved movements)

**Speeds:**
- SLOW, MEDIUM, FAST, MAX

### Enemy Module (`src/app/enemy.c/h`)

Processes 5 VL53L0X distance sensors to determine enemy position and range:

**Outputs:**
- Position: FRONT, FRONT_LEFT, FRONT_RIGHT, LEFT, RIGHT, etc.
- Range: CLOSE (<100mm), MID (200mm), FAR (300mm)

### Line Module (`src/app/line.c/h`)

Processes 4 QRE1113 reflectance sensors for boundary detection:

**Positions:** FRONT, BACK, LEFT, RIGHT, and diagonal combinations

### Input History (`src/app/input_history.c/h`)

6-element ring buffer storing recent sensor readings for intelligent decision-making.

---

## Build System

### Makefile Targets

```bash
make HW=LAUNCHPAD       # Build for LaunchPad eval board (20-pin)
make HW=NSUMO           # Build for Nsumo robot (28-pin)
make format             # Format code with clang-format
make cppcheck           # Static analysis
make clean              # Remove build artifacts
make flash              # Program target device
make size               # Show binary size statistics
make symbols            # List symbols sorted by size
make tests              # Build all test functions
make terminal           # Open serial terminal (picocom)
```

### Toolchain

- **Compiler:** msp430-elf-gcc (MSP430-GCC 9.3.1.11)
- **Environment Variable:** `TOOLS_PATH` must point to toolchain location

---

## CI/CD Pipeline

**GitHub Actions Workflow** (`.github/workflows/ci.yml`):

1. Checkout repository with submodules
2. Run code formatter check (clang-format)
3. Run static analysis (cppcheck)
4. Build for NSUMO hardware
5. Build for LAUNCHPAD hardware
6. Build all test functions

**Docker Image:** `artfulbytes/msp430-gcc-9.3.1.11:latest`

---

## Technology Stack Summary

| Category | Technology |
|----------|------------|
| **Language** | C (Embedded C) |
| **MCU** | MSP430G2553 (16KB flash, 512B RAM) |
| **Compiler** | msp430-elf-gcc |
| **Build System** | GNU Make |
| **IDE** | Code Composer Studio (optional) |
| **Code Formatter** | clang-format-12 |
| **Static Analyzer** | cppcheck |
| **CI/CD** | GitHub Actions |
| **Containerization** | Docker |

---

## Key Design Patterns

1. **State Machine Pattern** - Clear state transitions with event-driven dispatch
2. **Layered Architecture** - Separation of concerns (app/driver/common)
3. **Poll-Based Non-Blocking** - No RTOS overhead; 1ms polling loop
4. **Lookup Tables** - Flash memory optimization for speed profiles
5. **Macro-Based Abstractions** - Generic ring buffer and timer implementations
6. **Input History** - Stateful decision making based on recent sensor readings

---

## Memory Considerations

- **Target:** MSP430G2553 (16KB flash, 512 bytes RAM)
- **Optimization:** Lookup tables, macro-based generics, short enums
- **Analysis Tools:** `make size`, `make symbols`, `make addr2line`

---

## Documentation Resources

| File | Description |
|------|-------------|
| `README.md` | Build instructions, project overview |
| `docs/coding_guidelines.md` | Coding standards and style guide |
| `docs/state_machine.uml` | State machine PlantUML source |
| `docs/retreat_state.uml` | Retreat behavior PlantUML source |
| `docs/sw_arch.png` | Software architecture diagram |
| `docs/sysdiag.jpg` | System block diagram |
| `docs/schematic.png` | Hardware schematic |
