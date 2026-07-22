#include "common/assert_handler.h"
#include "common/defines.h"
#include <msp430.h>

/* MSP430-GCC: 0x4343 breakpoint opcode is assembly instruction "CLR.B R3". */
#define BREAKPOINT __asm volatile("CLR.B R3");

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
    GPIO_OUTPUT_LOW(1, 0); /* Test LED (Launchpad) */
    GPIO_OUTPUT_LOW(2, 6); /* Test LED (Nsumo) */
    while (1) {
        P1OUT ^= BIT0;
        P2OUT ^= BIT6;
        BUSY_WAIT_ms(250);
    };
}

void assert_handler(uint16_t program_counter)
{
    UNUSED(program_counter);
    BREAKPOINT
    assert_blink_led();
}
