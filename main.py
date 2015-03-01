import sys_gen
import queues
import devices

from pcb import PCB


def main():

	##### SYS GEN PHASE

	# Generate system devices from user input
	valid_device_types = frozenset(["Disk Drive", "Printer", "CD/RW"])
	all_devices = sys_gen.generate(valid_device_types)

	# Set up CPU, Ready Queue & PID 
	ready = queues.ReadyQueue()
	cpu = devices.CPU()
	pid_count = 0

	##### RUNNING PHASE

	print "Your system is now running with the following devices: " 
	for dev in all_devices: 
		print dev
		
	while True: 
		try: 
			cmd = raw_input("COMMAND: ")

			## NEW PROCESS
			if cmd.lower() == "a":

				pid_count += 1
				new_proc = PCB(pid_count)

				# Send process to CPU or ready queue
				if cpu.empty():
					cpu.set_process(new_proc)
				else:
					ready.enqueue(new_proc)

			## TERMINATE CURRENT PROCESS IN CPU
			elif cmd.lower() == "t": 

				# Terminates current process in CPU
				# Removes process from head of ready queue, moves to CPU
				if not cpu.empty():
					cpu.terminate_process()

				try: 
					cpu.set_process(ready.dequeue())
				except:
					#TODO: THROW EXCEPT

			### SNAPSHOTS
			elif cmd.lower() == "s":

				print "##### SNAPSHOT MODE"
				type_to_snapshot = input("WHICH DEVICE? ").lower()

				if type_to_snapshot == "r": 
					ready.snapshot()

				# TODO: FIX THIS
				elif type_to_snapshot in [dtype[0]for dtype in valid_device_types]:
					for d in all_devices: 
						if d.type()[0] == type_to_snapshot: 
							d.snapshot()

				else: #TODO: ASK AGAIN IF NOT KNOWN DEV
					print ">>> ERROR: Unknown Device Type"

			# QUIT PROGRAM
			elif cmd.lower() in ["q", "quit", "exit"]:
				print " \n>>> Goodbye!"
				break

			# DEVICE INTERRUPT
			else: 

				# Check if input is a device name
				for dev in all_devices: 
					if dev.is_device_name(cmd.lower()): # Found the device!

						if cmd.islower(): # SYSTEM CALL (lowercase input)
							# Get active process from CPU
							proc = cpu.get_process()

							# Prompt user for and set PCB params 
							proc.set_syst_call_params()
							proc.set_read_write_params(dev.get_dev_type())

							# Add process to back of device queue
							dev.enqueue(proc)

							# Move process at head of ready queue to CPU
							cpu.set_process(ready.dequeue())


						else: # INTERRUPT  (uppercase input)
							# Process at head of device queue complete
							# Remove from device queue, move to back of ready queue
							ready.enqueue(dev.dequeue())

					# INVALID USER INPUT: i.e. input not a device on system
					else:
						invalid_command_error = True

				if invalid_command_error:
					print ">>> ERROR: Please enter a valid command."

		# USER EXITED PROGRAM
		except EOFError:
			print " \n>>> Goodbye!"
			break

if __name__ == '__main__':
	main()