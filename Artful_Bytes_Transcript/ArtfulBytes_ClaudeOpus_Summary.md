# Artful Bytes — Embedded System Project Series: Comprehensive Summary

> **Course:** Embedded System Project Series by Artful Bytes (Niklas)
> **Target Platform:** MSP430G2553 (Texas Instruments LaunchPad + Custom Nsumo PCB)
> **Lessons Covered:** 1-28
> **Source Code:** `Code/source_code/nsumo_video/`
> **Transcripts:** `Artful_Bytes_Transcript/`

---

## Table of Contents

- [Quick Reference Card](#quick-reference-card)
- [1. Course Overview](#1-course-overview)
- [2. Course Progression Map](#2-course-progression-map)
- [3. Lesson Summaries](#3-lesson-summaries)
  - [Section 1: Hardware Design & Component Selection (Lessons 1-3)](#section-1-hardware-design--component-selection)
  - [Section 2: Development Environment Setup (Lessons 4-5)](#section-2-development-environment-setup)
  - [Section 3: Software Architecture & Project Organization (Lessons 6-7)](#section-3-software-architecture--project-organization)
  - [Section 4: Development Workflow & Best Practices (Lessons 8-11)](#section-4-development-workflow--best-practices)
  - [Section 5: Low-Level Programming Fundamentals (Lessons 12-20)](#section-5-low-level-programming-fundamentals)
  - [Section 6: Motor Control & PWM (Lesson 21)](#section-6-motor-control--pwm)
  - [Section 7: Sensor Integration (Lessons 22-23)](#section-7-sensor-integration)
  - [Section 8: System Integration & Testing (Lessons 24-28)](#section-8-system-integration--testing)
- [4. Course Interconnections](#4-course-interconnections)
- [5. Hardware, Software & Tools Inventory](#5-hardware-software--tools-inventory)
- [6. Complete Techniques Catalog](#6-complete-techniques-catalog)
- [7. Best Practices & Industry Patterns](#7-best-practices--industry-patterns)
- [8. Common Pitfalls](#8-common-pitfalls)
- [9. Source Code & Project Reference](#9-source-code--project-reference)
- [10. Lesson Transcript Index](#10-lesson-transcript-index)
- [Appendix A: Pareto Base](#appendix-a-pareto-base)
- [Conclusion](#conclusion)

---

## Quick Reference Card

| What I Need | Where to Find It | Key Command / Pattern |
|---|---|---|
| Build firmware (LaunchPad) | Lesson 5, `Makefile` | `TOOLS_PATH=$HOME/dev/tools make HW=LAUNCHPAD` |
| Build firmware (Robot PCB) | Lesson 5, `Makefile` | `TOOLS_PATH=$HOME/dev/tools make HW=NSUMO` |
| Flash to target | Lesson 5, `Makefile` | `make flash` |
| Run static analysis | Lesson 9, `Makefile` | `make cppcheck` |
| Format all code | Lesson 11, `.clang-format` | `make format` |
| Check memory usage | Lesson 16, `Makefile` | `make size` / `make symbols` |
| Resolve assert address | Lesson 14, `Makefile` | `make HW=LAUNCHPAD addr2line ADDR=0x1234` |
| Open serial terminal | Lesson 18, `Makefile` | `picocom -b 115200 /dev/ttyUSB0` |
| Run a test function | Lesson 15, `src/test/test.c` | `make HW=LAUNCHPAD TEST=test_assert` |
| Generate PlantUML diagram | Lesson 26, `docs/*.uml` | `java -jar plantuml.jar diagram.uml` |
| Init sequence | Lesson 24, `src/main.c` | `mcu_init() → trace_init() → drive_init() → enemy_init() → line_init() → ir_remote_init() → state_machine_run()` |
| State machine flow | Lesson 26, `src/app/state_machine.c` | `WAIT →(cmd)→ SEARCH →(enemy)→ ATTACK →(line)→ RETREAT →(done)→ SEARCH` |
| Register-level GPIO | Lesson 12, `src/drivers/io.c` | `PxDIR \|= BITn;` (output), `PxOUT \|= BITn;` (set high) |
| I2C read sensor | Lesson 23, `src/drivers/i2c.c` | `i2c_read(addr, reg, buf, len)` |

> **Purpose:** One-page lookup table for working mode. Pin this next to your monitor.

---

## 1. Course Overview

### What This Course Covers

This is a 28-lesson YouTube series by Niklas (Artful Bytes), an embedded systems engineer, documenting the complete process of programming a mini-class sumo robot (Nsumo) from scratch using bare-metal C on an MSP430G2553 microcontroller. The course covers everything from hardware selection and PCB design through writing peripheral drivers (GPIO, UART, I2C, ADC, PWM), implementing a state machine for autonomous behavior, and integrating all components into a competition-ready robot.

What makes this course unique is its project-driven approach — rather than teaching isolated concepts, every topic is grounded in the real sumo robot project. The instructor writes all drivers from register level (no HAL libraries, no Arduino), demonstrates professional practices (git workflow, CI/CD, static analysis, coding guidelines), and shows the full development lifecycle including board bring-up, simulation, and real-world testing. The course deliberately uses a resource-constrained MCU (16 KB flash, 512 B RAM) to teach embedded-specific challenges like memory optimization and peripheral timer sharing.

### Target Audience and Prerequisites

- Programmers wanting to transition from Arduino/hobby to professional bare-metal embedded development
- CS/EE students learning microcontroller programming with C
- Anyone interested in building a complete embedded project from scratch
- Prerequisites: Basic C programming, basic electronics understanding helpful but not required

### Learning Progression

1. Understand the hardware system (parts, schematic, PCB)
2. Set up the development environment (IDE + command-line toolchain)
3. Design the software architecture (layered: drivers → app → common)
4. Establish professional workflow (git, CI/CD, static analysis, formatting)
5. Write peripheral drivers one by one (GPIO → UART → PWM → ADC → I2C)
6. Learn MCU fundamentals along the way (memory, interrupts, registers)
7. Integrate motors and sensors on the actual PCB (board bring-up)
8. Build a 2D simulator for algorithm development
9. Design and implement the autonomous state machine
10. Transfer from simulation to real robot and test

---

## 2. Course Progression Map

### Dependency Chain

```
Section 1: Hardware Design & Component Selection (Lessons 1-3)
   |
   |  Provides: Understanding of the physical system — what parts exist,
   |            how they connect, what the MCU must control
   |
   v
Section 2: Development Environment Setup (Lessons 4-5)
   |
   |  Provides: Ability to compile, flash, and debug code on the MSP430.
   |            Makefile build system for all future development
   |
   v
Section 3: Software Architecture & Project Organization (Lessons 6-7)
   |
   |  Provides: Layered architecture (drivers/app/common), file structure,
   |            module conventions that all future code follows
   |
   v
Section 4: Development Workflow & Best Practices (Lessons 8-11)
   |
   |  Provides: Git workflow, CI/CD pipeline, static analysis, code formatting —
   |            the infrastructure around the code
   |
   v
Section 5: Low-Level Programming Fundamentals (Lessons 12-20)
   |
   |  Provides: All peripheral drivers (GPIO, UART, PWM, IR remote),
   |            MCU memory model, interrupts, assert handler, printf
   |
   v
Section 6: Motor Control & PWM (Lesson 21)
   |
   |  Provides: Motor driver (TB6612FNG), tank drive abstraction,
   |            speed/direction control via PWM
   |
   v
Section 7: Sensor Integration (Lessons 22-23)
   |
   |  Provides: ADC + DMA for line sensors (QRE1113),
   |            I2C for range sensors (VL53L0X) — robot perception
   |
   v
Section 8: System Integration & Testing (Lessons 24-28) [Capstone]
   |
   |  Provides: Board bring-up, 2D simulator, state machine design,
   |            simulation-to-real transfer, competition readiness
```

### Why Each Section Requires the Previous

| Transition | Why It Is Needed |
|---|---|
| S1 before S2 | You must know what MCU and peripherals you're targeting before setting up the toolchain and IDE |
| S2 before S3 | You need a working build system before you can organize source files into a multi-file architecture |
| S3 before S4 | Git, CI, and formatting only make sense once you have a project structure to version-control and build |
| S4 before S5 | Professional workflow must be in place before writing substantial driver code — ensures every driver commit is tested and formatted |
| S5 before S6 | Motor control requires GPIO (pin configuration) + PWM (timer peripheral) + understanding of interrupts — all taught in S5 |
| S6 before S7 | Sensor integration builds on the same peripheral patterns (ADC, I2C) and needs motors working to test robot behavior |
| S7 before S8 | Board bring-up, state machine, and autonomous behavior require all drivers and sensors operational |

### Visual Topic Connection Map

```
              +-----------------------------+
              |  Hardware Design (S1)       |
              |  Parts, Schematic, PCB      |
              +-------------+---------------+
                            |
               +------------+------------+
               |                         |
   +-----------v-----------+  +----------v-----------+
   | Dev Environment (S2)  |  | SW Architecture (S3) |
   | IDE, Makefile, GCC    |  | Layers, Modules      |
   +-----------+-----------+  +----------+-----------+
               |                         |
               +------------+------------+
                            |
              +-------------v--------------+
              | Dev Workflow (S4)           |
              | Git, CI/CD, cppcheck, fmt  |
              +-------------+--------------+
                            |
              +-------------v--------------+
              | Low-Level Drivers (S5)     |
              | GPIO, UART, Interrupts,    |
              | Memory, Assert, IR, printf |
              +-------------+--------------+
                            |
               +------------+------------+
               |                         |
   +-----------v-----------+  +----------v-----------+
   | Motor Control (S6)   |  | Sensor Integration   |
   | PWM, TB6612FNG,      |  | (S7) ADC+DMA, I2C,  |
   | Tank Drive            |  | QRE1113, VL53L0X    |
   +-----------+-----------+  +----------+-----------+
               |                         |
               +------------+------------+
                            |
              +-------------v--------------+
              | System Integration (S8)    |
              | Board Bring-up, Simulator, |
              | State Machine, Real Robot  |
              +----------------------------+
```

---

## 3. Lesson Summaries


### Section 1: Hardware Design & Component Selection

---

### Lesson 001 --- Intro and Overview

**File Path:** [Lesson_001_transcript.txt](Artful_Bytes_Transcript/1%20Intro%20and%20Overview%20%20Embedded%20System%20Project%20Series%20%231.txt)

**Objective:** Introduces the Artful Bytes Embedded System Project Series, framing a sumo robot as a practical vehicle for learning bare-metal embedded programming in C --- covering drivers, peripherals, schematics, data sheets, and real hardware tools.

**Terminology & Key Concepts:**
- **Sumo Bot (nsumo)**: A small autonomous robot built to compete in robotic sumo, where two robots attempt to push each other out of a circular platform (dohyo). The mini class limits dimensions to 10x10 cm and 500 grams.
- **Bare Metal Programming**: Writing firmware directly on the microcontroller without an operating system or abstraction layer like Arduino, requiring the developer to write all drivers from scratch.
- **Evaluation Board (LaunchPad)**: A development board (MSP430 LaunchPad) used to prototype and test code before deploying to the custom PCB --- common practice in professional embedded workflows.
- **Robotic Sumo Competition**: A competition format where autonomous robots compete by pushing opponents out of a ring. Rules require autonomy, remote start capability, and no intentional harm to opponent or platform.
- **Embedded System**: A combination of hardware and software where a microcontroller executes purpose-built firmware to control physical devices (sensors, motors, etc.).

**Techniques & Methods:**
- **Project Scoping via Competition Rules**: Using competition constraints (size, weight, autonomy requirements) to define project requirements and guide component selection decisions.
- **Incremental Development**: The series follows a structured progression --- hardware overview first, then driver development on an evaluation board, then PCB integration, then autonomous behavior via state machine.
- **Evaluation Board Prototyping**: Using the MSP430 LaunchPad to develop and test drivers in isolation before migrating code to the final PCB, making videos more modular and easier to follow.

**Source Code Mapping:**
- No source code is introduced in this lesson. It is purely an overview and motivation video.

**Demo / Example:**
- **Goal:** Present the sumo robot hardware and outline the video series structure.
- **Why Important:** Establishes the full scope of the project --- from blank microcontroller to autonomous robot --- and sets expectations for what will be covered (GPIO, UART, I2C, PWM, ADC, state machine, simulation).
- **Demo Flow:**
  1. Physical demonstration of the finished sumo robot.
  2. Overview of the series structure: hardware overview -> development environment -> driver videos (GPIO, UART, PWM, I2C) on LaunchPad -> PCB integration -> state machine and autonomous behavior -> 2D simulation.
  3. Emphasis that most content is applicable to any embedded system, not just sumo robots.

**Discussion Prompts:**
- **Q1: Why does the instructor choose bare-metal C over Arduino for this project?**
  - To teach real embedded development skills --- selecting components, designing PCBs, writing drivers from scratch, and reading datasheets --- skills required for professional embedded work and advanced projects where Arduino is not a viable option.
- **Q2: Why use an evaluation board when the final PCB is already built?**
  - To simulate a realistic development workflow where hardware is not immediately available. It also isolates driver development, makes lessons more modular, and allows viewers to follow along without the custom PCB.

---

### Lesson 002 --- Picking the Parts for a Small Robot

**File Path:** [Lesson_002_transcript.txt](Artful_Bytes_Transcript/2%20Picking%20the%20Parts%20for%20a%20Small%20Robot%20%20%20Embedded%20System%20Project%20Series%20%232.txt)

**Objective:** Teaches the hardware component selection process for an embedded system project, using competition requirements and engineering trade-offs to choose motors, sensors, power supply, and the microcontroller for the nsumo robot.

**Terminology & Key Concepts:**
- **Brushed DC Motor**: A simple DC motor where current flows through brushes to commutate the rotor. Easier to control than brushless motors (just vary voltage), cheaper, but less efficient and durable. Selected for simplicity in this project.
- **Gearbox / Gear Ratio**: Mechanical gears attached to a motor to trade RPM for torque. Small DC motors have very high RPM and low torque by default; a gearbox corrects this balance.
- **Motor Driver (TB6612FNG)**: An IC containing MOSFET transistor switches that sits between the microcontroller and motors. The MCU's GPIO pins cannot source enough current for motors, so the motor driver switches the larger battery current using the small MCU control signals (PWM).
- **Time-of-Flight (ToF) Sensor (VL53L0X)**: A laser-based range sensor from ST that measures distance by timing how long laser light takes to bounce back. Small, accurate (0 to ~80 cm), fast (50 Hz), but complex to interface (I2C with extensive configuration).
- **QRE1113 Line Sensor**: An infrared reflectance sensor used to detect the white border of the sumo platform. Interfaces via a single ADC pin --- simple and effective.
- **LiPo Battery**: Lithium Polymer battery chosen for high energy density in a small form factor. Two single-cell (3.7V each) in series yield 7.4V total.
- **MSP430G2553**: A 16-bit microcontroller from Texas Instruments with 16 KB flash, 512 B RAM, 16 MHz clock. Chosen for good documentation, beginner-friendly ecosystem, and university adoption --- though limited in pins and flash for this project.
- **PWM (Pulse Width Modulation)**: A technique for controlling motor speed by rapidly switching voltage on/off at varying duty cycles, effectively varying the average voltage delivered to the motor.
- **Cross Tool Chain**: A compiler toolchain that runs on a host computer (e.g., x86) but produces executables for a different target architecture (e.g., MSP430).

**Techniques & Methods:**
- **Requirements-Driven Component Selection**: Starting from competition rules (10x10 cm, 500g, autonomous, 77cm platform, 3-min rounds) to systematically narrow down motor type, sensor type, battery, and MCU.
- **Block Diagram as Design Reference**: Drawing a system-level block diagram showing all components and their interfaces (I2C, ADC, PWM, GPIO) to the microcontroller --- used throughout the series as an orientation tool.
- **Trade-off Analysis**: Explicitly weighing pros and cons at each decision point (e.g., 2 vs. 4 motors: more pushing power vs. simpler design; brushed vs. brushless: ease of control vs. efficiency).
- **Peripheral Interface Listing**: Before choosing an MCU, listing all required interfaces (2 PWM, 1 I2C, 4 ADC, timer, 10+ GPIO) to establish minimum MCU requirements.
- **Hindsight Reflection**: Instructor openly discusses what he would change in retrospect (fewer motors, fewer range sensors, beefier MCU), modeling the iterative learning process.

**Source Code Mapping:**
- No source code is introduced in this lesson. The lesson is focused on hardware selection rationale.

**Demo / Example:**
- **Goal:** Walk through the complete component selection process for the sumo robot.
- **Why Important:** Demonstrates that embedded development starts long before writing code --- selecting the right components is foundational and affects everything from PCB design to driver complexity.
- **Demo Flow:**
  1. Start from competition rules to define requirements (autonomous, 10x10cm, 500g, remote start).
  2. Motor selection: Rule out servos/steppers/AC/brushless -> choose brushed DC with gearbox -> pick 4x 400 RPM @ 6V motors.
  3. Motor driver: Need TB6612FNG (MOSFET-based, 1A continuous, 2 motors per IC) -> 2 drivers, but only 2 PWM signals needed (tank drive).
  4. Range sensors: Rule out ultrasonic (bulky/slow) and IR (limited range) -> choose VL53L0X ToF (0-80cm, I2C, 50Hz). Use 3 front + 2 side (hindsight: 3 front would suffice).
  5. Line sensors: QRE1113 infrared reflectance, 4 total (2 front, 2 back), single ADC pin each.
  6. IR receiver: 38 kHz, 3-pin component for remote start signal + development-time remote control.
  7. Battery: 2x single-cell LiPo (750mAh each, 30C discharge), 7.4V series.
  8. MCU: MSP430G2553 --- 16-bit, 16KB flash, 16MHz, good docs/tools, but tight on pins/flash.
  9. Return to block diagram showing all connections.

**Discussion Prompts:**
- **Q1: Why did the instructor choose the MSP430 over a more powerful MCU?**
  - Primarily because of prior familiarity, excellent documentation, active community, and university-level teaching resources. Technical specs are borderline (tight flash, few pins) but sufficient for the project. The advice: pick something simple and well-documented for learning; don't fear making the wrong choice since fundamental concepts transfer between MCUs.
- **Q2: What is the "less parts, less problems" design philosophy?**
  - The instructor repeatedly notes that minimizing component count reduces mechanical complexity, electronic design effort, software bugs, and debugging difficulty. Hindsight examples: 2 motors instead of 4 would simplify mechanics; 3 range sensors instead of 5 would reduce I2C complexity and false detections.
- **Q3: Why not use an Arduino?**
  - The project intentionally avoids Arduino to develop deeper embedded skills: selecting your own MCU, designing a PCB, writing drivers from scratch, and understanding the hardware at register level. Arduino is fine for quick prototypes but insufficient for learning professional embedded development.

---

### Lesson 003 --- PCB Design Walkthrough (Sumo Robot)

**File Path:** [Lesson_003_transcript.txt](Artful_Bytes_Transcript/3%20PCB%20Design%20Walkthrough%20Sumo%20Robot%20%20Embedded%20System%20Project%20Series%20%233.txt)

**Objective:** Provides a walkthrough of the custom PCB schematic and layout for the sumo robot, teaching how to read schematics, understand power regulation circuits, pin assignments, and the physical mapping between schematic and PCB --- essential skills for embedded software engineers.

**Terminology & Key Concepts:**
- **PCB (Printed Circuit Board)**: A board that mechanically supports and electrically connects electronic components using conductive traces. This is a 2-layer board (5x6 cm): one layer for signals, one for ground.
- **Schematic**: A drawing showing components and their electrical connections. For embedded programming, the schematic (not the PCB layout) is the primary reference for knowing which pin connects to which peripheral.
- **KiCad**: An open-source EDA (Electronic Design Automation) tool used to design the PCB schematic and layout.
- **Voltage Regulator (Switching / Linear)**: Circuits that step down battery voltage (7.4V) to levels needed by components (5V then 3.3V). The switching regulator is more efficient; the linear regulator provides cleaner output but wastes energy as heat.
- **Reverse Polarity Protection**: A MOSFET placed after the power switch to prevent damage from connecting the battery backwards.
- **Bypass Capacitors (Decoupling Caps)**: Small capacitors placed near IC power pins to reduce noise and stabilize the voltage supply.
- **Pin Multiplexing (Pin Muxing)**: MSP430 pins serve multiple functions (GPIO, I2C, ADC, PWM, interrupt). The designer must carefully assign pins based on which peripheral functions each physical pin supports.
- **Molex Connectors**: Small, space-efficient connectors used for sensor connections. Fragile but suitable for the size constraints.
- **Spy-Bi-Wire**: A 2-wire debug/programming interface used to program the MSP430 on the custom PCB via the LaunchPad's onboard debugger.

**Techniques & Methods:**
- **Prototype Before PCB**: The instructor emphasizes that he prototyped extensively on breadboards and the LaunchPad before designing the PCB --- a critical professional practice.
- **Following Datasheet Reference Circuits**: Power regulation circuits (switching and linear regulators) are built following the example circuits in the component datasheets.
- **Pin Assignment by Peripheral Requirement**: I2C on P1.6/P1.7 (dedicated I2C peripheral), ADC inputs on Port 1 (only port with ADC), interrupts on Port 1/2 (only interrupt-capable ports), PWM on Timer A0 output pins.
- **LED-Everywhere Debugging Strategy**: Placing LEDs on line sensors, IR receiver, power rails, and a test LED for visual debugging during bring-up.
- **Using Evaluation Board as Programmer**: Disconnecting the LaunchPad's onboard MSP430 and using its debug circuitry to program the MSP430 on the custom PCB via jumper wires, avoiding the need for dedicated programming hardware on the custom board.
- **Tank Drive Motor Wiring**: Both motors on each side share the same PWM signal and direction pins, reducing pin count since same-side motors always drive together.

**Source Code Mapping:**
- `io_e` enum: `io.h:22-66` --- Maps physical pin assignments from the schematic to named enum values in code.
  ```c
  typedef enum {
      // NSUMO pin mapping
      IO_LINE_DETECT_FRONT_RIGHT = IO_10,
      IO_UART_RXD = IO_11,
      IO_UART_TXD = IO_12,
      IO_I2C_SCL = IO_16,
      IO_I2C_SDA = IO_17,
      IO_IR_REMOTE = IO_20,
      IO_PWM_MOTORS_LEFT = IO_35,
      IO_PWM_MOTORS_RIGHT = IO_36,
      // ...
  } io_e;
  ```
- `io_initial_configs[]`: `io.c:103-166` --- The initial configuration array for every IO pin, directly reflecting the schematic's pin assignments (which pins are GPIO output, which are ADC, which are I2C alternate function, etc.).

**Demo / Example:**
- **Goal:** Walk through the complete PCB schematic, explaining each section and how it maps to the physical board.
- **Why Important:** Embedded software engineers must read schematics to know which pins to configure and how peripherals are connected --- this is the bridge between hardware design and driver code.
- **Demo Flow:**
  1. Power section: Battery connectors -> power switch -> reverse polarity MOSFET -> switching regulator (7.4V to 5V) -> linear regulator (5V to 3.3V) -> power LEDs and fuses.
  2. MCU section: MSP430 with bypass caps, reset pull-up resistor, manual reset switch. Pin assignments reviewed: I2C (P1.6/P1.7), ADC (Port 1), PWM (Timer A0), UART (P1.1/P1.2), interrupts (Port 1/2).
  3. Sensor connectors: 5 range sensor connectors (3.3V, GND, I2C, XSHUT reset, one interrupt), 4 line sensor connectors (power, GND, ADC), IR receiver (3-pin with LED and filtering).
  4. Motor drivers: Left and right TB6612FNG, each controlling 2 motors with shared PWM and direction pins.
  5. Programming header: 2-pin Spy-Bi-Wire connection to LaunchPad for flashing.
  6. Three unused pins broken out to headers for future use.

**Discussion Prompts:**
- **Q1: Why use two voltage regulators instead of one?**
  - Originally thought 5V was needed for line sensors (corrected in revision 2 --- they work at 3.3V). Kept the dual-regulator design for safety and potential noise isolation from motors. In hindsight, a single switching regulator would suffice since there are no high-precision ADC requirements.
- **Q2: Why is reading schematics important for embedded software engineers?**
  - Schematics tell you which MCU pin connects to which peripheral, what alternate functions to configure, where pull-ups/pull-downs exist, and how the power tree works. Without this knowledge, you cannot correctly write initialization code or debug hardware issues.

---

### Section 2: Development Environment Setup

---

### Lesson 004 --- Install an IDE and Blink an LED (Code Composer Studio + MSP430)

**File Path:** [Lesson_004_transcript.txt](Artful_Bytes_Transcript/4%20Install%20an%20IDE%20and%20Blink%20an%20LED%20(Code%20Composer%20Studio%20+%20MSP430)%20%20Embedded%20System%20Project%20Series%20%234.txt)

**Objective:** Sets up the vendor-provided IDE (Code Composer Studio) for the MSP430, compiles and flashes a blink LED example onto the LaunchPad evaluation board, and explains the fundamental concepts of cross-compilation, GPIO output, watchdog timers, and the role of vendor-provided header files.

**Terminology & Key Concepts:**
- **Code Composer Studio (CCS)**: Texas Instruments' Eclipse-based IDE for MSP430 and other TI microcontrollers. Free, includes the proprietary TI compiler toolchain, debugger, and project templates. Provides a GUI for building, flashing, and debugging.
- **Cross Tool Chain / Cross Compiler**: A compiler that runs on the host computer (x86/x64) but generates machine code for a different target architecture (MSP430). Needed because the MCU has a different CPU architecture than the development machine.
- **Evaluation Board (MSP430 LaunchPad)**: A development board with the MSP430G2553 MCU, onboard debugger, header pins, buttons, and LEDs. Used to evaluate the MCU's capabilities and prototype code before deploying to a custom PCB.
- **Watchdog Timer (WDT)**: A hardware timer enabled by default on the MSP430 that automatically resets the MCU if not periodically refreshed. Prevents the system from getting stuck. Must be explicitly stopped (`WDTCTL = WDTPW | WDTHOLD`) in simple programs that don't use it.
- **GPIO (General Purpose Input/Output)**: Microcontroller pins that can be configured as digital inputs or outputs. Blinking an LED means configuring a pin as output and toggling it between high (3.3V) and low (0V).
- **Vendor-Provided Header File (msp430.h)**: A header file from TI containing register definitions and bitfield macros for the specific MSP430 variant. Maps register names (e.g., `P1DIR`, `P1OUT`, `WDTCTL`) to their memory addresses.
- **Volatile Keyword**: Tells the compiler not to optimize away a variable. Used on the busy-wait loop counter to prevent the compiler from removing the delay loop as "dead code."

**Techniques & Methods:**
- **IDE-First Workflow**: Installing the vendor IDE first to get a quick baseline confirming that hardware, debugger, and compiler all work before attempting more advanced setups.
- **Blink LED as Validation**: The classic "hello world" of embedded systems --- blinking an LED confirms the entire toolchain (editor -> compiler -> linker -> flasher -> MCU -> GPIO -> LED) is working end-to-end.
- **XOR Toggle for GPIO**: Using `P1OUT ^= BIT0` to toggle a GPIO pin. XOR with the bit mask flips only that bit without affecting other pins on the same port.
- **Step Debugging**: CCS allows pausing execution, stepping through code line-by-line, and inspecting register values --- useful for understanding program flow and verifying register configurations.
- **Custom Installation**: Installing only the MSP430 component of CCS to save space and avoid unnecessary components.

**Source Code Mapping:**
- Blink LED example (CCS-provided example, not in nsumo codebase):
  ```c
  #include <msp430.h>

  int main(void)
  {
      volatile unsigned int i;
      WDTCTL = WDTPW | WDTHOLD;  // Stop watchdog timer
      P1DIR |= BIT0;              // Configure P1.0 as output
      while(1) {
          P1OUT ^= BIT0;          // Toggle P1.0 (LED)
          for(i = 0; i < 10000; i++);  // Busy-wait delay
      }
  }
  ```
- `WDTCTL`, `P1DIR`, `P1OUT`, `BIT0`: Defined in `msp430.h` vendor header. These map directly to hardware register addresses resolved at link time.

**Demo / Example:**
- **Goal:** Install CCS, import the blink LED example, compile it, flash it onto the LaunchPad, and observe the LED blinking.
- **Why Important:** Validates the entire development toolchain end-to-end. This is the first proof that the hardware and software environment are correctly configured.
- **Demo Flow:**
  1. Download and install Code Composer Studio (Linux version, custom install for MSP430 only).
  2. Launch CCS, search for MSP430G2553, import the blink LED example project.
  3. Install the MSP430Ware software package (contains example projects and register definitions).
  4. Connect the LaunchPad via USB (bridges in correct orientation).
  5. Build and flash the project --- debugger halts at main.
  6. Resume execution --- LED blinks on the LaunchPad.
  7. Pause execution --- LED stops. Step through code to observe the while loop and XOR toggle.
  8. Walk through the code: include msp430.h, stop WDT, set P1DIR for output, XOR toggle in while loop with busy-wait delay.

**New Tools Introduced:**
- **Code Composer Studio (CCS)** --- TI's IDE for MSP430 development (Eclipse-based, includes compiler, debugger, project templates)
- **MSP430 LaunchPad** --- evaluation board with onboard debugger for programming and debugging the MSP430G2553

**Discussion Prompts:**
- **Q1: Why stop the watchdog timer in the blink example?**
  - The MSP430's watchdog timer is enabled by default and will repeatedly reset the MCU if not stopped or periodically serviced. In simple examples that don't use the WDT for recovery, it must be explicitly stopped with `WDTCTL = WDTPW | WDTHOLD` to prevent the program from resetting during the busy-wait delay.
- **Q2: Why is the loop counter declared as `volatile`?**
  - Without `volatile`, the compiler's optimizer recognizes that the busy-wait loop performs no useful work and would eliminate it entirely. The `volatile` qualifier forces the compiler to execute the loop as written, preserving the delay. This is a common pattern in bare-metal embedded code.
- **Q3: Why set up the IDE first if the command-line workflow is preferred?**
  - The IDE provides a quick, reliable baseline. It confirms that hardware (LaunchPad), debugger, and compiler all work before investing effort in a custom Makefile-based setup. Additionally, the IDE's step debugger remains useful even when daily development uses the command line.

---

### Lesson 005 --- Microcontroller Programming without IDE (Makefile + Toolchain)

**File Path:** [Lesson_005_transcript.txt](Artful_Bytes_Transcript/5%20Microcontroller%20Programming%20without%20IDE%20(Makefile%20+%20Toolchain)%20%20Embedded%20System%20Project%20Series%20%235.txt)

**Objective:** Shows how to program an MSP430 without an IDE by installing the GCC cross-toolchain, invoking the compiler directly from the command line, and building a reusable Makefile from scratch --- establishing the command-line workflow used throughout the rest of the series.

**Terminology & Key Concepts:**
- **GCC (GNU Compiler Collection)**: The open-source, cross-platform compiler toolchain used instead of TI's proprietary compiler. Widely used (including the Linux kernel), well-documented, free, and transferable across projects and architectures.
- **Makefile**: A file that describes how to build a project (inputs -> recipe -> output). The `make` program processes it, tracking which files changed to avoid unnecessary recompilation. Acts as the build system for the project.
- **Cross-Compilation**: Compiling code on a host machine (x86) that will execute on a different target architecture (MSP430). Requires a cross toolchain with a cross compiler, cross linker, and target-specific libraries.
- **Linker Script**: A file (e.g., `msp430g2553.ld`) that describes the memory layout of the target MCU --- flash size, RAM size, peripheral addresses. Used by the linker to place code and data in the correct memory regions.
- **Compiler Flags**: Options passed to the compiler to control behavior. Key flags covered: `-mmcu=msp430g2553` (target MCU), `-I` (include search path), `-L` (linker search path), `-Wall -Wextra -Werror -Wshadow` (warnings), `-Og` (optimization for debugging), `-g` (debug symbols), `-c` (compile only, don't link).
- **Object File (.o)**: The intermediate output of compilation. Each source file compiles to an object file; the linker then combines all object files into the final executable.
- **Phony Target**: A Makefile target that doesn't produce a file (e.g., `clean`, `all`, `flash`). Marked as `.PHONY` to prevent Make from confusing it with an actual file of the same name.
- **Make Variables**: Named values in a Makefile (e.g., `CC`, `TARGET`, `CFLAGS`) that improve readability, maintainability, and reusability.
- **Make Functions**: Built-in functions like `addprefix`, `patsubst`, suffix replacement (`.c=.o`) used to transform file lists and reduce repetition.

**Techniques & Methods:**
- **Direct Compiler Invocation**: Running `msp430-elf-gcc` from the command line with explicit flags to understand what the IDE does "under the hood."
- **Incremental Makefile Construction**: Building the Makefile from scratch, step-by-step: simple one-rule file -> add variables -> separate compile/link stages -> pattern rules -> build directory -> phony targets -> flash rule.
- **Separate Compilation and Linking**: Using `-c` flag to compile each .c file to .o independently, then linking all .o files together. This is what enables Make's incremental rebuild capability.
- **Pattern Rules (%)**: Using `$(OBJ_DIR)/%.o: %.c` to define a single compilation rule that applies to all source files, avoiding repetition.
- **Automatic Variables ($@, $^)**: Using Make's special symbols: `$@` for the target, `$^` for all prerequisites --- making rules generic and reusable.
- **Build Directory Separation**: Generating all output files (objects, binary) in a `build/` directory to keep the source tree clean. Using `mkdir -p` with `@` prefix to silently create directories.
- **Modular File Organization**: Breaking the blink example into `main.c` and `led.c/led.h` to demonstrate multi-file compilation and the need for a build system.
- **Inspecting IDE Build Commands**: Using CCS console output to discover which compiler flags the IDE passes, then replicating them in the command-line workflow.

**Source Code Mapping:**
- `Makefile`: `Makefile` (nsumo_video project root) --- The production Makefile evolved from this lesson's foundation.
  ```makefile
  # Core structure shown in lesson
  CC = $(MSPGCC_BIN_DIR)/msp430-elf-gcc
  MCU = msp430g2553
  WFLAGS = -Wall -Wextra -Werror -Wshadow
  CFLAGS = -mmcu=$(MCU) $(WFLAGS) $(addprefix -I,$(INCLUDE_DIRS)) -Og -g
  LDFLAGS = -mmcu=$(MCU) $(addprefix -L,$(LIB_DIRS))

  $(TARGET): $(OBJECTS)
  	$(CC) $(LDFLAGS) $^ -o $@

  $(OBJ_DIR)/%.o: %.c
  	$(CC) $(CFLAGS) -c -o $@ $^
  ```
- `led_init()`, `led_toggle()`: Created in this lesson as separate `led.c/led.h` to demonstrate multi-file projects.
  ```c
  // led.h
  void led_init(void);
  void led_toggle(void);

  // led.c
  #include <msp430.h>
  #include "led.h"
  void led_init(void) { P1DIR |= BIT0; }
  void led_toggle(void) { P1OUT ^= BIT0; }
  ```

**Demo / Example:**
- **Goal:** Build and flash the blink LED project entirely from the command line using GCC and a custom Makefile.
- **Why Important:** Establishes the command-line workflow used for the entire series. Understanding the build process removes the IDE as a "black box" and enables build automation (CI/CD), editor freedom, and cross-project reusability.
- **Demo Flow:**
  1. Download and unpack the MSP430 GCC toolchain from TI's website.
  2. Add the toolchain bin directory to PATH.
  3. Attempt to compile the blink example with bare `msp430-elf-gcc main.c` --- encounter errors.
  4. Fix each error by adding flags: `-I` for include path (msp430.h), `-mmcu=msp430g2553` for target, `-L` for linker script path.
  5. Successful compilation produces `a.out`. Rename with `-o blink`.
  6. Inspect CCS build output to discover additional useful flags (`-Og`, `-g`, `-Wall`).
  7. Break blink into `main.c` + `led.c/led.h` to demonstrate multi-file compilation.
  8. Create Makefile from scratch: simple rule -> variables -> separated compile/link -> pattern rules -> build directory -> `all`/`clean`/`flash` phony targets.
  9. Run `make flash` to program the LaunchPad via mspdebug --- LED blinks.
  10. Verify by commenting out toggle line, reflashing --- LED stops.
- **What Changed:**
  - New `led.c` / `led.h` files created (module separation).
  - New `Makefile` created from scratch (entire build system).

**New Tools Introduced:**
- **msp430-elf-gcc** --- GCC cross compiler for MSP430 (open-source, replaces TI's proprietary compiler)
- **Make / Makefile** --- Build automation tool that tracks dependencies and rebuilds only what changed
- **mspdebug** --- Command-line tool for flashing firmware to MSP430 via the LaunchPad's onboard debugger
- **Vim** --- The editor used by the instructor (mentioned, not required)

**Discussion Prompts:**
- **Q1: Why use GCC instead of TI's proprietary compiler?**
  - GCC is open-source, free, widely used (Linux kernel), well-documented, and transferable across architectures. TI's compiler is MSP430-specific. Third-party compilers (IAR, Keil) may produce smaller/faster binaries but require paid licenses. For learning and hobby projects, GCC is the best choice.
- **Q2: What are the key advantages of a command-line workflow over an IDE?**
  - (1) Build automation / CI compatibility --- CI systems run commands, not GUI buttons. (2) Editor freedom --- use any editor you prefer. (3) Deeper understanding of the build process. (4) Reusability across projects and toolchains. (5) Customizability and scriptability.
- **Q3: Why not use CMake instead of Make?**
  - CMake generates build files (including Makefiles) and is powerful for cross-platform/multi-target projects. But for a small single-target MCU project, CMake is overkill. A plain Makefile is simpler, more direct, and sufficient. CMake would be worth considering if the project needed to build for multiple platforms or integrate with an IDE that parses CMakeLists.txt.

---

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

---

### Section 4: Development Workflow & Best Practices

---

### Lesson 008 --- How I Version Control with Git (Best Practices)

**File Path:** [Lesson_008_transcript.txt](Artful_Bytes_Transcript/8%20How%20I%20version%20control%20with%20git%20(Best%20Practices)%20%20Embedded%20System%20Project%20Series%20%238.txt)

**Objective:** Initializes the nsumo git repository, makes the first commit (project skeleton), adds the printf submodule, and establishes git best practices including commit conventions, commit message formatting, and a branching workflow that will be used throughout the series.

**Terminology & Key Concepts:**
- **Git**: A distributed version control system (created by Linus Torvalds) that tracks changes as commits, maintains a complete history, and enables collaboration. The de facto standard for software projects.
- **Commit**: A snapshot of changes with a unique SHA-1 hash, an author, a timestamp, and a message describing what changed. Commits are the building blocks of a project's history.
- **Conventional Commits**: A commit message convention that structures messages as: `type(scope): description` on the subject line, followed by a body explaining *why*, and an optional footer for metadata. Types include `feat`, `fix`, `build`, `docs`, etc.
- **Git Submodule**: A mechanism to embed one git repository inside another at a pinned commit. Used to include the external printf library while preserving its origin and version.
- **`.gitignore`**: A file listing patterns of files/directories that git should not track. For this project, the `build/` directory is gitignored because its contents are generated artifacts.
- **Repository Hosting (GitHub)**: A platform for hosting git repositories remotely, enabling backup, collaboration, pull requests, and CI/CD integration.
- **Agile Mindset / Incremental Development**: The philosophy of delivering small, well-defined, working increments rather than large monolithic changes. Aligns with small, frequent commits.

**Techniques & Methods:**
- **Commit Rules (Three Rules)**:
  1. Each commit contains only one change (single feature, fix, or logical unit).
  2. Each commit must build successfully (and pass static analysis).
  3. Each commit has a good message explaining what and especially *why*.
- **Conventional Commit Message Format**:
  ```
  type(scope): short description (max 50 chars)

  Body: explain WHY this change is needed,
  not just what it does. Motivate the change
  to a potential reviewer or future self.

  Footer: video name, issue number, etc.
  ```
- **Imperative Mood**: Write "Add feature" not "Added feature" or "Adding feature." Think of the commit as something to be applied.
- **Command-Line Git**: Using git exclusively from the terminal (`git init`, `git add`, `git commit`, `git push`, `git log`, `git config --local`). Editor plugins (Vim + fugitive) supplement but don't replace CLI usage.
- **Local Git Configuration**: Using `git config --local` to set username and email per-repository rather than relying on global configuration.
- **Feature-per-Video Workflow**: Each video covers one module or feature, resulting in one or more well-defined commits that map cleanly to the video series progression.

**Source Code Mapping:**
- First commit message example:
  ```
  build: set project structure and add initial files

  Fill the project directory with all the required directories
  to immediately clarify the project structure to be used
  throughout the project series. Some placeholder files added
  because otherwise git won't pick up the directories.

  Video: How I Version Control with Git (Best Practices)
  ```
- Second commit message example:
  ```
  feat(external): add stripped-down printf implementation

  The printf implementation part of the standard library is too
  large for a small microcontroller, so use an external stripped-down
  implementation. Added unchanged as a submodule for better tracking.

  Video: How I Version Control with Git (Best Practices)
  ```

**Demo / Example:**
- **Goal:** Initialize the repository, make the first two commits following best practices, and push to GitHub.
- **Why Important:** Establishes the version control workflow and commit conventions that will be followed for the entire project. Good git practices are a professional necessity and improve project traceability.
- **Demo Flow:**
  1. Verify the project builds with `make` before committing.
  2. `git init` to initialize the repository.
  3. `git config --local user.name` and `user.email` for per-repo config.
  4. `git add .` to stage all files (`.gitignore` excludes `build/`).
  5. `git commit` with a Conventional Commits message (type: `build`, no scope, body explains why).
  6. Add GitHub remote, push to GitHub. README images render nicely on GitHub.
  7. Second commit: `git submodule add` the printf library under `external/printf`. Commit with type `feat`, scope `external`, body explains why the standard printf is too large.
  8. `git push`, verify both commits appear in `git log`.

**New Tools Introduced:**
- **Git** --- distributed version control system (command-line usage)
- **GitHub** --- repository hosting platform for remote backup, collaboration, and CI

**Discussion Prompts:**
- **Q1: Why focus on commit message quality for a solo project?**
  - Even as a sole developer, good commit messages serve as documentation of your decision-making process. When revisiting code weeks or months later, a well-written commit message explains *why* a change was made, not just what changed. It also builds the habit needed for professional collaborative development.
- **Q2: Why prefer many small commits over few large ones?**
  - Small commits are easier to review (including self-review), easier to revert if something breaks, create a more granular history for `git bisect`, and align with an agile workflow of incremental progress. Large commits often mix unrelated changes, making them harder to understand and debug.
- **Q3: Why use git submodules for the printf library?**
  - Submodules preserve the connection to the upstream repository and pin to a specific commit. This makes it clear where the code came from, which version is in use, and avoids modifying third-party code. Alternatives (copy-paste, package managers) lose this traceability.

---

### Lesson 009 --- Static Analysis for C/C++ with cppcheck (+Makefile)

**File Path:** [Lesson_009_transcript.txt](Artful_Bytes_Transcript/9%20Static%20Analysis%20for%20CC+%20with%20cppcheck%20(+Makefile)%20%20Embedded%20System%20Project%20Series%20%239.txt)

**Objective:** Introduces static analysis using cppcheck to catch bugs that the compiler misses, demonstrates running it from the command line and integrating it into the Makefile as a `make cppcheck` rule for convenient project-wide analysis.

**Terminology & Key Concepts:**
- **Static Analysis**: Analyzing source code without executing it to find potential bugs, code quality issues, and violations. Complements compiler warnings by catching deeper issues like out-of-bounds array access, unused functions, null pointer dereferences, etc.
- **cppcheck**: A free, open-source static analyzer for C and C++. Available in Ubuntu's standard repository via `sudo apt install cppcheck`. Catches errors the compiler does not, such as buffer overflows and unused code.
- **Error Exit Code (`--error-exitcode=1`)**: A cppcheck flag that makes the tool return a non-zero exit code when errors are found. Critical for CI integration --- the CI pipeline can fail if static analysis detects issues.
- **Inline Suppression**: A way to suppress specific cppcheck warnings directly in the source code using `// cppcheck-suppress unusedFunction` comments, combined with the `--inline-suppr` flag.
- **Command-Line Suppression (`--suppress`)**: Suppressing specific warnings via command-line flags, optionally scoped to a specific file and line number. E.g., `--suppress=unusedFunction:main.c:5`.
- **Enable All Checks (`--enable=all`)**: Enables all cppcheck analysis categories (style, performance, portability, etc.) beyond just errors. More comprehensive but may produce more warnings.

**Techniques & Methods:**
- **Running cppcheck on Individual Files**: `cppcheck --quiet --enable=all --error-exitcode=1 main.c` for quick single-file analysis.
- **Running cppcheck on Directories**: `cppcheck src/` to recursively analyze all files in a directory. Use `-I` flag to add include directories for header resolution.
- **Makefile Integration**: Adding a `cppcheck` phony target to the Makefile for one-command project-wide analysis.
  ```makefile
  cppcheck:
  	@$(CPPCHECK) $(CPPCHECK_FLAGS) $(SOURCES_FORMAT_CPPCHECK)
  ```
- **Suppression Strategies**: Three levels of suppression: (1) inline `// cppcheck-suppress` in source, (2) `--suppress=errorId:file:line` on command line, (3) `--suppress=errorId` globally. Use judiciously --- suppress only when the warning is a false positive or intentional.
- **Excluding External Code**: Using `-i` flag to exclude directories (like `external/printf/`) from analysis, since third-party code should not be modified.

**Source Code Mapping:**
- `Makefile:116-130` --- cppcheck configuration in the production Makefile:
  ```makefile
  CPPCHECK_INCLUDES = ./src ./
  CPPCHECK_FLAGS = \
  	--quiet --enable=all --error-exitcode=1 \
  	--inline-suppr \
  	--suppress=missingIncludeSystem \
  	--suppress=unmatchedSuppression \
  	--suppress=unusedFunction \
  	$(addprefix -I,$(CPPCHECK_INCLUDES))
  ```
- `Makefile:160-161` --- The cppcheck phony target:
  ```makefile
  cppcheck:
  	@$(CPPCHECK) $(CPPCHECK_FLAGS) $(SOURCES_FORMAT_CPPCHECK)
  ```

**Demo / Example:**
- **Goal:** Install cppcheck, demonstrate it catching bugs the compiler misses, and integrate it into the Makefile.
- **Why Important:** Static analysis catches bugs earlier in the development cycle, before they become runtime errors. Integrating it into the Makefile (and later CI) makes it effortless to run and impossible to skip.
- **Demo Flow:**
  1. Install cppcheck: `sudo apt install cppcheck`.
  2. Create a C file with an intentional out-of-bounds array access. Run cppcheck --- it detects the error.
  3. Fix the array error, add an unused function. Run cppcheck with `--enable=all` --- it detects the unused function.
  4. Demonstrate suppression: `--suppress=unusedFunction:main.c` and inline `// cppcheck-suppress unusedFunction`.
  5. Add `cppcheck` phony target to the Makefile with all flags.
  6. Exclude `external/` directory with `-i external/` to avoid analyzing third-party code.
  7. Run `make cppcheck` --- clean output with no errors.
  8. Commit the Makefile changes.

**New Tools Introduced:**
- **cppcheck** --- free, open-source static analyzer for C/C++ that catches bugs the compiler misses

**Discussion Prompts:**
- **Q1: Why use static analysis in addition to compiler warnings?**
  - Compilers focus on language correctness (syntax, types, linking). Static analyzers perform deeper semantic analysis --- detecting buffer overflows, null dereferences, unused code, resource leaks, and logic errors that compile without warnings but cause runtime bugs.
- **Q2: Should you fix all cppcheck warnings or suppress some?**
  - Fix genuine issues. Suppress only false positives (e.g., unused functions that will be used in future commits, system header warnings). The `--suppress=unusedFunction` in this project is used because functions are added incrementally across videos --- they may appear unused in early commits but are used later.

---

### Lesson 010 --- Simple CI/CD with GitHub Actions and Docker (Compile + Analysis)

**File Path:** [Lesson_010_transcript.txt](Artful_Bytes_Transcript/10%20Simple%20CICD%20with%20GitHub%20Actions%20and%20Docker%20(Compile+Analysis)%20%20%20Embedded%20System%20Project%20Series%20%2310.txt)

**Objective:** Sets up a continuous integration (CI) pipeline using GitHub Actions and Docker to automatically build the project and run static analysis on every push, establishing a workflow where code must pass CI before merging to the main branch.

**Terminology & Key Concepts:**
- **Continuous Integration (CI)**: The practice of automatically building, analyzing, and testing code on every commit/push to catch integration errors early. Prevents broken code from reaching the main branch.
- **GitHub Actions**: GitHub's built-in CI/CD platform. Workflows are defined in YAML configuration files under `.github/workflows/`. Jobs run on GitHub's servers, triggered by events like pushes or pull requests.
- **Docker Container**: A lightweight, reproducible environment that packages an OS, tools, and dependencies. Used here to package the MSP430 GCC toolchain so the CI system has a consistent, reproducible build environment.
- **Docker Hub**: A hosting platform for Docker container images (analogous to GitHub for git repositories). The instructor pushes the custom MSP430 toolchain container to Docker Hub so GitHub Actions can pull it.
- **Dockerfile**: A script defining how to build a Docker image. Specifies the base OS (Ubuntu 22.04), installs tools (wget, unzip), and sets up the user environment.
- **Pull Request (PR)**: A GitHub feature for proposing changes. The developer pushes a branch, opens a PR, CI runs automatically, and the PR can only be merged if CI passes.
- **Branch Protection Rules**: GitHub settings that enforce policies on the main branch: require PRs before merging, require CI checks to pass, prevent direct pushes.
- **Environment Variable (`TOOLS_PATH`)**: A variable passed to the Makefile at build time to specify the path to the toolchain. Makes the Makefile portable across different environments (local machine vs. Docker container).
- **Rebase and Merge**: A merge strategy that replays commits on top of the main branch without creating a merge commit, resulting in a cleaner linear history.

**Techniques & Methods:**
- **Docker for Toolchain Encapsulation**: The MSP430 GCC cross-toolchain is not available in standard OS package repositories and is too large to commit to git. A Docker container solves both problems --- it encapsulates the toolchain in a reusable, shareable image.
- **CI Pipeline Design**: Three checks executed sequentially on every push: (1) format check, (2) static analysis, (3) build. If any step fails, the pipeline fails and the PR cannot be merged.
- **Branch-Based Development Workflow**:
  1. Create a local feature branch (`git checkout -b feature-name`).
  2. Make code changes, build, and test locally.
  3. Commit and push the branch to GitHub.
  4. Open a pull request.
  5. CI runs automatically; review the PR diff.
  6. If CI passes, merge (rebase and merge for clean history).
- **Environment Variable for Portability**: Using `TOOLS_PATH` environment variable instead of hardcoded paths in the Makefile, allowing the same Makefile to work on the developer's local machine and inside the Docker container.
- **Branch Protection**: Configuring GitHub to require CI checks to pass before allowing merges to main. Also disabling direct pushes to main --- all changes must go through PRs.
- **Self-Review via PR**: Even as a sole developer, reviewing your own PR diff in GitHub's interface helps catch issues you might miss in your editor.

**Source Code Mapping:**
- `.github/workflows/ci.yml` --- The CI configuration file:
  ```yaml
  on: [push]
  jobs:
    build_and_static_analysis:
      runs-on: ubuntu-latest
      container:
        image: artfulbytes/msp430-gcc-9.3.1.11:latest
      env:
        TOOLS_PATH: /home/ubuntu/dev/tools
      steps:
        - name: Checkout the repository
          uses: actions/checkout@v3
          with:
            submodules: "true"
        - run: make format && git diff --quiet
        - run: make cppcheck
        - run: make HW=NSUMO
        - run: make HW=LAUNCHPAD
        - run: make tests
  ```
- `Makefile:26` --- `TOOLS_DIR = ${TOOLS_PATH}` --- Reads the toolchain path from an environment variable instead of hardcoding it.
- `tools/dockerfile` --- Docker image definition (Ubuntu 22.04 base, wget, unzip, user setup).

**Demo / Example:**
- **Goal:** Create a Docker container with the MSP430 toolchain, configure GitHub Actions to run CI on every push, and set up branch protection rules.
- **Why Important:** CI prevents broken code from reaching the main branch. Even for a one-person project, it enforces discipline and catches errors automatically. The setup is reusable for any MSP430 project.
- **Demo Flow:**
  1. Install Docker, create Docker group for non-root access.
  2. Create Dockerfile under `tools/`: base Ubuntu 22.04, install wget/unzip.
  3. Build Docker image, log in, download MSP430 GCC toolchain and support files from TI's website using wget.
  4. Unpack and organize toolchain inside the container, commit the Docker image.
  5. Push the image to Docker Hub as `artfulbytes/msp430-gcc-9.3.1.11:latest`.
  6. Create `.github/workflows/ci.yml`: trigger on push, run in Docker container, checkout repo, run `make` and `make cppcheck`.
  7. Commit and push --- CI fails (indentation error in YAML). Fix and force-push.
  8. Set up branch protection rules on GitHub: require PR, require CI status checks, disallow bypass.
  9. Demonstrate that pushing directly to main is now blocked.
  10. Update Makefile to use `TOOLS_PATH` environment variable. Update CI config to set `TOOLS_PATH` for the Docker container.
  11. Create branch, commit, push, open PR --- CI passes --- merge with rebase.
- **What Changed:**
  - `Makefile`: `TOOLS_DIR` now reads from `${TOOLS_PATH}` environment variable.
  - `.github/workflows/ci.yml`: New CI configuration file.
  - `tools/dockerfile`: New Dockerfile for the MSP430 toolchain container.

**New Tools Introduced:**
- **GitHub Actions** --- CI/CD platform integrated with GitHub for automated build/test/analysis pipelines
- **Docker** --- containerization platform for creating reproducible build environments
- **Docker Hub** --- hosting platform for Docker container images

**Discussion Prompts:**
- **Q1: Why use Docker for CI instead of installing the toolchain directly in the GitHub Actions VM?**
  - (1) The toolchain download URL from TI may break when they update versions. (2) Downloading ~500MB+ on every CI run is wasteful. (3) A Docker container provides a consistent, reproducible environment that matches local development. (4) The container can be reused across multiple projects.
- **Q2: Is CI overkill for a one-person project?**
  - Yes, in terms of strict necessity. But it enforces discipline, catches mistakes automatically, and teaches professional practices. The instructor acknowledges this is "overkill" but justifies it as part of the series' goal to demonstrate professional development practices.
- **Q3: Why use rebase-and-merge instead of regular merge commits?**
  - Rebase-and-merge adds the PR's commits directly on top of the main branch, creating a clean linear history without merge commits. This makes `git log` easier to read and `git bisect` more effective. Regular merge commits add noise to the history for simple single-commit PRs.

---

### Lesson 011 --- Documentation and Clang Format (+2 Bugs)

**File Path:** [Lesson_011_transcript.txt](Artful_Bytes_Transcript/11%20Documentation%20and%20Clang%20format%20(+2%20bugs)%20%20%20Embedded%20System%20Project%20Series%20%2311.txt)

**Objective:** Covers four commits: adding project documentation (README, coding guidelines), integrating clang-format into the Makefile and CI pipeline, fixing a Makefile bug where header file changes were not triggering rebuilds, and fixing a cppcheck performance issue caused by the vendor header file.

**Terminology & Key Concepts:**
- **README.md**: The primary documentation file for the project. Contains a project introduction, directory structure description, setup instructions, build commands, and workflow description. Rendered by GitHub on the repository page.
- **Coding Guidelines (`docs/coding_guidelines.md`)**: A document describing the coding conventions followed in the project: snake_case naming, 4-space indentation, module-prefixed functions, fixed-width integers, typedef rules for enums (suffix `_e`, don't typedef structs, don't use `_t`), include order (local -> project -> system), always use `{}` for if/else, `void` in empty parameter lists, `static` for internal functions, const correctness.
- **Clang-format**: An auto-formatter for C/C++ built on LLVM/Clang. Enforces consistent code formatting (indentation, brace style, line width) based on a `.clang-format` configuration file. Version 12 is used.
- **`.clang-format` Configuration**: Defines the formatting rules. Based on WebKit style with customizations: 100-character column limit, Allman-style braces for functions/structs/classes, K&R-style for control statements, 4-space indent, no tab, pointer binds to variable not type.
- **Makefile Header Dependency Bug**: The original Makefile only listed `.c` files as prerequisites for the build target. Modifying a `.h` file did not trigger a rebuild because Make was unaware of the dependency. Fixed by adding header files to the dependency list.
- **cppcheck Slowness Bug**: cppcheck became extremely slow when analyzing `msp430.h`, which contains thousands of `#ifdef` branches. Fixed by excluding the vendor header from cppcheck's analysis scope.
- **`git diff --quiet`**: A command that returns non-zero if there are uncommitted changes. Used in CI to detect if `make format` produced any changes --- if so, the code was not properly formatted before committing.

**Techniques & Methods:**
- **Formatting as CI Gate**: Adding `make format && git diff --quiet` as the first CI step. If any file is unformatted, `make format` reformats it, `git diff --quiet` detects the change, and CI fails. This prevents unformatted code from being merged.
- **Makefile Format Rule**: Adding a `format` phony target that runs clang-format on all project source and header files in one command.
  ```makefile
  format:
  	@$(FORMAT) -i $(SOURCES_FORMAT_CPPCHECK) $(HEADERS_FORMAT)
  ```
- **Header File Dependency Fix**: Deriving the list of header files from the source file list using suffix replacement (`.c=.h`), then adding headers as prerequisites to the build rule.
  ```makefile
  HEADERS = $(SOURCES_WITH_HEADERS:.c=.h) src/common/defines.h
  $(TARGET): $(OBJECTS) $(HEADERS)
  ```
- **cppcheck Performance Fix**: Separating the include paths for cppcheck (`CPPCHECK_INCLUDES = ./src ./`) from the compiler's include paths (which include the vendor header directory). This prevents cppcheck from analyzing the massive `msp430.h` file.
- **Suppression for System Headers**: Adding `--suppress=missingIncludeSystem` to avoid warnings about system headers that cppcheck cannot find.
- **Docker Image Update**: Updating the Dockerfile to include `clang-format-12` and `git` so the CI container can run formatting checks.
- **Four-Commit Workflow**: Each of the four changes (docs, clang-format, header bug fix, cppcheck bug fix) is a separate commit with its own branch, PR, and CI run --- demonstrating the disciplined workflow from Lesson 10.

**Source Code Mapping:**
- `Makefile:163-164` --- Format rule:
  ```makefile
  format:
  	@$(FORMAT) -i $(SOURCES_FORMAT_CPPCHECK) $(HEADERS_FORMAT)
  ```
- `Makefile:98-101` --- Header derivation from sources:
  ```makefile
  HEADERS = \
  	$(SOURCES_WITH_HEADERS:.c=.h) \
  	src/common/defines.h \
  ```
- `Makefile:139` --- Build rule with header dependencies:
  ```makefile
  $(TARGET): $(OBJECTS) $(HEADERS)
  ```
- `.clang-format` --- Formatting configuration:
  ```yaml
  BasedOnStyle: WebKit
  Language: Cpp
  ColumnLimit: 100
  BreakBeforeBraces: Custom
  BraceWrapping:
      AfterFunction: true
      AfterControlStatement: false
  AllowShortFunctionsOnASingleLine: Empty
  SortIncludes: false
  ```
- `docs/coding_guidelines.md` --- Key guidelines:
  - snake_case for files, functions, variables; UPPER_CASE for defines
  - Prefix functions with module name: `uart_init()`, `i2c_read()`
  - One module = one `.c/.h` pair
  - 4-space indent, no tabs
  - Always use `{}` for if/else
  - `void` in empty parameter lists
  - Internal functions must be `static`
  - Fixed-width integers (`uint8_t`, `uint16_t`)
  - Typedef enums with `_e` suffix; do NOT typedef structs or use `_t`
  - Include order: local -> project -> system
- `.github/workflows/ci.yml:14` --- Format check in CI pipeline:
  ```yaml
  - run: make format && git diff --quiet
  ```

**Demo / Example:**
- **Goal:** Add documentation, integrate clang-format into the build and CI pipeline, and fix two build system bugs.
- **Why Important:** Documentation makes the project accessible to others. Automated formatting eliminates style debates and ensures consistency. The bug fixes demonstrate real-world Makefile debugging --- exactly the kind of issues developers encounter when building their own build systems.
- **Demo Flow:**
  **Commit 1 --- Documentation:**
  1. Create README.md with project intro, directory structure, setup instructions, workflow.
  2. Create `docs/coding_guidelines.md` with all naming, formatting, and coding conventions.
  3. Add `.compile_commands.json` and `.cache` to `.gitignore` (editor-generated files).
  4. Branch, commit (type: `docs`), push, PR, CI passes, merge.

  **Commit 2 --- Clang-format Integration:**
  1. Add `format` phony target to Makefile: `clang-format-12 -i` on all source and header files.
  2. Update Dockerfile to install `clang-format-12` and `git`.
  3. Add `make format && git diff --quiet` as first CI step.
  4. Demonstrate locally: modify a file, `git diff` returns error; run `make format`, `git diff` returns zero.
  5. Branch, commit, push, PR, CI passes, merge.

  **Commit 3 --- Header Dependency Bug Fix:**
  1. Problem: modifying a `.h` file and running `make` says "up to date" --- the bug is not detected until a clean rebuild.
  2. Root cause: header files were not listed as prerequisites in the Makefile.
  3. Fix: create `HEADERS` variable from `SOURCES_WITH_HEADERS` using `.c=.h` substitution, add to build rule dependencies.
  4. Verify: modify a header, run `make` --- rebuild triggered, compilation error detected.
  5. Branch, commit, push, PR, CI passes, merge.

  **Commit 4 --- cppcheck Performance Bug Fix:**
  1. Problem: `make cppcheck` takes minutes instead of seconds after adding code.
  2. Root cause: cppcheck was analyzing `msp430.h`, which has thousands of `#ifdef` branches.
  3. Fix: use separate include paths for cppcheck (`CPPCHECK_INCLUDES = ./src ./`) that exclude the vendor header directory.
  4. Add suppressions: `missingIncludeSystem`, `unmatchedSuppression`, `unusedFunction`.
  5. Also fix `make cppcheck` error on second run by adding `-p` flag to `mkdir`.
  6. Branch, commit, push, PR, CI passes, merge.
- **What Changed:**
  - `README.md`: Complete project documentation.
  - `docs/coding_guidelines.md`: New coding conventions document.
  - `Makefile`: Added `format` target, fixed header dependencies, fixed cppcheck include paths and suppressions.
  - `.github/workflows/ci.yml`: Added format check step.
  - `tools/dockerfile`: Added `clang-format-12` and `git` packages.
  - `.gitignore`: Added editor-generated files.

**New Tools Introduced:**
- **clang-format (v12)** --- auto-formatter for C/C++ that enforces consistent coding style based on a configuration file

**Discussion Prompts:**
- **Q1: Why automate code formatting instead of relying on developers to format manually?**
  - Manual formatting is inconsistent, error-prone, and leads to style debates during code reviews. An auto-formatter applied via CI ensures every file in the repository follows the same style. Developers never have to think about formatting --- just run `make format` before committing, or let CI catch it.
- **Q2: Why was the header dependency bug significant?**
  - Without header files in the Makefile's dependency list, modifying a struct definition, changing a constant in `defines.h`, or altering a function signature in a header would not trigger a rebuild. The developer would run `make`, see "up to date," and believe the code is correct --- but the binary would contain the old definitions. This could cause subtle, hard-to-debug runtime errors. Only a `make clean && make` would catch it, which defeats Make's purpose.
- **Q3: Why did cppcheck become slow on the vendor header file?**
  - The `msp430.h` header contains hundreds of `#ifdef` blocks (one for each MSP430 variant). cppcheck attempts to analyze all possible preprocessing paths, leading to combinatorial explosion. Since the vendor header is trusted and unmodifiable, excluding it from analysis is the correct approach.

---

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

---

### Section 6: Motor Control & PWM

### Lesson 21 — Motor Control with PWM in C

**File Path:** [21 20 Motor Control with PWM in C  Embedded System Project Series #21.txt](Artful_Bytes_Transcript/21%2020%20Motor%20Control%20with%20PWM%20in%20C%20%20Embedded%20System%20Project%20Series%20%2321.txt)

**Objective:** Teaches how to control DC motors using Pulse Width Modulation (PWM) on a microcontroller that lacks dedicated PWM hardware, implementing a three-layer abstraction from timer peripheral up through motor driver to application-level drive interface.

**Terminology & Key Concepts:**
- **Pulse Width Modulation (PWM)**: A method of toggling a pin on and off at a set duty cycle ratio to produce an effective average voltage. Used to control motor speed and LED brightness.
- **Duty Cycle**: The percentage of time a PWM signal is HIGH during one period. A 70% duty cycle on a 7.4V signal yields an average of ~5.2V.
- **Capture/Compare Register (CCR)**: Timer peripheral registers that can be configured to trigger outputs at specific count values, enabling hardware-timed PWM generation.
- **Motor Driver (H-Bridge)**: An external IC (TB6612FNG) that takes low-current control signals from the MCU and drives high-current motors. Accepts two direction control pins and one PWM speed input.
- **Skid Steering**: A driving method where motors on each side always run at the same speed and direction; turning is achieved by running sides at different speeds or opposite directions.
- **Out Mode 7 (Reset/Set)**: Timer capture/compare output mode where the output goes HIGH from count 0 to the CCR value, then LOW for the rest of the period.
- **Base Frequency**: The PWM switching frequency (20 kHz chosen here) -- must be 1-20 kHz for stable DC motor behavior; below 1 kHz, motors visibly speed up and slow down with each cycle.

| Concept | Details |
|---|---|
| MCU | MSP430G2553 -- no dedicated PWM peripheral |
| Timer Used | Timer A0 (Timer A1 reserved for IR remote) |
| PWM Frequency | 20,000 Hz (20 kHz) |
| Clock Source | SMCLK (16 MHz) with input divider /8 = 2 MHz |
| Period Ticks | 2,000,000 / 20,000 = 100 ticks (duty cycle % maps 1:1) |
| PWM Channels | 2 (one per motor driver: left, right) |
| CC Registers | TA0CCR0 = base period (99), TA0CCR1 = left PWM, TA0CCR2 = right PWM |
| Duty Cycle Scaling | Scaled down by 25% (multiply by 3, divide by 4) because battery is ~8V but motors rated for 6V max |
| Motor Driver IC | TB6612FNG -- CC1/CC2 pins set direction (forward/reverse/stop), PWM pin sets speed |
| Drive Directions | Forward, Reverse, Rotate Left/Right, Arc Turn Sharp/Mid/Wide Left/Right |
| Drive Speeds | Slow (25%), Medium (45-50%), Fast (55-60%), Max (100%) |

**Techniques & Methods:**
- **Timer-based PWM emulation**: Using Timer A0's three capture/compare channels -- CCR0 for the base period, CCR1 and CCR2 for two independent PWM outputs. Setting OUTMOD_7 (Reset/Set) on a channel makes it output HIGH from count 0 to the CCR value, then LOW for the remainder.
- **Duty cycle scaling for voltage protection**: Multiplying duty cycle by 3/4 to prevent overdriving 6V-rated motors with an 8V battery. Division by 4 compiles to a bit shift, avoiding expensive hardware division on MSP430.
- **Three-layer abstraction (PWM -> Motor Driver -> Drive)**: PWM driver handles timer peripheral configuration, TB6612FNG driver adds direction control via GPIO pins, and Drive module provides a simplified application-level interface with discrete directions and speed levels.
- **Primary direction optimization**: Only storing speed values for "primary" directions (forward, rotate_left, arcturn_sharp_left, etc.) and deriving opposite directions by inverting or swapping left/right speeds. Saves flash space and eliminates duplicate data.
- **Power-saving channel management**: Disabling individual PWM channels (OUTMOD_0) when duty cycle is 0, and stopping the entire timer peripheral (MC_0) when all channels are disabled.
- **Assert-based motor safety**: Adding motor stop code to the assert handler so motors shut off immediately on any assertion failure, preventing the robot from driving uncontrolled into walls.

**Source Code Mapping:**
- `pwm_init()`: `pwm.c:113` -- Configures Timer A0 with SMCLK, divider /8, and sets period to 99 ticks. Asserts IO pin configuration matches expected PWM mux settings.
  ```c
  TA0CTL = TASSEL_2 + ID_3 + MC_0;
  TA0CCR0 = PWM_TA0CCR0;
  ```
- `pwm_set_duty_cycle()`: `pwm.c:89` -- Sets the CCR value for a given channel. Scales duty cycle by 75%, enables/disables channels as needed.
  ```c
  const bool enable = duty_cycle_percent > 0;
  if (enable) {
      *pwm_cfgs[pwm].ccr = pwm_scale_duty_cycle(duty_cycle_percent);
  }
  pwm_channel_enable(pwm, enable);
  ```
- `pwm_channel_enable()`: `pwm.c:66` -- Toggles a PWM channel on/off by writing OUTMOD_7 (Reset/Set) or OUTMOD_0 (Off) to the channel's control register.
  ```c
  *pwm_cfgs[pwm].cctl = enable ? OUTMOD_7 : OUTMOD_0;
  ```
- `pwm_scale_duty_cycle()`: `pwm.c:81` -- Reduces duty cycle by 25% to protect 6V motors from 8V battery. Ensures result is never 0 for non-zero input.
  ```c
  return duty_cycle_percent == 1 ? duty_cycle_percent : duty_cycle_percent * 3 / 4;
  ```
- `tb6612fng_set_mode()`: `tb6612fng.c:23` -- Sets motor direction by writing HIGH/LOW to the two control pins per motor driver.
  ```c
  case TB6612FNG_MODE_FORWARD:
      io_set_out(tb6612fng_cc_pins[tb].cc1, IO_OUT_HIGH);
      io_set_out(tb6612fng_cc_pins[tb].cc2, IO_OUT_LOW);
      break;
  ```
- `tb6612fng_set_pwm()`: `tb6612fng.c:43` -- Passes duty cycle through to the PWM driver, casting the motor driver enum to the PWM channel enum.
  ```c
  pwm_set_duty_cycle((pwm_e)tb, duty_cycle);
  ```
- `drive_set()`: `drive.c:71` -- Maps a direction + speed enum pair to specific left/right duty cycles using a lookup table, then sets motor driver mode and PWM accordingly.
  ```c
  drive_dir_e primary_direction = DRIVE_PRIMARY_DIRECTION(direction);
  int8_t speed_left = drive_primary_speeds[primary_direction][speed].left;
  int8_t speed_right = drive_primary_speeds[primary_direction][speed].right;
  if (direction != primary_direction) {
      drive_inverse_speeds(&speed_left, &speed_right);
  }
  ```
- `drive_stop()`: `drive.c:90` -- Stops both motor drivers by setting mode to STOP and duty cycle to 0.
- `drive_inverse_speeds()`: `drive.c:58` -- For non-primary directions: if speeds are equal (forward/reverse), negates both; if unequal (turning), swaps left and right values.

**Demo / Example:**
- **Goal:** Demonstrate PWM output at multiple duty cycles, then verify motor direction control, then test full drive interface with IR remote control.
- **Why Important:** Validates the entire three-layer motor control stack from timer registers up to application-level direction/speed commands before deployment on the actual robot.
- **Demo Flow:**
  1. PWM test: Cycle through duty cycles (100%, 75%, 50%, 25%, 1%, 0%) and verify output voltage with multimeter and oscilloscope. At 100% duty cycle (scaled to 75%), output reads ~2.4V from 3.3V MCU pin. Oscilloscope confirms 20 kHz base frequency.
  2. Motor driver test: Connect a DC motor via TB6612FNG H-bridge. Cycle through forward/reverse modes at various duty cycles. Motor spins CW/CCW at corresponding speeds and stops between transitions.
  3. Drive interface test: Use IR remote to control direction (up=forward, down=reverse, left=rotate left, right=rotate right) and speed (buttons 1-4 for slow to max). Motor responds to each remote command.
  4. Assert safety test: Drive forward for 3 seconds, then trigger an assertion. Motors stop immediately and LED blinks to indicate the assert condition.
- **What Changed:**
  - `pwm.c` / `pwm.h`: New PWM driver using Timer A0 with two channels, 20 kHz base frequency, duty cycle scaling
  - `tb6612fng.c` / `tb6612fng.h`: New motor driver layer controlling direction pins and delegating speed to PWM driver
  - `drive.c` / `drive.h`: New application-layer drive interface with discrete directions (10 options) and speeds (4 levels)
  - `assert_handler.c`: Added motor stop on assertion -- directly writes GPIO registers LOW to disable all motor driver pins without depending on any other module
  - `Makefile`: Added new source files to build
  - `io.c`: Assigned PWM and motor control pins for both Launchpad and nsumo targets
  - `defines.h`: Moved SMCLK and timer input divider defines to common location
- **Related Code:**
  ```c
  // PWM period calculation with static assertion
  #define PWM_TIMER_FREQ_HZ (SMCLK / TIMER_INPUT_DIVIDER_3)
  #define PWM_PERIOD_FREQ_HZ (20000)
  #define PWM_PERIOD_TICKS (PWM_TIMER_FREQ_HZ / PWM_PERIOD_FREQ_HZ)
  static_assert(PWM_PERIOD_TICKS == 100, "Expect 100 ticks per period");
  ```

**Discussion Prompts:**
- **Q1: Why was 20 kHz chosen as the PWM frequency rather than a lower frequency like 1 kHz?**
  - Two reasons: (1) At frequencies below ~1 kHz, the motor sees individual voltage pulses rather than a smooth average voltage, causing it to visibly speed up and slow down with each pulse. At 20 kHz, the switching is fast enough that the motor's mechanical inertia smooths the pulses into steady rotation. (2) With a 2 MHz timer clock (16 MHz SMCLK / 8 divider), 20 kHz yields exactly 100 ticks per period. This means duty cycle percentage (0-100) maps directly to the CCR value with no conversion math needed.
- **Q2: Why does the assert handler stop motors by writing directly to GPIO registers instead of calling `drive_stop()`?**
  - The assert handler must be as standalone as possible and not depend on other modules that might themselves contain assertions or be in an inconsistent state. If the assertion was triggered by a bug in the drive or motor driver code, calling those same functions could trigger a recursive assertion. By writing directly to the hardware registers, the motor stop is guaranteed to work regardless of what other code has done.
- **Q3: Why is the duty cycle scaled down by 25% in the PWM driver instead of in the drive module?**
  - Scaling at the PWM level ensures that no code path -- including test functions or future modules -- can accidentally overdrive the motors beyond their 6V rating. It acts as a hardware protection layer. The drive module works with "logical" duty cycles (0-100%), and the PWM driver transparently caps the actual output. The division by 4 compiles to a single right-shift instruction, so the overhead is negligible.

---

### Section 7: Sensor Integration

### Lesson 22 — ADC Driver with DMA in C

**File Path:** [22 ADC driver with DMA in C  Embedded System Project Series #22.txt](Artful_Bytes_Transcript/22%20ADC%20driver%20with%20DMA%20in%20C%20%20Embedded%20System%20Project%20Series%20%2322.txt)

**Objective:** Teaches how to implement an ADC driver using DMA (Data Transfer Controller) to sample multiple analog channels with minimal CPU involvement, then layers a line sensor driver (QRE1113) and an application-level line detection module on top to detect the sumo platform boundary.

**Terminology & Key Concepts:**
- **ADC (Analog-to-Digital Converter)**: A peripheral that converts continuous analog voltage levels into discrete digital values. The MSP430G2553 has a 10-bit ADC (ADC10) producing values 0-1023.
- **DMA / DTC (Data Transfer Controller)**: Hardware that moves data between memory locations without CPU involvement. On the MSP430, the ADC10's DTC automatically writes sampled channel values into a memory block, interrupting only when the entire sequence completes.
- **ACLK (Auxiliary Clock)**: A slow internal clock source (~12 kHz from VLO) used to reduce CPU load. The ADC is clocked from ACLK to minimize interrupt frequency.
- **Sequence of Channels (CONSEQ_1)**: An ADC mode that samples multiple channels contiguously from the highest configured channel index down to channel 0 in a single sweep.
- **Sample and Hold Time (SHT)**: How long the ADC charges its internal capacitor before conversion. Longer times give more accurate readings but slower sampling.
- **QRE1113**: A reflectance sensor that emits infrared light and measures the reflected intensity. White surfaces reflect more light (low voltage output), black surfaces absorb it (high voltage output).
- **Line Detection Threshold**: A voltage threshold (700 out of 1023) used to distinguish the white boundary line from the black platform surface.
- **Volatile Keyword**: Tells the compiler not to optimize away reads/writes to a variable because its value can change outside normal program flow (e.g., modified by hardware DMA or ISR).

| Concept | Details |
|---|---|
| ADC Peripheral | ADC10 (10-bit, values 0-1023) |
| ADC Channels | 8 total on Port 1 (pins P1.0-P1.7); 4 used for line sensors |
| Clock Source | ACLK (low-frequency internal oscillator) -- reduces CPU load |
| Clock Divider | ADC10DIV_7 (maximum divider for slowest sampling) |
| Sample Mode | CONSEQ_1 -- sequence of channels (contiguous, high to low) |
| DTC Config | Continuous transfer mode, writes to volatile buffer array |
| Cache Strategy | ISR copies DTC buffer to cache; application reads from cache with interrupts disabled |
| Line Sensors | QRE1113 x4 (front-left, front-right, back-left, back-right) |
| Detection Threshold | Voltage < 700 means white line detected |
| Line Positions | 11 positions: NONE, FRONT, BACK, LEFT, RIGHT, FRONT_LEFT, FRONT_RIGHT, BACK_LEFT, BACK_RIGHT, DIAGONAL_LEFT, DIAGONAL_RIGHT |

**Techniques & Methods:**
- **DMA-based ADC sampling**: Configuring the DTC to automatically transfer sampled values into a memory block after each complete channel sweep. This eliminates the need for per-channel interrupts and reduces CPU wake-ups.
- **Double-buffered caching**: Maintaining two arrays -- one written by DMA hardware, one read by application code. The ISR copies from the DTC block to the cache, and the application disables interrupts globally while reading the cache to prevent mid-read corruption.
- **Contiguous channel sampling limitation**: The ADC10 in CONSEQ_1 mode can only sample channels contiguously from the highest index down to 0. Even if only channels 0, 3, 4, 5 are needed, channels 1 and 2 are also sampled (and discarded). The driver accounts for this by computing `dtc_channel_cnt = last_idx + 1`.
- **Reverse-order DTC correction**: The DTC writes samples in reverse order (highest channel first). The ISR reverses the array indexing when copying to the cache: `adc_dtc_block_cache[i] = adc_dtc_block[dtc_channel_cnt - 1 - i]`.
- **Three-layer sensor abstraction**: ADC driver (peripheral registers) -> QRE1113 driver (named voltages per sensor position) -> Line module (discrete line position enum from combined sensor readings).
- **Threshold-based line detection**: Comparing each sensor's ADC reading against a fixed threshold (700). Combining four boolean results through a priority-ordered if-else chain to determine the line's position relative to the robot.

**Source Code Mapping:**
- `adc_init()`: `adc.c:26` -- Configures ADC10 registers: clock source (ACLK), clock divider (max), sequence mode (CONSEQ_1), sample-and-hold time, DTC setup, and starts first conversion.
  ```c
  ADC10CTL1 = inch + ADC10DIV_7 + CONSEQ_1 + SHS_0 + ADC10SSEL_1;
  ADC10CTL0 = ADC10ON + SREF_0 + ADC10SHT_2 + MSC + ADC10IE;
  ADC10AE0 = adc10ae0;
  ADC10DTC1 = dtc_channel_cnt;
  ADC10SA = (uint16_t)adc_dtc_block;
  ```
- `isr_adc10()`: `adc.c:73` -- Interrupt handler that copies DTC buffer to cache in reverse order and restarts conversion.
  ```c
  INTERRUPT_FUNCTION(ADC10_VECTOR) isr_adc10(void) {
      for (uint8_t i = 0; i < dtc_channel_cnt; i++) {
          adc_dtc_block_cache[i] = adc_dtc_block[dtc_channel_cnt - 1 - i];
      }
      adc_enable_and_start_conversion();
  }
  ```
- `adc_get_channel_values()`: `adc.c:82` -- Disables interrupts globally, copies only the configured ADC pin values from cache, then re-enables interrupts.
  ```c
  _disable_interrupts();
  for (uint8_t i = 0; i < adc_pin_cnt; i++) {
      const uint8_t channel_idx = io_to_adc_idx(adc_pins[i]);
      values[channel_idx] = adc_dtc_block_cache[channel_idx];
  }
  _enable_interrupts();
  ```
- `qre1113_get_voltages()`: `qre1113.c:15` -- Wraps ADC channel access with named sensor positions (front_left, front_right, back_left, back_right).
  ```c
  voltages->front_left = values[io_to_adc_idx(IO_LINE_DETECT_FRONT_LEFT)];
  ```
- `line_get()`: `line.c:17` -- Converts four sensor voltage readings into one of 11 discrete line position values using threshold comparison and a priority if-else chain.
  ```c
  const bool front_left = voltages.front_left < LINE_DETECTED_VOLTAGE_THRESHOLD;
  const bool front_right = voltages.front_right < LINE_DETECTED_VOLTAGE_THRESHOLD;
  if (front_left) {
      if (front_right) { return LINE_FRONT; }
      else if (back_left) { return LINE_LEFT; }
      // ...
  }
  ```

**Demo / Example:**
- **Goal:** Verify ADC reads correct values for analog inputs, then confirm line sensor detects white vs. black surfaces.
- **Why Important:** The line sensors are critical safety sensors that prevent the sumo robot from driving off the platform. If the ADC or threshold logic is wrong, the robot will drive off the edge during competition.
- **Demo Flow:**
  1. ADC test: Connect a jumper wire to ADC pin (P1.3). Pull to VCC (3.3V) and read ~1023. Pull to ground and read ~0. Confirms ADC peripheral and DTC are working.
  2. QRE1113 test: Connect one reflectance sensor to the ADC pin. Hold white paper over sensor -- voltage drops below threshold. Remove paper -- voltage returns to high reading. Confirms sensor hardware and voltage mapping.
  3. Line position test: Print the `line_e` enum value. With one sensor detecting white: returns `LINE_FRONT_RIGHT` (value 6). Without detection: returns `LINE_NONE` (value 0). Confirms threshold and position logic.
- **What Changed:**
  - `adc.c` / `adc.h`: New ADC driver with DTC/DMA continuous sampling and cached readout
  - `qre1113.c` / `qre1113.h`: Thin sensor driver mapping ADC channels to named sensor positions
  - `line.c` / `line.h`: Application-layer module converting four sensor voltages to 11 discrete line positions
  - `io.c`: Added ADC pin array, `io_adc_pins()` and `io_to_adc_idx()` helper functions, and ADC pin configuration
  - `mcu_init.c`: Configured ACLK source (VLO internal low-frequency oscillator)
  - `Makefile`: Added new source files

**Discussion Prompts:**
- **Q1: Why are interrupts disabled globally rather than just for the ADC peripheral when reading cached values?**
  - The author discovered through debugging that disabling only the ADC interrupt caused the ADC to stop working after a while. The root cause was unclear, so disabling interrupts globally was used as a reliable workaround. This is safe because the critical section is very short (just copying a few 16-bit values), so other interrupts are only delayed briefly.
- **Q2: Why use a slow clock (ACLK) for the ADC instead of the faster SMCLK?**
  - Since the application's main loop runs at roughly 10 iterations per second (with 1 ms sleep per iteration), there is no need for rapid ADC sampling. Using the slow ACLK reduces the number of interrupts and DTC transfers, lowering CPU utilization and power consumption. The sensors are reading a static surface (white vs. black), so high sampling speed is unnecessary.
- **Q3: What is the limitation of CONSEQ_1 mode and how does the driver handle it?**
  - CONSEQ_1 (sequence of channels) mode can only sample channels contiguously from the highest configured channel down to channel 0. If you need channels 3, 4, and 5, channels 0, 1, and 2 are also sampled and wasted. The driver handles this by computing `dtc_channel_cnt = last_idx + 1` to allocate enough buffer space, but only copies the channels of interest in `adc_get_channel_values()` using the `io_adc_pins` array to filter.

---

### Lesson 23 — I2C Driver in C (with VL53L0X Sensor)

**File Path:** [23 I2C driver in C (with VL53L0X sensor)  Embedded System Project Series #23.txt](Artful_Bytes_Transcript/23%20I2C%20driver%20in%20C%20(with%20VL53L0X%20sensor)%20%20Embedded%20System%20Project%20Series%20%2323.txt)

**Objective:** Teaches how to implement a polling-based I2C master driver for the MSP430 and integrate five VL53L0X Time-of-Flight range sensors, then layer an application-level enemy detection module that converts raw distance measurements into discrete enemy positions and ranges.

**Terminology & Key Concepts:**
- **I2C (Inter-Integrated Circuit)**: A two-wire serial communication protocol (SDA for data, SCL for clock) supporting multiple slave devices on the same bus. Each slave has a unique 7-bit address.
- **VL53L0X**: A Time-of-Flight (ToF) laser range sensor from ST Microelectronics that measures distances up to ~2 meters. Contains its own microcontroller and complex initialization sequence.
- **XSHUT Pin**: A hardware standby pin on the VL53L0X. Pulling LOW puts the sensor in standby; pulling HIGH wakes it up. Used to address multiple sensors on the same I2C bus by waking them one at a time and assigning unique addresses.
- **SPAD (Single Photon Avalanche Diode)**: The light-detecting elements inside the VL53L0X. Factory-calibrated SPAD maps stored in NVM are used during initialization to configure which SPADs are active.
- **Polling-based I2C**: Instead of using interrupts, the driver busy-waits for each byte transmission/reception to complete. Simpler to implement but blocks the CPU during transfers.
- **NACK (Negative Acknowledge)**: An I2C error condition where the slave does not acknowledge a transmitted byte, indicating a communication failure.
- **VHV Calibration**: Voltage High Voltage calibration -- a temperature-dependent reference calibration that must be re-run if temperature changes by more than 8 degrees Celsius.
- **Enemy Detection Threshold**: Range readings below 600 mm indicate an enemy is present. Ranges are further classified as CLOSE (<100mm), MID (<200mm), or FAR (<300mm).

| Concept | Details |
|---|---|
| I2C Peripheral | USCI_B0 (UCB0) on MSP430G2553 |
| I2C Clock | SMCLK / 160 = ~100 kHz (standard mode) |
| I2C Pins | P1.6 (SCL), P1.7 (SDA) -- configured as ALT3 function |
| Range Sensors | VL53L0X x5 (front, front-left, front-right, left, right) |
| Default Address | 0x29 (all VL53L0X ship with this address) |
| Reassigned Addresses | Front=0x30, Left=0x31, Right=0x32, Front-Right=0x33, Front-Left=0x34 |
| Address Assignment | Wake sensors one-by-one via XSHUT pin, assign unique I2C address to each |
| Sampling Strategy | Start all sensors measuring in parallel, use front sensor interrupt to detect completion, read all results |
| Detection Threshold | < 600 mm = enemy detected |
| Enemy Positions | NONE, FRONT, FRONT_LEFT, FRONT_RIGHT, LEFT, RIGHT, FRONT_AND_FRONT_LEFT, FRONT_AND_FRONT_RIGHT, FRONT_ALL, IMPOSSIBLE |
| Enemy Ranges | NONE, CLOSE (<100mm), MID (<200mm), FAR (<300mm) |
| Side Sensors | Left and right sensors disabled in final code -- mounted poorly, gave false detections |

**Techniques & Methods:**
- **Polling-based I2C with retry/timeout**: Each byte TX/RX waits in a busy loop with a `UINT16_MAX` retry count. Checks for NACK errors after each transmission. Returns structured error codes (`I2C_RESULT_OK`, `ERROR_START`, `ERROR_TX`, `ERROR_RX`, `ERROR_STOP`, `ERROR_TIMEOUT`).
- **Multi-sensor I2C addressing via XSHUT**: All VL53L0X sensors start at address 0x29. By keeping all sensors in hardware standby (XSHUT LOW), then waking them one at a time and immediately assigning a unique address, each sensor gets a distinct I2C address. This follows AN4846 (ST application note).
- **Parallel range measurement with interrupt gating**: All sensors start measuring simultaneously. The front sensor's GPIO interrupt pin signals completion (`STATUS_MULTIPLE_DONE`). The driver then checks if other sensors are also done before reading. If not done, cached (stale) values are returned. This avoids blocking the main loop.
- **SPAD configuration from NVM**: During initialization, the factory-calibrated SPAD map and count are read from NVM (non-volatile memory). A subset of SPADs is activated based on this calibration data to get optimal signal rates without needing to run the full reference SPAD management procedure.
- **Three-layer sensor abstraction**: I2C driver (bus protocol) -> VL53L0X driver (sensor initialization + measurement) -> Enemy module (discrete position/range from combined readings).
- **Convenience wrapper functions**: `i2c_read_addr8_data8()`, `i2c_read_addr8_data16()`, `i2c_read_addr8_data32()`, and `i2c_write_addr8_data8()` simplify common I2C register access patterns used throughout the VL53L0X driver.

**Source Code Mapping:**
- `i2c_init()`: `i2c.c:204` -- Configures USCI_B0 as I2C master with SMCLK/160 (~100 kHz), verifies SDA/SCL pin mux configuration.
  ```c
  UCB0CTL1 |= UCSWRST;
  UCB0CTL0 = UCMST + UCSYNC + UCMODE_3;
  UCB0CTL1 |= UCSSEL_2;
  UCB0BR0 = 160;
  UCB0CTL1 &= ~UCSWRST;
  i2c_set_slave_address(DEFAULT_SLAVE_ADDRESS);
  ```
- `i2c_write()`: `i2c.c:117` -- Sends address bytes then data bytes over I2C, checking for errors at each step, then sends stop condition.
- `i2c_read()`: `i2c.c:143` -- Sends register address, switches to receiver mode with repeated start, reads data bytes (stop condition sent before last byte per I2C spec).
  ```c
  // Must stop before last byte
  result = i2c_stop_transfer();
  result = i2c_wait_rx_byte();
  data[0] = i2c_get_rx_byte();
  ```
- `vl53l0x_init()`: `vl53l0x.c:852` -- Master initialization: I2C init, wake sensors one-by-one (XSHUT pin), assign addresses, run data_init + static_init + ref_calibration for each sensor, configure front sensor interrupt.
- `vl53l0x_init_address()`: `vl53l0x.c:560` -- Wakes a single sensor from hardware standby, verifies it booted (reads device ID 0xEE), and assigns a unique I2C address.
  ```c
  vl53l0x_set_hardware_standby(idx, false);
  i2c_set_slave_address(VL53L0X_DEFAULT_ADDRESS);
  __delay_cycles(10000);
  vl53l0x_configure_address(vl53l0x_cfgs[idx].addr);
  ```
- `vl53l0x_read_range_multiple()`: `vl53l0x.c:788` -- Non-blocking multi-sensor read: starts all sensors, blocks only on first call, then returns cached values if measurement not yet complete.
  ```c
  if (status_multiple == STATUS_MULTIPLE_DONE
      && vl53l0x_is_sysrange_done(VL53L0X_IDX_LEFT)
      && vl53l0x_is_sysrange_done(VL53L0X_IDX_RIGHT) /* ... */) {
      // Read all ranges and start new measurement
  } else {
      *fresh_values = false;
  }
  ```
- `enemy_get()`: `enemy.c:12` -- Reads range measurements from all sensors, applies 600mm detection threshold, determines enemy position from which sensor(s) triggered, and classifies range as CLOSE/MID/FAR.
  ```c
  if (front_left && front && front_right) {
      enemy.position = ENEMY_POS_FRONT_ALL;
      range = ((((range_front_left + range_front) / 2) + range_front_right) / 2);
  }
  ```
- `enemy_at_left()`, `enemy_at_right()`, `enemy_at_front()`: `enemy.c:109-124` -- Boolean helper functions that check if the enemy is at a given relative position (used by state machine to decide drive direction).

**Demo / Example:**
- **Goal:** Verify I2C communication with a single VL53L0X sensor, then test multi-sensor reading and enemy position detection.
- **Why Important:** The range sensors are the robot's only way to locate the enemy. Correct I2C communication and accurate distance measurement are essential for the attack and search behaviors.
- **Demo Flow:**
  1. I2C single sensor test: Read device ID register (0xC0) from front sensor. Expected value: 0xEE. Write and read-back test confirms bidirectional communication works.
  2. Multi-sensor test: Start all sensors measuring. Move hand in front at varying distances. Print range values -- close range gives small numbers, far range gives large numbers, no obstacle gives 8190 (out of range).
  3. Enemy position test: Move hand to different positions. "front_all_mid" when hand is centered at medium distance. "front_all_close" when closer. "front_all_far" when further away. Moving hand left/right changes position to FRONT_LEFT or FRONT_RIGHT.
- **What Changed:**
  - `i2c.c` / `i2c.h`: New polling-based I2C master driver with convenience wrappers for 8/16/32-bit register access
  - `vl53l0x.c` / `vl53l0x.h`: Full VL53L0X driver with multi-sensor support, XSHUT-based addressing, SPAD configuration, interrupt-gated parallel measurement
  - `enemy.c` / `enemy.h`: Application-layer module converting raw range measurements into discrete enemy positions (9 positions) and ranges (4 levels)
  - `io.c`: Added XSHUT pin configurations and I2C pin assignments, front sensor interrupt pin configuration
  - `Makefile`: Added new source files
- **Related Code:**
  ```c
  // Multi-sensor addressing strategy (AN4846)
  static const struct vl53l0x_cfg vl53l0x_cfgs[] = {
      [VL53L0X_IDX_FRONT] = { .addr = 0x30, .xshut_io = IO_XSHUT_FRONT },
      [VL53L0X_IDX_LEFT]  = { .addr = 0x31, .xshut_io = IO_XSHUT_LEFT },
      [VL53L0X_IDX_RIGHT] = { .addr = 0x32, .xshut_io = IO_XSHUT_RIGHT },
      // ...
  };
  ```

**Discussion Prompts:**
- **Q1: Why is polling used for I2C instead of interrupts, given that interrupts were used for ADC?**
  - I2C communication with the VL53L0X requires many sequential register reads and writes (the initialization sequence alone involves dozens of register accesses). Using interrupts would require a complex state machine to track the current operation. Polling is simpler to implement and debug for this use case. The trade-off is that the CPU is blocked during each I2C transfer, but since the transfers are short (a few bytes each) and the main loop is not time-critical, this is acceptable.
- **Q2: Why were the left and right side sensors ultimately disabled?**
  - The physical mounting position of the side sensors caused frequent false detections. The sensors' field of view was too close to the robot body or the platform surface, giving unreliable readings. Rather than complicate the code with filtering or recalibrate, the author pragmatically disabled them (using `#if 0` blocks) and relied on the three front-facing sensors (front, front-left, front-right) for enemy detection.
- **Q3: How does the multi-sensor read avoid blocking the main loop?**
  - After the first call (which blocks until the initial measurement completes), subsequent calls check `status_multiple`. If the front sensor's GPIO interrupt has fired (`STATUS_MULTIPLE_DONE`) and all other sensors have completed (`vl53l0x_is_sysrange_done()`), new values are read and a fresh measurement is started. If not yet done, the function returns the previously cached `latest_ranges` with `*fresh_values = false`. This allows the main loop to continue processing (checking line sensors, updating state machine) rather than waiting for slow I2C transfers.

---

### Section 8: System Integration & Testing

### Lesson 24 — How to Board Bring-up

**File Path:** [24 How to Board Bring-up  Embedded System Project Series #24.txt](Artful_Bytes_Transcript/24%20How%20to%20Board%20Bring-up%20%20Embedded%20System%20Project%20Series%20%2324.txt)

**Objective:** Teaches the process of board bring-up -- verifying that a custom PCB works as intended by systematically running through hardware tests -- and demonstrates the transition from development board to the actual robot PCB.

**Terminology & Key Concepts:**
- **Board Bring-up**: The process of verifying a newly manufactured PCB works as intended. Involves visual inspection, electrical measurements, and running test software to validate each hardware subsystem.
- **PCB (Printed Circuit Board)**: The physical board that connects all electronic components (MCU, sensors, motor drivers, etc.) through copper traces. The nsumo robot uses a custom 2-layer PCB.
- **Revision / Spin**: Different iterations of a PCB design. Each revision fixes issues found in the previous one. The nsumo robot is on revision 2 after fixing a diode orientation and motor driver wiring mistakes in revision 1.
- **Hardware Patching**: Physically modifying a PCB (cutting traces, adding wires) to fix design mistakes without waiting for a new board revision. Essential for quickly confirming a suspected issue before ordering new boards.
- **Build Targets**: Separate compilation configurations for different hardware platforms (Launchpad dev board vs. nsumo PCB). Each produces different binaries with `#ifdef` controlling pin assignments and enabled peripherals.
- **Schematic-driven Checklist**: Using the circuit schematic as a systematic guide for board bring-up, testing each connection and IC shown on the schematic.

| Concept | Details |
|---|---|
| PCB Revision | Rev 2 (Rev 1 had reversed diode + swapped motor driver inputs) |
| Debug Interface | No dedicated connector -- jumper wires from Launchpad debugger |
| Test Sequence | Power -> Flash -> LED -> UART -> IR Remote -> Motors -> ADC/Line Sensors -> I2C/Range Sensors |
| Build Target Fix | Separate build directories per target (`build/launchpad/`, `build/nsumo/`) to avoid stale object files when switching |
| Tests Skipped on PCB | GPIO enumeration test, individual PWM test (not useful for PCB verification) |
| Bug Found | Assert handler configured wrong UART pin for trace output (P3 instead of P2) |

**Techniques & Methods:**
- **Systematic hardware verification**: Working through each subsystem on the schematic in order of dependency: power supply first, then debug interface, then peripherals (UART, IR, motors, ADC, I2C). Each test uses the pre-written test functions from earlier lessons.
- **Separate build directories per target**: Modified the Makefile to place object files in `build/<target>/` subdirectories. This prevents stale objects from a previous target causing incorrect builds when switching between Launchpad and nsumo.
- **Visual indicators as debugging aids**: Using onboard LEDs alongside serial output to confirm sensor operation. Line sensors light up LEDs near each sensor position, providing immediate visual feedback without needing a serial terminal.
- **Incremental verification**: Testing each hardware subsystem independently before combining them. Motor drivers tested with reduced duty cycle to prevent the robot from driving off the desk.
- **Makefile improvements**: Adding convenience rules (`make terminal`, `make tests`), using variables for goals-without-hardware, and using `filter` to conditionally require a target argument.

**Source Code Mapping:**
- `main.c:10` -- The main function initializes all subsystems and runs the state machine.
  ```c
  int main(void) {
      mcu_init();
      trace_init();
      drive_init();
      enemy_init();
      line_init();
      ir_remote_init();
      state_machine_run();
  }
  ```
- `assert_handler.c` -- Bug fix: changed UART TX pin configuration from Port 3 to Port 2 in the assert trace function. The previous code would fail to output trace data if an assertion fired before `io_init()` ran.
- `Makefile` -- Multiple improvements:
  ```makefile
  # Separate build directories per target
  OBJ_DIR = build/$(TARGET)/obj
  BIN_DIR = build/$(TARGET)/bin

  # Convenience rules
  terminal: ; sleep 1 && mspdebug ...
  tests: ; $(MAKE) ... build_tests.sh
  .PHONY: clean cppcheck format terminal tests
  ```

**Demo / Example:**
- **Goal:** Demonstrate the full board bring-up process on the nsumo Rev 2 PCB, validating every hardware connection using pre-written test functions.
- **Why Important:** Board bring-up is a critical milestone in any embedded project. It confirms that the hardware design is correct and the software can communicate with all peripherals. Issues found here drive PCB revisions.
- **Demo Flow:**
  1. Power up board -- LED lights up, no smoke (good sign). Rev 1 had reversed diode that prevented power LED.
  2. Flash firmware via Launchpad debugger -- confirms MCU boots and debug interface works.
  3. Test LED blink -- confirms GPIO output works on PCB.
  4. Test UART -- terminal shows expected output, confirms serial communication.
  5. Test IR remote -- press buttons, terminal shows received commands. Confirms IR receiver connection.
  6. Test motors -- all four motors spin at reduced duty cycle, change direction correctly. Robot held elevated to prevent driving off desk.
  7. Test ADC/line sensors -- hold white paper under each sensor, see voltage change and LED indicator. All four sensors respond correctly.
  8. Test I2C/range sensors -- read device IDs, measure distances at close/mid/far. Front sensor interrupt works. Debug fix needed: side sensors not started but driver waited for their completion, causing hang.
- **What Changed:**
  - `Makefile`: Separate build directories, convenience rules, conditional target requirement, PHONY targets
  - `assert_handler.c`: Fixed UART TX pin from Port 3 to Port 2
  - `.github/workflows/ci.yml`: Updated to use new Makefile targets, added `TOOLS_PATH` environment variable
  - `test.c`: Added `#ifdef` guards to skip Launchpad-only tests on nsumo target

**Discussion Prompts:**
- **Q1: Why is time so critical during board bring-up?**
  - PCB manufacturing and shipping take significant time (often weeks). If hardware issues are discovered, the hardware designer needs to revise the design and order new boards as soon as possible. The faster software engineers can run through bring-up and identify issues, the sooner the next revision can be ordered, keeping the project timeline on track. This is why you should prepare minimal verification software early rather than waiting for full drivers to be complete.
- **Q2: Why did this bring-up go so smoothly, and what would a real one look like?**
  - This was the second revision of the board, and the first revision's issues (reversed diode, swapped motor driver pins) had already been fixed. Additionally, all the driver code was already written and tested on the Launchpad. In a typical first bring-up, you would expect more issues: incorrect footprints, wrong component values, signal integrity problems, missing pull-up resistors, and similar hardware bugs that require debugging with oscilloscopes and logic analyzers.

---

### Lesson 25 — I Made a Robot 2D Simulator with C++

**File Path:** [25 I made a Robot 2D Simulator with C++  Embedded System Project Series #25.txt](Artful_Bytes_Transcript/25%20I%20made%20a%20Robot%202D%20Simulator%20with%20C%2B%2B%20%20Embedded%20System%20Project%20Series%20%2325.txt)

**Objective:** Explains the design and implementation of a custom 2D robot simulator ("Bots2D") built from scratch in C++ to accelerate application code development by avoiding the slow flash-test cycle of embedded targets.

**Terminology & Key Concepts:**
- **Bots2D**: The author's custom 2D robotics simulator framework, written in C++ with OpenGL rendering and Box2D physics. Designed as a framework that users extend through code rather than a GUI.
- **Box2D**: An open-source 2D physics engine used by many popular games. Provides rigid body dynamics, collision detection, and raycasting. Originally designed for side-view games but adapted for top-down by disabling gravity.
- **Top-down Physics Hack**: Disabling Box2D's gravity and using its friction system to simulate a top-down view of robots on a flat surface. Not perfect but sufficient for the sumo robot scenario.
- **Game Loop / Main Loop**: The central while loop that drives the simulator, executing physics updates, controller updates, and rendering in sequence at a fixed frequency.
- **Voltage Line Concept**: An abstraction linking the simulated microcontroller to simulated hardware components. A voltage line is a float pointer representing the voltage on a wire. Motors read voltage as input; sensors write voltage as output. This mirrors how real MCU pins connect to peripherals via wires.
- **Scene Object**: The simulator's entity model. Each object can have components: Renderable (graphics), Physics (dynamics), Transform (position/orientation), and Controller (I/O logic). Scene objects can be composed of other scene objects.
- **OpenGL Rendering**: Low-level graphics API used to draw shapes. Everything is composed of triangles. Uses shader programs, vertex buffers, and transform matrices for positioning/rotation/scaling.
- **Entity Component System (ECS)**: A compositional design pattern common in game engines where entities are composed of reusable components rather than using deep inheritance hierarchies. Bots2D uses a simpler version of this approach.

| Concept | Details |
|---|---|
| Language | C++ (simulator), C (target application code) |
| Physics Engine | Box2D (open source, 2D) |
| Graphics | Custom OpenGL renderer with GLFW + GLAD helper libraries |
| UI Library | Dear ImGui (for menus, parameter tuning, statistics) |
| Math Library | GLM (linear algebra for transform matrices) |
| Texture Loading | stb_image library |
| Architecture Pattern | Composition over inheritance (scene objects composed of components) |
| Component Types | Renderable, Physics, Transform, Controller |
| Update Frequency | 1000 Hz (1 ms loop, matching embedded target) |
| Target Code Isolation | Application code (C) runs in a separate thread, communicates via voltage lines |
| Platform Support | Linux and Windows |

**Techniques & Methods:**
- **Hardware abstraction via voltage lines**: Creating float pointers that represent electrical connections between simulated components. The controller (microcontroller code) reads sensor voltage lines and writes motor voltage lines. This makes the application code portable between simulation and real hardware -- only the driver layer changes.
- **Composition-based scene design**: Objects like the sumo robot are composed of sub-objects (motors, sensors, body), each with their own physics and renderable components. This promotes code reuse -- a wheel motor object works for any robot type.
- **Simulated sensor implementation**: Range sensors use Box2D's raycast feature to measure distance between objects. Line sensors use a contact listener with an invisible body representing the boundary line and a tiny body representing the sensor.
- **Simulated DC motor model**: Takes voltage input and produces force output proportional to the voltage, mimicking real motor behavior (speed proportional to applied voltage).
- **Application class inheritance**: Users create a simulation by inheriting from an `Application` base class and registering scenes. This framework pattern allows flexibility through code configuration rather than GUI-based setup.

**Source Code Mapping:**
- The simulator code lives in a separate repository (bots2d on GitHub), not in the nsumo firmware codebase. No direct source file mappings to nsumo source, but the concepts connect:
  - The simulated motor driver replaces `tb6612fng.c` -- sets voltage line values instead of GPIO pins
  - The simulated line sensor replaces `qre1113.c` -- reads Box2D contact listener instead of ADC values
  - The simulated range sensor replaces `vl53l0x.c` -- uses Box2D raycast instead of I2C communication
  - `state_machine.c` and all `state_*.c` files run unchanged in simulation

**Demo / Example:**
- **Goal:** Show the complete simulator architecture and demonstrate interactive physics simulation with rendered robots on a sumo platform.
- **Why Important:** Developing application code (state machine) directly on the MCU requires flashing for every code change -- extremely slow iteration. The simulator allows instant recompile-and-test cycles, making it practical to iterate on complex autonomous behavior.
- **Demo Flow:**
  1. Clone bots2d repository recursively (has git submodules)
  2. Build test application with CMake
  3. Run test app -- shows multiple simulation scenes including sumo bots on a circular platform
  4. One robot controlled by keyboard, another by state machine code
  5. Physics simulation shows collision, pushing, platform boundary detection
- **What Changed:**
  - No changes to the nsumo firmware codebase in this lesson
  - New project: bots2d simulator framework (separate repository)

**New Tools Introduced:**
- **Bots2D** -- Custom 2D robotics simulator framework for developing and testing embedded application code on a host computer
- **Box2D** -- Open-source 2D physics engine providing rigid body simulation, collision detection, and raycasting
- **Dear ImGui** -- Immediate-mode GUI library for creating debug menus and parameter tuning panels
- **CMake** -- Build system used for the simulator project (cross-platform Linux/Windows support)

**Discussion Prompts:**
- **Q1: Was building a custom simulator from scratch worth the effort?**
  - The author admits in hindsight it was not. While it was a good learning exercise in C++, object-oriented design, and graphics programming, the effort-to-benefit ratio was poor. A simpler approach (Python script, existing simulator, or just developing on-target) would have been more pragmatic. The key lesson is to weigh development tool investment against the actual time saved.
- **Q2: Why does the simulator use voltage lines instead of directly calling the application code's functions?**
  - Voltage lines create a clean separation between the simulation framework and the target code. The target code (state machine, drive, enemy, line modules) does not need to know it is running in a simulator. Only the driver layer is swapped out -- the simulated drivers translate voltage line values to/from sensor readings and motor commands. This mirrors the real hardware where the MCU communicates with peripherals through voltage on wires, making the abstraction intuitive and the code transfer seamless.

---

### Lesson 26 — How to Code a State Machine

**File Path:** [26 How to Code a State Machine  Embedded System Project Series #26.txt](Artful_Bytes_Transcript/26%20How%20to%20Code%20a%20State%20Machine%20%20Embedded%20System%20Project%20Series%20%2326.txt)

**Objective:** Teaches how to design and implement a poll-based state machine in C for autonomous robot behavior, covering state diagrams, transition tables, event processing, and the skeleton code for five states (Wait, Search, Attack, Retreat, Manual).

**Terminology & Key Concepts:**
- **State Machine**: A software pattern that breaks a system into discrete states with defined transitions between them, triggered by events. Each state encapsulates specific behavior.
- **Transition Table**: A data structure (array of structs) mapping `{from_state, event} -> to_state`. The state machine iterates this table to find the matching transition when an event occurs.
- **Poll-based / Non-blocking State Machine**: A state machine where the main loop continuously polls for input (sensors, timers) without ever blocking. This eliminates the need for event synchronization mechanisms like semaphores or queues.
- **Internal Event**: An event posted from within a state handler (e.g., retreat state posting `STATE_EVENT_FINISHED` when its move sequence completes). Checked in the next iteration's input processing.
- **Input History**: A ring buffer storing recent sensor inputs (enemy position + line position). Used by the search state to decide which direction to rotate toward -- rotate toward where the enemy was last seen.
- **Retreat Substates**: The retreat state contains its own internal state machine with substates (REVERSE, FORWARD, ROTATE_LEFT/RIGHT, ARCTURN_LEFT/RIGHT, ALIGN_LEFT/RIGHT), each defining a sequence of timed drive moves.
- **State Common Data**: A shared data struct passed to all state handlers containing current sensor readings (enemy, line, IR command), timer reference, and input history reference.

| State | Enter From | Behavior | Exit Events |
|---|---|---|---|
| WAIT | Boot | Do nothing; wait for IR remote command | COMMAND -> SEARCH |
| SEARCH | WAIT, ATTACK, RETREAT | Rotate (toward last enemy direction), then drive forward, alternating on timeout | ENEMY -> ATTACK, LINE -> RETREAT |
| ATTACK | SEARCH | Drive toward enemy (forward, arc-left, arc-right) based on enemy position | LINE -> RETREAT, NONE -> SEARCH (enemy lost) |
| RETREAT | SEARCH, ATTACK | Execute timed move sequence based on line position and enemy direction | FINISHED -> SEARCH |
| MANUAL | Any | IR remote direct control (forward, reverse, rotate) -- debug mode | (stays in MANUAL) |

| Event | Trigger |
|---|---|
| STATE_EVENT_NONE | No sensor input detected |
| STATE_EVENT_COMMAND | IR remote button pressed |
| STATE_EVENT_ENEMY | Range sensor detects enemy |
| STATE_EVENT_LINE | Line sensor detects boundary |
| STATE_EVENT_TIMEOUT | Poll-based timer expired |
| STATE_EVENT_FINISHED | Internal event -- retreat move sequence complete |

**Techniques & Methods:**
- **Table-driven state transitions**: Defining all valid state transitions as an array of `{from, event, to}` structs. The `process_event()` function scans this table linearly. Invalid transitions trigger an assertion, catching logic bugs at runtime.
  ```c
  static const struct state_transition state_transitions[] = {
      { STATE_WAIT, STATE_EVENT_COMMAND, STATE_SEARCH },
      { STATE_SEARCH, STATE_EVENT_ENEMY, STATE_ATTACK },
      { STATE_ATTACK, STATE_EVENT_LINE, STATE_RETREAT },
      // ...
  };
  ```
- **Priority-ordered input processing**: In `process_input()`, events are checked in priority order: COMMAND (highest) > internal event > TIMEOUT > LINE > ENEMY > NONE. This ensures safety-critical events (IR override, line detection) take precedence over enemy tracking.
- **Non-blocking constraint**: No state handler is allowed to block (no busy-waits, no sleep). The 1 ms main loop sleep is the only wait. This ensures input processing happens frequently, keeping sensor readings fresh and reactions fast.
- **Input history for smarter search**: A ring buffer of size 6 stores recent `{enemy, line}` inputs, deduplicating identical consecutive entries. The search state queries `input_history_last_directed_enemy()` to find the most recent left/right enemy detection and rotates toward that direction.
- **Retreat as a sub-state machine**: Each retreat substate defines a sequence of up to 3 timed moves (direction + speed + duration). The retreat state machine advances through moves on timeouts and posts `STATE_EVENT_FINISHED` when the sequence completes.
- **Poll-based timer**: A simple timer implementation using `millis()` -- stores the target timestamp (`millis() + timeout_ms`), and `timer_timeout()` checks if current time exceeds the target. Cleared by setting to 0.

**Source Code Mapping:**
- `state_machine_run()`: `state_machine.c:187` -- The main entry point. Allocates input history ring buffer on the stack, initializes state machine data, then enters the infinite poll loop.
  ```c
  void state_machine_run(void) {
      struct state_machine_data data;
      LOCAL_RING_BUFFER(input_history, INPUT_HISTORY_BUFFER_SIZE, struct input);
      data.input_history = input_history;
      state_machine_init(&data);
      while (1) {
          const state_event_e next_event = process_input(&data);
          process_event(&data, next_event);
          sleep_ms(1);
      }
  }
  ```
- `process_input()`: `state_machine.c:142` -- Reads all sensors once per loop iteration, saves to input history, checks events in priority order.
  ```c
  data->common.enemy = enemy_get();
  data->common.line = line_get();
  data->common.cmd = ir_remote_get_cmd();
  input_history_save(&data->input_history, &input);
  ```
- `process_event()`: `state_machine.c:131` -- Scans transition table for matching `{current_state, event}` pair, calls `state_enter()` for the target state.
- `state_enter()`: `state_machine.c:103` -- Dispatches to the appropriate state handler. Clears timer and traces transition when state changes.
- `state_search_enter()`: `state_search.c:33` -- Alternates between ROTATE and FORWARD substates on timeout. Uses input history to choose rotation direction.
- `state_attack_enter()`: `state_attack.c:39` -- Drives toward enemy: FORWARD if front, ARC_WIDE_LEFT if left, ARC_WIDE_RIGHT if right. Only re-issues drive command if attack substate changed.
- `state_retreat_enter()`: `state_retreat.c:176` -- Selects retreat substate based on line position and enemy direction. Executes timed move sequence, posts FINISHED when done.
- `next_retreat_state()`: `state_retreat.c:80` -- Complex decision logic choosing from 8 retreat substates based on where the line was detected and where the enemy is.
  ```c
  case LINE_FRONT_LEFT:
      if (enemy_at_right(&data->common->enemy) || enemy_at_front(&data->common->enemy)) {
          return RETREAT_STATE_ALIGN_RIGHT;
      } else if (enemy_at_left(&data->common->enemy)) {
          return RETREAT_STATE_ALIGN_LEFT;
      } else {
          return RETREAT_STATE_REVERSE;
      }
  ```
- `input_history_save()`: `input_history.c:10` -- Saves sensor input to ring buffer, skipping if no detection or if identical to last entry.
- `input_history_last_directed_enemy()`: `input_history.c:29` -- Scans history from newest to oldest, returning the first entry where enemy was detected at a left or right position.
- `timer_start()`: `timer.c:7` -- Sets timer to `millis() + timeout_ms`.
- `timer_timeout()`: `timer.c:12` -- Returns true if current `millis()` exceeds the stored target time.

**Demo / Example:**
- **Goal:** Design the state machine on paper first, then implement skeleton code with all transitions, events, and state handlers.
- **Why Important:** The state machine is the brain of the robot. A well-structured state machine makes behavior predictable, debuggable, and extensible. This lesson establishes the architecture; the next lesson fills in the details.
- **Demo Flow:**
  1. Draw state diagram showing WAIT -> SEARCH -> ATTACK -> RETREAT cycle with transition events
  2. Draw detailed retreat sub-state diagram with 8 substates and their move sequences
  3. Implement transition table as an array of structs
  4. Implement state_machine_run() with the poll loop: process_input() -> process_event() -> sleep(1ms)
  5. Implement skeleton for each state handler (state_wait_enter, state_search_enter, etc.)
  6. Create timer and input_history utility modules
  7. Code compiles but robot does not move yet (details filled in next lesson)
- **What Changed:**
  - `state_machine.c` / `state_machine.h`: Core state machine with transition table, event processing, and main loop
  - `state_common.h`: Shared data structures and state/event enums
  - `state_wait.c` / `.h`: Wait state handler (trivial -- just waits for COMMAND event)
  - `state_search.c` / `.h`: Search state with ROTATE/FORWARD substates and input history integration
  - `state_attack.c` / `.h`: Attack state driving toward enemy with FORWARD/LEFT/RIGHT substates
  - `state_retreat.c` / `.h`: Retreat state with 8 substates and timed move sequences
  - `state_manual.c` / `.h`: Manual IR remote control state
  - `timer.c` / `timer.h`: Poll-based timer using millis()
  - `input_history.c` / `input_history.h`: Ring buffer-based sensor input history
  - `ring_buffer.c`: Extended to support elements larger than 1 byte

**Discussion Prompts:**
- **Q1: Why use a table-driven state machine instead of nested switch statements?**
  - The transition table separates the state machine's structure (what transitions are valid) from the behavior (what happens in each state). This makes it easy to visualize and verify all transitions at a glance, add new states or transitions without restructuring code, and catch invalid transitions with assertions. Nested switch statements mix structure and behavior, making them harder to maintain as the state machine grows.
- **Q2: Why must state handlers never block?**
  - If a state handler blocks (e.g., with a busy-wait loop), the main loop stops iterating and `process_input()` is not called. This means sensor readings become stale, line detection is delayed (robot could drive off the platform), and IR remote commands are missed. The 1 ms loop sleep is the maximum acceptable delay -- everything else must be non-blocking, using timers for timed operations instead.

---

### Lesson 27 — Simulation to Real-world Demo

**File Path:** [27 Simulation to Real-world Demo  Embedded System Project Series #27.txt](Artful_Bytes_Transcript/27%20Simulation%20to%20Real-world%20Demo%20%20Embedded%20System%20Project%20Series%20%2327.txt)

**Objective:** Completes the state machine implementation by filling in remaining details, tests the autonomous behavior in the Bots2D simulator, then deploys and validates on the actual sumo robot, demonstrating the full embedded development workflow from simulation to real hardware.

**Terminology & Key Concepts:**
- **Simulated Drivers**: Replacement driver implementations (C files) that interface with the simulator's voltage lines instead of MCU hardware registers. Same header files (same API), different implementation bodies.
- **Voltage Line Enum**: An enumeration mapping each simulated I/O to a voltage line index (motor left front, motor left rear, line sensor front-left, range sensor front, etc.). This is the simulation's equivalent of MCU pin assignments.
- **Flash/RAM Pressure**: The MSP430G2553 has only 16 KB flash and 512 B RAM. By lesson 27, the code is so large that tracing and IR remote must be compiled out to fit. Stack overflow from trace calls was corrupting RAM.
- **ADC Sampling Speed Issue**: The line sensors' ADC sampling (using slow ACLK) was not fast enough for the robot's driving speed. The robot would cross the white line before the ADC registered it. Reducing sample-and-hold time from SHT_3 to SHT_2 improved reaction time.
- **Compile-time Feature Toggling**: Using `#define DISABLE_TRACE`, `#define DISABLE_IR_REMOTE`, and `#define DISABLE_ENUM_TO_STRING` in the Makefile to remove features and reclaim flash/RAM space.

| Concept | Details |
|---|---|
| Simulated Drivers | `tb6612fng.c`, `qre1113.c`, `vl53l0x.c`, `ir_remote.c`, `assert_handler.c`, `trace.c` -- all reimplemented for simulation |
| Simulator Thread | State machine runs in a separate thread from the simulator's physics/render loop |
| Simulation Update Rate | 1000 Hz (matches 1 ms embedded main loop) |
| Flash Usage | Nearly full 16 KB -- had to disable trace, IR remote, and enum_to_string |
| RAM Issue | Stack overflow from trace calls -- fixed by disabling trace entirely |
| ADC Fix | Changed `ADC10SHT_3` (64 clock sample-and-hold) to `ADC10SHT_2` (16 clock) for faster line detection |
| State Manual Test | Re-enabled IR remote temporarily to test manual control via IR on the real robot |
| Timer Rename | Renamed IR remote's timer references from `timer` to `ir_timer` to avoid collision with new state machine timer type |

**Techniques & Methods:**
- **Simulated driver pattern**: For each hardware driver, create an alternative `.c` file with the same function signatures but different implementation. The simulated TB6612FNG driver writes to voltage lines instead of GPIO; the simulated QRE1113 reads voltage lines instead of ADC channels; the simulated VL53L0X reads voltage lines instead of I2C. The build system selects which implementation to compile.
- **Simulation-first development**: Write and iterate on the state machine logic in the simulator where the compile-test cycle is seconds. Once behavior is satisfactory, build for the MCU target and flash to the robot. This dramatically reduces development time.
- **Feature compile-out for space**: Adding Makefile defines (`-DDISABLE_TRACE`, `-DDISABLE_IR_REMOTE`) and wrapping code in `#ifndef DISABLE_*` blocks to remove non-essential features when flash/RAM is exhausted.
- **Cross-platform assert handler**: Modified `assert_handler.h` to use `__asm__ volatile("mov r2, %0" : "=r" (saved_pc))` only on MSP430 targets. On host (simulation), a simpler implementation is used since the assembly instruction is architecture-specific.
- **Iterative tuning in simulation**: The retreat states' move durations, search timeouts, and drive speeds were all tuned by running the simulation repeatedly and observing the robot's behavior. The author notes this iterative process is not shown in the video.

**Source Code Mapping:**
- `state_machine.c:process_input()` (completed): Full implementation reading enemy, line, and IR command, saving to input history, checking events in priority order.
- `state_search.c:state_search_run()` (completed): Uses `input_history_last_directed_enemy()` to choose rotation direction.
  ```c
  const struct enemy last_enemy =
      input_history_last_directed_enemy(data->common->input_history);
  if (enemy_at_right(&last_enemy)) {
      drive_set(DRIVE_DIR_ROTATE_RIGHT, DRIVE_SPEED_FAST);
  } else {
      drive_set(DRIVE_DIR_ROTATE_LEFT, DRIVE_SPEED_FAST);
  }
  ```
- `state_retreat.c:next_retreat_state()` (completed): Full decision tree for all line positions with enemy-aware alignment choices. 8 retreat substates with timed move sequences.
- `state_retreat.c:state_retreat_enter()` (completed): On TIMEOUT event, advances to next move in sequence. When all moves complete, posts `STATE_EVENT_FINISHED`.
  ```c
  case STATE_EVENT_TIMEOUT:
      data->move_idx++;
      if (retreat_state_done(data)) {
          state_machine_post_internal_event(data->common->state_machine_data,
                                            STATE_EVENT_FINISHED);
      } else {
          start_retreat_move(data);
      }
  ```
- Simulated `tb6612fng.c`: Sets voltage line values based on duty cycle and mode (forward/reverse/stop). Converts duty cycle to proportional voltage.
- Simulated `qre1113.c`: Reads voltage line values and applies the same 700 threshold as the real driver.
- Simulated `vl53l0x.c`: Reads voltage line values and scales to corresponding range values.
- `adc.c:55` -- Changed `ADC10SHT_3` to `ADC10SHT_2` to reduce sample-and-hold time for faster line sensor response.

**Demo / Example:**
- **Goal:** Complete the state machine, validate in simulation, then deploy to the real robot and demonstrate autonomous sumo behavior.
- **Why Important:** This is the culmination of the entire project -- every driver, every abstraction layer, every state handler comes together to produce autonomous behavior. The simulation-to-hardware transition validates the software architecture's portability.
- **Demo Flow:**
  1. Set up Bots2D simulator with nsumo application: two sumo bots on a circular platform (one keyboard-controlled, one state-machine-controlled).
  2. Initially robot doesn't move -- state machine starts in WAIT with no IR remote in simulation. Temporarily change start state to SEARCH.
  3. Fix missing motor mode setting in simulated driver. Rebuild. Robot now moves.
  4. Simulation demo: state-machine robot searches for enemy, attacks when found, retreats from line. Author uses keyboard to control opponent and compete against their own algorithm.
  5. Flash to real robot. Initially drives off platform -- line detection too slow (ADC sampling speed). Fix: reduce sample-and-hold time (SHT_3 -> SHT_2).
  6. After fix: robot detects lines, retreats, searches for enemy, pushes opponent. Not perfect but functional.
  7. Test manual mode with IR remote: WAIT -> IR command -> SEARCH -> IR command -> MANUAL (direct control via remote).
  8. Final commit and merge.
- **What Changed:**
  - `state_machine.c`: Completed `process_input()` with full event priority logic
  - `state_search.c`: Added input history-based rotation direction
  - `state_retreat.c`: Completed all retreat substates and transition logic
  - `adc.c`: Changed sample-and-hold time from `ADC10SHT_3` to `ADC10SHT_2`
  - `Makefile`: Added defines to disable trace, IR remote, and enum_to_string for space savings; renamed IR timer references
  - `assert_handler.h`: Conditional assembly for MSP430 vs. host targets
  - `state_manual.c`: Added `#ifndef DISABLE_IR_REMOTE` guard
  - Simulator repository: Added nsumo application, controller, scene, and simulated driver files

**Discussion Prompts:**
- **Q1: What was the most impactful real-world issue when moving from simulation to hardware?**
  - The ADC sampling speed. In simulation, sensor readings are instantaneous (just reading a float value), but on real hardware, the ADC using ACLK with maximum sample-and-hold time was too slow. The robot would drive past the white line before the ADC completed a conversion. Reducing the sample-and-hold time was a partial fix, but the author notes the robot's performance is still limited by sensor speed. This highlights that simulation cannot fully predict real-world timing constraints.
- **Q2: How does the simulated driver pattern enable code portability?**
  - The application code (state_machine.c, state_search.c, etc.) calls the same API functions (e.g., `drive_set()`, `enemy_get()`, `line_get()`) regardless of whether it runs on hardware or in simulation. Only the lowest-layer driver files are swapped: the real `tb6612fng.c` writes GPIO registers while the simulated one writes voltage line floats. The build system (CMake for simulation, Makefile for hardware) selects which driver files to compile. This clean separation is a direct benefit of the three-layer software architecture.

---

### Lesson 28 — The End

**File Path:** [28 The End  Embedded System Project Series #28.txt](Artful_Bytes_Transcript/28%20The%20End%20%20Embedded%20System%20Project%20Series%20%2328.txt)

**Objective:** Provides a retrospective on the entire 28-lesson embedded systems project series, reflecting on design decisions, lessons learned, and advice for future projects.

**Terminology & Key Concepts:**
- **Bare Metal Programming**: Writing firmware that directly controls hardware registers without an operating system or HAL library. Educational for understanding fundamentals, but not always practical for production projects.
- **Code Reuse vs. From Scratch**: In modern embedded development, leveraging existing libraries, vendor HAL code, and RTOS frameworks is preferred over writing everything from scratch. This series wrote everything from scratch for educational purposes.
- **Mechanical Design Impact on Software**: Poor hardware choices (too many motors, too many sensors, wrong MCU) compound into software difficulties. Simpler mechanical designs lead to smoother firmware development.
- **Sensor Sampling Speed**: The dominant performance bottleneck for the sumo robot. Both the line sensors (ADC) and range sensors (I2C VL53L0X) sampled too slowly for fast robot movements, limiting reaction time and maximum safe driving speed.
- **MCU Selection Trade-offs**: The MSP430G2553 was good for teaching but poor for this project: no dedicated PWM peripheral (had to share timer), insufficient flash/RAM (had to compile out features), and limited peripheral count.

**Terminology & Key Concepts (Course Retrospective):**
- **Register-level Understanding**: Even when using HALs or libraries in production, understanding what happens at the register level is invaluable for debugging, optimization, and adapting code to new hardware.
- **Project-based Learning**: Some aspects of embedded development (software architecture, build systems, CI, board bring-up) are easier to learn and understand in the context of a full project rather than isolated tutorials.

| Retrospective Topic | Assessment |
|---|---|
| Mechanical Design | Too many motors (4) and sensors (5 range, 4 line). 2 motors and fewer/simpler sensors would have been better. Side range sensors were unusable due to poor placement. |
| MCU Choice | MSP430G2553 too constrained -- no dedicated PWM, 16KB flash ran out, 512B RAM caused stack issues. A slightly larger MCU would have been far more practical. |
| Simulator Investment | Over-engineered. Building Bots2D from scratch was a C++ learning exercise but not worth the time for this project. A Python script or existing tool would have sufficed. |
| Bare Metal Approach | Good for education (reveals how hardware works), impractical for production (should reuse existing code). Still relevant for understanding fundamentals. |
| Sensor Performance | Line sensors and range sensors both too slow. This was the main performance limiter for the robot's reaction time. |
| Software Architecture | Three-layer separation (drivers, device drivers, application) paid off for portability between Launchpad, PCB, and simulation. |
| Overall Outcome | Robot works (locates and pushes enemy, retreats from line) but performance is mediocre due to hardware choices. The educational value was the primary achievement. |

**Techniques & Methods:**
- **Design simplicity principle**: For hobby/one-off projects, prefer fewer components, simpler sensor configurations, and over-specced MCUs. The cost difference between a $1 and $5 MCU is irrelevant for a single board, but the development time savings can be enormous.
- **Layered architecture payoff**: The three-layer code structure (application -> device driver -> peripheral driver) enabled running the same application code on three different platforms (Launchpad, nsumo PCB, Bots2D simulator) with only the lowest layer changing.
- **Start bare metal, then abstract**: Begin by learning register-level programming to understand the fundamentals, then move to using HALs, libraries, and RTOSes for production work. The register-level knowledge helps when things go wrong with higher-level abstractions.

**Demo / Example:**
- **Goal:** Summarize the complete project and share lessons learned for embedded systems practitioners.
- **Why Important:** Provides practical wisdom that only comes from completing an end-to-end embedded project, including mistakes that textbooks don't cover.
- **Demo Flow:**
  1. Review of all 28 lessons: Makefile, Git, CI, software architecture, GPIO, UART, memory, interrupts, ADC, I2C, PWM, board bring-up, simulation, state machine
  2. Reflection on writing all code from scratch -- educational but impractical for real projects
  3. Critique of mechanical design: 4 motors caused wobbly driving, 5 range sensors added complexity, side sensors were unusable
  4. Critique of MCU choice: MSP430G2553 lacked PWM, ran out of memory, timer peripheral conflicts
  5. Critique of simulator: valuable exercise but disproportionate effort for the benefit gained
  6. Acknowledgment: the robot works but is not competitive; the real value was the educational journey
  7. Farewell and mention of future project-based content

**Discussion Prompts:**
- **Q1: What single change would have the most impact on the robot's performance?**
  - Choosing a microcontroller with dedicated PWM outputs and more flash/RAM would have been the single highest-impact change. It would have eliminated the timer peripheral conflicts, removed the need to compile out features for space, and likely offered faster ADC peripherals with DMA that could sample at higher rates. A larger MCU (e.g., STM32F4 or MSP432) would cost negligible extra for a hobby project but save dozens of hours of development time.
- **Q2: What is the lasting value of this bare-metal approach?**
  - Understanding that "there is no magic behind anything at the deep level -- it is just register writes and then you layer code on top." When working with HALs, RTOSes, or vendor libraries in production, this foundation allows engineers to debug issues that abstraction layers hide, optimize critical paths, and adapt code to unusual hardware configurations. The three-layer architecture pattern (application -> device driver -> peripheral driver) demonstrated in this series is directly applicable to professional embedded projects.
- **Q3: Why does the author recommend simpler mechanical designs for embedded projects?**
  - More components mean more drivers to write, more pins to allocate, more I2C addresses to manage, more potential points of failure, and more complex application logic. The four-motor skid steering caused wobbly driving behavior. The five range sensors required complex I2C multiplexing and the side sensors had to be disabled due to poor mounting. Two motors with two wheels and a single front-facing range sensor would have produced a more reliable robot with far less code. In robotics, mechanical simplicity translates directly to software simplicity.


---

## 4. Course Interconnections

### Topic Interconnection Table

| Concept | Introduced In | Reused / Extended In | How |
|---|---|---|---|
| Register-level programming | Lesson 12 (GPIO) | Lessons 17-23 (all drivers) | Same PxDIR/PxSEL/PxIE pattern applied to UART, PWM, ADC, I2C peripherals |
| Makefile build system | Lesson 5 | Lessons 9-11 (CI, cppcheck, format) | Makefile extended with `cppcheck`, `format`, `size`, `symbols`, `flash` targets |
| Layered architecture | Lesson 6 | All driver/app lessons | Every new module placed in correct layer (drivers/ vs app/ vs common/) |
| Interrupt service routines | Lesson 17 | Lessons 18, 20, 21, 22 | ISR pattern reused for UART RX, IR remote decoding, PWM, ADC completion |
| Timer peripheral | Lesson 17 (interrupts) | Lessons 20 (IR), 21 (PWM), 22 (ADC) | Single Timer_A shared across PWM, millisecond tick, and IR timing — resource contention |
| State machine pattern | Lesson 26 (design) | Lesson 27 (implementation) | Skeleton in L26, filled with sensor/motor logic in L27; sub-states in retreat |
| Ring buffer | Lesson 18 (UART) | Lesson 26 (input history) | Ring buffer from UART RX reused for state machine input history tracking |
| I2C protocol | Lesson 23 | Lesson 24 (bring-up) | I2C driver tested during board bring-up with VL53L0X range sensors |
| Assert handler | Lesson 14 | All subsequent lessons | `ASSERT()` macro used throughout codebase for defensive programming |
| Module prefix convention | Lesson 7 (project structure) | All modules | Every function prefixed: `uart_init()`, `drive_forward()`, `state_search_enter()` |
| Conditional compilation | Lesson 13 (HW versions) | Lesson 16 (memory), 27 (sim) | `#ifdef LAUNCHPAD`/`NSUMO` pattern extended to `DISABLE_TRACE`, simulator builds |
| Test functions | Lesson 15 | Lessons 18, 21, 23, 24 | `test_uart()`, `test_pwm()`, `test_i2c()` pattern used to validate each new driver |

### Key Technical Threads

**Thread 1: Peripheral Driver Development**
- Lesson 12 (GPIO) → Lesson 17 (Interrupts) → Lesson 18 (UART) → Lesson 20 (IR remote) → Lesson 21 (PWM/Motors) → Lesson 22 (ADC/DMA) → Lesson 23 (I2C)
- Builds from simple register writes to complex multi-peripheral systems. Each driver builds on the GPIO and interrupt foundations. The timer peripheral becomes increasingly contended as PWM, IR timing, and millisecond ticks all need it.

**Thread 2: Build System & Quality Infrastructure**
- Lesson 5 (Makefile) → Lesson 8 (Git) → Lesson 9 (cppcheck) → Lesson 10 (CI/CD) → Lesson 11 (clang-format + docs)
- Starts with bare compilation, then layers version control, static analysis, automated CI, and formatting. Each addition makes the development workflow more professional and catches more errors earlier.

**Thread 3: From Components to Autonomous Robot**
- Lesson 2 (parts selection) → Lesson 6 (SW architecture) → Lessons 12-23 (drivers) → Lesson 24 (board bring-up) → Lesson 25 (simulator) → Lesson 26-27 (state machine) → Lesson 28 (reflection)
- The overarching project thread: choose parts, design architecture, implement drivers, bring up hardware, simulate behavior, implement autonomy, test on real robot.

**Thread 4: Memory & Resource Constraints**
- Lesson 5 (Makefile size target) → Lesson 16 (memory layout) → Lesson 19 (printf footprint) → Lesson 27 (ran out of flash)
- The 16 KB flash limit is a recurring constraint. Lightweight printf is chosen over standard printf. Trace/enum strings are compiled out via defines. In the final build, flash ran out and features had to be disabled.

---

## 5. Hardware, Software & Tools Inventory

### Hardware

| Item | Details |
|---|---|
| **Primary MCU** | MSP430G2553 — 16-bit RISC, 16 MHz, 16 KB flash, 512 B RAM, 20-pin (LaunchPad) / 28-pin (Nsumo PCB) |
| **Development Board** | MSP430 LaunchPad (MSP-EXP430G2ET) — used for isolated driver development |
| **Custom PCB** | Nsumo sumo robot board — 4 motors, 3 front range sensors, 4 line sensors, IR receiver |
| **Motor Driver** | TB6612FNG — dual H-bridge, controls 2 motors per chip (2 chips for 4 motors) |
| **Range Sensors** | VL53L0X — I2C time-of-flight laser, 3 units (front left, center, right) |
| **Line Sensors** | QRE1113 — analog reflectance, 4 units (front-left, front-right, back-left, back-right) |
| **IR Receiver** | TSOP38238 — 38 kHz, NEC protocol, used with standard IR remote |
| **Motors** | 4x micro brushed DC motors with gearboxes |
| **Battery** | LiPo battery (3.7V), with voltage regulators on PCB |
| **Debug Tools** | Oscilloscope, logic analyzer, multimeter, MSP430 LaunchPad debugger |

### Software & Tools

| Tool | Purpose | Notes |
|---|---|---|
| **msp430-elf-gcc 9.3.1.11** | Cross-compiler | TI's GCC toolchain for MSP430 |
| **Code Composer Studio 11.x** | IDE | Eclipse-based, used for step-debugging |
| **GNU Make** | Build system | Primary build method, custom Makefile |
| **mspdebug** | Flash programmer | Command-line tool, `make flash` target |
| **cppcheck** | Static analyzer | `make cppcheck`, catches common C bugs |
| **clang-format-12** | Code formatter | Rules in `.clang-format`, `make format` target |
| **Git** | Version control | Conventional commits format |
| **GitHub Actions** | CI/CD | Builds + cppcheck on every push |
| **Docker** | CI environment | `artfulbytes/msp430-gcc-9.3.1.11:latest` image |
| **PlantUML** | Diagram generation | State machine and architecture diagrams from plain text |
| **picocom** | Serial terminal | 115200 baud, `/dev/ttyUSB0` |
| **readelf / objdump** | Memory analysis | `make size`, `make symbols` |
| **addr2line** | Assert debugging | Converts program counter to file:line |

### Libraries

| Library | Purpose | Notes |
|---|---|---|
| **mpaland/printf** | Lightweight printf | Git submodule under `external/printf/`, configured via `printf_config.h`, ~2 KB vs ~8 KB standard printf |

---

## 6. Complete Techniques Catalog

| Technique | Description | Example |
|---|---|---|
| Register-level GPIO | Configure pins via PxDIR, PxOUT, PxSEL, PxREN registers | `P1DIR \|= BIT0; P1OUT \|= BIT0;` |
| Bit manipulation | Set/clear/toggle individual bits in registers | `reg \|= BIT3;` (set), `reg &= ~BIT3;` (clear), `reg ^= BIT3;` (toggle) |
| Polling-based main loop | Continuous 1 ms loop checking sensors and running state logic | `while(1) { process_input(); process_event(); sleep_ms(1); }` |
| Interrupt-driven UART | RX via ISR + ring buffer, TX via polling | `__interrupt void USCI_RX_ISR(void) { ring_buffer_put(&rx_buf, UCA0RXBUF); }` |
| NEC protocol decoding | Timer-based edge detection to decode IR remote commands | Measure pulse widths: 562.5 us = bit boundary, long space = 1, short = 0 |
| PWM motor control | Timer capture/compare for variable duty cycle | `TAxCCRn = duty;` where duty controls motor speed |
| Tank drive | Differential steering via independent left/right motor speeds | `drive_set(left_speed, right_speed)` — positive = forward, negative = reverse |
| ADC with DMA | Hardware-triggered conversion with automatic memory transfer | Configure DMA channel to transfer ADC results to buffer on conversion complete |
| I2C bit-banging alternative | Software I2C when hardware peripheral unavailable | Toggle SCL/SDA pins manually with timing delays |
| State machine (table-driven) | Transition table array mapping (state, event) → next_state | `{ STATE_SEARCH, STATE_EVENT_ENEMY, STATE_ATTACK }` |
| Conditional compilation | `#ifdef HW_VERSION` to support multiple hardware targets | `#ifdef LAUNCHPAD ... #elif NSUMO ... #endif` |
| Custom assert handler | Trigger breakpoint + UART trace + LED blink on failure | `ASSERT(ptr != NULL)` → prints PC address, blinks LED forever |
| Lightweight printf | Submodule-based printf with config header to minimize flash | `#define PRINTF_DISABLE_SUPPORT_FLOAT` in `printf_config.h` |
| Static analysis integration | cppcheck in Makefile and CI pipeline | `cppcheck --enable=all --error-exitcode=1 src/` |
| Docker-based CI | Consistent build environment via container | `artfulbytes/msp430-gcc-9.3.1.11:latest` in GitHub Actions |
| Memory footprint analysis | readelf/size to track flash and RAM usage | `make size` → shows text/data/bss segment sizes |
| Board bring-up | Systematic per-peripheral validation on new hardware | Test each driver individually: LED → UART → motors → sensors |
| 2D simulation | C++ simulator for algorithm development without hardware | Simulated sensors/motors with same API as real drivers |
| Sub-state machines | Nested states within a parent state | Retreat state has internal sequence: reverse → rotate → resume search |
| Input history ring buffer | Track recent sensor readings for smarter decisions | `ring_buffer` stores last N (enemy, line) readings for state transitions |

---

## 7. Best Practices & Industry Patterns

### 1. Code Organization Practices

Code Organization = Structuring source files into layers and modules with clear interfaces

#### 1.1 Layered Architecture

##### Definition
Separate code into driver, application, and common layers where higher layers depend on lower layers but not vice versa.

##### Why Important
Prevents circular dependencies, makes drivers reusable across projects, isolates hardware-specific code from application logic.

##### Pattern to Adopt
```c
// src/drivers/uart.c — driver layer (hardware-specific)
#include "drivers/uart.h"
void uart_init(void) { /* register-level config */ }

// src/app/drive.c — application layer (uses drivers)
#include "drivers/tb6612fng.h"
#include "drivers/pwm.h"
void drive_forward(uint16_t speed) {
    tb6612fng_set_direction(MOTOR_LEFT, DIR_FORWARD);
    pwm_set_duty(PWM_MOTOR_LEFT, speed);
}
```

##### Anti-Pattern to Avoid
```c
// BAD: Application logic mixed into driver
void uart_init(void) {
    // Register config here...
    // Then directly calling state machine logic — wrong layer!
    state_machine_notify(UART_READY);
}
```

##### Course Reference
Lesson 6 — "Software Architecture" and Lesson 7 — "Project Structure"

---

#### 1.2 Module Naming Convention

##### Definition
Every function is prefixed with its module name. One module = one `.c/.h` pair.

##### Why Important
Avoids name collisions in C (no namespaces), makes it immediately clear where a function lives, enables grep-based navigation.

##### Pattern to Adopt
```c
// uart.c / uart.h
void uart_init(void);
void uart_write(const char *data, uint16_t len);

// i2c.c / i2c.h
void i2c_init(void);
void i2c_read(uint8_t addr, uint8_t reg, uint8_t *buf, uint16_t len);
```

##### Anti-Pattern to Avoid
```c
// BAD: Generic names without module prefix
void init(void);       // Which init? uart? i2c? adc?
void read(uint8_t *buf); // Read from where?
```

##### Course Reference
Lesson 7 — "Project Structure", `docs/coding_guidelines.md`

---

### 2. Defensive Programming Practices

Defensive Programming = Writing code that fails safely and helps you find bugs fast

#### 2.1 Custom Assert Handler

##### Definition
Implement a project-specific assert macro that triggers a debugger breakpoint, prints the failing address, and blinks an LED — instead of silently continuing.

##### Why Important
On a microcontroller there is no console to print stack traces. Without asserts, bugs manifest as mysterious hardware behavior that is extremely hard to trace.

##### Pattern to Adopt
```c
// assert_handler.h
#define ASSERT(expr) \
    do { \
        if (!(expr)) { \
            assert_handler(__FILE__, __LINE__); \
        } \
    } while (0)

// assert_handler.c
void assert_handler(const char *file, int line) {
    __disable_interrupt();
    // Trigger breakpoint if debugger attached
    __op_code(0x4343);
    // Trace address via UART
    trace("ASSERT: %s:%d", file, line);
    // Blink LED forever
    while (1) { led_toggle(); sleep_ms(500); }
}
```

##### Anti-Pattern to Avoid
```c
// BAD: Silent failure
void process_data(uint8_t *data) {
    if (data == NULL) return; // Silently does nothing — bug hidden
    // ...
}
```

##### Course Reference
Lesson 14 — "Assert on a Microcontroller"

---

### 3. Build System & Quality Practices

Build System & Quality = Automated tooling that catches errors before they reach hardware

#### 3.1 CI/CD Pipeline with Docker

##### Definition
Use GitHub Actions with a Docker container to automatically build and statically analyze every commit.

##### Why Important
Catches compilation errors and static analysis warnings before code is merged. Docker ensures the CI environment matches the development environment exactly.

##### Pattern to Adopt
```yaml
# .github/workflows/ci.yml
jobs:
  build:
    runs-on: ubuntu-latest
    container: artfulbytes/msp430-gcc-9.3.1.11:latest
    steps:
      - uses: actions/checkout@v2
      - run: make HW=LAUNCHPAD
      - run: make HW=NSUMO
      - run: make cppcheck
```

##### Anti-Pattern to Avoid
```yaml
# BAD: No CI — relies on developer to remember to build and check
# (No ci.yml at all, or CI that only builds without analysis)
```

##### Course Reference
Lesson 10 — "Simple CI/CD with GitHub Actions and Docker"

---

#### 3.2 Static Analysis in Build System

##### Definition
Integrate cppcheck as a Makefile target and CI step so static analysis runs with a single command.

##### Why Important
Catches bugs the compiler misses: null pointer dereferences, buffer overflows, unused functions, unreachable code.

##### Pattern to Adopt
```makefile
# Makefile
CPPCHECK_FLAGS = --quiet --enable=all --error-exitcode=1 \
    --inline-suppr --suppress=missingIncludeSystem
cppcheck:
    @$(CPPCHECK) $(CPPCHECK_FLAGS) $(SOURCES)
```

##### Anti-Pattern to Avoid
```makefile
# BAD: Running cppcheck manually with inconsistent flags
# Developer runs: cppcheck src/main.c (misses other files)
# No --error-exitcode so CI never fails on warnings
```

##### Course Reference
Lesson 9 — "Static Analysis with cppcheck"

---

### 4. Embedded-Specific Practices

Embedded-Specific = Patterns unique to resource-constrained MCU development

#### 4.1 Memory-Conscious Development

##### Definition
Continuously monitor flash and RAM usage with `make size` and `make symbols`, and use conditional compilation to disable non-essential features.

##### Why Important
MSP430G2553 has only 16 KB flash and 512 B RAM. Running out of flash during development (as happened in Lesson 27) blocks progress and forces feature removal.

##### Pattern to Adopt
```c
// defines.h — compile out features to save flash
#define DISABLE_TRACE
#define DISABLE_ENUM_STRINGS

// trace.c — conditional implementation
#ifndef DISABLE_TRACE
void trace(const char *fmt, ...) { /* full implementation */ }
#else
void trace(const char *fmt, ...) { /* empty */ }
#endif
```

##### Anti-Pattern to Avoid
```c
// BAD: Using standard printf (8 KB) instead of lightweight printf (2 KB)
#include <stdio.h>
printf("Debug: %f\n", voltage); // Pulls in float support — huge flash cost
```

##### Course Reference
Lesson 16 — "How Microcontroller Memory Works", Lesson 19 — "Printf on a Microcontroller"

---

#### 4.2 Hardware Abstraction via Conditional Compilation

##### Definition
Use `#ifdef` blocks and Makefile defines to support multiple hardware targets (LaunchPad vs Nsumo PCB) from a single codebase.

##### Why Important
Development happens on the LaunchPad (20-pin) but deployment is on the Nsumo PCB (28-pin) with different pin mappings. Code must work on both without manual changes.

##### Pattern to Adopt
```c
// io.c — different pin mappings per hardware
#ifdef LAUNCHPAD
    #define LED_PIN BIT0
    #define LED_PORT P1OUT
#elif NSUMO
    #define LED_PIN BIT5
    #define LED_PORT P3OUT
#endif

void led_on(void) { LED_PORT |= LED_PIN; }
```

##### Anti-Pattern to Avoid
```c
// BAD: Hardcoded pins, requires manual editing to switch targets
void led_on(void) { P1OUT |= BIT0; } // Only works on LaunchPad
```

##### Course Reference
Lesson 13 — "Handling Multiple Hardware Versions"

---

## 8. Common Pitfalls

| Pitfall | Consequence | Prevention |
|---|---|---|
| Using standard `printf` on MCU | Consumes ~8 KB flash (half of MSP430's 16 KB) | Use lightweight printf library (mpaland/printf, ~2 KB) with float support disabled |
| Not checking flash/RAM usage regularly | Run out of flash late in project, must remove features | Run `make size` after every major addition; set up size budget early |
| Forgetting volatile on ISR-shared variables | Compiler optimizes away reads; variable appears stuck | Always `volatile` for variables modified in ISR and read in main loop |
| Blocking code in polling loop | Entire system freezes; sensors stop being read | Never block in the main loop; use timer-based state machines instead of delays |
| Too many sensors/motors for MCU | Timer/peripheral contention, not enough PWM channels | Choose MCU based on project peripheral requirements, not just familiarity |
| Skipping board bring-up | Multiple failing systems make debugging impossible | Test each peripheral in isolation before integrating (LED → UART → motors → sensors) |
| No assert handler | Bugs manifest as mysterious hardware behavior | Implement custom assert with breakpoint + LED + UART trace from day one |
| Ignoring static analysis warnings | Null pointer dereferences, buffer overflows ship to hardware | Integrate cppcheck in CI; use `--error-exitcode=1` to block merges |
| Not using version control from start | Can't track what change broke something; no rollback | `git init` before writing first line of code; conventional commits for history |
| Hardcoded pin mappings | Code breaks when switching between dev board and target PCB | Use `#ifdef` per hardware version in a centralized io module |
| Over-engineering simulation | Effort exceeds benefit; C++ simulator took too long | Use simple simulation (Python) or skip; test on real hardware when possible |
| Side-mounted range sensors | False detections due to placement; sensors discarded | Fewer, better-placed sensors beat many poorly placed ones |
| Four motors instead of two | Wobbly driving behavior, complex wiring | Simpler mechanical design with 2 larger motors gives better stability |

---

## 9. Source Code & Project Reference

### Project Summary

| # | Project Name | Demonstrates | Key Files |
|---|---|---|---|
| 1 | Nsumo Sumo Robot | Complete bare-metal embedded project: drivers, state machine, autonomous behavior | `src/main.c`, `src/app/state_machine.c`, `Makefile` |
| 2 | Blink Example | Minimal Makefile-based MSP430 project | `Code/blink_example/main.c`, `Code/blink_example/Makefile` |

### Key Code Locations

| Module | Header | Implementation | Build Command |
|---|---|---|---|
| Main entry | — | `src/main.c` | `make HW=LAUNCHPAD` |
| State machine | `src/app/state_machine.h` | `src/app/state_machine.c` | — |
| Wait state | `src/app/state_wait.h` | `src/app/state_wait.c` | — |
| Search state | `src/app/state_search.h` | `src/app/state_search.c` | — |
| Attack state | `src/app/state_attack.h` | `src/app/state_attack.c` | — |
| Retreat state | `src/app/state_retreat.h` | `src/app/state_retreat.c` | — |
| Manual state | `src/app/state_manual.h` | `src/app/state_manual.c` | — |
| Drive control | `src/app/drive.h` | `src/app/drive.c` | — |
| Enemy detection | `src/app/enemy.h` | `src/app/enemy.c` | — |
| Line detection | `src/app/line.h` | `src/app/line.c` | — |
| Timer utility | `src/app/timer.h` | `src/app/timer.c` | — |
| Input history | `src/app/input_history.h` | `src/app/input_history.c` | — |
| GPIO driver | `src/drivers/io.h` | `src/drivers/io.c` | — |
| UART driver | `src/drivers/uart.h` | `src/drivers/uart.c` | — |
| I2C driver | `src/drivers/i2c.h` | `src/drivers/i2c.c` | — |
| PWM driver | `src/drivers/pwm.h` | `src/drivers/pwm.c` | — |
| ADC driver | `src/drivers/adc.h` | `src/drivers/adc.c` | — |
| Motor H-bridge | `src/drivers/tb6612fng.h` | `src/drivers/tb6612fng.c` | — |
| IR remote | `src/drivers/ir_remote.h` | `src/drivers/ir_remote.c` | — |
| VL53L0X ToF | `src/drivers/vl53l0x.h` | `src/drivers/vl53l0x.c` | — |
| QRE1113 line | `src/drivers/qre1113.h` | `src/drivers/qre1113.c` | — |
| LED driver | `src/drivers/led.h` | `src/drivers/led.c` | — |
| MCU init | `src/drivers/mcu_init.h` | `src/drivers/mcu_init.c` | — |
| Millis timer | `src/drivers/millis.h` | `src/drivers/millis.c` | — |
| Assert handler | `src/common/assert_handler.h` | `src/common/assert_handler.c` | — |
| Ring buffer | `src/common/ring_buffer.h` | `src/common/ring_buffer.c` | — |
| Trace/debug | `src/common/trace.h` | `src/common/trace.c` | — |
| Sleep utility | `src/common/sleep.h` | `src/common/sleep.c` | — |
| Enum strings | `src/common/enum_to_string.h` | `src/common/enum_to_string.c` | — |
| Defines | `src/common/defines.h` | — | — |
| Lightweight printf | `external/printf/printf.h` | `external/printf/printf.c` | Config: `external/printf_config.h` |
| Tests | — | `src/test/test.c` | `make HW=LAUNCHPAD TEST=test_xxx` |

### Build Configuration

- **Makefile targets:** `all`, `clean`, `flash`, `cppcheck`, `format`, `size`, `symbols`, `addr2line`, `terminal`, `tests`
- **Hardware selection:** `HW=LAUNCHPAD` (20-pin dev board) or `HW=NSUMO` (28-pin robot PCB)
- **Toolchain path:** `TOOLS_PATH` env var pointing to TI toolchain root
- **Compiler flags:** `-mmcu=msp430g2553 -Wall -Wextra -Werror -Wshadow -fshort-enums -Og -g`
- **Key defines:** `PRINTF_INCLUDE_CONFIG_H`, `DISABLE_ENUM_STRINGS`, `DISABLE_TRACE`
- **CI container:** `artfulbytes/msp430-gcc-9.3.1.11:latest`
- **Code formatter:** `.clang-format` in root, applied via `make format`

---

## 10. Lesson Transcript Index

| Section | Lesson | Transcript File |
|---|---|---|
| S1: Hardware Design | 001: Intro and Overview | [1 Intro and Overview.txt](Artful_Bytes_Transcript/1%20Intro%20and%20Overview%20%20Embedded%20System%20Project%20Series%20%231.txt) |
| S1: Hardware Design | 002: Picking the Parts | [2 Picking the Parts.txt](Artful_Bytes_Transcript/2%20Picking%20the%20Parts%20for%20a%20Small%20Robot%20%20%20Embedded%20System%20Project%20Series%20%232.txt) |
| S1: Hardware Design | 003: PCB Design Walkthrough | [3 PCB Design Walkthrough.txt](Artful_Bytes_Transcript/3%20PCB%20Design%20Walkthrough%20Sumo%20Robot%20%20Embedded%20System%20Project%20Series%20%233.txt) |
| S2: Dev Environment | 004: Install IDE and Blink LED | [4 Install IDE and Blink LED.txt](Artful_Bytes_Transcript/4%20Install%20an%20IDE%20and%20Blink%20an%20LED%20%28Code%20Composer%20Studio%20%2B%20MSP430%29%20%20Embedded%20System%20Project%20Series%20%234.txt) |
| S2: Dev Environment | 005: Programming without IDE (Makefile) | [5 Makefile + Toolchain.txt](Artful_Bytes_Transcript/5%20Microcontroller%20Programming%20without%20IDE%20%28Makefile%20%2B%20Toolchain%29%20%20Embedded%20System%20Project%20Series%20%235.txt) |
| S3: SW Architecture | 006: Software Architecture | [6 Software Architecture.txt](Artful_Bytes_Transcript/6%20How%20to%20Create%20a%20Software%20Architecture%20%20Embedded%20System%20Project%20Series%20%236.txt) |
| S3: SW Architecture | 007: Project Structure | [7 Project Structure.txt](Artful_Bytes_Transcript/7%20The%20BEST%20Project%20Structure%20for%20CC%2B%2BMCU%20%20Embedded%20System%20Project%20Series%20%237.txt) |
| S4: Workflow | 008: Version Control with Git | [8 Git Best Practices.txt](Artful_Bytes_Transcript/8%20How%20I%20version%20control%20with%20git%20%28Best%20Practices%29%20%20Embedded%20System%20Project%20Series%20%238.txt) |
| S4: Workflow | 009: Static Analysis (cppcheck) | [9 Static Analysis.txt](Artful_Bytes_Transcript/9%20Static%20Analysis%20for%20CC%2B%20with%20cppcheck%20%28%2BMakefile%29%20%20Embedded%20System%20Project%20Series%20%239.txt) |
| S4: Workflow | 010: CI/CD with GitHub Actions | [10 CI/CD.txt](Artful_Bytes_Transcript/10%20Simple%20CICD%20with%20GitHub%20Actions%20and%20Docker%20%28Compile%2BAnalysis%29%20%20%20Embedded%20System%20Project%20Series%20%2310.txt) |
| S4: Workflow | 011: Documentation and Clang-format | [11 Documentation.txt](Artful_Bytes_Transcript/11%20Documentation%20and%20Clang%20format%20%28%2B2%20bugs%29%20%20%20Embedded%20System%20Project%20Series%20%2311.txt) |
| S5: Low-Level | 012: GPIO Programming in C | [12 GPIO.txt](Artful_Bytes_Transcript/12%20How%20I%20program%20GPIOs%20in%20C%20%20Embedded%20System%20Project%20Series%20%2312.txt) |
| S5: Low-Level | 013: Multiple Hardware Versions | [13 Hardware Versions.txt](Artful_Bytes_Transcript/13%20Handling%20multiple%20Hardware%20Versions%20%20Embedded%20System%20Project%20Series%20%2313.txt) |
| S5: Low-Level | 014: Assert on Microcontroller | [14 Assert.txt](Artful_Bytes_Transcript/14%20Assert%20on%20a%20Microcontroller%20%20Embedded%20System%20Project%20Series%20%2314.txt) |
| S5: Low-Level | 015: Small Test Functions | [15 Test Functions.txt](Artful_Bytes_Transcript/15%20My%20Small%20Test%20Functions%20%20Embedded%20System%20Project%20Series%20%2315.txt) |
| S5: Low-Level | 016: Microcontroller Memory | [16 Memory.txt](Artful_Bytes_Transcript/16%20How%20Microcontroller%20Memory%20Works%20%20Embedded%20System%20Project%20Series%20%2316.txt) |
| S5: Low-Level | 017: Interrupts | [17 Interrupts.txt](Artful_Bytes_Transcript/17%20Microcontroller%20Interrupts%20%20Embedded%20System%20Project%20Series%20%2317.txt) |
| S5: Low-Level | 018: UART Driver | [18 UART.txt](Artful_Bytes_Transcript/18%20Write%20a%20UART%20driver%20%28Polling%20and%20Interrupt%29%20%20Embedded%20System%20Project%20Series%20%2318.txt) |
| S5: Low-Level | 019: Printf on Microcontroller | [19 Printf.txt](Artful_Bytes_Transcript/19%20Printf%20on%20a%20Microcontroller%20%20Embedded%20System%20Project%20Series%20%2319.txt) |
| S5: Low-Level | 020: NEC Protocol (IR Remote) | [20 NEC IR Remote.txt](Artful_Bytes_Transcript/20%20NEC%20Protocol%20Driver%20%28Infrared%20remote%29%20%20Embedded%20System%20Project%20Series%20%2320.txt) |
| S6: Motor Control | 021: Motor Control with PWM | [21 PWM Motor Control.txt](Artful_Bytes_Transcript/21%2020%20Motor%20Control%20with%20PWM%20in%20C%20%20Embedded%20System%20Project%20Series%20%2321.txt) |
| S7: Sensors | 022: ADC Driver with DMA | [22 ADC DMA.txt](Artful_Bytes_Transcript/22%20ADC%20driver%20with%20DMA%20in%20C%20%20Embedded%20System%20Project%20Series%20%2322.txt) |
| S7: Sensors | 023: I2C Driver (VL53L0X) | [23 I2C.txt](Artful_Bytes_Transcript/23%20I2C%20driver%20in%20C%20%28with%20VL53L0X%20sensor%29%20%20Embedded%20System%20Project%20Series%20%2323.txt) |
| S8: Integration | 024: Board Bring-up | [24 Board Bring-up.txt](Artful_Bytes_Transcript/24%20How%20to%20Board%20Bring-up%20%20Embedded%20System%20Project%20Series%20%2324.txt) |
| S8: Integration | 025: 2D Robot Simulator | [25 Simulator.txt](Artful_Bytes_Transcript/25%20I%20made%20a%20Robot%202D%20Simulator%20with%20C%2B%2B%20%20Embedded%20System%20Project%20Series%20%2325.txt) |
| S8: Integration | 026: State Machine Design | [26 State Machine.txt](Artful_Bytes_Transcript/26%20How%20to%20Code%20a%20State%20Machine%20%20Embedded%20System%20Project%20Series%20%2326.txt) |
| S8: Integration | 027: Simulation to Real-world | [27 Sim to Real.txt](Artful_Bytes_Transcript/27%20Simulation%20to%20Real-world%20Demo%20%20Embedded%20System%20Project%20Series%20%2327.txt) |
| S8: Integration | 028: The End (Reflection) | [28 The End.txt](Artful_Bytes_Transcript/28%20The%20End%20%20Embedded%20System%20Project%20Series%20%2328.txt) |

---

## Appendix A: Pareto Base

> Based on the Pareto principle (80/20 rule): the ~20% of topics that deliver ~80% of the course's practical value.

### Essential Topics (80/20)

These 6 topic areas cover the vast majority of what you need to build a complete embedded project:

| # | Essential Topic | Lessons | Why This Is 80/20 |
|---|---|---|---|
| 1 | **Register-Level GPIO & Peripheral Access** | 12, 17, 18 | Every driver starts here. Understanding PxDIR/PxSEL/PxOUT/PxIE registers is the foundation for all hardware interaction. Once you can configure GPIO and read the datasheet, you can write any driver. |
| 2 | **Interrupt-Driven Architecture** | 17, 18, 20 | The mechanism that makes embedded systems responsive. ISR + ring buffer pattern for UART. Timer interrupts for PWM and IR decoding. Without interrupts, you can't handle real-time events. |
| 3 | **State Machine Design & Implementation** | 26, 27 | The pattern that organizes all application logic. Table-driven transitions, per-state enter/run functions, event processing loop. This is how most embedded products structure their behavior. |
| 4 | **Makefile Build System + Toolchain** | 5, 9, 10 | The infrastructure that makes everything else possible. Cross-compilation, hardware targets, cppcheck integration, CI/CD — you'll use this pattern in every professional embedded project. |
| 5 | **Layered Software Architecture** | 6, 7 | Drivers → Application → Common separation. Module naming conventions. This architectural decision shapes every file and function you write. Get this wrong and the project becomes unmaintainable. |
| 6 | **Communication Protocols (UART, I2C)** | 18, 23 | The two most common protocols in embedded. UART for debug/printf. I2C for sensors. Understanding clock, data, addresses, and bus arbitration transfers to any MCU platform. |

### Essential Diagrams

These diagrams provide the highest-value visual understanding of the system:

| # | Diagram | Location | What It Shows | Why Essential |
|---|---|---|---|---|
| 1 | **Software Architecture** | `docs/sw_arch.png` | Three-layer view: drivers, app, common with module dependencies | Shows how ALL code modules relate — the single most important architectural reference |
| 2 | **State Machine** | `docs/state_machine.png` | WAIT → SEARCH → ATTACK → RETREAT transitions with events | The complete autonomous behavior logic in one diagram — how the robot "thinks" |
| 3 | **Retreat Sub-State** | `docs/retreat_state.png` | Internal states within RETREAT (reverse → rotate → resume) | The most complex state; understanding its sub-states is key to understanding robot behavior |
| 4 | **System Block Diagram** | `docs/sysdiag.jpg` | Hardware blocks: MCU, motors, sensors, power, debug interfaces | Maps every physical component to its electrical connections — essential for board bring-up |
| 5 | **Schematic** | `docs/schematic.png` | Full electrical schematic of the Nsumo PCB | Pin-level connections between MCU and peripherals — the reference for all driver code |
| 6 | **Memory Map (conceptual)** | Lesson 16 transcript | Flash layout: interrupt vectors, .text, .data, .bss, stack | Understanding where code/data lives in 16 KB flash + 512 B RAM — critical for optimization |

### Pareto Study Strategy

If you have limited time, study in this order:
1. **Lesson 6** (SW Architecture) — understand the big picture
2. **Lesson 12** (GPIO) — learn register-level programming
3. **Lesson 17** (Interrupts) — understand how MCUs handle events
4. **Lesson 18** (UART) — implement your first complete driver with ISR
5. **Lesson 26** (State Machine) — see how application logic is structured
6. **Lesson 5** (Makefile) — understand the build system

These 6 lessons (21% of the course) give you the conceptual framework to understand the remaining 22 lessons.

---

## Conclusion

This 28-lesson series by Artful Bytes is a comprehensive, project-driven course that takes the learner from an empty microcontroller to a fully autonomous sumo robot. The key takeaway is that professional embedded development is not just about writing drivers — it's about the entire ecosystem: architecture design, build systems, version control, CI/CD, static analysis, testing, and systematic integration.

The course demonstrates that bare-metal programming reveals there is "no magic" — at the deepest level, everything is register reads and writes, layered with abstractions to make code manageable. The state machine pattern ties everything together, transforming individual peripheral drivers into coordinated autonomous behavior.

### Closing Reflection

- I was able to understand all 28 lessons and their implementation in the nsumo source code. The layered architecture, state machine design, and driver implementations are clearly mapped between transcripts and code.
- Areas of minor uncertainty: The 2D simulator (Lesson 25) is written in C++ and lives in a separate repository not included here — the specific simulator implementation details are based solely on the transcript description. The exact VL53L0X driver implementation (`vl53l0x.c` at 31 KB) contains vendor-specific register sequences that are complex but not fully explained in the transcript.
