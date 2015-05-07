#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             memory.py
# Created:          May 4, 2015
# Last Updated:     May 7, 2015
# Description:      Classes for long term scheduling and memory management

import sys 
from collections import deque
import heapq
import io
from pcb import PCB

class LongTermScheduler:

	def __init__(self, mem_size, pg_size):
		self.ram = Memory(mem_size, pg_size)
		self.job_pool = JobPool()

	def schedule(self, proc):
		try: 
			self.ram.allocate(proc)
			return True

		except InsufficientMemory:
			self.job_pool.enqueue(proc)
			return False

	def kill(self, proc):
		true: 
			self.ram.deallocate(proc)
			if 



class Memory: 

	def __init__(self, s, p):
		self._size = s
		self._page_size = p
		self._num_of_pages = s/p

		# Create empty frame table & free frame list containing all frames
		self._frame_table = dict.fromkeys(range(self._num_of_pages))
		self._free_frames = deque(self._frame_table.keys())

	def free_mem(self):
		return len(self._free_frames) * self._page_size

	def allocate(self, proc):
		"""
		Allocates memory to a process if there is enough free memory (else
		throws exception). If enough memory, breaks process up into pages,
		assigns pages to frames in frame table and updates free frame list. 
		"""
		if proc.proc_size > self.free_mem(): 
			raise InsufficientMemory
			
		# For every page needed for process, insert into first free frame from
		# free frames list and update free frames list
		for p in range(ceil(proc.proc_size / self._page_size)):
			self._frame_table[self._free_frames.popleft()] = proc.pid

	def deallocate(self, proc):
		"""
		Deallocates framesin mem for a given process and updates frame table & 
		free frames list. If process not in memory, throws exception. 
		"""

		if not proc.pid in dict.values()
			raise InvalidProcess

		for k,v in self._frame_table.iteritems(): 
			if v is proc.pid: 
				self._frame_table[k] = None
				self.free_frames.append(k)

class JobPool(Queue):

    def __init__(self):
        self._q = []
        self._dev_name = "job pool"

    def enqueue(self, proc): 
    	""" Add process to job pool, maintaining sorted order """
        proc.set_proc_loc(self._dev_name)
        self._q.insort(proc)

    def dequeue(self, free_mem):
        """ Dequeue largest job in job pool that will fit """
        # Nothing to dequeue
        if not self._q: 
        	raise IndexError

        # Traverse list from largest first
        # Return process that is the largest that will fit in given mem
        for p in reversed(self._q):
        	if p.proc_size <= free_mem
        		return p

        # Process not in queue
        raise InvalidProcess


    def dequeue(self, proc):
    	""" Remove given process from job pool """
    	return proc 

class InsufficientMemory(Exception):
    """
    Exception raised for trying to enqueue while there is not enough free memory
    """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class InvalidProcess(Exception):
    """
    Exception raised when requested process does not exist
    """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)