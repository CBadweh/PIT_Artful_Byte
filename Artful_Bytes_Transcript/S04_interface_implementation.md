# Interface Implementation — From Binary Fundamentals to GPIO Bit-Packing

| | |
|---|---|
| **Course link** | Section 5, Lesson 12 — "How I Program GPIOs in C" |
| **Section file** | `S05_Low_Level_Programming_Fundamentals.md` → Lesson 012 → Techniques: "Bitwise Port/Pin Extraction" |
| **Source files** | `Code/S05_GPIO_Hardware/src/drivers/io.c` (functions: `io_port()`, `io_pin_idx()`, `io_pin_bit()`) |
| **Header** | `Code/S05_GPIO_Hardware/src/drivers/io.h` (enum: `io_generic_e`, `io_e`) |
| **Why this exists** | The bit-packing pattern encodes port+pin into a single enum value so one line of code handles all pins — avoiding per-pin switch statements that waste flash on a 16 KB MCU |
| **Prerequisite concepts** | Binary counting, bitwise AND, bit shifting, masking |

A mini lesson plan to build up to the `io_generic_e` enum bit-packing pattern in `io.c`.
Work through each level before moving to the next.

---

## Level 1: Binary Number System

Decimal counts in powers of 10. Binary counts in powers of 2.

```
Decimal    Binary     How to read it
───────    ──────     ──────────────
  0         000       0
  1         001       1
  2         010       2
  3         011       2+1
  4         100       4
  5         101       4+1
  6         110       4+2
  7         111       4+2+1
  8        1000       8         ← needs a 4th bit
  9        1001       8+1
 10        1010       8+2
```

**Key insight:** With N bits you can represent 2^N values.
- 3 bits → 8 values (0-7)
- 2 bits → 4 values (0-3)
- 8 bits → 256 values (0-255)

**Exercise:** Convert these to binary by hand: 6, 11, 15, 16

---

## Level 2: Bitwise AND — Extracting Bits (Masking)

`&` compares each bit pair. Both must be 1 to get 1.

```
    1 0 1 1 0 1 1 0     ← original value
  & 0 0 0 0 0 1 1 1     ← mask (0x7)
    ─────────────────
    0 0 0 0 0 1 1 0     ← only the lower 3 bits survive
```

A mask **keeps** the bits where the mask is 1, and **zeroes** everything else.

```
Common masks:
  0x7  = 00000111  → keeps lower 3 bits
  0x3  = 00000011  → keeps lower 2 bits
  0xF  = 00001111  → keeps lower 4 bits
  0x18 = 00011000  → keeps bits 3 and 4
```

**Exercise:** What is `13 & 0x7`?  (13 = 00001101, 0x7 = 00000111)

---

## Level 3: Bit Shifting — Moving Bits Left or Right

`<<` shifts bits left (multiply by 2).  `>>` shifts bits right (divide by 2).

```
Left shift:
  00000001 << 3  =  00001000    (1 becomes 8)
  00000001 << 0  =  00000001    (1 stays 1)

Right shift:
  00011000 >> 3  =  00000011    (24 becomes 3)
  00001000 >> 3  =  00000001    (8 becomes 1)
```

**Exercise:** What is `1 << 5`?  What is `16 >> 4`?

---

## Level 4: Combining Mask + Shift

To extract bits from the middle of a byte: mask first, then shift.

```
Example: extract bits 3-4 from the value 10 (00001010)

  Step 1 — mask:    00001010 & 00011000  =  00001000   (keep bits 3-4)
  Step 2 — shift:   00001000 >> 3        =  00000001   (move to position 0)

  Result: 1
```

This is the core pattern: `(value & mask) >> shift`

**Exercise:** Extract bits 3-4 from the value 9 (00001001).

---

## Level 5: Packing Two Values into One Byte

You can store multiple small values in a single byte by assigning them different bit positions.

```
Layout: [ unused(3) | field_A(2) | field_B(3) ]

Example: field_A = 1, field_B = 5

  field_A = 1   →  in bits 3-4:  00001000
  field_B = 5   →  in bits 0-2:  00000101
  combined:                      00001101  = 13 decimal

To read them back:
  field_B = 13 & 0x7             = 00000101 = 5    (mask lower 3 bits)
  field_A = (13 & 0x18) >> 3     = 00000001 = 1    (mask bits 3-4, shift right)
```

**Exercise:** Pack field_A=2, field_B=3 into one byte. Then extract them back.

---

## Level 6: The GPIO Enum — Applying It

Now apply this to the MSP430. Each pin has a **port** (0-2) and a **pin** (0-7).
We need 2 bits for port, 3 bits for pin. They fit in one byte:

```
Layout: [ 000 | Port(2) | Pin(3) ]

Enum     Int   Binary      Port  Pin
────     ───   ────────    ────  ───
IO_10  →  0  → 00|000|000    0    0   → P1.0
IO_11  →  1  → 000|00|001    0    1   → P1.1
IO_12  →  2  → 000|00|010    0    2   → P1.2
IO_13  →  3  → 000|00|011    0    3   → P1.3
IO_14  →  4  → 000|00|100    0    4   → P1.4
IO_15  →  5  → 000|00|101    0    5   → P1.5
IO_16  →  6  → 000|00|110    0    6   → P1.6
IO_17  →  7  → 000|00|111    0    7   → P1.7
IO_20  →  8  → 000|01|000    1    0   → P2.0   ← port increments!
IO_21  →  9  → 000|01|001    1    1   → P2.1
IO_22  → 10  → 000|01|010    1    2   → P2.2
  :      :        :          :    :
IO_30  → 16  → 000|10|000    2    0   → P3.0
IO_31  → 17  → 000|10|001    2    1   → P3.1
```

The enum auto-increments from 0. Because there are exactly 8 pins per port,
the port bits naturally roll over at 8 — no extra encoding needed.

---

## Level 7: The Code — Extract Port and Pin

```c
// Defined in io.c

#define IO_PORT_OFFSET (3u)                   // port starts at bit 3
#define IO_PORT_MASK   (0x3u << IO_PORT_OFFSET)  // 0x18 = 00011000
#define IO_PIN_MASK    (0x7u)                 // 0x07 = 00000111

static uint8_t io_port(io_e io)               // extract port
{
    return (io & IO_PORT_MASK) >> IO_PORT_OFFSET;
}

static inline uint8_t io_pin_idx(io_e io)     // extract pin index
{
    return io & IO_PIN_MASK;
}

static uint8_t io_pin_bit(io_e io)            // convert to bit mask
{
    return 1 << io_pin_idx(io);
}
```

Trace through with `IO_21` (= 9 = `00001001`):

```
io_port(IO_21):
    00001001 & 00011000 = 00001000     (mask keeps bits 3-4)
    00001000 >> 3       = 00000001     → port = 1 (Port 2)

io_pin_idx(IO_21):
    00001001 & 00000111 = 00000001     → pin index = 1

io_pin_bit(IO_21):
    1 << 1              = 00000010     → bit mask = BIT1
```

Result: port 1, pin 1 → `P2.1` — which is the pin for `IO_RANGE_SENSOR_FRONT_INT` on the Launchpad.

---

## Exercises — Trace These Yourself

1. `IO_TEST_LED` = `IO_10` = 0. What are `io_port()`, `io_pin_idx()`, `io_pin_bit()`?
2. `IO_I2C_SCL` = `IO_16` = 6. Trace all three functions.
3. `IO_PWM_MOTORS_LEFT` (nsumo) = `IO_35` = 21. Trace all three functions.

---

## Why This Matters

Without bit-packing, every function would need a switch/case for every pin:

```c
// BAD: nested switch — grows with every new pin
switch (io) {
    case IO_TEST_LED:  P1SEL &= ~BIT0; break;
    case IO_UART_RXD:  P1SEL &= ~BIT1; break;
    case IO_I2C_SCL:   P1SEL &= ~BIT6; break;
    ...  // 16-24 cases, repeated in EVERY function
}

// GOOD: bit-packing — one line handles all pins
*port_sel1_regs[io_port(io)] &= ~io_pin_bit(io);
```

On a 16 KB flash MCU, this difference matters. The array-indexed version is smaller,
faster, and doesn't need updating when pins change.
