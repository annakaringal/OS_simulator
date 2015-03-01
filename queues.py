import sys 
from collections import deque
from pcb import PCB

class DeviceQueue: 

    def __init__(self): 
    	""" Initialize class with empty queue """
    	self._q = deque()

    def enqueue(self, proc):
    	### TODO: CHECK IF PROCESS IS A PCB
    	""" Add process to end of queue """
    	self._q.append(proc)

    def dequeue(self):
    	""" Removes & returns process at head of queue """
    	try: 
    		head = self._q.popleft()
    	except IndexError: 
    		raise
    	else: 
    		return head

    def length(self):
        return len(self._q)

    def snapshot(self):
        if self._q: 
            print '{:<4}{:^5}{:<25}{:<20}{:^5}{:^15}'.format("Pos", "PID", *map(lambda pf: pf.replace("_", " ").title(), self._q[0].param_fields))
            for i in range(self.length()):
                print '{:<4}{:^5}{:<25}{:<20}{:^5}{:^15}'.format(i+1, self._q[i].pid, *self._q[i].params.values())
        else:
            print '{:^78}'.format("EMPTY: No processes in queue")

class ReadyQueue(DeviceQueue):

    def __init__(self): 
    	""" Initialize class with empty queue """
    	DeviceQueue.__init__(self)

    def enqueue(self,proc):
    	proc.set_proc_loc("Ready")
    	DeviceQueue.enqueue(self,proc)
    	print proc.status()

    def snapshot(self):
        print '{0:=^78}'.format(" READY QUEUE ")
        DeviceQueue.snapshot(self)

