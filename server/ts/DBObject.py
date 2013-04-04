# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import ts.db as db
from ts.exceptions import *

# Base class for a database-backed object.

class DBObject(object):
	id = None
	
	def __init__(self, id):
		if id:
			assert(type(id) == int)
			if (db.get(("object", id, "type")) != self.__class__.__name__):
				raise InvalidObjectReference
			self.id = id

	def __getstate__(self):
		id = self.id
		assert(id)
		return id 
				
	def __setstate__(self, p):
		self.id = p

	def __getattr__(self, k):
		if (k == "id"):
			return object.__getattr__(self, k)
			
		id = self.id
		assert(id != None)
		return db.get((self.__class__.__name__, id, k))
		
	def __setattr__(self, k, v):
		if (k == "id"):
			return object.__setattr__(self, k, v)
			
		id = self.id
		assert(id != None)
		db.set((self.__class__.__name__, id, k), v)
	
	def __cmp__(self, other):
		return self.id.__cmp__(other.id)
		
	def create(self):
		assert(self.id == None)
		id = db.createObject()
		self.id = id
		
		db.set(("object", id, "type"), self.__class__.__name__)
		