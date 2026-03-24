# Minimal build — MSP430G2553 LaunchPad LED blink (raw registers only).
# Usage: make TOOLS_PATH=/c/ti

TOOLS_PATH ?= /c/ti
MSPGCC_ROOT_DIR = $(TOOLS_PATH)/msp430-gcc
MSPGCC_BIN_DIR = $(MSPGCC_ROOT_DIR)/bin
MSPGCC_INCLUDE_DIR = $(MSPGCC_ROOT_DIR)/include

BUILD_DIR = build
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin

CC = $(MSPGCC_BIN_DIR)/msp430-elf-gcc
RM = rm

MCU = msp430g2553
CFLAGS = -mmcu=$(MCU) -Wall -Og -g -I$(MSPGCC_INCLUDE_DIR)
LDFLAGS = -mmcu=$(MCU) -L$(MSPGCC_INCLUDE_DIR)

TARGET = $(BIN_DIR)/blink.elf
SOURCES = src/main.c
OBJECTS = $(patsubst src/%.c,$(OBJ_DIR)/%.o,$(SOURCES))

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
