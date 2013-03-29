# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import db

# Base class for a database-backed object.

class DBObject(object):
	type = None
	oid = None
	
	def __init__(self, type, oid):
		self.type = type
		self.oid = oid
		
	def create(self):
		assert(self.oid == None)
		self.oid = db.createObject()
		
		db.set(("object", self.oid, "type"), self.type)
		
	def set(self, k, v):
		assert(self.oid != None)
		db.set((self.type, self.oid, k), v)
		
	def get(self, k):
		assert(self.oid != None)
		return db.get((self.type, self.oid, k))
		