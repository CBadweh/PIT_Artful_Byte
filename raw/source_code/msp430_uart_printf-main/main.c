#include <msp430.h>
#include "trace.h"
#include "uart.h"

static void msp430_init()
{
    WDTCTL = WDTPW | WDTHOLD; /* Stop watchdog timer */
    if (CALBC1_1MHZ == 0xFF) { /* Check if calibration constat erased */
        while(1); /* Trap CPU */
    }
    /* Configure the MCLK (and SMCLK) for 1 MHz using the Digitally controlled
     * oscillator (DCO) as source. */
    DCOCTL = 0;
    BCSCTL1 = CALBC1_1MHZ;
    DCOCTL = CALDCO_1MHZ;
}

int main(void)
{
    msp430_init();
    uart_init();

    int i = 0;
    while(1) {
        TRACE_INFO("Index %d", i++);
    }
}
