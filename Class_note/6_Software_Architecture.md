# Lesson 6: Software Architecture - Codebase Mapping

## Overview

This document maps the concepts from **Lesson 6: How to Create a Software Architecture** to the actual NSUMO codebase implementation. Lesson 6 introduces the layered architecture pattern for embedded systems, emphasizing separation between hardware-dependent (drivers) and hardware-independent (application) code.

---

## Why Organize Software? (Lesson 6 Key Points)

| Benefit | How NSUMO Implements It |
|---------|-------------------------|
| **Easier Reasoning** | Code divided into `app/`, `drivers/`, `common/` layers |
| **Improved Readability** | Each module is a single .c/.h pair with clear purpose |
| **Maintainability** | Changing `uart.c` doesn't affect `i2c.c` or application code |
| **Scalability** | New states added as separate files (e.g., `state_manual.c`) |
| **Collaboration** | Different developers can work on different modules |
| **Reusability** | `ring_buffer.c`, `io.c` reused across multiple modules |
| **Portability** | `HW=LAUNCHPAD` vs `HW=NSUMO` build targets |
| **Testability** | `src/test/test.c` + app layer can run on host computer |

---

## Application Layer Modules

**Location:** `src/app/`

The application layer is **hardware-independent** - it doesn't know about MCU registers or specific peripherals.

### State Machine (Core Decision-Making)

| Lesson 6 Concept | Codebase File | Description |
|------------------|---------------|-------------|
| State Machine | `state_machine.c/h` | Main loop that dispatches to state handlers |
| Search State | `state_search.c/h` | Rotates robot to find enemy |
| Attack State | `state_attack.c/h` | Engages and pushes enemy |
| Retreat State | `state_retreat.c/h` | Backs away from ring edge |
| *Not in Lesson 6* | `state_wait.c/h` | Idle state waiting for IR command |
| *Not in Lesson 6* | `state_manual.c/h` | Manual control via IR remote |
| Common Definitions | `state_common.h` | Shared state types and definitions |

**Lesson 6 Quote:** *"The state machine is the big machinery that makes the decisions. It takes input from the sensors and makes decisions based on this and outputs a drive command to the motors."*

---

### Abstraction Modules (Simplifying Interfaces)

These modules translate raw driver data into simplified representations for the state machine.

| Lesson 6 Concept | Codebase File | Input | Output |
|------------------|---------------|-------|--------|
| **Enemy Module** | `enemy.c/h` | Raw distance values (mm) from VL53L0X | Position: `FRONT`, `LEFT`, `RIGHT`, etc. Range: `CLOSE`, `MID`, `FAR` |
| **Line Module** | `line.c/h` | Raw ADC values from QRE1113 | Position: `FRONT`, `BACK`, `LEFT`, `RIGHT` |
| **Drive Module** | `drive.c/h` | Commands: `FORWARD`, `ROTATE_LEFT`, `ARC_TURN_RIGHT` | Duty cycles and direction signals to motor driver |

**Lesson 6 Quote:** *"The enemy module is going to translate these values into a rougher representation... tell whether the enemy is close or nearby or whether the enemy is to the left or to the right."*

---

### Support Modules

| Lesson 6 Concept | Codebase File | Purpose |
|------------------|---------------|---------|
| **Timer** | `timer.c/h` | Measures elapsed time for state timeouts and timed movements |
| **Trace/Printf** | `src/common/trace.c/h` | Debug output functions |
| **Printf (External)** | `external/printf/` | Lightweight printf optimized for embedded (mpaland/printf) |
| *Not in Lesson 6* | `input_history.c/h` | 6-element ring buffer storing recent sensor readings |

**Lesson 6 Quote:** *"The printf module here is actually an external project... because the regular printf implementation in the standard library is too large for an embedded system."*

---

## Driver Layer Modules

**Location:** `src/drivers/`

The driver layer is **hardware-dependent** - it contains code that directly interacts with MCU registers and peripherals.

### Hardware Initialization

| Lesson 6 Concept | Codebase File | Purpose |
|------------------|---------------|---------|
| **MCU Init** | `mcu_init.c/h` | Configures clock rate, initializes I/O pins at boot |

**Lesson 6 Quote:** *"This module will take care of initializing the microcontroller... configuring the clock rate as well as initializing the IO pins."*

---

### Communication Drivers

| Lesson 6 Concept | Codebase File | Peripheral | Purpose |
|------------------|---------------|------------|---------|
| **UART** | `uart.c/h` | UART | Sends characters to host computer for debugging |
| **I²C** | `i2c.c/h` | I²C | Communicates with VL53L0X distance sensors |

**Lesson 6 Quote:** *"The I²C driver is just focused on providing functionality for sending things over I²C."*

---

### Sensor Drivers

| Lesson 6 Concept | Codebase File | Sensor | Communication |
|------------------|---------------|--------|---------------|
| **Range Sensor** | `vl53l0x.c/h` | VL53L0X (x5) | Uses I²C driver |
| **Line Sensor** | `qre1113.c/h` | QRE1113 (x4) | Uses ADC driver |
| **ADC** | `adc.c/h` | ADC Peripheral | Reads analog values from line sensors |
| **IR Remote** | `ir_remote.c/h` | IR Receiver | Uses timer peripheral to parse signals |

**Lesson 6 Quote:** *"The module above the VL53L0X is going to hold the code that knows what messages to send over I²C to communicate with the range sensor."*

---

### Motor Control

| Lesson 6 Concept | Codebase File | Purpose |
|------------------|---------------|---------|
| **PWM** | `pwm.c/h` | Generates PWM signals using timer peripheral |
| **Motor Driver** | `tb6612fng.c/h` | Controls TB6612FNG H-bridge IC (direction + PWM) |

**Lesson 6 Quote:** *"The PWM module is going to make use of the timer peripheral to create the PWM signal sent to the motor driver."*

---

### Utility Modules

| Lesson 6 Concept | Codebase File | Purpose |
|------------------|---------------|---------|
| **IO** | `io.c/h` | Pin configuration, pin mapping enum, GPIO operations |
| **LED** | `led.c/h` | Toggles test LED on PCB |
| **Millis** | `millis.c/h` | Returns time elapsed since boot (repurposes watchdog timer) |

**Lesson 6 Quote:** *"This IO module is going to hold functions for configuring the individual pins. It's also going to keep track of the pin mapping by having an enum that names all of the pins."*

---

## Common Layer (Additional to Lesson 6)

**Location:** `src/common/`

The codebase includes a **Common Layer** not explicitly discussed in Lesson 6, containing shared utilities:

| File | Purpose |
|------|---------|
| `assert_handler.c/h` | Assertion and error handling |
| `defines.h` | Global defines and constants |
| `enum_to_string.c/h` | Converts enums to strings for debugging |
| `ring_buffer.c/h` | Generic circular buffer (used by `input_history`) |
| `sleep.c/h` | Delay/sleep functionality |
| `trace.c/h` | Debug tracing (wraps printf) |

---

## Dependency Diagram

Based on Lesson 6's architecture diagram, here's how the NSUMO modules relate:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         APPLICATION LAYER (src/app/)                         │
│                         Hardware Independent                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                        ┌──────────────────────┐                              │
│                        │    STATE MACHINE     │                              │
│                        │  state_machine.c/h   │                              │
│                        └──────────┬───────────┘                              │
│                                   │                                          │
│            ┌──────────────────────┼──────────────────────┐                   │
│            │                      │                      │                   │
│            ▼                      ▼                      ▼                   │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐           │
│   │  state_search   │   │  state_attack   │   │  state_retreat  │           │
│   │  state_wait     │   │  state_manual   │   │                 │           │
│   └────────┬────────┘   └────────┬────────┘   └────────┬────────┘           │
│            │                     │                      │                    │
│            └─────────────────────┼──────────────────────┘                    │
│                                  │                                           │
│         ┌────────────────────────┼────────────────────────┐                  │
│         │                        │                        │                  │
│         ▼                        ▼                        ▼                  │
│  ┌─────────────┐          ┌─────────────┐          ┌─────────────┐          │
│  │   enemy.c   │          │   line.c    │          │   drive.c   │          │
│  │  (input)    │          │  (input)    │          │  (output)   │          │
│  └──────┬──────┘          └──────┬──────┘          └──────┬──────┘          │
│         │                        │                        │                  │
├─────────┼────────────────────────┼────────────────────────┼──────────────────┤
│         │              DRIVER LAYER (src/drivers/)        │                  │
│         │              Hardware Dependent                 │                  │
├─────────┼────────────────────────┼────────────────────────┼──────────────────┤
│         │                        │                        │                  │
│         ▼                        ▼                        ▼                  │
│  ┌─────────────┐          ┌─────────────┐          ┌─────────────┐          │
│  │  vl53l0x.c  │          │  qre1113.c  │          │ tb6612fng.c │          │
│  └──────┬──────┘          └──────┬──────┘          └──────┬──────┘          │
│         │                        │                        │                  │
│         ▼                        ▼                        ▼                  │
│  ┌─────────────┐          ┌─────────────┐          ┌─────────────┐          │
│  │    i2c.c    │          │    adc.c    │          │    pwm.c    │          │
│  └─────────────┘          └─────────────┘          └─────────────┘          │
│                                                                              │
│                    ┌─────────────────────────────┐                           │
│                    │           io.c              │                           │
│                    │  (used by all drivers)      │                           │
│                    └─────────────────────────────┘                           │
│                                                                              │
│  Other Drivers:  mcu_init.c | uart.c | millis.c | led.c | ir_remote.c       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         COMMON LAYER (src/common/)                           │
│  trace.c | ring_buffer.c | assert_handler.c | sleep.c | defines.h           │
├─────────────────────────────────────────────────────────────────────────────┤
│                         EXTERNAL LAYER (external/)                           │
│                    printf/ (mpaland/printf submodule)                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Design Principles Applied

| Principle | Lesson 6 Explanation | NSUMO Implementation |
|-----------|---------------------|----------------------|
| **Decoupling** | Boxes independent from each other | `src/app/` has no `#include` of MCU headers |
| **Modularity** | Separate independent ideas | Each sensor/peripheral has its own file pair |
| **Separation of Concerns** | Boxing in independent ideas | `enemy.c` only handles enemy detection logic |
| **Single Responsibility** | One thing per module | `i2c.c` only handles I²C protocol, not sensor logic |
| **DRY (Don't Repeat Yourself)** | Shared code in single place | `io.c` shared by all drivers; `ring_buffer.c` reused |
| **Cohesion** | Related code close together | All state handlers in `src/app/` directory |
| **Encapsulation** | Hide implementation details | App layer doesn't see register addresses |
| **Layered Architecture** | Low-to-high abstraction | Drivers → Application → State Machine |

---

## Design Methodology

### 1. Understand the Problem First

**Lesson 6:** *"To create a sensible architecture you must first understand the problem you're dealing with."*

**NSUMO Problem:** Make robot detect enemy, push it out, while staying inside the ring.

### 2. Use Hardware as Reference

**Lesson 6:** *"The hardware block diagram can be extremely useful... as a reference or guide when we architect our software."*

**NSUMO:** `docs/sysdiag.jpg` shows hardware components that map directly to driver files:
- VL53L0X sensors → `vl53l0x.c`
- QRE1113 sensors → `qre1113.c`
- TB6612FNG motor driver → `tb6612fng.c`

### 3. Map Hardware to Software

**Lesson 6:** *"Things that are conceptually one thing in the hardware should also be one thing and separated in the software."*

| Hardware Component | Software Module |
|--------------------|-----------------|
| UART peripheral | `uart.c/h` |
| I²C peripheral | `i2c.c/h` |
| ADC peripheral | `adc.c/h` |
| Timer peripheral | `pwm.c/h`, `millis.c/h`, `ir_remote.c/h` |

### 4. Define Logical Relationships

**Lesson 6:** *"It makes sense for the enemy module to depend on the range sensors... but it doesn't make sense for the enemy module to have any kind of dependence to the PWM module."*

**NSUMO Dependencies:**
- `enemy.c` → `vl53l0x.c` → `i2c.c` ✓
- `enemy.c` → `pwm.c` ✗ (no dependency - correct!)
- `drive.c` → `tb6612fng.c` → `pwm.c` ✓

### 5. Separate Platform-Dependent from Platform-Independent

**Lesson 6:** *"We really want to separate these two layers of the code to make it as easy as possible to change platform."*

**NSUMO:**
- Platform-independent: `src/app/` (can run on host computer for simulation)
- Platform-dependent: `src/drivers/` (MSP430-specific register access)
- Build targets: `HW=LAUNCHPAD` vs `HW=NSUMO` demonstrate portability

---

## Differences from Lesson 6 Diagram

| Lesson 6 Diagram | NSUMO Implementation | Reason |
|------------------|----------------------|--------|
| 3 states (Search, Attack, Retreat) | 5 states (+Wait, +Manual) | Added idle and remote control states |
| Generic "motor driver" | Specific `tb6612fng.c` | Named after actual IC used |
| Timer in Application | Timer split: `timer.c` (app) + `millis.c` (driver) | Cleaner separation |
| No Input History | `input_history.c` added | Enables smarter decision-making |
| No Common layer | `src/common/` added | Shared utilities extracted |

---

## Key Takeaways

1. **Architecture follows from understanding the problem** - The robot's task (find enemy, push, stay in ring) naturally leads to the module structure.

2. **Hardware guides software structure** - Physical components (sensors, motors, MCU peripherals) map to software modules.

3. **Layered architecture enables portability** - Application layer can run on host computer for simulation/testing.

4. **Abstraction modules simplify state machine** - Enemy, Line, and Drive modules translate complex data into simple decisions.

5. **Good separation prevents cascading changes** - Modifying UART code doesn't affect I²C code or application logic.

---

## References

- **Lesson 6 Video:** "How to Create a Software Architecture - Embedded System Project Series #6"
- **Codebase:** `nsumo_video-main/`
- **Architecture Diagram:** `docs/sw_arch.png`
- **Hardware Diagram:** `docs/sysdiag.jpg`
