/* Lesson 12 — MCU initialization. Only stops the watchdog for now; clocks (16 MHz)
 * and global interrupts are added in later lessons (17/18). */

#include "drivers/mcu_init.h"
#include "drivers/io.h"
#include <msp430.h>

static inline void watchdog_setup(void)
{
    WDTCTL = WDTPW + WDTHOLD;
}

void mcu_init(void)
{
    watchdog_setup();
    io_init();
}
