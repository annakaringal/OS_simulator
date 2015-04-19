#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             queues.py
# Created:          February 27, 2015
# Last Updated:     April 9, 2015
# Description:      Classes for different types of queues in the system.
#                   Contains methods allowing user to view what is in the
#                   queue and enqueue or dequeue a process.

import sys 
from collections import deque
import heapq
import msg
from pcb import PCB

class FIFOQueue: 

    def __init__(self): 
    	""" Initialize class with empty queue """
    	self._q = deque()

    def length(self): 
        """ Returns length of queue """
        return len(self._q)

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
                print '{:<5}{:<5}{:<20}{:<20}{:^5}{:^20}'.format("Pos", "PID", *map(lambda pf: pf.replace("_", " ").upper(), self._q[0].params.keys()))

                print msg.ruler()
                
                for p in range(start, end):
                    # Print single process in queue

                    print '{:<5}{:<5}{:<20}{:<20}{:^5}{:^20}'.format(p+1, self._q[p].pid, *[str(val)[:20] for val in self._q[p].params.values()])

                if end < self.length(): 
                    try: 
                        print ""
                        raw_input("\t" + "... press any key to view next items in queue ...")
                        print ""
                    except EOFError: 
                        print "Goodbye"
                        raise SystemExit

                start += max_height
                end += max_height

        else:
            print '{:^78}'.format("EMPTY: No processes in queue") + "\n"


class PriorityQueue:

    def __init__(self, f = False):
        """
        Initialize with empty min heap

        """
        self._q = []
        frozen = f

    def length(self):
        return len(_q)

    def frozen(self): 
        return frozen

    def freeze(self):
        frozen = True

    def unfreeze(self):
        frozen = False

    def enqueue(self, proc):
        """
        Add to heap maintaining heap order property
        """
        heappush(_q,proc)

    def dequeue(self):
        """
        Remove and return task with lowest priority
        """
        return heappop(_q)

    def snapshot():
        pass


