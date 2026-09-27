/* Lesson 12 — intermediate: IO driver + manual watchdog in main. */

#include <msp430.h>

#include "drivers/io.h"

static void test_blink_led(void)
{
    /* Configure the LED */
    const struct io_config led_config = {
        .dir = IO_DIR_OUTPUT,
        .select = IO_SELECT_GPIO,
        .resistor = IO_RESISTOR_DISABLED,
        .out = IO_OUT_LOW,
    };
    // Now we can access led_config through . operator

    /* Initialize LED */
    io_set_select(IO_TEST_LED, led_config.select);   // set P1SEL  = 0 and P1SEL2 = 0  
    io_set_direction(IO_TEST_LED, led_config.dir);   // set P1DIR = 1 for output
    io_set_out(IO_TEST_LED, led_config.out);         // set P1OUT 
    io_set_resistor(IO_TEST_LED, led_config.resistor); // set P1REN 0
    
    // io_configure(IO_TEST_LED, &led_config);
    
    io_out_e out = IO_OUT_LOW;
    while (1) {
        out = (out == IO_OUT_LOW) ? IO_OUT_HIGH : IO_OUT_LOW;
        io_set_out(IO_TEST_LED, out);
        __delay_cycles(250000);
    }
}

int main(void)
{
    WDTCTL = WDTPW + WDTHOLD; /* stop watchdog timer */
    test_blink_led();
    return 0;
}
