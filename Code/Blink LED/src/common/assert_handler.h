#ifndef ASSERT_HANDLER_H

#include <stdint.h>

// Assert implementation suitable for a microcontroller

/* TI compiler does not support GCC extended inline assembly for capturing
 * the program counter. Use the CCS debugger call stack instead — when the
 * breakpoint fires, the call stack shows exactly which ASSERT triggered. */
#define ASSERT(expression)                                                                         \
    do {                                                                                           \
        if (!(expression)) {                                                                       \
            assert_handler(0);                                                                     \
        }                                                                                          \
    } while (0)

// TODO: Decide what this should do
#define ASSERT_INTERRUPT(expression)                                                               \
    do {                                                                                           \
        if (!(expression)) {                                                                       \
            while (1) { }                                                                          \
        }                                                                                          \
    } while (0)

void assert_handler(uint16_t program_counter);

#endif // ASSERT_HANDLER_H
