#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             queues.py
# Created:          February 27, 2015
# Last Updated:     March 1, 2015
# Description:      Contains classes for different queues on the system.
#                   Contains methods allowing user to view what is in the
#                   queue and enqueue or dequeue a process.

import sys 
from collections import deque
import msg
from pcb import PCB

class DeviceQueue: 

    def __init__(self): 
    	""" Initialize class with empty FIFO queue """
    	self._q = deque()

    def enqueue(self, proc):
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
        """ Returns length of queue """
        return len(self._q)

    def snapshot(self):
        """
        Prints a paginated view of processes & process parameters in 
        queue.

        """
        if self._q: 
            
            # max number of lines to show
            max_height = 18
            start = 0
            end = max_height

            while start < self.length():

                if end > self.length(): end = self.length()

                # Parameter field headers
                print '{:<4}{:<5}{:<25}{:<20}{:^5}{:^15}'.format("Pos", "PID", *map(lambda pf: pf.replace("_", " ").upper(), self._q[0].params.keys()))

                print msg.ruler()
                
                for p in range(start, end):
                    # Print single process in queue

                    print '{:<4}{:<5}{:<25}{:<20}{:^5}{:^15}'.format(p+1, self._q[p].pid, *[str(val)[:20] for val in self._q[p].params.values()])

                if end < self.length(): 
                    try: 
                        print ""
                        raw_input("\t" + "... press any key to view next items in queue ...")
                    except EOFError: 
                        print "Goodbye"
                        raise SystemExit

                start += max_height
                end += max_height

        else:
            print '{:^78}'.format("EMPTY: No processes in queue") + "\n"

class ReadyQueue(DeviceQueue):

    def __init__(self): 
    	""" Initialize class with empty queue """
    	DeviceQueue.__init__(self)

    def enqueue(self,proc):
        """
        Adds process to back of ready queue and updates PCB 
        status/location 

        """
    	proc.set_proc_loc("Ready")
    	DeviceQueue.enqueue(self,proc)
    	print proc.status()

    def snapshot(self):
        """ Prints processes in ready queue with header """
        print msg.snapshot_header("ready")
        DeviceQueue.snapshot(self)

