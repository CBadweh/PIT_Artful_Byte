#ifndef IO_H
#define IO_H

#include <stdint.h>

/* Trimmed IO driver for intermediate LED demo only (Launchpad). */

// clang-format off
typedef enum {
    IO_10, IO_11, IO_12, IO_13, IO_14, IO_15, IO_16, IO_17,
    IO_20, IO_21, IO_22, IO_23, IO_24, IO_25, IO_26, IO_27,
} io_generic_e;
// clang-format on

typedef enum
{
    IO_TEST_LED = IO_10,
    IO_UART_RXD = IO_11,
    IO_UART_TXD = IO_12,
    IO_LINE_DETECT_FRONT_LEFT = IO_13,
    IO_UNUSED_2 = IO_14,
    IO_UNUSED_3 = IO_15,
    IO_I2C_SCL = IO_16,
    IO_I2C_SDA = IO_17,
    IO_IR_REMOTE = IO_20,
    IO_MOTORS_LEFT_CC_1 = IO_21,
    IO_MOTORS_LEFT_CC_2 = IO_22,
    IO_RANGE_SENSOR_FRONT_INT = IO_23,
    IO_XSHUT_FRONT = IO_24,
    IO_UNUSED_11 = IO_25,
    IO_PWM_MOTORS_LEFT = IO_26,
    IO_UNUSED_13 = IO_27,
} io_e;

typedef enum
{
    IO_SELECT_GPIO,
    IO_SELECT_ALT1,
    IO_SELECT_ALT2,
    IO_SELECT_ALT3,
} io_select_e;

typedef enum
{
    IO_DIR_INPUT,
    IO_DIR_OUTPUT,
} io_dir_e;

typedef enum
{
    IO_RESISTOR_DISABLED,
    IO_RESISTOR_ENABLED,
} io_resistor_e;

typedef enum
{
    IO_OUT_LOW,
    IO_OUT_HIGH,
} io_out_e;

typedef enum
{
    IO_IN_LOW,
    IO_IN_HIGH,
} io_in_e;


struct io_config
{
    io_select_e select;
    io_resistor_e resistor;
    io_dir_e dir;
    io_out_e out;
};

void io_configure(io_e io, const struct io_config *config);
void io_set_select(io_e io, io_select_e select);
void io_set_direction(io_e io, io_dir_e direction);
void io_set_resistor(io_e io, io_resistor_e resistor);
void io_set_out(io_e io, io_out_e out);
io_in_e io_get_input(io_e io);

#endif /* IO_H */
