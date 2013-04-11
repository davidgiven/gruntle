# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.DBObject import DBObject
from ts.DBRoom import DBRoom
from ts.DBInstance import DBInstance
import ts.db as db

# Base class for a realm.

class DBRealm(DBObject):
	def __init__(self, id=None):
		super(DBRealm, self).__init__(id)
		
	# Return the rooms contained in this realm.
	
	@property
	def rooms(self):
		return [ DBRoom(id) for (id,) in
			db.sql.cursor().execute(
				"SELECT id FROM rooms WHERE realm=?",
				(self.id,)
			)
		]
	
	def create(self, name, owner):
		super(DBRealm, self).create()
		(self.name, self.owner) = name, owner
		
	# Verifies that this object is owned by the specified player.
	
	def checkOwner(self, player):
		if (self.owner != player):
			raise PermissionDenied
		
	# Room management
	
	def addRoom(self, name, title, description):
		room = DBRoom()
		room.create(self, name, title, description)
		return room

	def findRoom(self, name):
		for r in self.rooms:
			if (r.name == name):
				return r
		return None
		
	def destroyRoom(self, room):
		# Eject any players currently in the room.
	 	
 		entrypoint = self.findRoom("entrypoint")
	 	for instance in self.instances:
	 		for player in instance.players:
	 			if (player.room == room):
	 				player.tell(
						{
							"event": "activity",
							"message": "Space-time abruptly shreds and tears "+
								"around you. You find yourself elsewhere."
	 					}
	 				)
	 				player.warpTo(instance, entrypoint)
	 	
	 	# Now we can destroy the room itself.
	 	
	 	room.destroy()

	# Something in this realm has changed.
	
	def fireChangeNotification(self):
		for instance in self.instances:
			instance.fireChangeNotification()
			
	# Instance management
	
	def addInstance(self):
		instance = DBInstance()
		instance.create(self)

		self.instances |= {instance}
		return instance	
		