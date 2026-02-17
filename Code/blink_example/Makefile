# Toolchain directories
TOOLCHAIN_DIR = C:/ti/msp430-gcc
INC_DIR = $(TOOLCHAIN_DIR)/include

# Commands
CC = msp430-elf-gcc
RM = rm -rf

# Microcontroller
MCU = msp430g2553

# Target
TARGET = bin/blink.elf

# Source files
SOURCES = main.c led.c

# Object files
OBJECTS = $(SOURCES:.c=.o)
OBJECTS := $(addprefix obj/,$(OBJECTS))

# Warning flags
WARN_FLAGS = -Wall -Werror -Wextra -Wshadow

# Compiler flags
CFLAGS = -mmcu=$(MCU)
CFLAGS += $(WARN_FLAGS)
CFLAGS += -I$(INC_DIR)
CFLAGS += -Og -g

# Linker flags
LDFLAGS = -mmcu=$(MCU)
LDFLAGS += -L$(INC_DIR)

# Default target
all: $(TARGET)

# Linking
$(TARGET): $(OBJECTS)
	@mkdir -p $(dir $@)
	$(CC) $(LDFLAGS) $^ -o $@

# Compilation pattern rule
obj/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

# Phony targets
.PHONY: all clean flash

# Clean build files
clean:
	$(RM) obj bin a.out

# Flash to board (uses DSLite)
DSLITE = C:/ti/ccs2041/ccs/ccs_base/DebugServer/bin/DSLite.exe
CCXML = msp430g2553.ccxml

flash: $(TARGET)
	$(DSLITE) load -c $(CCXML) -f $(TARGET)
