#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             devices.py
# Created:          February 27, 2015
# Last Updated:     April 19, 2015
# Description:      Classes for different devices on the system. Contains
#                   methods allowing user to see/change what process(es) a
#                   device is running or are in the device queue. 

import sys
from collections import deque
import msg
from queues import FIFOQueue, PriorityQueue
from pcb import PCB

class Device(FIFOQueue):

    def __init__(self, dname, dtype): 
        """
        Initializes new device with device name & device type, and new
        empty FIFO queue

        """ 
        FIFOQueue.__init__(self)
        self._dev_name = dname
        self._dev_type = dtype

    ## Queue methods

    def enqueue(self, proc):
        """ Add process to end of queue """
        proc.set_proc_loc(self._dev_name)
        FIFOQueue.enqueue(self,proc)
        print proc.status()

    def dequeue(self):
        """
        Remove and return process at head of queue
        Clear any parameters passed when queued
        """
        proc = FIFOQueue.dequeue(self)
        proc.clear_params()
        return proc

    ## Methods to print device in human readable form to console

    def __repr__(self):
        """ Returns device name and type as a string """ 
        return self._dev_name + " (" + self._dev_type.lower() + ")"

    def __str__(self):
        """ Returns device name and type as a string """ 
        return self._dev_type + " " + self._dev_name

    def snapshot(self):
        """ Prints all processes in queue to console """
        print msg.snapshot_header(self._dev_name)
        FIFOQueue.snapshot(self)

    ## Methods to check/return device name/type

    def is_device_name(self, query_name):
        return True if self._dev_name == query_name else False

    def is_device_type(self, query_type):
        return True if self._dev_type == query_type else False

    def get_dev_type(self):
        return self._dev_type

    def get_dev_name(self):
        return self._dev_name

class DiskDrive(PriorityQueue):
    """
    Initializes new disk drive with device name and two empty queues
    to implement FSCAN scheduling
    """ 

    def __init__(self, dname, cyl):

        self._dev_type = "Disk Drive"
        self._dev_name = dname
        self._cylinders = cyl

        # Two priority queues to implement FSCAN. Q2 is frozen
        self._q1 = PriorityQueue()
        self._q2 = PriorityQueue(True)

    ## Methods to check/return device properties

    def get_num_cylinders(self):
        return self._cylinders

    def is_device_name(self, query_name):
        return True if self._dev_name == query_name else False

    def get_dev_name(self):
        return self._dev_name

    def is_device_type(self, query_type):
        return True if self._dev_type == query_type else False

    def get_dev_type(self):
        return self._dev_type

    ## Scheduling methods

    def enqueue(self, proc):
        """
        Enqueue processes to unfrozen queue. Update process location.
        If frozen queue is empty, unfreeze and freeze other queue

        """
        if self._q1.is_frozen(): #Q1 is frozen, add to Q2
            proc.set_proc_loc(self._dev_name)
            self._q2.enqueue(proc)
            if self._q1.empty():
                self._q2.freeze()
                self._q1.unfreeze()

        else: #Q2 frozen, add to Q1
            proc.set_proc_loc(self._dev_name)
            self._q1.enqueue(proc)
            if self._q2.empty():
                self._q1.freeze()
                self._q2.unfreeze()

    def dequeue(self):
        """
        Remove and return process at head of frozen queue. Clear any
        parameters passed when queued.

        Only dequeue processes from whichever queue is frozen. If dequeuing
        empties queue, freeze queue and unfreeze other queue
        """ 
        if self._q1.is_frozen():
            proc = self._q1.dequeue()
            if self._q1.empty():
                self._q2.freeze()
                self._q1.unfreeze()

        else: 
            proc = self._q2.dequeue()
            if self._q2.empty():
                self._q1.freeze()
                self._q2.unfreeze()

        proc.clear_params()
        return proc

     ## Methods to print device in human readable form to console

    def __repr__(self):
        """ Returns device name and type as a string """ 
        return self._dev_name + " (" + self._dev_type.lower() + ")"

    def __str__(self):
        """ Returns device name and type as a string """ 
        return self._dev_type + " " + self._dev_name

    def snapshot(self):
        print msg.snapshot_header(self._dev_name)

        if self._q1.empty() and self._q2.empty():
            print '{:^78}'.format("EMPTY: No processes in queue") + "\n"
        else:
            if self._q1.is_frozen():
                print msg.snapshot_header("PROCESSING [FROZEN]", " ")
                self._q1.snapshot()
                print msg.snapshot_header("NEW REQUESTS", " ")
                self._q2.snapshot()
            else:
                print msg.snapshot_header("PROCESSING [FROZEN]", " ")
                self._q2.snapshot()
                print msg.snapshot_header("NEW REQUESTS", " ")
                self._q1.snapshot()

class CPU(PriorityQueue): 

    def __init__(self):
        """
        Initializes CPU with no active processes and empty non-frozen
        Priority Queue
        """ 
        self.active = None
        PriorityQueue.__init__(self)

    def empty(self):
        return True if self.active else False

    ## Methods to modify active process in CPU

    def enqueue(self,proc):
        """
        Adds process to back of ready queue and updates PCB status/location 
        """
        if not self.active: # No processes in CPU
            proc.set_proc_loc("CPU")
            self.active = proc
        else: # Something in CPU, put in ready queue
            proc.set_proc_loc("ready")
            PriorityQueue.enqueue(self,proc)
        print proc.status()

    def ready_to_CPU(self):
        """
        Moves process at head of ready queue to CPU
        """
        if not PriorityQueue.empty(self):
                self.active = PriorityQueue.dequeue(self)
                self.active.set_proc_loc("CPU")
        else: # Nothing in ready queue
            self.active = None
            print msg.nothing_in_ready()

    def terminate(self):
        """
        Terminates active process in CPU, deallocates memory used by process.
        Moves next process in Ready Queue to CPU.
        """
        if self.active: 
            # Terminate active process and replace from ready queue
            print "{a!s} terminated".format(a = str(self.active).capitalize())
            proc = self.active

            self.ready_to_CPU()

            print "\n" + "{:-^78}".format(" Terminated Process Report ")
            print "PID: {:<4} Avg CPU Burst Time: {:<5} Total CPU Time: {:<5}".format(proc.pid, proc.avg_burst_time(), proc.total_cpu_time).center(78," ")
            
            del proc

        else: # Nothing to dequeue
            raise IndexError 

    def dequeue(self):
        """
        Returns current active process in CPU. Removes from CPU and moves next
        process in Ready Queue to CPU.

        """
        if self.active: 
            # Terminate active process and replace from ready queue
            print "{a!s} removed from CPU".format(a = str(self.active).capitalize())
            proc = self.active
            self.ready_to_CPU()

            # Update burst times
            burst = msg.get_valid_int("Time Spent in CPU")
            proc.record_burst_time(burst)
            return proc

        else: # Nothing to dequeue
            raise IndexError 

    def snapshot(self):
        """ Prints processes in ready queue with header """
        print msg.snapshot_header("ready")
        PriorityQueue.snapshot(self)
        if self.active: 
            print "\n" + "Active process in CPU: {a!s}".format(a=str(self.active))
        else:
            print "\n" + "No active process in the CPU"

    def get_active_process(self):
        """ Returns copy of active process in CPU """ 
        if self.active:
            return self.active
        else: 
            raise IndexError

