#include "drivers/io.h"
#include "drivers/mcu_init.h"
#include "drivers/led.h"
#include "common/assert_handler.h"
#include "common/defines.h"
#include <msp430.h>

SUPPRESS_UNUSED
static void test_setup(void)
{
    mcu_init();
}

SUPPRESS_UNUSED
static void test_assert(void)
{
    test_setup();
    ASSERT(0);
}

SUPPRESS_UNUSED
static void test_blink_led(void)
{
    test_setup();
    led_init();
    while (1) {
        led_set(LED_TEST, LED_STATE_ON);
        BUSY_WAIT_ms(250);
        led_set(LED_TEST, LED_STATE_OFF);
        BUSY_WAIT_ms(250);
    }
}

int main(void)
{
    TEST();
    ASSERT(0);
}
