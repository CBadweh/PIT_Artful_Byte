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
