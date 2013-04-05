# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging

from ts.DBObject import DBObject
from ts.DBRealm import DBRealm
from ts.DBInstance import getDefaultInstance
from ts.exceptions import *
import ts.db as db

# Represents a player.

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
	
	# Return markup which describes the player.
	
	def markup(self):
		return {
			"type": "player",
			"name": self.name,
			"oid": self.id
		}
		
	# Moves the player from the current room to another one in the same
	# instance.
	
	def moveTo(self, newroom):
		instance = self.instance
		realm = instance.realm
		room = self.room

		if (room == newroom):
			# If not going anywhere, do nothing.
			return
		
		instance.tell(room, self,
			{
				"event": "departed",
				"user": self.name,
				"uid": self.id,
				"markup":
				[
					self.markup(),
					" leaves for ",
					newroom.markup(),
					"."
				]
			}
		);
		
		instance.tell(newroom, self,
			{
				"event": "arrived",
				"user": self.name,
				"uid": self.id,
				"markup":
				[
					self.markup(),
					" arrives from ",
					room.markup(),
					"."
				]
			}
		);
		
		self.room = newroom
		
		self.tell(
			{
				"event": "moved"
			}
		)
		
		self.onLook()
		
	# Moves the player from the current room to another one in a different
	# instance.
	
	def warpTo(self, newinstance, newroom):
		instance = self.instance
		realm = instance.realm
		newrealm = newinstance.realm
		room = self.room

		if (instance == newinstance) and (room == newroom):
			# If not going anywhere, do nothing.
			return
		
		instance.tell(room, self,
			{
				"event": "departed",
				"user": self.name,
				"uid": self.id,
				"markup":
				[
					self.markup(),
					" warps out."
				]
			}
		);
		
		instance.tell(newroom, self,
			{
				"event": "arrived",
				"user": self.name,
				"uid": self.id,
				"markup":
				[
					self.markup(),
					" warps in."
				]
			}
		);
		
		instance.players = instance.players - {self}
		newinstance.players = newinstance.players | {self}
		self.room = newroom
		
		self.tell(
			{
				"event": "moved"
			}
		)
		
		self.onLook()
		
	# A connection has just opened to this player. (This does not necessarily
	# mean that the player has logged in; they might be reconnecting.)
	
	def onConnectionOpened(self, newconnection):
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
			self.onLogin()
			
	# The player has just logged out.
	
	def onConnectionClosed(self):
		id = self.id
		connection = self.connection
		
		if connection:
			del DBPlayer.connections[connection]
			del DBPlayer.connections[id]
			self.onLogout()			
		
	# The player has just logged in.
	
	def onLogin(self):
		# Announce that the player has logged in.
				
		logging.info("player %s logged in", self.name)
		
		self.tell(
			{
				"event": "loggedin",
				"user": self.name,
				"uid": self.id
			}
		)
		
		instance = self.instance
		instance.players = instance.players | {self}
		
		instance.tell(self.room, self,
			{
				"event": "arrived",
				"markup":
				[
					self.markup(),
					" has connected."
				]
			}
		)

		self.onLook()
		self.onRealms()

	# The player has just logged out.
	
	def onLogout(self):
		logging.info("player %s logged out", self.name)
		
		instance = self.instance
		instance.players = instance.players - {self}
		
		instance.tell(self.room, self,
			{
				"event": "departed",
				"markup":
				[
					self.markup(),
					" has disconnected."
				]
			}
		)
							
	# Announce the current room to the client.
	
	def onLook(self):
		instance = self.instance
		realm = instance.realm
		room = self.room
		
		contents = {}
		for player in instance.players:
			if (player.room == room) and (player != self):
				contents[player.name] = player.id
				
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
			"contents": contents,
			"actions": self.validActionsForRoom(),
			"editable": editable
		}

		if editable:
			msg["allactions"] = room.actions
						
		self.tell(msg)
		
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
	
	# Execute a player action.
	
	def onAction(self, actionid):
		room = self.room
		
		try:
			action = room.actions[int(actionid)]
			type = action["type"]
			target = action["target"]
		except KeyError:
			self.connection.onMalformed()
			return
			
		if (type == "room"):
			targetroom = self.instance.realm.findRoom(target)
			self.moveTo(targetroom)
		elif (type == "message"):
			self.tell(
				{
					"command": "activity",
					"message": target 
				}
			)
		else:
			pass

	# The player has asked to warp to a new room.
	
	def onWarp(self, instance, roomname):
		realm = instance.realm
		room = realm.findRoom(roomname)
		if not room:
			raise AppError("room '%s' does not exist", roomname)
		
		# If the player doesn't own the realm, only allow warping to the
		# entrypoint.
		
		if (realm.owner != self) and (roomname != "entrypoint"):
			raise AppError("permission denied")
		
		self.warpTo(instance, room)
		
def findPlayerFromConnection(connection):
	try:
		return DBPlayer.connections[connection]
	except KeyError:
		return None
		
DBPlayer.connections = {}
