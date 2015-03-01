import sys, cmd, devices, queues, sys_gen
from pcb import PCB

#TODO: how to DRY if not args??? 

class SysCommand(cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = " >> "

		## SYS GEN PHASE: Set up queues & devices in system
		self.valid_device_types = frozenset(["Disk Drive", "Printer", "CD/RW"])
		self.all_devices = sys_gen.generate(self.valid_device_types)

		self.ready = queues.ReadyQueue()
		self.cpu = devices.CPU()
		self.pid_count = 0

		print "Your system is now running with the following devices: "
		for dev in self.all_devices: 
			print dev

		print ""
		## Now in the RUNNING PHASE


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
			print "ERROR: Invalid Command"

	def help_a(self):
		print "A or a", 
		print "-- activates a new process"

	## User Command: Terminate Process
	def do_t(self, args):
		""" Terminates current process in CPU"""

		if not args: 

			try:
				self.cpu.terminate_process()
			except IndexError: 
				print "ERROR: No process to terminate in CPU."

			try: 
				# Remove process from head of ready queue, moves to CPU
				self.cpu.set_process(self.ready.dequeue())
			except IndexError:
				print "No processes in ready queue. CPU empty."
		else: 
			print "ERROR: Invalid Command"

	def help_t(self):
		print "T or t", 
		print "-- terminates current process in CPU"

	## User Command: Queue Snapshot
	def do_s(self, args):

		if not args: 
			print "\n" + "##### SNAPSHOT MODE"
			type_to_snapshot = raw_input("Device Type: ").lower()

			if type_to_snapshot == "r": 
				self.ready.snapshot()

			elif type_to_snapshot in [dtype[0].lower() for dtype in self.valid_device_types]:
				for dev in self.all_devices: 
					if type_to_snapshot == dev.get_dev_type()[0].lower(): 
						dev.snapshot()

			else: #TODO: ASK AGAIN IF NOT KNOWN DEV
				print "ERROR: Unknown Device Type"

		else: 
			print "ERROR: Invalid Command"

	def help_s(self):
		print "S or s", 
		print "-- outputs the proccesses in a given queue"


	## User Command: Device request or unknown (Invalid) command
	def default(self, args):

		# TODO: IS THERE A WAY TO NOT NEST THIS???

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
							print "No active process in the CPU"
							# TO DO: CHECK: IS BREAK THE RIGHT THING?????? 
							break

						# Prompt user for and set PCB params 
						proc.set_syst_call_params()
						proc.set_read_write_params(dev.get_dev_type())

						# Add process to back of device queue
						dev.enqueue(proc)

						# Move process at head of ready queue to CPU
						try: 
							self.cpu.set_process(self.ready.dequeue())
						except IndexError:
							print "No processes in ready queue. CPU empty."
					else: 
						print "No process active in CPU"

				else:  # INTERRUPT  (uppercase input)
					# Process at head of device queue complete
					# Remove from device queue, move to back of ready queue
					try: 
						proc = dev.dequeue()
						self.ready.enqueue(proc)
					except IndexError:
						print "%s queue is empty" %dev
					else:
						print "%s completed %s" %(dev, proc)

		if not device_found: 
			print "ERROR: Invalid Command"

	## User Command: Exit
	def do_quit(self, args):
		if not args: 
			print "   Goodbye!"
			raise SystemExit
		else: 
			print "ERROR: Invalid Command"

	def help_quit(self):
		print "quit", 
		print "-- quits the program"

	def do_EOF(self, line):
		print "Goodbye!"
		return True

	## Command shortcuts & aliases
	do_A = do_a
	do_T = do_t
	do_S = do_s
	do_q = do_quit
	do_Q = do_quit
