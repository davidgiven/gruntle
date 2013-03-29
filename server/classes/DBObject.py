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
	def __init__(self, oid):
		self.setOid(oid)

	def __getstate__(self):
		oid = self.getOid()
		assert(oid)
		return oid 
				
	def __setstate__(self, p):
		self.setOid(p)

	def getOid(self):
		return self.__dict__["oid"]

	def setOid(self, oid):
		self.__dict__["oid"] = oid
		
	def __getattr__(self, k):
		oid = self.getOid()
		assert(oid != None)
		return db.get((self.__class__.__name__, oid, k))
		
	def __setattr__(self, k, v):
		oid = self.getOid()
		assert(oid != None)
		db.set((self.__class__.__name__, oid, k), v)
	
	def create(self):
		assert(self.getOid() == None)
		oid = db.createObject()
		self.setOid(oid)
		
		db.set(("object", oid, "type"), self.__class__.__name__)
		