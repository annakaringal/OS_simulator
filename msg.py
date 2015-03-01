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
	return "{:-^{l}}".format("", l=len)

def sys_mode(mode_name, len=screen_width):
	return "\n" + "{:#^{l}}".format(" " + mode_name.upper() + " ", l=len) + "\n"

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
	""" Sets value of dictionary key to a positive integer given by user. 

	Checks user input to ensure it is a positive integer value. Keeps
	prompting user until a valid value is entered.
	"""
	while dict[key] == None: 
		try: 
			num = int(input(prompt + ": "))
			# Check to see if positive whole number
			if num <= 0: raise ValueError
			dict[key] = num
		except:
			print msg.err("Please enter a valid positive integer")


