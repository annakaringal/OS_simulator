import sys
from queues import DeviceQueue
from collections import deque
from pcb import PCB

class CPU(): 

    def __init__(self):
        self.active = None

    def empty(self):
        return True if not self.active else False

    ## Methods to modify active process in CPU

    def set_process(self, proc):
        proc.set_proc_loc("CPU")
        self.active = proc
        print "%s is in the CPU" %self.active

    def get_process(self):
        return self.active

    def terminate_process(self):
        if self.active: 
            print "%s terminated" %self.active
            proc = self.active
            del proc
            self.active = None
        else: #TODO: THROW EXCEP
            print "ERROR: No process in CPU"

class Device(DeviceQueue):

    def __init__(self, dname, dtype): 
    	""" Initializes new device with device name & device type, and new
    	empty queue """ 

    	DeviceQueue.__init__(self)
    	self._dev_name = dname
    	self._dev_type = dtype

    ## Queue methods

    def enqueue(self, proc):
    	""" Add process to end of queue """
    	proc.set_proc_loc(self._dev_name)
    	DeviceQueue.enqueue(self,proc)
    	print proc.status()

    ## Methods to print device in human readable form to console

    def __repr__(self):
    	return self._dev_name + " (" + self._dev_type.lower() + ")"

	def __str__(self):
		return self._dev_type.lower() + " " + self._dev_name

    def snapshot(self):
        title = " " + self._dev_type.upper() + " " + self._dev_name.upper() + " QUEUE "
        print '{0:=^78}'.format(title)
        DeviceQueue.snapshot(self)

    ## Methods to check/return device name/type

    def is_device_name(self, query_name):
        return True if self._dev_name == query_name else False

    def is_device_type(self, query_type):
        return True if self._dev_type == query_type else False

    def get_dev_type(self):
        return self._dev_type

    def get_dev_name(self):
        return self._dev_name
