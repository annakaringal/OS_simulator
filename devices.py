#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             devices.py
# Created:          February 27, 2015
# Last Updated:     March 5, 2015
# Description:      Classes for different devices on the system. Contains
#                   methods allowing user to see/change what process(es) a
#                   device is running or are in the device queue. 


import sys
from collections import deque
import msg
from queues import DeviceQueue
from pcb import PCB

class Device(DeviceQueue):

    def __init__(self, dname, dtype): 
        """
        Initializes new device with device name & device type, and new
        empty queue

        """ 
        DeviceQueue.__init__(self)
        self._dev_name = dname
        self._dev_type = dtype

    ## Queue methods

    def enqueue(self, proc):
        """ Add process to end of queue """
        proc.set_proc_loc(self._dev_name)
        DeviceQueue.enqueue(self,proc)
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
        DeviceQueue.snapshot(self)

    ## Methods to check/return device name/type

    def is_device_name(self, query_name):
        return True if self._dev_name == query_name else False

    def is_device_type(self, query_type):
        return True if self._dev_type == query_type else False

    def get_dev_type(self):
        return self._dev_type

    def get_dev_name(self):
        return self._dev_name


class CPU(): 

    def __init__(self):
        """ Initializes CPU with no active processes """ 
        self.active = None

    def empty(self):
        """ Returns true if no active process in CPU """ 
        return False if self.active else True

    ## Methods to modify active process in CPU

    def set_process(self, proc):
        """ Sets active process in CPU to given process """
        proc.set_proc_loc("CPU")
        self.active = proc
        print "{a!s} is in the CPU".format(a = str(self.active).capitalize())

    def get_process(self):
        """ Returns copy of active process in CPU """ 
        if self.active:
            return self.active
        else: 
            raise IndexError

    def terminate_process(self):
        """
        Terminates active process in CPU, deallocates memory used by process.

        """
        if self.active: 
            print "{a!s} terminated".format(a = str(self.active).capitalize())
            proc = self.active
            del proc
            self.active = None
        else: 
            raise IndexError

