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

    def snapshot(self):
        if self._q: 

            start = 0
            max_height = 20
            end = max_height

            while start < len(self._q):

                if end > len(self._q): end = len(self._q)

                # Parameter field headers
                print '{:<4}{:^5}{:<25}{:<20}{:^5}{:^15}'.format("Pos", "PID", *map(lambda pf: pf.replace("_", " ").upper(), self._q[0].param_fields))

                print msg.ruler()
                
                for p in range(start, end):
                    # Print single process in queue
                    print '{:<4}{:^5}{:<25}{:<20}{:^5}{:^15}'.format(p+1, self._q[p].pid, *self._q[p].params.values())

                if end < len(self._q): 
                    try: 
                        print ""
                        raw_input("... press any key to view next 20 items in queue >>> ")
                    except EOFError: 
                        print "Goodbye"
                        raise SystemExit

                start += max_height
                end += max_height

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

