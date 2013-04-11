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
		
	def create(self, room, description, type, target):
		super(DBAction, self).create()
		(self.room, self.description, self.type, self.target) = \
			room, description, type, target
		
	# Return markup which describes the action.
	
	def markup(self):
		return self.description
