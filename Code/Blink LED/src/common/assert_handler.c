#include "common/assert_handler.h"
#include "common/defines.h"
#include <msp430.h>

/* The TI compiler provides intrinsic support for calling a specific opcode, which means
 * you can write __op_code(0x4343) to trigger a software breakpoint (when LAUNCHPAD FET
 * debugger is attached). MSP430-GCC uses __asm volatile("CLR.B R3") instead, but both
 * produce the same opcode 0x4343. */
#define BREAKPOINT __op_code(0x4343);

#define GPIO_OUTPUT_LOW(port, bit)                                                                 \
    do {                                                                                           \
        P##port##SEL &= ~(BIT##bit);                                                               \
        P##port##SEL2 &= ~(BIT##bit);                                                              \
        P##port##DIR |= BIT##bit;                                                                  \
        P##port##REN &= ~(BIT##bit);                                                               \
        P##port##OUT &= ~(BIT##bit);                                                               \
    } while (0)

static void assert_blink_led(void)
{
    GPIO_OUTPUT_LOW(1, 0); // Test LED (Launchpad)
    GPIO_OUTPUT_LOW(2, 6); // Test LED (Nsumo)
    while (1) {
        // Blink LED on both targets in case the wrong target was flashed
        P1OUT ^= BIT0;
        P2OUT ^= BIT6;
        BUSY_WAIT_ms(250);
    };
}

/* Minimize code dependency in this function to reduce the risk of accidently calling
 * a function with an assert in it, which would cause the assert_handler to be called
 * recursively until stack overflow. */
void assert_handler(uint16_t program_counter)
{
    UNUSED(program_counter);
    BREAKPOINT
    assert_blink_led();
    while(1){};
    // assert_blink_led();
}
