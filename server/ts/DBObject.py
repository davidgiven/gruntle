# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.exceptions import *
import ts.db as db
import cPickle as pickle

# Connects the specified class to a particular table.

def linkToTable(cls, table):
	@classmethod
	def gettable(cls):
		return table
	setattr(cls, "table", gettable)

# Creates setters and getters for some string fields.

def simpleSettersGetters(cls, fields):
	table = cls.table()
	
	for f in fields:
		def get(self, f=f):
			(value,) = db.sql.cursor().execute(
				"SELECT "+f+" FROM "+self.table()+" WHERE id = ?",
				(self.id,)
			).next()
			return value
		
		def set(self, value, f=f):
			db.sql.cursor().execute(
				"UPDATE "+self.table()+" SET "+f+" = ? WHERE id = ?",
				(value, self.id)
			)
			
		setattr(cls, f, property(get, set))

# Creates setters and getters for object references.

def objrefSettersGetters(cls, destclass, fields):
	table = cls.table()
	
	for f in fields:
		def get(self, f=f):
			(value,) = db.sql.cursor().execute(
				"SELECT "+f+" FROM "+self.table()+" WHERE id = ?",
				(self.id,)
			).next()
			if value:
				return destclass(value)
			return None
		
		def set(self, value, f=f):
			if value:
				db.sql.cursor().execute(
					"UPDATE "+self.table()+" SET "+f+" = ? WHERE id = ?",
					(value.id, self.id)
				)
			else:
				db.sql.cursor().execute(
					"UPDATE "+self.table()+" SET "+f+" = NULL WHERE id = ?",
					(self.id,)
				)
			
		setattr(cls, f, property(get, set))

# Creates setters and getters for pickled fields.

def pickledSettersGetters(cls, fields):
	table = cls.table()
	
	for f in fields:
		def get(self, f=f):
			(value,) = db.sql.cursor().execute(
				"SELECT "+f+" FROM "+self.table()+" WHERE id = ?",
				(self.id,)
			).next()
			return pickle.loads(value)
		
		def set(self, value, f=f):
			print("UPDATE "+self.table()+" SET "+f+" = ? WHERE id = ?")
			db.sql.cursor().execute(
				"UPDATE "+self.table()+" SET "+f+" = ? WHERE id = ?",
				(pickle.dumps(value), self.id)
			)
			
		setattr(cls, f, property(get, set))
		
# Base class for a database-backed object.

class DBObject(object):
	def __init__(self, id):
		self.id = id
		if id:
			assert(type(id) == int)

	def __hash__(self):
		return self.id
		
	def __getstate__(self):
		id = self.id
		assert(id)
		return id 
				
	def __setstate__(self, p):
		self.id = p

	def __cmp__(self, other):
		if not other:
			return -1
		return self.id.__cmp__(int(other.id))
	
	@classmethod
	def table(cls):
		assert(False)

	def setfield(self, key, value):
		db.sql.cursor().execute(
			"UPDATE "+self.table()+" SET "+key+" = ? WHERE id = ?",
			(pickle.dumps(value), self.id)
		)
		
	def getfield(self, key):
		(value,) = db.sql.cursor().execute(
			"SELECT "+key+" FROM "+self.table()+" WHERE id = ?",
			(self.id,)
		)
		return pickle.loads(value)
		 

	# Creates a new instance of this class in the database.
		
	def create(self):
		assert(self.id == None)
		
		db.sql.cursor().execute(
				"INSERT INTO "+self.table()+" (id) VALUES (NULL)"
			)
			
		self.id = db.sql.last_insert_rowid()
	
	# Destroys this object in the database. Strictly we should remove all
	# instance variables, but we don't track these yet, so we just leak them.
		
	def destroy(self):
		assert(self.id != None)
		db.unset(("object", self.id, "type"))
			
