#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             queues.py
# Created:          February 27, 2015
# Last Updated:     April 20, 2015
# Description:      Classes for different types of queues in the system.
#                   Contains methods allowing user to view what is in the
#                   queue and enqueue or dequeue a process.

import sys 
from collections import deque
import heapq
import msg
from pcb import PCB

class Queue:

    def __init__(self):
        self._q = None


    def empty(self):
        return True if not self._q else False
    
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

                if end > self.length():
                    end = self.length()

                # Parameter field headers
                self._q[0].headers()

                print msg.ruler()
                
                for p in range(start, end):
                    # Print single process in queue
                    self._q[p].snapshot()

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

class FIFOQueue(Queue): 

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


class PriorityQueue(Queue):

    def __init__(self, f = False):
        """
        Initialize with empty min heap, and an unfrozen queue
        """
        self._q = []
        self._frozen = f

    # Methods to freeze/unfreeze queue
    def is_frozen(self):
        return self._frozen

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        self._frozen = False

    # Enqueue/Dequeue methods
    def enqueue(self, proc):
        """
        Add to heap maintaining heap order property. Only add to heap if queue
        is not frozen.
        """
        if not self._frozen:
            heapq.heappush(self._q,proc)
        else: 
            raise FrozenQueueError("Cannot enqueue to frozen queue")

    def dequeue(self):
        """
        Remove and return task with lowest priority
        """
        return heapq.heappop(self._q)


class FrozenQueueError(Exception):
    """
    Exception raised for trying to enqueue to frozen queue 
    """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
