#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             msg.py
# Created:          March 1, 2015
# Last Updated:     May 10, 2015
# Description:      Contains methods to display formatted output to terminal
#					and check input for validity

screen_width = 78
import re

## Formatting Input

def ruler(len=screen_width): 
	""" Prints a horizontal line the width of the screen """
	return "{:-^{l}}".format("", char="=", l=len)

def sys_mode(mode_name, char='#', len=screen_width):
	""" Prints name of system mode as a header """
	return "\n" + "{:{c}^{l}}".format(" " + mode_name.upper() + " ", c=char, l=len) + "\n"

def snapshot_header(q_name, char = "=", len=screen_width):
	""" Prints name of queue displayed as a header """
	return "\n" + "{:{c}^{l}}".format(" " + q_name.upper() + " ", c=char, l=len)

## Error messages

def err(err_msg):
	return "ERROR: " + err_msg 

def invalid_command():
	return "ERROR: Invalid command"

def nothing_in_cpu():
	return "ERROR: No active process in CPU"

def nothing_in_ready():
	return "Ready queue is empty"

## Validating Input
def get_valid_int(prompt, err_msg="Please enter a valid positive integer"):
	is_int = False
	while not is_int:
		try:
			num = input(prompt + " >>> ")
			# Check to see if positive whole number
			if isinstance(num, (int, long)):
				if num <= 0: raise ValueError
				is_int = True
				return num
			else: raise ValueError
		except:
			print err(err_msg)

def get_valid_hex(prompt, err_msg="Please enter a valid hexadecimal number"):
    is_hex = False
    while not is_hex:
        try:
            num = raw_input(prompt + " >>> ")
            if re.match("[0-9a-fA-F]", str(num)):
                is_hex = True
                num = "0x" + num
                num = int(num, 16)
                return num
            else:
                raise ValueError
        except Exception as e:
            print err(err_msg)

def get_pow_two(prompt, err_msg="Please enter a valid power of two"):
	is_pow = False
	while not is_pow: 
		try:
			num = input(prompt + " >>> ")

			# Check to see if positive number
			if num <= 0: raise ValueError

			# Check to see if num is pow of two
			if not (num != 0 and ((num & (num-1)) == 0)): raise ValueError

			# Got this far. Congrats, it's a positive power of two!
			is_pow = True
			return num

		except:
			print err(err_msg)



## System messages

def command_list():
	return """    A or a   -- Activates a new process
    T or t   -- Terminates active process in the CPU
    S or s   -- Enters snapshot mode.
                View processes in the queues of devices
                of a specified type
    H or h   -- Displays list of valid commands.
    Q or q   -- Terminates the program.
    K# or k# -- Kill Process with pid number '#'.
    
    You can also request a device by its device name: 
           -- lowercase moves a process from the CPU to the device queue
           -- uppercase signals the process active in the device is complete
    """


