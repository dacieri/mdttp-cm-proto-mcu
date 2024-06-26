# File: Makefile
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 03 Jun 2022
# Rev.: 20 Sep 2022
#
# Makefile for the firmware running on the ATLAS MDT Trigger Processor (TP)
# Command Module (CM) prototype MCU.
#



# ********** Check on which OS we are compiling. **********
OS       = $(shell uname -s)



# Directory with the common firmware files.
COMMON_DIR=../../Common
COMMON_LINK=Common



# ********** Program parameters. **********
PROJECT       = cm_mcu_hwtest
SOURCE_FILES  = cm_mcu_hwtest.c                     \
                cm_mcu_hwtest_aux.c                 \
                cm_mcu_hwtest_gpio.c                \
                cm_mcu_hwtest_i2c.c                 \
                cm_mcu_hwtest_io.c                  \
                cm_mcu_hwtest_qssi.c                \
                cm_mcu_hwtest_uart.c                \
                power_control.c                     \
                sm_cm.c                             \
                startup_gcc.c                       \
                $(COMMON_LINK)/uart_ui.c            \
                $(COMMON_LINK)/hw/gpio/gpio.c       \
                $(COMMON_LINK)/hw/gpio/gpio_pins.c  \
                $(COMMON_LINK)/hw/i2c/i2c.c         \
                $(COMMON_LINK)/hw/qssi/qssi.c       \
                $(COMMON_LINK)/hw/uart/uart.c       \
                $(COMMON_LINK)/utils/uartstdio.c    \

HEADER_FILES  = cm_mcu_hwtest.h                     \
                cm_mcu_hwtest_aux.h                 \
                cm_mcu_hwtest_gpio.h                \
                cm_mcu_hwtest_i2c.h                 \
                cm_mcu_hwtest_io.h                  \
                cm_mcu_hwtest_qssi.h                \
                cm_mcu_hwtest_uart.h                \
                power_control.h                     \
                sm_cm.h                             \
                $(COMMON_LINK)/uart_ui.h            \
                $(COMMON_LINK)/hw/gpio/gpio.h       \
                $(COMMON_LINK)/hw/gpio/gpio_pins.h  \
                $(COMMON_LINK)/hw/i2c/i2c.h         \
                $(COMMON_LINK)/hw/qssi/qssi.h       \
                $(COMMON_LINK)/hw/uart/uart.h       \
                $(COMMON_LINK)/utils/uartstdio.h    \

LINKER_FILE   = cm_mcu_hwtest.ld

EXTRA_SOURCES = ustdlib.c                           \



# ********** Additional settings. **********
BACKUP_DIR         = backup
BACKUP_FILES_SRC   = $(SOURCE_FILES) $(HEADER_FILES) Makefile
RM_FILES_CLEAN     = core *.o $(COMPILER)/*.axf $(COMPILER)/*.bin $(COMPILER)/*.d $(COMPILER)/*.o
RM_FILES_REALCLEAN = $(RM_FILES_CLEAN) $(COMPILER) *.bak *~ \
                     $(addsuffix ~, $(SOURCE_FILES)) \
                     $(addsuffix ~, $(HEADER_FILES)) \
                     $(COMMON_LINK)



# ********** TivaWare configuration. **********
# Defines the part type that this project uses.
PART=TM4C1290NCPDT

# The base directory for TivaWare.
TIVAWARE=../../TivaWare/SW-TM4C-2.2.0.295

# Include the common make definitions.
include $(TIVAWARE)/makedefs

# Where to find source files that do not live in this directory.
#VPATH  = $(TIVAWARE)/utils
VPATH  = $(COMMON_LINK)/utils
VPATH += $(TIVAWARE)/utils

# Where to find header files that do not live in the source directory.
IPATH  = $(TIVAWARE)
IPATH += $(COMMON_LINK)
IPATH += $(COMMON_LINK)/hw
IPATH += $(COMMON_LINK)/hw/gpio
IPATH += $(COMMON_LINK)/hw/i2c
IPATH += $(COMMON_LINK)/hw/qssi
IPATH += $(COMMON_LINK)/hw/uart
IPATH += $(COMMON_LINK)/utils

# Rules for building the project.
SCATTERgcc_$(PROJECT)=$(PROJECT).ld
ENTRY_$(PROJECT)=ResetISR
CFLAGSgcc=-DTARGET_IS_TM4C129_RA2

# Minicom configuration.
MINICOM_CONFIG = cm_mcu



# ********** Compiler configuration. **********
CPP      = $(CC) -E
CFLAGS   += -O2 -Wall
CXXFLAGS += -O2 -Wall
LDFLAGS  +=
INCLUDES += -I.
LDLIBS   += -L.



# ********** Auxiliary programs, **********
BZIP2           = bzip2
CD              = cd
CP              = cp -a
CVS             = cvs
DATE            = date
DATE_BACKUP     = $(DATE) +"%Y-%m-%d_%H-%M-%S"
DIRNAME         = dirname
ECHO            = echo
ECHO_ERR        = $(ECHO) "**ERROR:"
EDIT			= gvim
EXIT            = exit
EXPORT          = export
FALSE           = false
GIT             = git
GREP            = grep
GZIP            = gzip
LM4FLASH        = lm4flash
LN              = ln -s
MAKE            = make
MKDIR           = mkdir
MSGVIEW         = msgview
MV              = mv
RM              = rm
SFLASH          = ../../../Software/$(subst ../,,$(TIVAWARE))/tools/sflash/sflash
SH              = sh -c 
SLEEP           = sleep
TAIL            = tail -n 5
TAR             = tar
TCL             = tclsh
TEE             = tee
TOUCH           = touch
WISH            = wish



# ********** Generate object files variable. **********
OBJS := $(SOURCE_FILES:.c=.o)
OBJS += $(EXTRA_SOURCES:.c=.o)
OBJS := $(addprefix $(COMPILER)/, $(OBJS))



# ********** Generate libraries variable. **********
LIBS  = ${TIVAWARE}/driverlib/${COMPILER}/libdriver.a
LIBS += ${TIVAWARE}/grlib/${COMPILER}/libgr.a



# ********** Rules. **********
.PHONY: all exec edit flash install sflash clean real_clean mrproper minicom mk_backup mk_backup_src $(COMPILER)

all: ${COMPILER}
all: $(COMMON_LINK) $(COMPILER) ${COMPILER}/$(PROJECT).axf

$(COMMON_LINK):
	@$(LN) -s $(COMMON_DIR) $(COMMON_LINK)

${COMPILER}:
	@$(MKDIR) -p ${COMPILER}
	@$(MKDIR) -p $(addprefix $(COMPILER)/, $(subst ../,,$(filter-out $(TIVAWARE), $(IPATH))))

edit: $(COMMON_LINK) $(SOURCE_FILES) $(HEADER_FILES) $(LINKER_FILE)
	@$(EDIT) $(SOURCE_FILES) $(HEADER_FILES) $(LINKER_FILE)

exec: install

flash: install

install: all ${COMPILER} ${COMPILER}/$(PROJECT).axf ${COMPILER}/$(PROJECT).bin
# Offest 0x4000 for boot loader.
#	@$(LM4FLASH) -E -v -S 0x4000 $(COMPILER)/$(PROJECT).bin
	@$(LM4FLASH) -E -S 0x4000 $(COMPILER)/$(PROJECT).bin

sflash: all $(COMPILER) $(COMPILER)/$(PROJECT).axf $(COMPILER)/$(PROJECT).bin $(SFLASH)
# Offest 0x4000 for boot loader.
	@$(SFLASH) -c /dev/ttyUSB0 -p 0x4000 -b 115200 -d -s 252 $(COMPILER)/$(PROJECT).bin

$(SFLASH):
	@$(CD) $(shell $(DIRNAME) $(SFLASH)) && $(MAKE)

${COMPILER}/$(PROJECT).axf: $(OBJS) $(LIBS)

$(OBJS): $(SOURCE_FILES) $(HEADER_FILES) $(LINKER_FILE)

$(LIBS): $(TIVAWARE)
	@$(CD) $(TIVAWARE) && $(MAKE)

debug: clean
debug: CFLAGS+=-g -D DEBUG
debug: ${COMPILER}
debug: ${COMPILER}/$(PROJECT).axf
debug: flash
debug:
	debug/debug_nemiver.sh $(PROJECT)

minicom: $(HOME)/.minirc.$(MINICOM_CONFIG)
	minicom -c on $(MINICOM_CONFIG)

$(HOME)/.minirc.$(MINICOM_CONFIG):
	@$(ECHO_ERR) "Minicom configuration \`$(HOME)/.minirc.$(MINICOM_CONFIG)' missing!"
	@$(FALSE)



# ********** Check if all necessary files and dirctories are there. **********
$(SOURCE_FILES) $(HEADER_FILES) $(LINKER_FILE):
	@$(ECHO_ERR) "Some source files are missing!"
	@$(ECHO) "Check:"
	@$(SH) 'for source_file in $(SOURCE_FILES) $(HEADER_FILES) $(LINKER_FILE); do \
		if [ ! -e $$source_file ]; then \
			$(ECHO) $$source_file; \
		fi; \
	done'
	@$(FALSE)

$(BACKUP_DIR):
	@$(ECHO_ERR) "Backup directory is missing!"
	@$(ECHO) "Check:"
	@$(ECHO) "$(BACKUP_DIR)"



# ********** Create backup of current state. **********
mk_backup: mk_backup_src

mk_backup_src: $(BACKUP_DIR) $(SOURCE_FILES) $(HEADER_FILES)
	@$(SH) ' \
	backup_file=$(PROJECT)_src_`$(DATE_BACKUP)`.tgz; \
	$(EXPORT) backup_file; \
	$(TAR) cfz "$(BACKUP_DIR)/$$backup_file" $(BACKUP_FILES_SRC); \
	TAR_RETURN=$$?; \
	if [ ! $$TAR_RETURN = 0 ]; then \
		$(ECHO_ERR) "Error occured backing up files."; \
	fi; \
	if [ -f $(BACKUP_DIR)/$$backup_file ]; then \
		$(ECHO) "Created source file(s) backup \"$(BACKUP_DIR)/$$backup_file\"."; \
	else \
		$(ECHO_ERR) "Cannot create \"$(BACKUP_DIR)/$$backup_file\"."; \
	fi'



# ********** Tidy up. **********
clean:
	@$(SH) 'RM_FILES="$(RM_FILES_CLEAN)"; \
		$(EXPORT) RM_FILES; \
		$(ECHO) "Removing files: \"$$RM_FILES\""; \
		$(RM) -r $$RM_FILES 2> /dev/null; \
		$(ECHO) -n'

real_clean:
	@$(SH) 'RM_FILES="$(RM_FILES_REALCLEAN)"; \
		$(EXPORT) RM_FILES; \
		$(ECHO) "Removing files: \"$$RM_FILES\""; \
		$(RM) -rf $$RM_FILES 2> /dev/null; \
		$(ECHO) -n'

mrproper: real_clean

