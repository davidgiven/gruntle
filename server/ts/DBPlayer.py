# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging

from ts.DBObject import *
from ts.DBRealm import DBRealm
from ts.DBInstance import *
from ts.DBRoom import DBRoom
from ts.exceptions import *
import ts.db as db

# Represents a player.

class DBPlayer(DBObject):
	connections = {}
	
	# Return the relmas owned by this player.
	
	@property
	def realms(self):
		return [ DBRealm(id) for (id,) in
			db.sql.cursor().execute(
				"SELECT id FROM realms WHERE owner=?",
				(self.id,)
			)
		]
	
	def __init__(self, id=None):
		super(DBPlayer, self).__init__(id)
			
	def create(self, name, email, password):
		super(DBPlayer, self).create()

		# Account data.		
		(self.name, self.email, self.password) = name, email, password
		
		# Game data.
		self.guest = 0
		self.connected = 0
		
	def addRealm(self, name):
		realm = DBRealm()
		realm.create(name, self)
		room = realm.addRoom("entrypoint", "Featureless Void",
			"Unshaped nothingness stretches as far as you can see, "
			"tempting you to start shaping it."
		)
		room.immutable = True

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
		
		newinstance.tell(newroom, self,
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
		
		self.instance = instance
		newinstance.players |= {self}
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
		self.connected = 1
		
		self.tell(
			{
				"event": "loggedin",
				"user": self.name,
				"uid": self.id
			}
		)
		
		self.instance.tell(self.room, self,
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
		self.connected = 0
		
		self.instance.tell(self.room, self,
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
		
		players = [ DBPlayer(id) for (id,) in
			db.cursor.execute(
				"SELECT id FROM players "
					"WHERE "
						"(instance = ?) AND "
						"(room = ?) AND "
						"(connected = 1)",
				(instance.id, room.id)
			) ]
	
		contents = {} 
		for player in players:
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
			msg["allactions"] = room.getActions()
						
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
			 
		from ts.DBInstance import getDefaultInstance
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
		for action in room.actions:
			 actions[action.id] = {
			 	"description": action.description,
				"type": action.type,
				"target": action.target
			}
		 
		return actions
	
	# Execute a player action.
	
	def onAction(self, actionid):
		room = self.room
		
		try:
			action = room.findAction(int(actionid))
			type = action.type
			target = action.target
		except KeyError:
			self.connection.onMalformed()
			return
			
		if (type == "room"):
			targetroom = self.instance.realm.findRoom(target)
			self.moveTo(targetroom)
		elif (type == "message"):
			self.tell(
				{
					"event": "activity",
					"message": target 
				}
			)
		else:
			pass

	# The player has asked to warp to a new room.
	
	def onWarp(self, instance, room):
		realm = instance.realm
		if isinstance(room, basestring):
			room = realm.findRoom(room)
			if not room:
				raise AppError("room '%s' does not exist", roomname)
		
		# If the player doesn't own the realm, only allow warping to the
		# entrypoint.
		
		if (realm.owner != self) and (roomname != "entrypoint"):
			raise AppError("permission denied")
		
		self.warpTo(instance, room)
		self.onRealms()
		
	# The player has asked to say something.
	
	def onSay(self, text):
		self.instance.tell(self.room, None,
			{
				"event": "speech",
				"user": self.name,
				"uid": self.id,
				"text": text
			}
		)
	
	# The player wants to create a room.

	def onCreateRoom(self, instance, name, title):
		realm = instance.realm
		room = realm.addRoom(name, title,
			"Unshaped nothingness stretches as far as you can see, " +
			"tempting you to start shaping it."
		)
		room.immutable = False
		
		self.onWarp(instance, room)
		self.onRealms()
	 
	# The player wants to destroy a room.
	 
	def onDestroyRoom(self, room):
		realm = room.realm
	 	
		# Don't allow destroying immutable rooms (i.e., the entrypoint).
		
		if room.immutable:
			raise PermissionDenied()
		
		realm.destroyRoom(room)
		self.onRealms()
	
	# The player wants to edit a room.
	
	def onEditRoom(self, room, name, title, description, actions):
		room.name = name
		room.title = title
		room.description = description
		room.setActions(actions)
		room.fireChangeNotification()
		self.onRealms()
		
	# The player wants to create a realm.
	
	def onCreateRealm(self, name):
		realm = self.addRealm(name)
		instance = realm.addInstance()
		self.warpTo(instance, realm.findRoom("entrypoint"))
		self.onRealms()
		
	# The player wants to rename a realm.
	
	def onRenameRealm(self, realm, newname):
		realm.name = newname
		realm.fireChangeNotification()
		self.onRealms()
		
	 	
def findPlayerFromConnection(connection):
	try:
		return DBPlayer.connections[connection]
	except KeyError:
		return None
