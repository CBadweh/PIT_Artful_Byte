/* Lesson 12 — Test 1: test_blink_led using io_configure on a single pin. */

#include "common/assert_handler.h"
#include "common/defines.h"
#include "drivers/io.h"
#include "drivers/mcu_init.h"

static void test_blink_led(void)
{
    const struct io_config led_config =
    {
        .dir = IO_DIR_OUTPUT,
        .select = IO_SELECT_GPIO,
        .resistor = IO_RESISTOR_DISABLED,
        .out = IO_OUT_LOW
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
    mcu_init();
    test_blink_led();
    ASSERT(0);
    return 0;
}
