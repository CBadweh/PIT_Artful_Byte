<!-- 
CBADWEH NOTE: NOT VERIFIED
 -->




# Alarm HAL Restructure — Living Reference

<!--
PURPOSE: Restructure alarm.c to include HAL calls (sensor read + LED actuation)
so that ONE module demonstrates both Phase 1B (CMock on host) and Phase 1C (real HAL on target).
This ticket follows from the unity-on-target milestone (2026-05-06).
-->

## Why This Ticket Exists

The Nucleo Coverage Pipeline spec (`raw/Nucleo_Coverage_Pipeline_Project.md`) requires:
- **Phase 1A**: Abstract a module with HAL calls
- **Phase 1B**: Test it on host using CMock to fake HAL
- **Phase 1C**: Test it on target with real HAL, collect .gcda

Currently, `alarm.c` only has the threshold logic (step 2). The HAL calls for reading sensors (step 1) and driving the LED (step 3) live in `main.c` instead. This means:
- CMock is **not exercised** on the alarm module — there's nothing to mock
- Host and target tests run identical code paths — no difference between phases
- The spec's intent of one module demonstrating both phases is **not fulfilled**

Dual-target [[pattern]]
This is exactly what JW asked for in the transcript:

1. "Run the unit tests on target" — 11 tests running on the NUCLEO board, printing pass/fail over UART ✓
2. "Two build configurations" — Debug (normal) and UnitTest (test runner replaces main) ✓
3. "No button press needed" — tests run automatically, no human trigger ✓
4. "See the name of the test printed out with pass/fail" — test_REQ_ALM_001_critical_temperature:PASS etc. ✓
5. "Add test cases to cover the other sensor" — pressure tests included, both branches hit ✓
6. "Red-to-green demo" — coverage report shows which lines are hit; comment out a test → red, put it back → green ✓
7. "Test runner that initializes, runs setup, executes test cases, runs teardown" — test_main.c does exactly this with UNITY_BEGIN → RUN_TEST → UNITY_END ✓
8. "Dumps everything out and then just completes" — gcov data dumps after tests, then while(1) { __WFI(); } halts ✓

## Original Design Intent (Realized During 2026-05-06 Session)

The button-driven demo in `main.c` was originally meant to **simulate sensor readings**:

```
Button press = simulates a sensor reading arriving
               (mimics HAL_ADC_GetValue() returning a new value)

Press 1: sensor reads 50.0F  -> NONE
Press 2: sensor reads 72.0F  -> WARNING
Press 3: sensor reads 90.0F  -> CRITICAL
Press 4: sensor reads 68.0F  -> WARNING (hysteresis)
Press 5: sensor reads 60.0F  -> NONE (clear)
```

The button wasn't just a "next test" trigger — it was standing in for a real sensor event.

## Current State (alarm.c)

```c
// alarm.c today — pure logic, NO HAL calls
alarm_level_t alarm_evaluate(sensor_type_t type, float reading, alarm_state_t *state)
{
    switch (type) {
        case SENSOR_TEMPERATURE:
            if (reading >= TEMP_CRIT) { ... }
            ...
        case SENSOR_PRESSURE:
            ...
        default:
            return ALARM_NONE;
    }
}
```

- Takes a float parameter (caller provides the reading)
- Returns an enum (caller decides what to do with it)
- Zero HAL dependencies

## Target State (what alarm.c should become)

```c
// alarm.c restructured — includes HAL calls
alarm_level_t alarm_check(sensor_type_t type, alarm_state_t *state)
{
    // Step 1: READ sensor via HAL
    float reading = HAL_ADC_GetValue(...);  // or I2C read, etc.

    // Step 2: EVALUATE (existing logic, unchanged)
    alarm_level_t level;
    switch (type) {
        case SENSOR_TEMPERATURE:
            if (reading >= TEMP_CRIT) { ... }
            ...
    }

    // Step 3: ACTUATE output via HAL
    if (level >= ALARM_WARNING)
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);   // LED on
    else
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET); // LED off

    return level;
}
```

## What This Enables

```
Phase 1B (host, Ceedling):
  CMock fakes HAL_ADC_GetValue()   -> feeds test temperatures
  CMock fakes HAL_GPIO_WritePin()  -> verifies LED was set correctly
  test/hal/stm32u5xx_hal.h        -> add HAL_ADC_GetValue prototype
  Coverage: gcovr on host

Phase 1C (target, UnitTest build):
  Real HAL_ADC_GetValue()          -> real sensor (or simulated values)
  Real HAL_GPIO_WritePin()         -> real LED lights up
  Coverage: gcov over UART -> .gcda

ONE module, BOTH phases, BOTH CMock and real HAL demonstrated.
```

## Files to Touch

| File | Change |
|------|--------|
| `Core/Src/alarm.c` | Add HAL read + HAL actuation calls |
| `Core/Inc/alarm.h` | Update function signature (remove `reading` param, add HAL include) |
| `test/test_alarm.c` | Rewrite tests to use CMock `_ExpectAndReturn` for HAL calls |
| `test/hal/stm32u5xx_hal.h` | Add `HAL_ADC_GetValue()` prototype (so CMock can mock it) |
| `Core/Test/test_main.c` | Update `RUN_TEST` calls if function names change |
| `Core/Src/main.c` | Simplify — remove HAL calls that move into alarm.c |

## Key Decisions To Make

- [ ] Which HAL function to use for sensor read? (`HAL_ADC_GetValue` vs a custom `sensor_read()` wrapper)
- [ ] Should LED actuation be inside `alarm_evaluate` or in a separate `alarm_actuate()`?
- [ ] Keep `alarm_evaluate()` as-is (pure logic) and add a new `alarm_check()` that wraps it with HAL? This preserves the existing pure-logic function for cases where you want to test logic separately.

## Decisions Made (2026-05-06 session)

- **Use dual-targeting pattern**: Same test file builds on both host (CMock) and target (real HAL) via `#ifdef TEST`. See `wiki/dual-targeting-pattern.md` for full pattern.
- **No wrapper layers**: Rejected `sensor_read()` wrapper, `alarm_check.c` separate file, and `mock_sensor.h`/`mock_led.h` approaches. Module calls HAL directly (like `button.c` does).
- **Button proves the pattern first**: Button dual-targeting implemented and verified on host (3/3 PASS). Must verify on target before applying to alarm.
- **`_Ignore()` over `_Expect()` for portability**: setUp uses `_Ignore()` for HAL calls instead of `_Expect()` in each test. Trades strict argument verification for host+target portability.

## Approaches Tried and Reverted (2026-05-06)

| # | Approach | Why it failed |
|---|----------|---------------|
| 1 | `sensor_read()` wrapper + `mock_sensor.h` + `mock_led.h` | Too many abstraction layers. Not the pattern from the sandbox button example. |
| 2 | `alarm_check()` in separate `alarm_check.c` | Ceedling couldn't auto-discover without matching header. Worked with `alarm_check.h` but added unnecessary files. |
| 3 | Everything in `alarm.c` + `test_alarm.c` with `mock_stm32u5xx_hal.h` | Broke target sharing — `test_alarm.c` included by `test_main.c` which has no CMock. |
| 4 | `TEST_SOURCE_FILE()` Ceedling directive | Ceedling 1.0.1 doesn't define this as a compiler macro. |

## Prerequisite

This ticket depends on the unity-on-target milestone being complete:
- [x] UnitTest build config working (2026-05-06)
- [x] 8/8 tests PASS on target
- [x] gcov streaming over UART
- [x] `test/test_alarm.c` shared between host and target via `#include`

## Source Documents

| Document | Location |
|----------|----------|
| Pipeline spec | `raw/Nucleo_Coverage_Pipeline_Project.md` (Phase 1A, 1B, 1C) |
| JW transcript | `raw/JW_Code_Coverage_2nd_input.txt` |
| Current ticket | `Progress/missions_tickets/Code-coverage-JW-rev2_Reference.md` |
| alarm.c | `Core/Src/alarm.c` |
| test_alarm.c | `test/test_alarm.c` |
| fake HAL | `test/hal/stm32u5xx_hal.h` |

---
<!-- STOP: Do not read below this line unless the user explicitly asks. CBadweh's personal notes. -->
## CBadweh's Notes

Diagram
### Directory Structure

```
C-unit-test-Basic-Ceedling/
├── src/
│   ├── main.c                   ← Application (not tested)
│   │   └── average.c            ← Component 1: pure logic (no hardware), ← swap failure cases (Wrong operation, null, negative)
│   │   └── led.c                ← Component 2: calls HAL_GPIO_TogglePin (void)  ← swap failure cases (Wrong port, name)
│   │   └── button.c             ← Component 3: calls HAL_GPIO_ReadPin (returns int) ← swap failure cases
│   ├── alarm/
│   │   ├── alarm.h
│   │   ├── alarm.c              ← Component 3: calls HAL_GPIO_ReadPin (returns int) ← swap failure cases
│   │   └── gcov_dump.c          ←   
│   └── hal/
│       └── stm32u5xx_hal.h      ← Minimal HAL declarations (CMock parses this). replaces real HAL
│ 
├── Test/
│   └──  test_main.c              ← On Target Unity runner: main() + 8 test functions + SystemClock_Config + Error_Handler
│ 
├── test/
│   ├── test_alarm.c                      ← 
│   └── test_led.c, test_button.c    ← Mock test (checks function call + args) ← Stub test (checks call + args + return value)
│                 
│
├── vendor/ceedling/              ← Ceedling + Unity + CMock frameworks
├── project.yml                   ← Ceedling config. Single config file (replaces all Makefiles)           
├── build/
|    ├── test/runners/test_alarm_runner.c  ← Oh Host Ceedling runner. Ceedling scan test_alarm.c and generate this runnder
|    │                     
|    ├── gcov/out/                 ← Host Side
|    │   ├── alarm.gcno             ← branch map (host GCC 14)
|    │   └── alarm.gcda             ← counters (auto-written at exit)
|    ├── artifacts/gcov/gcovr/
|    |   └── GcovCoverageResults.html  ← Host report
|    |
|    └── on_target                  ← Target Side
|       ├── alarm.gcno
|       ├── alarm.gcda
|       └── GcovCoverageResults.html  ← report
|
├── ThirdParty/Unity/src/
│   ├── unity.c                    ← 
│   ├── unity.h                    ← 
│   ├── unity_internals.h          ←
│   └── test_button.c              ← 
|
└── gcov_decode.py                ← 


```

### Flow Charts

```


```



### Architecture 
```
      ┌───────────────────────────────────────────────────────┐
      │          APPLICATION                                  │
      │          main.c                                       │
      └───────────────────────────────────────────────────────┘
      ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
      │  COMPONENT 1  │   │  COMPONENT 2  │   │  COMPONENT 3  │
      │  src/average/ │   │  src/led/     │   │  src/button/  │
      └───────────────┘   └───────────────┘   └───────────────┘
      ┌──────────────────────────────────────────────────────┐
      │            DRIVERS                                   │
      └──────────────────────────────────────────────────────┘

COMPONENT 1 = src/average/ (average.h + average.c)



     ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
     │    TEST 1       │   │    TEST 2       │   │    TEST 3       │
     │ test_average.c  |   │  test_led.c     │   │ test_button.c   │
     │ simple   null   |   │  simple empty   │   │ button_pressed  │
     └─────────────────┘   └─────────────────┘   └─────────────────┘
     ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
     │  COMPONENT 1    │   │  COMPONENT 2    │   │  COMPONENT 3    │
     │  src/average/   │   │  src/sum/       │   │  COMPONENT 3    │
     └─────────────────┘   └─────────────────┘   └─────────────────┘
     ┌ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ┐
     │                    TEST DOUBLES                             │
     └ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ┘


Hardward Dependent
Stub : predefined return for interface  
Mock : predefined behavior for interaction  
Fake : limited working implementation
```




## Run

```bash
ceedling test:all              # Run all tests (4 total)
ceedling test:test_average     # Run one suite
ceedling test:test_led
ceedling test:test_button

ceedling gcov:all   # for coverage, I need to modify project.yml for enable - gcov    

ceedling clean                 # Remove build artifacts
```



# Dual-target pattern
see [[pattern]]
## How test_button.c Dual-Targets

**One file, two builds.** The `#ifdef TEST` guard is the only difference between host and target.

```c
#include "unity.h"
#include "button.h"

#ifdef TEST                          // Ceedling defines TEST
#include "mock_stm32u5xx_hal.h"      // CMock provides HAL implementations
#endif

void setUp(void)
{
#ifdef TEST
    HAL_Delay_Ignore();              // Tell CMock: let HAL_Delay pass
#endif
}

// Test functions — zero platform-specific code
void test_button_pressed_returns_true(void)
{
    HAL_GPIO_EXTI_Rising_Callback(GPIO_PIN_13);   // simulate press
    bool result = button_was_pressed();            // calls real button logic
    TEST_ASSERT_TRUE(result);                      // check result
}
```

**What happens on each platform:**

| | Host (Ceedling) | Target (STM32CubeIDE UnitTest) |
|---|---|---|
| `TEST` defined? | Yes | No |
| `mock_stm32u5xx_hal.h` | Included → CMock provides HAL | Skipped → real HAL linked by IDE |
| `HAL_Delay(200)` | CMock intercepts, `_Ignore` lets it pass | Real 200ms delay runs |
| Runner | Ceedling auto-generates | `test_main.c` includes the file, hand-written `RUN_TEST()` |
| setUp/tearDown | Defined in file (`#ifndef TEST_RUNNER`) | `test_main.c` defines its own (`#define TEST_RUNNER`) |
| Coverage | `ceedling gcov:test_button` | `gcov_decode.py --port COM3 --gcno-dir UnitTest` |

**Three mechanisms make it work:**

1. **`#ifdef TEST`** — conditionally includes mock layer. Host gets CMock, target gets real HAL.
2. **`_Ignore()` not `_Expect()`** — test functions stay platform-neutral. No CMock-specific calls in test logic.
3. **`#ifndef TEST_RUNNER`** — guards setUp/tearDown so test_main.c can provide a shared version when including multiple test files.









