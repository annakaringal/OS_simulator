#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:			Anna Cristina Karingal
# Name:				commands.py
# Created: 			February 27, 2015
# Last Updated: 	March 1, 2015
# Description:		Generates instances of system deveices and queues.
#	 				Prompts user for commands in command lineand performs 
#						actions on system devices, queues and processes 
#						based on input.

import sys
import cmd

import devices
import queues
import sys_gen
import msg
from pcb import PCB

#TODO: how to DRY if not args??? 

class SysCommand(cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = " >>> "

		## SYS GEN PHASE: Set up queues & devices in system
		self.all_devices = sys_gen.generate()

		self.ready = queues.ReadyQueue()
		self.cpu = devices.CPU()
		self.pid_count = 0

		print "Your system is now running with the following devices: "
		print msg.ruler(38)
		print "{:<10}{:<28}".format("DEV NAME", "DEV TYPE")
		print msg.ruler(38)
		for dev in self.all_devices: 
			print dev

		## Now in the RUNNING PHASE
		print msg.sys_mode("System running")
		print "Input a command to start a process in the system."
		print "-- Type H or h to view a list of valid commands" + "\n"


	## User Command: New process
	def do_a(self, args):
		""" Activates a new process """

		if not args: 
			self.pid_count += 1
			new_proc = PCB(self.pid_count)

			# Send process to CPU or ready queue based on what's in CPU
			if self.cpu.empty():
				self.cpu.set_process(new_proc)
			else:
				self.ready.enqueue(new_proc)

		else: 
			print msg.invalid_command()

	## User Command: Terminate Process
	def do_t(self, args):
		""" Terminates current process in CPU"""

		if not args: 

			try:
				self.cpu.terminate_process()
			except IndexError: 
				print msg.nothing_in_cpu()

			try: 
				# Remove process from head of ready queue, moves to CPU
				self.cpu.set_process(self.ready.dequeue())
			except IndexError:
				print msg.nothing_in_ready()
		else: 
			print msg.invalid_command()

	## User Command: Queue Snapshot
	def do_s(self, args):

		if not args:
			print msg.sys_mode("Snapshot Mode")
			print "Enter the first letter of a device type to view the queues of all devices of"
			print "that type." + "\n"

			type_to_snapshot = raw_input("Device Type >>> ").lower()

			if type_to_snapshot == "r": 
				self.ready.snapshot()

			elif type_to_snapshot in [dtype[0].lower() for dtype in self.valid_device_types]:
				for dev in self.all_devices: 
					if type_to_snapshot == dev.get_dev_type()[0].lower(): 
						dev.snapshot()

			else: 
				print msg.err("Unknown device type")

			print msg.sys_mode("Exiting Snapshot Mode")

		else: 
			print msg.invalid_command()


	## User Command: Device request or unknown (Invalid) command
	def default(self, args):

		device_found = False 

		for dev in self.all_devices:
			if dev.is_device_name(self.lastcmd.lower()): 
				device_found = True

				if self.lastcmd.islower(): # SYSTEM CALL (lowercase input)

					# Get active process from CPU
					if not self.cpu.empty(): 
						try: 
							proc = self.cpu.get_process()
						except IndexError: 
							print msg.nothing_in_cpu()
							break

						# Prompt user for and set PCB params 

						print msg.sys_mode("Set system call parameters")
						proc.set_syst_call_params()
						proc.set_read_write_params(dev.get_dev_type())
						print msg.sys_mode("System call parameters set")

						# Add process to back of device queue
						dev.enqueue(proc)

						# Move process at head of ready queue to CPU
						try: 
							self.cpu.set_process(self.ready.dequeue())
						except IndexError:
							print msg.nothing_in_ready()
					else: 
						print msg.nothing_in_cpu()

				else:  # INTERRUPT  (uppercase input)
					# Process at head of device queue complete
					# Remove from device queue, move to back of ready queue
					try: 
						proc = dev.dequeue()
						print "%s completed %s" %(dev, proc)
						proc.clear_params()
						self.ready.enqueue(proc)
					except IndexError:
						print "%s queue is empty" %dev				

		if not device_found: 
			print msg.invalid_command()

	## User Command: Display Help
	def do_h(self, args): 
		""" Displays the list of valid command line inputs to user """
		if not args: 
			print msg.sys_mode("Help - Commands")
			print msg.command_list()
		else:
			print msg.invalid_command()

	## User Command: Exit
	def do_q(self, args):
		""" Exits program """
		if not args: 
			print "Goodbye!"
			raise SystemExit
		else: 
			print msg.invalid_command()

	def do_EOF(self, line):
		""" Exits program if end of file char is inputted by user """
		print "Goodbye!"
		return True

	## Command shortcuts & aliases
	do_A = do_a
	do_T = do_t
	do_S = do_s
	do_Q = do_q
	do_H = do_h

