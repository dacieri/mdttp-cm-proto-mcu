#!/usr/bin/env python3
#
# File: pyMcuCm.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 26 Jul 2022
# Rev.: 16 Sep 2022
#
# Python script to access the ATLAS MDT Trigger Processor (TP) Command Module
# (CM) Prototype via the TI Tiva TM4C1290 MCU.
#



# Append hardware classes folder to Python path.
import os
import sys
sys.path.append(os.path.relpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'hw')))



# System modules.
import time



# Hardware classes.
from hw import MdtTp_CM



# Message prefixes and separators.
prefixDebug             = "DEBUG: {0:s}: ".format(__file__)
prefixError             = "ERROR: {0:s}: ".format(__file__)



# ===================================================================
# Access the Command Module.
# ===================================================================

if __name__ == "__main__":
    # Command line arguments.
    import argparse
    parser = argparse.ArgumentParser(description='Run an automated set of MCU tests.')
    parser.add_argument('-c', '--command', action='store', type=str,
                        choices=['power_up', 'power_down', 'power_detail','power_check',
                                 'sn', 'sn_sm', 'status', 'mon_temp',
                                 'mcu_cmd_raw', 'mcu_led_user',
                                 'i2c_reset', 'i2c_detect', "i2c_mux_reset",
                                 'i2c_io_exp_init', 'i2c_io_exp_status', 'i2c_io_exp_get_input', 'i2c_io_exp_get_output', 'i2c_io_exp_set_output',
                                 'pm_status', 'pm_status_raw',
                                 'clk_setup', 'clk_reset', 'clk_status', 'ff_status','clk_status_regs'],
                        dest='command', default='status',
                        help='Command to execute on the CM.')
    parser.add_argument('-d', '--device', action='store', type=str,
                        dest='serialDevice', default='/dev/ttyUL1', metavar='SERIAL_DEVICE',
                        help='Serial device to access the MCU. Hint: An empty device string ("") enables simulated access.')
    parser.add_argument('-p', '--parameters', action='store', type=str, nargs='*',
                        dest='commandParameters', default=None, metavar='PARAMETER',
                        help='Parameter(s) for the selected command.')
    parser.add_argument('-v', '--verbosity', action='store', type=int,
                        dest='verbosity', default="1", choices=range(0, 5),
                        help='Set the verbosity level. The default is 1.')
    args = parser.parse_args()

    command = args.command
    commandParameters = args.commandParameters
    serialDevice = args.serialDevice
    verbosity = args.verbosity

    # Define the Command Module object.
    mdtTp_CM = MdtTp_CM.MdtTp_CM(serialDevice, verbosity)
    ret = 0
    # Execute requested command.
    if not command:
        print("Please specify a command using the `-c' option.")
        ret = -1
    elif command == "power_up":
        ret = mdtTp_CM.power_up()
    elif command == "power_down":
        ret = mdtTp_CM.power_down()
    elif command == "power_detail":
        ret = mdtTp_CM.power_status_detail()
    elif command == "power_check":
        ret = mdtTp_CM.power_check()
        if ret == 0:
            sys.exit(0)
        else:
            print ('FAIL! power no completely on')
            sys.exit(1)
    elif command == "sn":
        ret = mdtTp_CM.serial_number()
    elif command == "sn_sm":
        ret = mdtTp_CM.serial_number_sm()
    elif command == "status":
        print("Board Serial Number")
        print("===================")
        mdtTp_CM.serial_number()
        print()
        print("Power Status")
        print("============")
        mdtTp_CM.power_status()
        print()
        print("Temperatures")
        print("============")
        ret = mdtTp_CM.mon_temp()
    elif command == "mon_temp":
        ret = mdtTp_CM.mon_temp()
    elif command == "mcu_cmd_raw":
        if commandParameters:
            ret, response = mdtTp_CM.mcu_cmd_raw(" ".join(commandParameters))
            print(response)
        else:
            print(prefixError, "Please specify the raw MCU command.")
    elif command == "mcu_led_user":
        if commandParameters:
            value = int(commandParameters[0], 0)
            ret = mdtTp_CM.mcu_led_user_set(value)
            if ret:
                print(prefixError, "Error setting the MCU user LED value!")
        else:
            ret, value = mdtTp_CM.mcu_led_user_get()
            if ret:
                print(prefixError, "Error reading the MCU user LED value!")
            else:
                print("MCU user LED value: 0x{0:03x}".format(value))
    elif command == "i2c_reset":
        ret = mdtTp_CM.i2c_reset()
    elif command == "i2c_detect":
        ret = mdtTp_CM.i2c_detect_devices()
    elif command == "i2c_mux_reset":
        if commandParameters:
            I2CMuxResetMask = int(commandParameters[0], 0)
        else:
            I2CMuxResetMask = 0x0f
        ret = mdtTp_CM.i2c_mux_reset(I2CMuxResetMask)
    elif command == "i2c_io_exp_init":
        ret = mdtTp_CM.i2c_io_exp_init()
    elif command == "i2c_io_exp_status":
        if commandParameters:
            ret = mdtTp_CM.i2c_io_exp_get_status(commandParameters[0])
        else:
            ret = mdtTp_CM.i2c_io_exp_get_status_all()
    elif command == "i2c_io_exp_get_input":
        if commandParameters:
            ret = mdtTp_CM.i2c_io_exp_get_input(commandParameters[0])
        else:
            ret = mdtTp_CM.i2c_io_exp_get_input_all()
    elif command == "i2c_io_exp_get_output":
        if commandParameters:
            ret = mdtTp_CM.i2c_io_exp_get_output(commandParameters[0])
        else:
            ret = mdtTp_CM.i2c_io_exp_get_output_all()
    elif command == "i2c_io_exp_set_output":
        if not commandParameters:
            print(prefixError, "Either the signal name and the value or the values for all I2C I/O expander outputs must be speficied with the `i2c_io_exp_set_output' command!")
            ret = -1
        else:
            if len(commandParameters) == 2:
                ret = mdtTp_CM.i2c_io_exp_set_output(commandParameters[0], int(commandParameters[1], 0))
            elif len(commandParameters) == 8:
                ret = mdtTp_CM.i2c_io_exp_set_output_all([int(p, 0) for p in commandParameters])
            else:
                print(prefixError, "Please specify either the signal name and the value or the values for all 8 I2C I/O expander outputs!")
                ret = -1
    elif command == "pm_status":
        ret = mdtTp_CM.power_module_status()
    elif command == "pm_status_raw":
        ret = mdtTp_CM.power_module_status_raw()
    elif command == "clk_setup":
        if commandParameters:
            if len(commandParameters) != 2 :
                print(prefixError, "Please specify the clock IC number and the register map file (or freq for IC11).")
                print(prefixError, "E.g.: -p IC1 config/clock/Pro_Design/IC1_0x68_100IN0_100_100_100_100_100_100_100_100_NA_FB-Registers.txt")
                print(prefixError, "E.g.: -p IC11 240.474")
                ret = -1
            else:
                ret = mdtTp_CM.clk_prog_device_by_name(commandParameters[0], commandParameters[1])
        else:
            ret = mdtTp_CM.clk_prog_all()
    elif command == "clk_reset":
        ret = mdtTp_CM.i2c_io_exp_reset_clk()
    elif command == "clk_status":
        ret = mdtTp_CM.i2c_io_exp_status_clk()
    elif command == "clk_status_regs":
        ret = mdtTp_CM.clk_print_status_all()    
    elif command == "ff_status":
        ret = mdtTp_CM.read_ff_status()
    else:
        print(prefixError + "Command `{0:s}' not supported!".format(command))
        ret = -1

    if ret == 0:
        print("\nBye-bye!")
    else:
        sys.exit(ret)
    

