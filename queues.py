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
    		return "ERROR: Queue is empty"
    	else: 
    		return head

    def length(self):
        return len(self._q)

    def snapshot(self):
        if self._q: 
            for i in range(self.length()):
                print i+1, self._q[i]
        else:
            print "queue empty"

class ReadyQueue(DeviceQueue):

    def __init__(self): 
    	""" Initialize class with empty queue """
    	DeviceQueue.__init__(self)

    def enqueue(self,proc):
    	""" Add process to end of queue """
    	proc.set_proc_loc("Ready")
    	DeviceQueue.enqueue(self,proc)
    	print proc.status()

