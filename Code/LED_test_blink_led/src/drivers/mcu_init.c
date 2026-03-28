#include "drivers/mcu_init.h"
#include "common/assert_handler.h"
#include "drivers/io.h"
#include <msp430.h>

static inline void init_clocks(void)
{
    ASSERT(CALBC1_1MHZ != 0xFF && CALBC1_16MHZ != 0xFF);

    BCSCTL1 = CALBC1_16MHZ;
    DCOCTL = CALDCO_16MHZ;
    BCSCTL3 = LFXT1S_2;
}

static inline void watchdog_setup(void)
{
    WDTCTL = WDTPW + WDTHOLD;
}

void mcu_init(void)
{
    watchdog_setup();
    init_clocks();
    io_init();
    _enable_interrupts();
}
