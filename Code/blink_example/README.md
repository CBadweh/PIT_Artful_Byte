# Blink Example (Lesson 5)

Minimal MSP430G2553 blink LED project built from the command line using GCC and a custom     Makefile — no IDE required. This is the outcome of **Lesson 5: Microcontroller Programming   without IDE (Makefile + Toolchain)**.                                                      

  ## What It Does

  Toggles the LED on P1.0 of the MSP430 LaunchPad in an infinite loop with a busy-wait delay.
   Demonstrates:
  - Cross-compiling with `msp430-elf-gcc`
  - Multi-file project structure (`main.c` + `led.c/led.h`)
  - Makefile with pattern rules, separate compile/link stages, and flash target

  ## Prerequisites

  - TI MSP430 GCC toolchain at `C:/ti/msp430-gcc`
  - `msp430-elf-gcc` on PATH
  - DSLite (included with CCS) at `C:/ti/ccs2041/ccs/ccs_base/DebugServer/bin/`
  - MSP430 LaunchPad connected via USB

  ## Commands

  ```bash
  make          # build → bin/blink.elf
  make flash    # flash to LaunchPad
  make clean    # remove build artifacts