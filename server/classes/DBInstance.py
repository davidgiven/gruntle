# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from DBObject import DBObject
import db

# An instance of a realm.

class DBInstance(DBObject):
	def __init__(self, id=None):
		super(DBInstance, self).__init__(id)
		
	def create(self, realm):
		super(DBInstance, self).create()
		self.realm = realm

# Return the default instance for the server.

def getDefaultInstance():
	return db.get(("root", "defaultinstance"))
	