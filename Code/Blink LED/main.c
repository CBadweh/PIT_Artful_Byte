// Lesson 14: Assert on a Microcontroller (CCS IDE + TI compiler version)

#include "common/assert_handler.h"
#include "common/defines.h"
#include "drivers/mcu_init.h"
#include "drivers/io.h"
#include "drivers/led.h"

static void test_assert(void)
{
    ASSERT(0); // Always fails -- triggers assert handler
}

static void test_blink_led(void)
{
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
    // mcu_init();
    // test_blink_led();
    test_assert(); // Uncomment to trigger assert handler
    return 0;
}
