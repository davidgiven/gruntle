# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from DBObject import DBObject

# Represents a room template.

class DBRoom(DBObject):
	def __init__(self, oid=None):
		super(DBRoom, self).__init__(oid)
		
	def create(self, realm, name, title, description):
		super(DBRoom, self).create()
		(self.realm, self.name, self.title, self.description) = \
			realm, name, title, description
		