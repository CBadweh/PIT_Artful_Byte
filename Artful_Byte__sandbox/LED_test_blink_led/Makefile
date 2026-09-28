# Lesson 12 Test 1 — test_blink_led with io_configure on a single pin (LaunchPad only).
# Usage: make | make flash | make clean

TOOLCHAIN_DIR = C:/ti/msp430-gcc
INC_DIR = $(TOOLCHAIN_DIR)/include

BUILD_DIR = build
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin

CC = msp430-elf-gcc
RM = rm

MCU = msp430g2553
WFLAGS = -Wall -Wextra -Werror -Wshadow
CFLAGS = -mmcu=$(MCU) $(WFLAGS) -fshort-enums -Og -g \
	-I$(INC_DIR) -I./src
LDFLAGS = -mmcu=$(MCU) -L$(INC_DIR)

SOURCES = \
	src/main.c \
	src/drivers/io.c \
	src/drivers/mcu_init.c

OBJECTS = $(patsubst src/%.c,$(OBJ_DIR)/%.o,$(SOURCES))
TARGET = $(BIN_DIR)/blink.elf

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJECTS)
	@mkdir -p $(dir $@)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

$(OBJ_DIR)/%.o: src/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	@$(RM) -rf $(BUILD_DIR)

# Flash to board (uses DSLite)
DSLITE = C:/ti/ccs2041/ccs/ccs_base/DebugServer/bin/DSLite.exe
CCXML = msp430g2553.ccxml

flash: $(TARGET)
	$(DSLITE) load -c $(CCXML) -f $(TARGET)
