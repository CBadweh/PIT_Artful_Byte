/* Lesson 12 — io_init() bulk pin initialization.
 * mcu_init() calls io_init(), which loops through io_initial_configs[]
 * and configures every pin at boot. No manual io_configure() needed. */

#include "common/assert_handler.h"
#include "common/defines.h"
#include "drivers/io.h"
#include "drivers/mcu_init.h"

int main(void)
{
    mcu_init();

    while (1) {
        io_set_out(IO_TEST_LED, IO_OUT_HIGH);
        BUSY_WAIT_ms(250);
        io_set_out(IO_TEST_LED, IO_OUT_LOW);
        BUSY_WAIT_ms(250);
    }

    ASSERT(0);
    return 0;
}
