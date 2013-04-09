# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging
import apsw
import cPickle as pickle
import ts.db as db

# A database-backed set.

class DatabaseSet(object):
	def __init__(self, dbobject, table, leftfield, rightfield, rightclass):
		self.dbobject = dbobject
		self.table = table
		self.leftfield = leftfield
		self.rightfield = rightfield
		self.rightclass = rightclass

	def __ior__(self, items):
		db.cursor.executemany(
			"INSERT OR IGNORE INTO "+self.table+
				" ("+self.leftfield+", "+self.rightfield+") "+
				" VALUES (?, ?)",
			[ (self.dbobject.id, item.id) for item in items ]
		)
		return self
		  
	def __isub__(self, items):
		db.cursor.executemany(
			"DELETE FROM "+self.table+
				" WHERE "+self.leftfield+"=? AND "+self.rightfield+"=?",
			[ (self.dbobject.id, item.id) for item in items ]
		)
		return self
	
	def __iter__(self):
		items = db.sql.cursor().execute(
			"SELECT "+self.rightfield+" FROM "+self.table+" WHERE "+
				self.leftfield+" = ?",
			(self.dbobject.id,)
		)

		return [ self.rightclass(id) for (id,) in items ].__iter__()
			