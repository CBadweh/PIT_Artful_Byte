#include "drivers/io.h"

#include <msp430.h>
#include <stdint.h>

#define IO_PORT_CNT (1u)

/* With "-fshort-enums", enum values are one byte; encoding:
 * [ zeros (3) | port (2) | pin (3) ] */
/*  CBadweh's Note
    Bitsise Operation (Code Trick) at timestamp 15:40
    pin = enum & 0x7
    pin_bit = 0x1 << pin
    port = (enum & (0x3<<3))
*/
#define IO_PORT_OFFSET (3u)
#define IO_PORT_MASK (0x3u << IO_PORT_OFFSET)
#define IO_PIN_MASK (0x7u)

static uint8_t io_port(io_e io)
{
    return (io & IO_PORT_MASK) >> IO_PORT_OFFSET;
}
static inline uint8_t io_pin_idx(io_e io)
{
    return io & IO_PIN_MASK;
}
static uint8_t io_pin_bit(io_e io)
{
    return 1 << io_pin_idx(io);
}

/*  CBadweh's Note
    Array Indexing (Code Trick) at timestamp 30:00
*/
static volatile uint8_t *const port_dir_regs[IO_PORT_CNT] = { &P1DIR };
static volatile uint8_t *const port_ren_regs[IO_PORT_CNT] = { &P1REN };
static volatile uint8_t *const port_out_regs[IO_PORT_CNT] = { &P1OUT };
static volatile uint8_t *const port_sel1_regs[IO_PORT_CNT] = { &P1SEL };
static volatile uint8_t *const port_sel2_regs[IO_PORT_CNT] = { &P1SEL2 };
void io_configure(io_e io, const struct io_config *config)
{
    io_set_select(io, config->select);
    io_set_direction(io, config->dir);
    io_set_out(io, config->out);
    io_set_resistor(io, config->resistor);
}
void io_set_select(io_e io, io_select_e select)
{
    const uint8_t port = io_port(io);
    const uint8_t pin = io_pin_bit(io);
    switch (select) {
    case IO_SELECT_GPIO:
        *port_sel1_regs[port] &= ~pin;
        *port_sel2_regs[port] &= ~pin;
        break;
    }
}

void io_set_direction(io_e io, io_dir_e direction)
{
    const uint8_t port = io_port(io);
    const uint8_t pin = io_pin_bit(io);
    switch (direction) {
    case IO_DIR_OUTPUT:
        *port_dir_regs[port] |= pin;
        break;
    }
}

void io_set_resistor(io_e io, io_resistor_e resistor)
{
    const uint8_t port = io_port(io);
    const uint8_t pin = io_pin_bit(io);
    switch (resistor) {
    case IO_RESISTOR_DISABLED:
        *port_ren_regs[port] &= ~pin;
        break;
    }
}

void io_set_out(io_e io, io_out_e out)
{
    const uint8_t port = io_port(io);
    const uint8_t pin = io_pin_bit(io);
    switch (out) {
    case IO_OUT_LOW:
        *port_out_regs[port] &= ~pin;
        break;
    case IO_OUT_HIGH:
        *port_out_regs[port] |= pin;
        break;
    }
}

