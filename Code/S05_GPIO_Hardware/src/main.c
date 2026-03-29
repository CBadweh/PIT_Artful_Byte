#include "common/assert_handler.h"
#include "drivers/mcu_init.h"

int main(void)
{
    mcu_init();
    ASSERT(0);
    return 0;
}

/*
 * Previous versions kept for reference:
 *
 * --- Raw register manipulation (Lesson 12) ---
 * P1DIR |= BIT0; P1OUT ^= BIT0; with volatile delay loop
 *
 * --- Intermediate io abstraction (Lesson 12) ---
 * io_configure(IO_TEST_LED, &led_config); io_set_out(); __delay_cycles()
 *
 * --- io_init + io_set_out (Lesson 13) ---
 * mcu_init(); io_set_out(IO_TEST_LED, ...); BUSY_WAIT_ms(250);
 *
 * --- Lesson 14: test functions in main.c ---
 * test_assert(), test_blink_led() — moved to src/test/test.c in Lesson 15
 */
