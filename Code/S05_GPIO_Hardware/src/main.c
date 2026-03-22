#include "common/assert_handler.h"
#include "drivers/mcu_init.h"
#include "drivers/io.h"

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
