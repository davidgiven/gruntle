# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.DBObject import DBObject
import ts.db as db
from ts.exceptions import *
import logging

# An instance of a realm.

class DBInstance(DBObject):
	def __init__(self, id=None):
		super(DBInstance, self).__init__(id)
		
	def create(self, realm):
		super(DBInstance, self).create()
		self.realm = realm
		self.players = frozenset()

	# Verifies that this object is owned by the specified player.
	
	def checkOwner(self, player):
		if (self.realm.owner != player):
			raise PermissionDenied
		
	# Broadcast a message to all players in this instance who are in a
	# specific room and who are not the specified player.
	
	def tell(self, room, eplayer, message):
		for player in self.players:
			if (player != eplayer) and (player.room == room):
				player.tell(message)
				
# Return the default instance for the server.

def getDefaultInstance():
	return db.get(("root", "defaultinstance"))
	