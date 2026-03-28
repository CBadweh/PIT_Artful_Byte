// Final version using io abstraction layer

#include "common/assert_handler.h"
#include "drivers/mcu_init.h"
#include "drivers/io.h"
/*
int main(void)
{
    mcu_init();

    // Test: Blink LED using IO abstraction layer
    while (1) {
        io_set_out(IO_TEST_LED, IO_OUT_HIGH);
        BUSY_WAIT_ms(250);
        io_set_out(IO_TEST_LED, IO_OUT_LOW);
        BUSY_WAIT_ms(250);
    }

    ASSERT(0);
    return 0;
}
*/


// Raw register manipulation, no abstraction layer
/*
#include <msp430.h>

static void test_blink_led(void)
{
    // TODO: Use io functions
    P1DIR |= BIT0;
    volatile unsigned int i; // volatile to prevent optimization
    while (1) {
        P1OUT ^= BIT0;
        for (i = 10000; i > 0; i--) { } // delay
    }
}

int main(void)
{
    // TODO: Move to mcu_init
    WDTCTL = WDTPW + WDTHOLD; // stop watchdog timer
    test_blink_led();
    return 0;
} */



// Intermediate version using io abstraction layer
// Pin:    IO_TEST_LED = IO_10 = P1.0 = Port 1, Pin 0
#include <msp430.h>          // WDTCTL, WDTPW, WDTHOLD (still used directly)
#include "drivers/io.h"      // io_configure, io_set_out, io_e, io_config, all enums

static void test_blink_led(void)
{
    const struct io_config led_config =
    {
        .dir = IO_DIR_OUTPUT,  // driving the LED, not reading it, 1
        .select = IO_SELECT_GPIO, // plain GPIO (not UART/I2C/PWM), 0
        .resistor = IO_RESISTOR_DISABLED, // note needed for output, 0
        .out = IO_OUT_LOW // LED starts off, 0
    };
    io_configure(IO_TEST_LED, &led_config);
    io_out_e out = IO_OUT_LOW;
    while (1) {
        out = (out == IO_OUT_LOW) ? IO_OUT_HIGH : IO_OUT_LOW;
        io_set_out(IO_TEST_LED, out);
        __delay_cycles(250000); // 250 ms
    }
}

int main(void)
{
    // TODO: Move to mcu_init
    WDTCTL = WDTPW + WDTHOLD; // stop watchdog timer
    test_blink_led();
    return 0;
}

