#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             msg.py
# Created:          March 1, 2015
# Last Updated:     March 1, 2015
# Description:      Contains methods to display formatted output to terminal

screen_width = 78

## Formatting Input

def ruler(len=screen_width): 
	""" Prints a horizontal line the width of the screen """
	return "{:-^{l}}".format("", l=len)

def sys_mode(mode_name, len=screen_width):
	""" Prints name of system mode as a header """
	return "\n" + "{:#^{l}}".format(" " + mode_name.upper() + " ", l=len) + "\n"

def snapshot_header(q_name, len=screen_width):
	""" Prints name of queue displayed as a header """
	return "\n" + "{:=^{l}}".format(" " + q_name.upper() + " QUEUE ", l=len) + "\n"

## Error messages

def err(err_msg):
	return "ERROR: " + err_msg 

def invalid_command():
	return "ERROR: Invalid command"

def nothing_in_cpu():
	return "ERROR: No active process in CPU"

def nothing_in_ready():
	return "ERROR: Ready queue is empty"

## Validating Input

def set_valid_int(dict, key, prompt):
	"""
	Sets value of dictionary key to a positive integer given by user. 

	Checks user input to ensure it is a positive integer value. Keeps
	prompting user until a valid value is entered.

	"""
	while dict[key] == None: 
		try: 
			num = int(input(prompt + " >>> "))
			# Check to see if positive whole number
			if num <= 0: raise ValueError
			dict[key] = num
		except:
			print err("Please enter a valid positive integer")

## System messages

def command_list():
	return """
    A or a -- Activates a new process
    T or t -- Terminates active process in the CPU
    S or s -- Enters snapshot mode.
              View processes in the queues of devices
              of a specified type
    H or h -- Displays list of valid commands.
    Q or q -- Terminates the program.
    
    You can also request a device by its device name: 
           -- lowercase moves a process from the CPU to the device queue
           -- uppercase signals the process active in the device is complete
    """


