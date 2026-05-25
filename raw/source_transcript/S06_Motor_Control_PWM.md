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
