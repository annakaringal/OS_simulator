#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             pcb.py
# Created:          February 27, 2015
# Last Updated:     April 20, 2015
# Description:      Class for the PCB (Process Control Block) that contains and
#                   sets all information about a process, its state and any
#                   parameters passed to it by a system call

import sys
from functools import total_ordering
import msg

param_fields = ["file_name","mem_loc","rw","file_len", "cylinder"]

@total_ordering
class PCB:

    def __init__(self, id_num, alpha, tau, p_loc="ready"): 
        """
        Initialize with new pid & location, empty system call params.
        Calculate next burst based on given history parameter alpha and inital
        burst estimate tau.
        """
        self.pid = id_num
        self.proc_loc = p_loc

        #Set params & burst history
        self.params = dict.fromkeys(param_fields)
        self.alpha = alpha
        self.burst_history = []
        self.next_est_burst = alpha * tau
        self.total_cpu_time = 0

    def set_proc_loc(self, p_loc):
        """ Sets location of process, i.e. which queue/device it is in"""
        self.proc_loc = p_loc

    ## Methods to print out contents/properties of PCB

    def __repr__(self):
    	return "process #" + str(self.pid) 

    def __str__(self):
    	return "process #" + str(self.pid)

    def status(self):
        """ Prints which queue/device process is currently in """
        if not self.proc_loc.lower()== "cpu":
            return "{a!s} is in {q!s} Queue".format(a = str(self).capitalize(), q = self.proc_loc.capitalize())
        else: 
            return "{a!s} is in {q!s}".format(a = str(self).capitalize(), q = self.proc_loc.upper())

    def snapshot(self):
        """
        Prints PCB attributes and any current system call parameters in a 
        formatted fashion, on a single line
        """
        print "{:<4}".format(str(self.pid)),

        for key, val in self.params.iteritems():
            if self.proc_loc.lower()[0]!="d" and key=="cylinder":
                continue
            print"{:^{w}}".format(str(val)[:10], w=len(key)+1),

        print "{:^9}".format(str(self.avg_burst_time())),
        print "{:^12}".format(str(self.total_cpu_time)),
        if self.proc_loc.lower()[0] == "r":
            print "{:^14}".format(str(self.next_est_burst)),
        print "\n",


    def headers(self):
        """
        Prints name of system call parameters and PCB attributes in formatted
        fashion, on a single line
        """
        print "{:<4}".format("PID"),
        for key,val in self.params.iteritems():
            if self.proc_loc.lower()[0]!="d" and key=="cylinder":
                continue
            print"{:<{w}}".format(str(key).replace("_"," ").capitalize()[:10], w=len(key)+1),

        print "{:9}".format("Avg Burst"),
        print "{:<12}".format("Tot CPU Time"),
        if self.proc_loc.lower()[0] == "r":
            print "{:^14}".format("Next Est Burst"),
        print "\n",


    ## Methods to compare PCBs

    def __eq__(self, other):
        """
        Compares equality based on different parameters that depend on which
        queue PCB is in.

        If in ready queue, compare based on next estimated burst time.
        If in disk drive queue, compare based on requested cylinder.
        Else, compare by PID.
        """
        if (self.proc_loc.lower()[0] == "r"):
            return self.next_est_burst == other.next_est_burst
        elif (self.proc_loc.lower()[0] == "d"):
            return self.params["cylinder"] == other.params["cylinder"]
        else:
            return self.pid == other.pid

    def __lt__(self, other):
        """
        Compares PCBs based on different parameters depending on which queue PCB
        is in.

        All other comparisons (>, <= and >=) are generated by
        functools/total_ordering
        """
        if (self.proc_loc.lower()[0] == "r"):
            return self.next_est_burst < other.next_est_burst
        elif (self.proc_loc.lower()[0]== "d"):
            return self.params["cylinder"] < other.params["cylinder"]
        else:
            return self.pid < other.pid


    ## Calculating burst time

    def calc_next_est_burst (self):
        """
        Calculates next estimated burst time based on previous estimated burst
        time, last recorded burst time, and history parameter alpha

        """
        self.last_est_burst = self.next_est_burst
        self.next_est_burst = (self.burst_history[-1]* (1-self.alpha)) + (self.alpha * self.last_est_burst)

    def record_burst_time(self, burst): 
        """
        Updates burst history, total CPU time and calculates next estimated
        burst time with given input
        """
        self.burst_history.append(burst)
        self.total_cpu_time += burst
        self.calc_next_est_burst()

    def avg_burst_time(self):
        """
        Returns average burst time for each CPU burst
        """
        return self.total_cpu_time / len(self.burst_history) if self.burst_history else 0

    ## Setting/clearing system call params for pcb

    def set_syst_call_params(self):
        """
        Sets system call params for file name & starting memory location
        """
        self.params["file_name"] = raw_input("File Name >>> ")
        self.params["mem_loc"] = msg.get_valid_int("Starting Memory Location")

    def set_read_write_params(self, dev_type):
        """
        Sets system call params for read/write and file length (if write)
        """
        if (dev_type.lower() == "printer"):
            self.params["rw"] = "w"
        else: 
            while self.params["rw"] == None:
                rw = raw_input("Read or Write? >>> ")
                if rw.lower() in ["r", "read"]:
                    self.params["rw"] = "r"
                elif rw.lower() in ["w", "write"]:
                    self.params["rw"] = "w"
                else: 
                    print msg.err("Invalid read/write parameters")
                    print "Please enter either 'r', 'read', 'w' or 'write'"

        if self.params["rw"] == "w":
            self.params["file_len"] = msg.get_valid_int("File Length")

    def set_cylinder_params(self, max_num_cylinders):
        """
        Prompts user for which disk drive cylinder to access, validates 
        input and sets appropriate system call parameter.

        Precondition: Process is in disk drive
        """
        while self.params["cylinder"] == None:
            cyl = msg.get_valid_int("Cylinder")
            if cyl > max_num_cylinders: 
                print "Invalid cylinder number. Please try again."
            else: 
                self.params["cylinder"] = cyl

    def clear_params(self):
        """ Clears all system call & read/write params """
        for p in self.params:
            self.params[p] = None
