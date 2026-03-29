# Check arguments
GOALS_WITHOUT_HW = clean cppcheck format
GOAL_HAS_TARGET = $(filter $(MAKECMDGOALS),$(GOALS_WITHOUT_HW))
ifeq ($(GOAL_HAS_TARGET),)

ifeq ($(HW),LAUNCHPAD) # HW argument
TARGET_HW=launchpad
else ifeq ($(HW),NSUMO)
TARGET_HW=nsumo
else
$(error "Must pass HW=LAUNCHPAD or HW=NSUMO")
endif

endif
TARGET_NAME=$(TARGET_HW)

# Directories
TOOLS_DIR = ${TOOLS_PATH}
MSPGCC_ROOT_DIR = $(TOOLS_DIR)/msp430-gcc
MSPGCC_BIN_DIR = $(MSPGCC_ROOT_DIR)/bin
MSPGCC_INCLUDE_DIR = $(MSPGCC_ROOT_DIR)/include
BUILD_DIR = build
OBJ_DIR = $(BUILD_DIR)/$(TARGET_HW)/obj
BIN_DIR = $(BUILD_DIR)/$(TARGET_HW)/bin
TI_CCS_DIR = $(TOOLS_DIR)/ccs1120/ccs
DEBUG_BIN_DIR = $(TI_CCS_DIR)/ccs_base/DebugServer/bin
DEBUG_DRIVERS_DIR = $(TI_CCS_DIR)/ccs_base/DebugServer/drivers

LIB_DIRS = $(MSPGCC_INCLUDE_DIR)
INCLUDE_DIRS = $(MSPGCC_INCLUDE_DIR) \
			   ./src \
			   ./external/ \
			   ./external/printf

# Toolchain
CC = $(MSPGCC_BIN_DIR)/msp430-elf-gcc
RM = rm
DEBUG = LD_LIBRARY_PATH=$(DEBUG_DRIVERS_DIR) $(DEBUG_BIN_DIR)/mspdebug
CPPCHECK = cppcheck
FORMAT = clang-format-12

# Files
TARGET = $(BIN_DIR)/$(TARGET_NAME)

SOURCES_WITH_HEADERS = \
		src/drivers/io.c \
		src/drivers/led.c \
		src/drivers/mcu_init.c \
		src/common/assert_handler.c \

SOURCES = \
		src/main.c \
		$(SOURCES_WITH_HEADERS)

HEADERS = \
		$(SOURCES_WITH_HEADERS:.c=.h) \
		src/common/defines.h \
		src/common/assert_handler.h \

OBJECT_NAMES = $(SOURCES:.c=.o)
OBJECTS = $(patsubst %,$(OBJ_DIR)/%,$(OBJECT_NAMES))

# Filter out external files from format and cppcheck
IGNORE_FILES_FORMAT_CPPCHECK = \
	external/printf/printf.h \
	external/printf/printf.c
SOURCES_FORMAT_CPPCHECK = $(filter-out $(IGNORE_FILES_FORMAT_CPPCHECK),$(SOURCES))
HEADERS_FORMAT = $(filter-out $(IGNORE_FILES_FORMAT_CPPCHECK),$(HEADERS))

# Static Analysis
## Don't check the msp430 helper headers (they have a LOT of ifdefs)
CPPCHECK_INCLUDES = ./src ./
CPPCHECK_FLAGS = \
	--quiet --enable=all --error-exitcode=1 \
	--inline-suppr \
	--suppress=missingIncludeSystem \
	--suppress=unmatchedSuppression \
	--suppress=unusedFunction \
	$(addprefix -I,$(CPPCHECK_INCLUDES)) \
	$(addprefix -i,$(CPPCHECK_IGNORE))

# Flags
MCU = msp430g2553
DEFINES = -D$(HW)
WFLAGS = -Wall -Wextra -Werror -Wshadow
CFLAGS = -mmcu=$(MCU) $(WFLAGS) -fshort-enums $(addprefix -I,$(INCLUDE_DIRS)) $(DEFINES) -Og -g
LDFLAGS = -mmcu=$(MCU) $(addprefix -L,$(LIB_DIRS))

# Build
## Linking
$(TARGET): $(OBJECTS) $(HEADERS)
	echo $(OBJECTS)
	@mkdir -p $(dir $@)
	$(CC) $(LDFLAGS) $^ -o $@

## Compiling
$(OBJ_DIR)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c -o $@ $^

# Phonies
.PHONY: all clean flash cppcheck format

all: $(TARGET)

clean:
	@$(RM) -rf $(BUILD_DIR)

flash: $(TARGET)
	@$(DEBUG) tilib "prog $(TARGET)"

cppcheck:
	@$(CPPCHECK) $(CPPCHECK_FLAGS) $(SOURCES_FORMAT_CPPCHECK)

format:
	@$(FORMAT) -i $(SOURCES_FORMAT_CPPCHECK) $(HEADERS_FORMAT)
