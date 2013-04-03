# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging

from DBObject import DBObject
from DBRealm import DBRealm
from DBInstance import getDefaultInstance
import db

# Represents a play.

class DBPlayer(DBObject):
	def __init__(self, id=None):
		super(DBPlayer, self).__init__(id)
		
	def create(self, name, email, password):
		super(DBPlayer, self).create()

		# Account data.		
		(self.name, self.email, self.password) = name, email, password
		
		# Game data.
		self.realms = frozenset()                # realms the player owns
		self.instance = None                     # current instance the player is in
		self.room = None                         # current room id player is in
		
		# Add the player to the lookup index.
		db.set(("player", unicode(name.lower())), self)
		
	def addRealm(self, name):
		realm = DBRealm()
		realm.create(self, name)
		room = realm.addRoom("entrypoint", "Featureless void",
			"Unshaped nothingness stretches as far as you can see, " +
			"tempting you to start shaping it."
		)
		room.immutable = True

		self.realms = self.realms | {realm}		
		return realm
	
	# Return the player's current connection, or None if the player is
	# disconnected.
	
	@property
	def connection(self):
		try:
			return DBPlayer.connections[self.id]
		except KeyError:
			return None
		
	# Send a message to the player.
	
	def tell(self, message):
		if self.connection:
			self.connection.sendMsg(message)
			
	# The player has just logged in.
	
	def onLogin(self, newconnection):
		id = self.id
		loggedin = False
		connection = self.connection
				
		if connection:
			# The player was previously logged in on another connection.
			
			logging.info("connection %s superceded by connection %s",
				connection, newconnection)
			
			# Tidy up and close the old connection.
				
			if (connection in DBPlayer.connections):
				del DBPlayer.connections[connection]
			connection.setPlayer(None)
			connection.close()
		else:
			loggedin = True
			
		DBPlayer.connections[id] = newconnection
		DBPlayer.connections[newconnection] = self

		if loggedin:
			# Announce that the player has logged in.
					
			logging.info("player %s logged in", self.name)
			
			self.tell(
				{
					"event": "loggedin",
					"user": self.name,
					"uid": self.id
				}
			)
			
			self.onLook()
			self.onRealms()
				
	# The player has just logged out.
	
	def onLogout(self):
		id = self.id
		connection = self.connection
		
		if connection:
			del DBPlayer.connections[connection]
			del DBPlayer.connections[id]			
			logging.info("player %s logged out", self.name)
		
	# Announce the current room to the client.
	
	def onLook(self):
		instance = self.instance
		realm = instance.realm
		room = self.room
		
		editable = (realm.owner == self)
		
		msg = {
			"event": "look",
			"instance": instance.id,
			"realm":
				{
					"id": realm.id,
					"name": realm.name,
					"user": realm.owner.name,
					"uid": realm.owner.id
				},
			"room": room.id,
			"name": room.name,
			"title": room.title,
			"description": room.description,
			"contents": [], # contents,
			"actions": self.validActionsForRoom(),
			"editable": editable
		}

		if editable:
			msg["allactions"] = room.actions
						
		self.tell(msg)
		
	# Determine the actions that are currently valid for the player.
	
	def validActionsForRoom(self):
		room = self.room
		
		actions = {}
		for id, action in room.actions.iteritems():
			 actions[id] = {
			 	"description": action["description"],
				"type": action["type"],
				"target": action["target"]
			}
		 
		return actions
	
	# Announce what realms the player currently owns.
	
	def onRealms(self):
		realms = {}
		for realm in self.realms:
			rooms = {}
			for room in realm.rooms:
				rooms[room.id] = {
					"name": room.name,
					"title": room.title,
					"immutable": room.immutable
				}
				
			realms[realm.id] = {
			 		"name": realm.name,
			 		"rooms": rooms,
			 		"instances": [ i.id for i in realm.instances ]
			 	}
			 
		defaultinstance = getDefaultInstance()
		defaultrealm = defaultinstance.realm
			 
		self.tell(
			{
				"event": "realms",
				"specialrealms":
					{
						defaultrealm.id:
						{
							"name": defaultrealm.name,
							"instance": defaultinstance.id
						}
					},
				"realms": realms
			}
		)
		
def findPlayerFromConnection(connection):
	try:
		return DBPlayer.connections[connection]
	except KeyError:
		return None
		
DBPlayer.connections = {}
