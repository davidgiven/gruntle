# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.DBObject import DBObject
from ts.exceptions import *
import ts.db as db
import logging

# An instance of a realm.

class DBInstance(DBObject):
	@classmethod
	def table(cls):
		return "instances"
			
	def __init__(self, id=None):
		super(DBInstance, self).__init__(id)
		
	def create(self, realm):
		super(DBInstance, self).create()
		self.realm = realm

	# Verifies that this object is owned by the specified player.
	
	def checkOwner(self, player):
		if (self.realm.owner != player):
			raise PermissionDenied
			
	# Something in this instance has changed.
	
	def fireChangeNotification(self):
		for player in self.players:
			player.onLook()
			
	# Broadcast a message to all players in this instance who are in a
	# specific room and who are not the specified player.
	
	def tell(self, room, eplayer, message):
		for player in self.players:
			if (player != eplayer) and (player.room == room):
				player.tell(message)
	
def setDefaultInstance(instance):
	db.setvar("defaultinstance", int(instance.id))

def getDefaultInstance():
	return DBInstance(int(db.getvar("defaultinstance")))
