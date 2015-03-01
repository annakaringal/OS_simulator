#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             pcb.py
# Created:          February 27, 2015
# Last Updated:     March 1, 2015
# Description:      Class for the PCB (Process Control Block) that contains
#                       and sets all information about a process, its state
#                       and any parameters passed to it by a system call

import sys
import msg

class PCB:

    def __init__(self, id_num, p_loc="ready"): 
        self.pid = id_num
        self.proc_loc = p_loc
        self.param_fields = ["file_name","mem_loc","rw","file_len"]
        self.params = dict.fromkeys(self.param_fields)

    def set_proc_loc(self, p_loc):
        """ Sets location of process, i.e. which queue/device it is in"""
        self.proc_loc = p_loc


    ## Methods to print out contents/properties of PCB

    def __repr__(self):
    	return "process #" + str(self.pid) 

    def __str__(self):
    	return "process #" + str(self.pid)

    def status(self):
        return "{a!s} is in {q!s} queue".format(a = str(self).capitalize(), q = self.proc_loc.lower())

    ## Setting/clearing system call params for pcb

    def set_syst_call_params(self):
        self.params["file_name"] = raw_input("File Name: ")
        msg.set_valid_int(self.params, "mem_loc", "Starting Memory Location")

    def set_read_write_params(self, dev_type):
        if (dev_type.lower() == "printer"):
            self.params["rw"] = "w"
        else: 
            while self.params["rw"] == None:
                rw = raw_input("Read or Write?: ")
                if rw.lower() in ["r", "read"]:
                    self.params["rw"] = "r"
                elif rw.lower() in ["w", "write"]:
                    self.params["rw"] = "w"
                else: 
                    print msg.err("Invalid read/write parameters")
                    print "Please enter either 'r', 'read', 'w' or 'write'" + "\n"

        if self.params["rw"] == "w":
            msg.set_valid_int(self.params, "file_len", "File Length")

    def clear_params(self): # TODO: FIGURE OUT WHEN NEED TO DO THIS
        """ Clears all system call & read/write params """
        for p in self.params:
            self.params[p] = None
