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
from math import ceil
from bisect import insort
import heapq
import io
from pcb import PCB
from queues import Queue

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

		"""
		Look for given process in memory or job pool and terminates process.
		If process was in memory, allocates any freed memory to largest job
		in job pool, until no more freed memory can be allocated. Returns list
		of new processes allocated
		Else, if process was in job pool, removes from job pool, terminates
		process and 
		"""
		if self.ram.is_in_mem(proc):
			# Deallocate process
			self.ram.deallocate(proc)

			# Try to allocate any processes in job queue
			procs = []
			while self.ram.free_mem: 
				try: 
					procs.append(self.job_pool.dequeue(ram.free_mem))
					self.ram.allocate(procs[-1])
				except: 
					# Either no more jobs or not enough free mem to allocate
					# any processes in queue
					break

			return procs

		else:
			# Not in memory, try the job pool
			# Return no processes, because no new processes were allocated mto
			# free memory
			try: 
				p = self.job_pool.dequeue(proc)
				del p
				return None
			except: 
				print io.error("Process could not be found")


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

	def page_size(self): 
		return self._page_size

	def is_in_mem(self, proc):
		return proc.pid in self._frame_table.values()

	def allocate(self, proc):
		"""
		Allocates memory to a process if there is enough free memory (else
		throws exception). If enough memory, breaks process up into pages,
		assigns pages to frames in frame table and updates free frame list. 
		"""
		if proc.proc_size > self.free_mem():
			raise InsufficientMemory(proc)
			
		# For every page needed for process, insert into first free frame from
		# free frames list and update free frames list
		for p in range(int(ceil(proc.proc_size / self._page_size))):
			self._frame_table[self._free_frames.popleft()] = proc.pid


	def deallocate(self, proc):
		"""
		Deallocates framesin mem for a given process and updates frame table & 
		free frames list. If process not in memory, throws exception. 
		"""

		if not proc.pid in self._frame_table.values():
			raise InvalidProcess

		for k,v in self._frame_table.iteritems(): 
			if v is proc.pid: 
				self._frame_table[k] = None
				self._free_frames.append(k)

class JobPool(Queue):

    def __init__(self):
        self._q = []
        self._dev_name = "job pool"

    def enqueue(self, proc): 
    	""" Add process to job pool, maintaining sorted order """
        proc.set_proc_loc(self._dev_name)
        insort(self._q, proc)
        print proc.status()

    def dequeue(self, free_mem):
        """
        Dequeue and return largest job in job pool that will fit in given 
        memory.
        """
        # Nothing to dequeue
        if not self._q: 
        	raise IndexError

        # Traverse list from largest first
        # Return process that is the largest that will fit in given memory
        for p in reversed(self._q):
        	if p.proc_size <= free_mem:
        		return p

        # No process in queue will fit in given memory
        raise InvalidProcess()


    def dequeue(self, proc):
    	""" Dequeue and return given process from job pool """
        # Nothing to dequeue
        if not self._q: 
        	raise IndexError

    	if (lambda x: x.pid == proc.pid) in self._q: 
    		return self._q.pop(lambda x: x.pid == proc.pid)
    	else: 
	        # Process not in queue
	        raise InvalidProcess

class InsufficientMemory(Exception):
    """
    Exception raised for trying to enqueue while there is not enough free mem
    """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class InvalidProcess(Exception):
    """
    Exception raised when requested process does not exist
    """
    def __init__(self, value="Process does not exist"):
        self.value = value
    def __str__(self):
        return repr(self.value)