#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             msg.py
# Created:          March 1, 2015
# Last Updated:     April 20, 2015
# Description:      Contains methods to display formatted output to terminal
#					and check input for validity

screen_width = 78

## Formatting Input

def ruler(len=screen_width): 
	""" Prints a horizontal line the width of the screen """
	return "{:-^{l}}".format("", char="=", l=len)

def sys_mode(mode_name, len=screen_width):
	""" Prints name of system mode as a header """
	return "\n" + "{:#^{l}}".format(" " + mode_name.upper() + " ", l=len) + "\n"

def snapshot_header(q_name, char = "=", len=screen_width):
	""" Prints name of queue displayed as a header """
	return "\n" + "{:{c}^{l}}".format(" " + q_name.upper() + " QUEUE ", c=char, l=len) + "\n"

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

## System messages

def command_list():
	return """    A or a -- Activates a new process
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


