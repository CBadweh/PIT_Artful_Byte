# Intermediate LED blink — IO abstraction, watchdog still in main.
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
DEFINES =
WFLAGS = -Wall -Wextra -Werror -Wshadow
CFLAGS = -mmcu=$(MCU) $(WFLAGS) -fshort-enums -Og -g \
	-I$(MSPGCC_INCLUDE_DIR) -I./src $(DEFINES)
LDFLAGS = -mmcu=$(MCU) -L$(MSPGCC_INCLUDE_DIR)

SOURCES = \
	src/main.c \
	src/drivers/io.c

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
