#!/usr/bin/env python
# 
# Author:			Anna Cristina Karingal
# Name:				sys_gen.py
# Created: 			February 27, 2015
# Last Updated: 	April 20, 2015
# Description:		Prompts user for input and generates instances of devices
#					in system based on user input

import sys
import devices
import msg

valid_device_types = frozenset(["Disk Drive", "Printer", "CD/RW"])

def generate(): 
	"""
	Generates all system device instances based on user input. 
	Returns list of all system devices.

	"""

	print msg.sys_mode("System Setup")

	# Dictionary of type of devices and how many devices of each type
	system_device_types = {}

	print "For each device type, please specify the number of devices."

	for d in valid_device_types: 	
		# Add device type & how many of each type 
		system_device_types[d] = None
		system_device_types[d] = msg.get_valid_int(d)

	print msg.ruler()

    # List of all individual devices in system
	system_devices = []

	for dev_type, num_of_dev in system_device_types.iteritems(): 
		name_prefix = dev_type[0].lower()

		# Create new device, add to list of system_devices
		for i in range(num_of_dev):
			name = name_prefix + str(i+1)

			if (dev_type == "Disk Drive"):
				cyl = msg.get_valid_int("Num of cylinders for " + name)
				system_devices.append(devices.DiskDrive(name,cyl))
			else:
				system_devices.append(devices.Device(name, dev_type))

	print msg.ruler()

	return system_devices
	