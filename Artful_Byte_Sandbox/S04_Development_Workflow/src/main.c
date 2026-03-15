#include <msp430.h>

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;

    P1DIR |= 0x01;

    while (1) {
        P1OUT ^= 0x01;
        __delay_cycles(250000);
    }

    return 0;
}
