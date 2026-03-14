# Blink LED (Lesson 4)

  IDE-generated blink LED project using **Code Composer Studio (CCS)** for the     
  MSP430G2553 LaunchPad. This is the outcome of **Lesson 4: Install an IDE and     
  Blink an LED (Code Composer Studio + MSP430)**.

  ## What It Does

  Toggles the LED on P1.0 of the MSP430 LaunchPad using a busy-wait delay.
  Demonstrates:
  - Setting up Code Composer Studio for MSP430 development
  - Cross-compilation via TI's IDE (the "black box" approach before Lesson 5's     
  Makefile)
  - Stopping the watchdog timer (`WDTCTL = WDTPW | WDTHOLD`)
  - GPIO output configuration and XOR toggle (`P1OUT ^= BIT0`)
  - Using `volatile` to prevent the compiler from optimizing away the delay loop   

  ## Prerequisites

  - Code Composer Studio (CCS) with MSP430 support installed
  - MSP430 LaunchPad connected via USB

  ## How to Build & Flash

  1. Open CCS
  2. Import this folder as an existing CCS project
  3. Build (hammer icon or `Ctrl+B`)
  4. Debug/Flash (bug icon or `F11`)