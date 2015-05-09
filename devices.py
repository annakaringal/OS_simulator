#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             devices.py
# Created:          February 27, 2015
# Last Updated:     May 9, 2015
# Description:      Classes for different devices on the system. Contains
#                   methods allowing user to see/change what process(es) a
#                   device is running or are in the device queue. 

import sys
from collections import deque
import io
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
        Clear any parameters passed when queued, records burst time
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
        print io.snapshot_header(self._dev_name)
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
    to implement FLOOK disk scheduling
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

    def contains(self,pid):
        return (self._q1.contains(pid) or self._q2.contains(pid))

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

    def terminate(self, pid):
        if self._q1.contains(pid): 
            self._q1.terminate(pid)
        elif self._q2.contains(pid):
            self._q2.terminate(pid)
        else:
            raise IndexError

     ## Methods to print device in human readable form to console

    def __repr__(self):
        return self._dev_name + " (" + self._dev_type.lower() + ")"

    def __str__(self):
        """ Returns device name and type as a string """ 
        return self._dev_type + " " + self._dev_name

    def snapshot(self):
        """
        Prints active processes in disk drive queue, in order they will be processed
        """
        print io.snapshot_header(self._dev_name)

        if self._q1.empty() and self._q2.empty():
            print '{:^78}'.format("EMPTY: No processes in queue")
        else:
            if self._q1.is_frozen():
                print io.snapshot_header("PROCESSING [FROZEN]", " ")
                self._q1.snapshot()
                print io.snapshot_header("NEW REQUESTS", " ")
                self._q2.snapshot()
            else:
                print io.snapshot_header("PROCESSING [FROZEN]", " ")
                self._q2.snapshot()
                print io.snapshot_header("NEW REQUESTS", " ")
                self._q1.snapshot()

class CPU(PriorityQueue): 

    def __init__(self):
        """
        Initializes CPU with no active processes and empty non-frozen
        Priority Queue
        """ 
        self.active = None
        self._dev_name = "CPU"
        PriorityQueue.__init__(self)

    def empty(self):
        return True if self.active else False

    def contains(self, pid): 
        if pid == self.active.pid: 
            return True
        else: 
            return PriorityQueue.contains(self,pid)

    ## Methods to modify active process in CPU

    def enqueue(self,proc):
        """
        Adds process to back of ready queue and updates PCB status/location 
        """
        if not self.active:
            # No processes in CPU, process goes straight to CPU
            # No need to prompt for time
            proc.set_proc_loc(self._dev_name)
            self.active = proc
        else:
            # Prompt for time since last interrupt
            elapsed = io.get_valid_int("Time since last interrupt")

            # Update burst time for current process
            self.active.update_burst_time(elapsed)

            # Insert  into ready queue
            proc.set_proc_loc("ready")
            PriorityQueue.enqueue(self,proc)

            # Move active process to ready queue if it now has a higher
            # remaining burst time left than any process in the ready queue
            if PriorityQueue.head(self) < self.active:
                p = PriorityQueue.dequeue(self)
                self.active.set_proc_loc("ready")
                p.set_proc_loc("CPU")
                PriorityQueue.enqueue(self,self.active)
                self.active = p

        print proc.status()

    def ready_to_CPU(self):
        """
        Moves process at head of ready queue to CPU
        """
        if not PriorityQueue.empty(self):
                self.active = PriorityQueue.dequeue(self)
                self.active.set_proc_loc(self._dev_name)
        else: # Nothing in ready queue
            self.active = None
            print io.nothing_in_ready()

    def terminate(self, pid = None):
        """
        If no pid given, terminates active process in CPU. Else, terminates 
        process with given pid. 
        If active process is terminated, moves head of Ready Queue to CPU.
        Precondition: pid is a valid PID for a process in the ready queue or CPU
        """
        proc = None
        if self.active: 

            # Terminate active process if no pid given or if active process has
            # given pid
            if not pid or self.active.pid == pid: 
                proc = self.active 
                self.ready_to_CPU()

            else: # Look for process in ready queue and remove
                proc = PriorityQueue.pop(self, pid)

            self.record_burst(proc)

            # Print stats
            print "\n" + "{:-^78}".format(" Terminated Process Report ")
            print "PID: {:<4} Avg CPU Burst Time: {:<5} Total CPU Time: {:<5}".format(proc.pid, proc.avg_burst_time(), proc.tot_burst_time()).center(78," ")
            
            del proc

        else: 
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

            # Get & record burst time
            self.record_burst(proc)

            # Clear current burst time before exiting CPU
            proc.clear_curr_burst()

            return proc

        else: # Nothing to dequeue
            raise IndexError 

    def snapshot(self):
        """ Prints processes in ready queue, plus active process in CPU with headers """
        print io.snapshot_header("ready")
        PriorityQueue.snapshot(self)
        if self.active: 
            print "\n" + "ACTIVE IN CPU: {a!s} (Estimated time remaining: {b!s})".format(a=str(self.active).capitalize(), b=str(self.active.next_est_burst))
        else:
            print "\n" + "No active process in the CPU"

    def get_active_process(self):
        """ Returns copy of active process in CPU """ 
        if self.active:
            return self.active
        else: 
            raise IndexError

