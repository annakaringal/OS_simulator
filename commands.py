#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:			Anna Cristina Karingal
# Name:				commands.py
# Created: 			February 27, 2015
# Last Updated: 	May 7, 2015
# Description:		Generates instances of system devices and queues.
#					Sets up system based on user input for CPU Scheduling
#					and memory management parameters.
#	 				Prompts user for commands in command lineand performs 
#					actions on system devices, queues and processes 
#					based on input.

from __future__ import division
import sys
import cmd

import sys_gen
import io 
import devices
import queues
from pcb import PCB
from memory import LongTermScheduler

class SysCommand(cmd.Cmd):

	def __init__(self, completekey = None):
		cmd.Cmd.__init__(self, completekey = None)
		self.prompt = " >>> "

		## SYS GEN PHASE: Set up queues & devices in system
		self.all_devices = sys_gen.generate()

  		# Set up history parameter alpha & initial bust estimate tau with valid values
 		print io.sys_mode("Initialize CPU Scheduling Parameters",'-')

		set_alpha = False
		while not set_alpha:
			try: 
				a = float(raw_input("History Parameter >>> "))
				if a < 0 or a > 1: raise ValueError
				self.alpha = a
				set_alpha = True
			except ValueError: 
				print io.err("Please enter a number between 0 and 1")
			except OverflowError:
				print io.err("Overflow error: Please enter a shorter number")

		self.tau = io.get_valid_int("Initial Burst Estimate")

		# Set up memory size & page size
		print io.sys_mode("Initialize Memory Parameters",'-')

		# Get page & mem size. Verify page size is a power of two and a factor of memory size.
		set_size = False
		while not set_size: 
			self.total_mem_size = io.get_valid_int("Total Memory Size")
			self.page_size = io.get_pow_two("Page Size")
			if self.total_mem_size % self.page_size == 0: 
				set_size = True
			else: 
				print io.err("Memory size must be divisible by page size")

		# Get & verify maximum process size
		set_proc_size = False
		while not set_proc_size: 
			self.max_proc_size = io.get_valid_int("Maximum Process Size")
			if self.max_proc_size <= self.total_mem_size: 
				set_proc_size = True
			else: 
				print io.err("Maximum process size cannot be larger than total memory. Please try again.")

		# Set up long term scheduler. This will also set up RAM & job pool
		self.lts = LongTermScheduler(self.total_mem_size, self.page_size)

		# Set up CPU & PID
		self.cpu = devices.CPU()
		self.pid_count = 0

		# Set up system stats
		self.completed = 0
		self.total_cpu_time = 0
		self.avg_cpu_time = 0

		# Print out list of devices to console
		print io.sys_mode("System Generation Complete")
		print "Your system is now running with the following devices: "
		print io.ruler(38)
		print "{:<10}{:<28}".format("DEV NAME", "DEV TYPE")
		print io.ruler(38)
		for dev in self.all_devices: 
			print "{:<10}{:<28}".format(dev.get_dev_name(), dev.get_dev_type())

		## Now in the RUNNING PHASE
		print io.sys_mode("System running")
		print "Input a command to start a process in the system."
		print "-- Type H or h to view a list of valid commands" + "\n"


	## User Command: New process
	def do_a(self, args):
		"""
		User input: A
		Get and validate process size. If process is larger than total memory or max process size, 
		reject process. Else, create a new process. If enough memory, add to ready queue, else 
		go to job pool. 
		"""

		psize = io.get_valid_int("Process size")
		if psize > self.total_mem_size: 
			print io.err("Proccess cannot be larger than total memory")
		elif psize > self.max_proc_size: 
			print self.io.err("Proccess cannot be larger than maximum process size of " + str(max_proc_size))
		else: 
			# Create new process
			self.pid_count += 1
			new_proc = PCB(self.pid_count, psize, self.alpha, self.tau)

			# If enough memory, new process can run, else goes to job pool
			if self.lts.schedule(new_proc): 
				self.cpu.enqueue(new_proc)

	## User Command: Terminate Process
	def do_t(self, args):
		"""
		User input: T
		Terminates current process in CPU.
		Replaces with head of ready queue, if ready queue is not empty.
		Update and print system statistics (Number of completed processes and
		average CPU time per process)
		"""
		try:
			proc = self.cpu.get_active_process()

			# Deallocate memory with long term scheduler
			# This will also allocate any freed memory to anything in job pool
			# and return a list of processes that it has allocated memory too
			new_procs = self.lts.kill(proc)

			# Terminate current process
			self.cpu.terminate()

			# Enqueue all new processes to ready queue
			for p in new_procs: 
				self.cpu.enqueue(p)

			# Update system stats with total CPU time for terminated process
			self.total_cpu_time += proc.tot_burst_time()
			self.completed += 1
			if self.completed == 0: 
				self.avg_cpu_time = 0
			else:
				self.avg_cpu_time = self.total_cpu_time / self.completed

			# Print system stats
			self.print_system_stats()

		except IndexError: 
			print io.nothing_in_cpu()

	## User Command: Queue Snapshot
	def do_s(self, args):
		"""
		User input: S
		Snapshot mode: Displays processes in queue specified by user
		"""

		# Request device type from user
		print io.sys_mode("Snapshot Mode")
		print "Enter the first letter of a device type to view the queues of all devices of"
		print "that type." + "\n"
		type_to_snapshot = raw_input("Device Type >>> ").lower()

		# Show active process in CPU & processes in ready queue 
		if type_to_snapshot == "r": 
			self.cpu.snapshot()

		# Show what's in memory
		elif type_to_snapshot == "m": 
			pass

		# Show processes in device 
		elif type_to_snapshot in [d.get_dev_type()[0].lower() for d in self.all_devices]:

			for dev in self.all_devices: 
				if type_to_snapshot == dev.get_dev_type()[0].lower(): 
					dev.snapshot()

		else: 
			print io.err("Unknown device type")

		# Print system stats
		self.print_system_stats()

		print io.sys_mode("Exiting Snapshot Mode")


	## User Command: Device request or unknown (Invalid) command
	def default(self, args):
		"""
		Default response to user input: Requesting a device or invalid command
		"""

		device_found = False 

		for dev in self.all_devices:
			if dev.is_device_name(self.lastcmd.lower()): 
				device_found = True

				if self.lastcmd.islower(): # SYSTEM CALL (lowercase input)

				# Get active process from CPU, replace with head of ready queue
					try: 
						proc = self.cpu.dequeue()
					except IndexError: 
						print io.nothing_in_cpu()
						break

					# Prompt user for and set PCB params 

					print io.sys_mode("Set system call parameters")
					proc.set_syst_call_params()
					proc.set_read_write_params(dev.get_dev_type())

					if (dev.get_dev_type().lower() == "disk drive"):
						proc.set_cylinder_params(dev.get_num_cylinders())

					print io.sys_mode("System call parameters set")

					# Add process to back of device queue
					dev.enqueue(proc)

				else:  # INTERRUPT  (uppercase input)
					# Process at head of device queue complete
					# Remove from device queue, move to back of ready queue
					try: 
						proc = dev.dequeue()
						print "%s completed %s" %(dev, proc)
						self.cpu.enqueue(proc)
					except IndexError:
						print io.err("{!s} queue is empty".format(dev))		

		if not device_found: 
			print io.invalid_command()

	## User Command: Display Help
	def do_h(self, args): 
		""" Displays the list of valid command line inputs to user """
		print io.sys_mode("Help - Commands")
		print io.command_list()

	## User Command: Unknown input (special cases)
	def emptyline(self):
		""" If empty line is entered, returns invalid input error """
		print io.invalid_command()

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

	def print_system_stats(self):
		print "\n" + "{:-^78}".format(" Completed Processes Report ")
		print "Total Completed: {:<5} Avg Total CPU Time: {:<5}".format(self.completed, self.avg_cpu_time).center(78, ' ')

	## Command shortcuts & aliases
	do_A = do_a
	do_T = do_t
	do_S = do_s
	do_Q = do_q
	do_H = do_h

