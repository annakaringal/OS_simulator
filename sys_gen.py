#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:			Anna Cristina Karingal
# Name:				sys_gen.py
# Created: 			February 27, 2015
# Last Updated: 	March 1, 2015
# Description:		Prompts user for input and generates instances of devices
#					in system based on user input

import sys
import devices

def generate(types_of_dev): 
	""" Generates all system device instances based on user input. 
	   Returns list of all system devices. """

	print "##### SYSTEM SETUP #####" + "\n"

	# Dictionary of type of devices and how many devices of each type
	system_device_types = {}

	for d in types_of_dev: 
		
		# Add device type & how many of each type 
		system_device_types[d] = None
        get_valid_int(system_device_types[d], "How many %ss? " %d)

	# List of all individual devices in system
	system_devices = []

	for dev_type, num_of_dev in system_device_types.iteritems(): 
		name_prefix = dev_type[0].lower()

		# Create new device, add to list of system_devices
		for i in range(num_of_dev):
			name = name_prefix + str(i+1)
			system_devices.append(devices.Device(name, dev_type))


	print "\n" + "##### SYSTEM GENERATION COMPLETE #####"

	return system_devices

def get_valid_int(var, prompt):
	new_int = None
	while new_int == None:
		try: 
			if var.isdigit():
				new_int = int(raw_input(prompt + ": "))
			else: 
				raise TypeError
		except:
			print "ERROR: Please enter a positiive integer."
		else: 
			var = new_int

