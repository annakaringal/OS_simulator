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
from queues import DeviceQueue
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
        self._dname = dname
        self._dname = dname

        # Two priority queues to implement FSCAN
        PriorityQueue.__init__(self) 
        self._q2 = PriorityQueue() 

    ## Methods to check/return device properties

    def get_num_cylinders(self):
        return self._cylinders

    def is_device_name(self, query_name):
        return True if self._dev_name == query_name else False

    def get_dev_name(self):
        return self._dev_name

    ## Scheduling methods

    def enqueue(self, proc):
        pass

    def dequeue(self, proc):
        pass


class CPU(PriorityQueue): 

    def __init__(self):
        """ Initializes CPU with no active processes and empty Priority Queue""" 
        self.active = None
        PriorityQueue.__init__(self)

    def empty(self):
        return True if self.active else False

    ## Methods to modify active process in CPU

    def enqueue(self,proc):
        """
        Adds process to back of ready queue and updates PCB 
        status/location 

        """
        if not (self.active): # No processes in CPU
            proc.set_proc_loc("CPU")
            self.active = proc
        else: # Something in CPU, put in ready queue
            proc.set_proc_loc("Ready")
            PriorityQueue.enqueue(self,proc)
        print proc.status()

    def ready_to_CPU(self):
        """
        Moves process at head of ready queue to CPU
        """
        if PriorityQueue: 
                self.active = PriorityQueue.dequeue()
            else: # Nothing in ready queue
                self.active = None
                print msg.nothing_in_ready()

    def terminate(self):
        """
        Terminates active process in CPU, deallocates memory used by process.
        Moves next process in Ready Queue to CPU

        """
        if self.active: 
            # Terminate active process and replace from ready queue
            print "{a!s} terminated".format(a = str(self.active).capitalize())
            proc = self.active
            del proc

            ready_to_CPU(self)

        else: # Nothing to dequeue
            raise IndexError 

    def dequeue(self):
        """
        Returns current active process in CPU. Removes from CPU and moves next
        process in Ready Queue to CPU.

        """
        if self.active: 
            # Terminate active process and replace from ready queue
            print "{a!s} terminated".format(a = str(self.active).capitalize())
            proc = self.active
            ready_to_CPU(self)
            return proc

        else: # Nothing to dequeue
            raise IndexError 

    def snapshot(self):
        """ Prints processes in ready queue with header """
        print msg.snapshot_header("ready")
        PriorityQueue.snapshot(self)

    def get_active_process(self):
        """ Returns copy of active process in CPU """ 
        if self.active:
            return self.active
        else: 
            raise IndexError

