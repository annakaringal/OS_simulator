import sys, cmd, devices, queues, sys_gen
from pcb import PCB

#TODO: how to DRY if not args??? 

class SysCommand(cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = "\n >> "

		# SYS GEN PHASE: Set up queues & devices in system
		self.valid_device_types = frozenset(["Disk Drive", "Printer", "CD/RW"])
		self.all_devices = sys_gen.generate(self.valid_device_types)

		self.ready = queues.ReadyQueue()
		self.cpu = devices.CPU()
		self.pid_count = 0

		print "Your system is now running with the following devices: "
		for dev in self.all_devices: 
			print dev


	# NEW PROCESS
	def do_a(self, args):
		""" Activates a new process """

		if not args: 
			self.pid_count += 1
			new_proc = PCB(self.pid_count)

			# Send process to CPU or ready queue
			if self.cpu.empty():
				self.cpu.set_process(new_proc)
			else:
				self.ready.enqueue(new_proc)

		else: 
			print "ERROR: Invalid Command"

	def help_a(self):
		print "A or a", 
		print "-- activates a new process"

	# TERMINATE PROCESS 
	def do_t(self, args):
		""" Terminates current process in CPU"""

		if not args: 
			# Check CPU for emptiness before terminating process
			if not self.cpu.empty():
				self.cpu.terminate_process()

			try: 
				# Remove process from head of ready queue, moves to CPU
				self.cpu.set_process(self.ready.dequeue())
			except:
				pass #TODO: THROW EXCEPT
		else: 
			print "ERROR: Invalid Command"

	def help_t(self):
		print "T or t", 
		print "-- terminates current process in CPU"

	# SNAPSHOT
	def do_s(self, args):

		if not args: 
			print "##### SNAPSHOT MODE"
			type_to_snapshot = raw_input("Which Device?: ").lower()

			if type_to_snapshot == "r": 
				self.ready.snapshot()

			# TODO: FIX THIS
			elif type_to_snapshot in [dtype[0]for dtype in self.valid_device_types]:
				for d in self.all_devices: 
					if d.type()[0] == type_to_snapshot: 
						d.snapshot()

			else: #TODO: ASK AGAIN IF NOT KNOWN DEV
				print ">>> ERROR: Unknown Device Type"

		else: 
			print "ERROR: Invalid Command"

	def help_s(self):
		print "S or s", 
		print "-- outputs the proccesses in a given queue"


	def default(self, args):

		# TODO: IS THERE A WAY TO NOT NEST THIS???

		device_found = False 

		for dev in self.all_devices:
			if dev.is_device_name(self.lastcmd.lower()): 
				device_found = True

				if self.lastcmd.islower(): # SYSTEM CALL (lowercase input)

					# Get active process from CPU
					if not self.cpu.empty(): #TODO: RAISE EXCEPT?
						proc = self.cpu.get_process()

						# Prompt user for and set PCB params 
						proc.set_syst_call_params()
						proc.set_read_write_params(dev.get_dev_type())

						# Add process to back of device queue
						dev.enqueue(proc)

						# Move process at head of ready queue to CPU
						self.cpu.set_process(self.ready.dequeue())
					else: 
						print "No process active in CPU"

				else:  # INTERRUPT  (uppercase input)
					# Process at head of device queue complete
					# Remove from device queue, move to back of ready queue
					try: 
						proc = dev.dequeue()
						self.ready.enqueue(proc)
					except:
						print "%s queue is empty" %dev
					else:
						print "%s completed %s" %(dev, proc)

		if not device_found: 
			print "ERROR: Invalid Command"

	# EXITING THE PROGRAM 
	def do_quit(self, args):
		if not args: 
			print "   Goodbye!"
			raise SystemExit
		else: 
			print "ERROR: Invalid Command"

	def help_quit(self):
		print "syntax: quit", 
		print "-- quits the program"

	def do_EOF(self, line):
		print "Goodbye!"
		return True

	# Shortcuts & aliases
	do_A = do_a
	do_T = do_t
	do_S = do_s
	do_q = do_quit
	do_Q = do_quit
