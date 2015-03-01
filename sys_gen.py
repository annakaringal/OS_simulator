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
from devices import Device

def generate(types_of_dev): 
	""" Generates all system device instances based on user input. 
	   Returns list of all system devices. """

	print "##### SYSTEM SETUP #####" + "\n"

	# Dictionary of type of devices and how many devices of each type
	system_device_types = {}

	for d in types_of_dev: 
		
		# Add device type & how many of each type 
		system_device_types[d] = None

		while system_device_types[d] == None:
			try:
				system_device_types[d] = validate_int(input("How many %ss? " %d))
			except:
				print "ERROR: Invalid entry. Please enter a positive integer."

	# List of all individual devices in system
	system_devices = []

	for dev_type, num_of_dev in system_device_types.iteritems(): 
		name_prefix = dev_type[0].lower()

		# Create new device, add to list of system_devices
		for i in range(num_of_dev):
			name = name_prefix + str(i+1)
			system_devices.append(Device(name, dev_type))


	print "\n" + "##### SYSTEM GENERATION COMPLETE #####"

	return system_devices

def validate_int(s):
	""" 
	If a given string is a positive integer, returns value of string.
	Else throws exception.
	"""
	if s.isdigit(): # Check if string contains ONLY digits, i.e. no - or .
		new_int = int(s) # Will throw excep if fails
		return new_int
	else: 
		raise TypeError
