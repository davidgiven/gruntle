# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.DBObject import DBObject

# Represents a room template.

class DBRoom(DBObject):
	def __init__(self, id=None):
		super(DBRoom, self).__init__(id)
		
	def create(self, realm, name, title, description):
		super(DBRoom, self).create()
		(self.realm, self.name, self.title, self.description) = \
			realm, name, title, description
		self.immutable = False
		self.actions = {}
		
	# Return markup which describes the room.
	
	def markup(self):
		return {
			"type": "room",
			"name": self.name,
			"title": self.title,
			"oid": self.id
		}
		
