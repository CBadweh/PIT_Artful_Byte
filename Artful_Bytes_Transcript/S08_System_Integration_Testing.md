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
