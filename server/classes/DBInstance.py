# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from DBObject import DBObject

# An instance of a realm.

class DBInstance(DBObject):
	def __init__(self, oid=None):
		super(DBInstance, self).__init__("instance", oid)
		
	def create(self, realm):
		super(DBInstance, self).create()
		self.set("realm", realm)
