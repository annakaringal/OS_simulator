#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             queues.py
# Created:          February 27, 2015
# Last Updated:     May 9, 2015
# Description:      Classes for different types of queues in the system.
#                       - FIFO Queue implemented with deque
#                       - Priority Queue implemented with min heap
#                           Priority can be frozen or unfrozen
#                           Raises FrozenQueueError if enqueing to frozen queue
#                   Contains methods allowing user to view what is in the
#                   queue and enqueue or dequeue a process.

import sys 
from collections import deque
import heapq
import io
from pcb import PCB

class Queue:

    def __init__(self):
        self._q = None
        self._dev_name = None

    def empty(self):
        return True if not self._q else False
    
    def length(self): 
        """ Returns length of queue """
        return len(self._q)

    ## Returns true if queue contains a process with given PID
    def contains(self, pid):
        return any(p.pid == pid for p in self._q) if self._q else False

    ## Set PCB attributes
    def record_burst(self, proc):
        """
        Get and update burst time for process proc
        """
        burst = io.get_valid_int("Time since last interrupt")
        proc.record_burst_time(burst)

    ## Terminate a given process

    def terminate(self, pid): 
        """
        Remove and delete task with given id 
        """
        if self._q: 
            proc = self.pop(pid)
        else: 
            raise IndexError

        # Print stats
        print "\n" + "{:-^78}".format(" Terminated Process Report ")
        print "PID: {:<4} Avg CPU Burst Time: {:<5} Total CPU Time: {:<5}".format(proc.pid, proc.avg_burst_time(), proc.tot_burst_time()).center(78," ")
        
        del proc


    ## View what's in the queue
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

            while start < len(self._q):

                if end > len(self._q):
                    end = len(self._q)

                # Parameter field headers
                self._q[0].headers()

                print io.ruler()
                
                for p in range(start, end):
                    # Print single process in queue
                    self._q[p].snapshot()

                if end < len(self._q): 
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

    def pop(self,pid):
        """
        Remove and return task with given pid
        """
        for p in self._q:
            if p.pid == pid:
                proc = p 
                self._q.remove(p)
                return proc

class PriorityQueue(Queue):

    def __init__(self, f = False):
        """
        Initialize with empty min heap, and an unfrozen queue
        """
        self._q = []
        self._frozen = f

    ## Methods to freeze/unfreeze queue
    def is_frozen(self):
        return self._frozen

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        self._frozen = False

    ## Enqueue/Dequeue methods
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

    def pop(self,pid):
        """
        Remove and return task with given pid
        """
        for p in self._q:
            if p.pid == pid:
                return self._q.pop(self._q.index(p))

    ## Methods to see what's in the queue
    def snapshot(self):
        """
        Prints a paginated view of processes & process parameters in 
        queue, in the order they will be processed
        """
        # Must sort heap first to display processes in order
        # Python's sort is O(n logn)... is there a better way to do this?
        self._q.sort()
        Queue.snapshot(self)

    def head(self):
        """
        Return process at head of queue, but do not dequeue
        """
        return self._q[0]


class FrozenQueueError(Exception):
    """
    Exception raised for trying to enqueue to frozen queue 
    """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
