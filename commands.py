#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:			Anna Cristina Karingal
# Name:				commands.py
# Created: 			February 27, 2015
# Last Updated: 	April 19, 2015
# Description:		Generates instances of system deveices and queues.
#	 				Prompts user for commands in command lineand performs 
#					actions on system devices, queues and processes 
#					based on input.

import sys
import cmd

import sys_gen
import msg 
import devices
import queues
from pcb import PCB

class SysCommand(cmd.Cmd):

	def __init__(self, completekey = None):
		cmd.Cmd.__init__(self, completekey = None)
		self.prompt = " >>> "

		## SYS GEN PHASE: Set up queues & devices in system
		self.all_devices = sys_gen.generate()

		self.cpu = devices.CPU() # TO DO: CHECK INPUTS
		self.alpha = input("History Parameter >> ");
		self.tau = input ("Initial Burst Estimate >> ")
		self.pid_count = 0

		print "Your system is now running with the following devices: "
		print msg.ruler(38)
		print "{:<10}{:<28}".format("DEV NAME", "DEV TYPE")
		print msg.ruler(38)
		for dev in self.all_devices: 
			print "{:<10}{:<28}".format(dev.get_dev_name(), dev.get_dev_type())

		## Now in the RUNNING PHASE
		print msg.sys_mode("System running")
		print "Input a command to start a process in the system."
		print "-- Type H or h to view a list of valid commands" + "\n"


	## User Command: New process
	def do_a(self, args):
		""" Activates a new process """

		self.pid_count += 1
		new_proc = PCB(self.pid_count, self.alpha, self.tau)

		# Send process to CPU or ready queue based on what's in CPU
		self.cpu.enqueue(new_proc)

	## User Command: Terminate Process
	def do_t(self, args):
		"""
		Terminates current process in CPU
		Replaces with head of ready queue, if ready queue is not empty

		"""

		try:
			self.cpu.terminate()
		except IndexError: 
			print msg.nothing_in_cpu()

	## User Command: Queue Snapshot
	def do_s(self, args):

		# Request device type from user
		print msg.sys_mode("Snapshot Mode")
		print "Enter the first letter of a device type to view the queues of all devices of"
		print "that type." + "\n"
		type_to_snapshot = raw_input("Device Type >>> ").lower()

		# Show active process in CPU & processes in ready queue 
		if type_to_snapshot == "r": 
			self.cpu.snapshot()
			if not self.cpu.empty(): 
				print "\n" + "Active process in CPU: {a!s}".format(a=str(self.cpu.get_active_process()).capitalize())
			else: 
				print "\n" + "No active process in the CPU"

		# Show processes in device 
		elif type_to_snapshot in [d.get_dev_type()[0].lower() for d in self.all_devices]:

			for dev in self.all_devices: 
				if type_to_snapshot == dev.get_dev_type()[0].lower(): 
					dev.snapshot()

		else: 
			print msg.err("Unknown device type")

		print msg.sys_mode("Exiting Snapshot Mode")


	## User Command: Device request or unknown (Invalid) command
	def default(self, args):

		device_found = False 

		for dev in self.all_devices:
			if dev.is_device_name(self.lastcmd.lower()): 
				device_found = True

				if self.lastcmd.islower(): # SYSTEM CALL (lowercase input)

				# Get active process from CPU, replace with head of ready queue
					try: 
						proc = self.cpu.dequeue()
					except IndexError: 
						print msg.nothing_in_cpu()
						break

					# Prompt user for and set PCB params 

					print msg.sys_mode("Set system call parameters")
					proc.set_syst_call_params()
					proc.set_read_write_params(dev.get_dev_type())

					if (dev.get_dev_type().lower() == "disk drive"):
						try:
							proc.set_cylinder_params(dev.get_num_cylinders())
						except IndexError: 
							print "Invalid cylinder number"

					print msg.sys_mode("System call parameters set")

					# Add process to back of device queue
					dev.enqueue(proc)

				else:  # INTERRUPT  (uppercase input)
					# Process at head of device queue complete
					# Remove from device queue, move to back of ready queue
					try: 
						proc = dev.dequeue()
						print "%s completed %s" %(dev, proc)
						proc.clear_params()
						self.CPU.enqueue(proc)
					except IndexError:
						print msg.err("{!s} queue is empty".format(dev))		

		if not device_found: 
			print msg.invalid_command()

	## User Command: Display Help
	def do_h(self, args): 
		""" Displays the list of valid command line inputs to user """
		print msg.sys_mode("Help - Commands")
		print msg.command_list()

	## User Command: Unknown input (special cases)
	def emptyline(self):
		""" If empty line is entered, returns invalid input error """
		print msg.invalid_command()

	def precmd(self, line):
		""" If > 1 argument entered, returns invalid input error """
		all_args = line.split(" ")
		if len(all_args) > 1: 
			return "INVALID"
		else: 
			command_only = str(all_args[0])
			return command_only


	## User Command: Exit
	def do_q(self, args):
		""" Exits program """
		print "Goodbye!"
		raise SystemExit

	def do_EOF(self, args):
		""" Exits program if end of file char is inputted by user """
		print "Goodbye!"
		return True
		

	## Command shortcuts & aliases
	do_A = do_a
	do_T = do_t
	do_S = do_s
	do_Q = do_q
	do_H = do_h

