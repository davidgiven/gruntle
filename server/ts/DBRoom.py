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
from ts.DBAction import *

# Represents a room template.

class DBRoom(DBObject):
	def __init__(self, id=None):
		super(DBRoom, self).__init__(id)
		
	# Return the realm this room is in.
	
	@property
	def realm(self):
		(realm,) = db.sql.cursor().execute(
				"SELECT realm FROM rooms_in_realm WHERE room = ?",
				(self.id,)
			).next()
			
		# avoid circular dependency
		from ts.DBRealm import DBRealm
		return DBRealm(realm)
	
	def create(self, name, title, description):
		super(DBRoom, self).create()
		(self.name, self.title, self.description) = \
			name, title, description
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
		
	# Verifies that this object is owned by the specified player.
	
	def checkOwner(self, player):
		if (self.realm.owner != player):
			raise PermissionDenied

	# Something in this room has changed.
	
	def fireChangeNotification(self):
		realm = self.realm
		for instance in realm.instances:
			for player in instance.players:
				if (player.room == self):
					player.onLook()

	# Extract the list of actions for this room and return it as a client-
	# manipulatable list.

	def getActions(self):	
		actions = {}
		for action in self.actions:
			 actions[action.id] = {
			 	"description": action.description,
				"type": action.type,
				"target": action.target
			}
		 
		return actions

	# Replace all actions on this room with the list supplied.
	
	def setActions(self, actions):
		processed = {}
		for action in self.actions:
			processed[action.id] = action
		
		for id, action in actions.iteritems():
			description = action["description"]
			type = action["type"]
			target = action["target"]
			
			newaction = None
			if id in processed:
				# We are updating an old action.
				
				newaction = processed[id]
				del processed[id]
				
				newaction.description = description
				newaction.type = type
				newaction.target = target
			else:
				# We are creating a new action.
				
				newaction = DBAction()
				newaction.create(description, type, target)
				self.actions |= {newaction}
			
		# Any left-over actions are being deleted.
		
		for id in processed:
			del self.actions[id]
	
	# Finds an action for this room.
	
	def findAction(self, actionid):
		# Verify that this action actually exists for this room.
		
		(exists,) = db.cursor.execute(
				"SELECT EXISTS (SELECT * FROM actions_in_room WHERE action=? AND room=?)",
				(actionid, self.id)
			).next()
		if (exists == 0):
			return None
		
		# Now we can return the action object itself.
		
		return DBAction(actionid)
	