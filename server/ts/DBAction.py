# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.DBObject import *
from ts.DBRealm import *

# Represents an action.

class DBAction(DBObject):
	def __init__(self, id=None):
		super(DBAction, self).__init__(id)
		
	# Return the room this action is attached to.
	
	@property
	def room(self):
		(room,) = db.sql.cursor().execute(
				"SELECT room FROM actions_in_room WHERE action = ?",
				(self.id,)
			).next()
		return DBRoom(room)
	
	def create(self, description, type, target):
		super(DBAction, self).create()
		(self.description, self.type, self.target) = \
			description, type, target
		
	# Return markup which describes the action.
	
	def markup(self):
		return self.description
