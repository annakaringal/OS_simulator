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
    	""" Initialize class with empty queue """
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
        return len(self._q)

    def snapshot(self):
        if self._q: 
            print '{:<4}{:^5}{:<25}{:<20}{:^5}{:^15}'.format("Pos", "PID", *map(lambda pf: pf.replace("_", " ").upper(), self._q[0].param_fields))
            for i in range(self.length()):
                print '{:<4}{:^5}{:<25}{:<20}{:^5}{:^15}'.format(i+1, self._q[i].pid, *self._q[i].params.values())
            print ""
        else:
            print '{:^78}'.format("EMPTY: No processes in queue") + "\n"

class ReadyQueue(DeviceQueue):

    def __init__(self): 
    	""" Initialize class with empty queue """
    	DeviceQueue.__init__(self)

    def enqueue(self,proc):
    	proc.set_proc_loc("Ready")
    	DeviceQueue.enqueue(self,proc)
    	print proc.status()

    def snapshot(self):
        print msg.snapshot_header("ready")
        DeviceQueue.snapshot(self)

