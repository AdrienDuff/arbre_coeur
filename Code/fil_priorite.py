#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
from heapq import heappush, heappop #gere les files de priorite avec un arbre binaire.
import itertools

class Test(object):
	"""docstring for Test"""
	def __init__(self, arg):
		super(Test, self).__init__()
		self.arg = arg
		


class Fil_prio(object):
	"""docstring for Fil_prio"""

	REMOVED = '<removed-task>'

	def __init__(self, tab , entry_finder, counter):
		#print(tab)
		super(Fil_prio, self).__init__()
		self.fil = tab
		self.entry_finder = entry_finder
		self.counter = counter


	def add_task(self,task, priority=0):
	    'Add a new task or update the priority of an existing task'
	    if task in self.entry_finder:
	        self.remove_task(task)
	    count = next(self.counter)
	    entry = [priority, count, task]
	    self.entry_finder[task] = entry
	    heappush(self.fil, entry)

	def remove_task(self,task):
	    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
	    entry = self.entry_finder.pop(task)
	    entry[-1] = self.REMOVED

	def pop_task(self):
	    'Remove and return the lowest priority task. Raise KeyError if empty.'
	    while self.fil:
	        priority, count, task = heappop(self.fil)
	        if task is not self.REMOVED:
	            del self.entry_finder[task]
	            return task
	    raise KeyError('pop from an empty priority queue')
 