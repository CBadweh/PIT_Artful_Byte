# Intermediate LED blink (hardcoded Port 1) — IO driver, watchdog still in main.
# Usage: make | make flash | make clean

TOOLCHAIN_DIR = C:/ti/msp430-gcc
INC_DIR = $(TOOLCHAIN_DIR)/include

BUILD_DIR = build
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin

CC = msp430-elf-gcc
RM = rm

MCU = msp430g2553
WFLAGS = -Wall -Wextra -Wshadow
CFLAGS = -mmcu=$(MCU) $(WFLAGS) -fshort-enums -Og -g -I$(INC_DIR) -I./src
LDFLAGS = -mmcu=$(MCU) -L$(INC_DIR)

TARGET = $(BIN_DIR)/blink.elf
SOURCES = \
	src/main.c \
	src/drivers/io.c
OBJECTS = $(patsubst src/%.c,$(OBJ_DIR)/%.o,$(SOURCES))

.PHONY: all clean flash

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
