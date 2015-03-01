import sys
from devices import Device

def generate(types_of_dev): 
	""" Generates all system device instances based on user input. 
	   Returns list of all system devices. """

	print "##### SYSTEM SETUP #####" + "\n"

	# Dictionary of type of devices and how many devices of each type
	system_device_types = {}

	for d in types_of_dev: 
		
		# Adds device type & how many of each type 
		# TODO: KEEP TRYING UNTIL ACCEPTABLE INPUT
		try:
			num_of_d = int(input("How many %ss? " %d))
		except:
			print "\n" + "ERROR: Invalid entry. Please enter an integer."
		else: 
			system_device_types[d] = num_of_d
			#break

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
