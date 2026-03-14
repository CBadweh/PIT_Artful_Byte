#include <msp430.h>
#include "led.h"

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;  // Stop watchdog timer
    led_init();

    volatile unsigned int i;    // volatile to prevent optimization

    while(1)
    {
        led_toggle();
        for(i = 50000; i > 0; i--); // Delay
    }
}
