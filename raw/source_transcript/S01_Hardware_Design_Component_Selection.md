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
