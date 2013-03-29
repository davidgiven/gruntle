# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from DBObject import DBObject
from DBRealm import DBRealm
import db

# Represents a play.

class DBPlayer(DBObject):
	def __init__(self, oid=None):
		super(DBPlayer, self).__init__(oid)
		self.__dict__["connection"] = None
		
	def create(self, name, email, password):
		super(DBPlayer, self).create()

		# Account data.		
		(self.name, self.email, self.password) = name, email, password
		
		# Game data.
		self.realms = frozenset()                # realms the player owns
		self.instance = None                     # current instance the player is in
		self.room = None                         # current room oid player is in
		
		# Add the player to the lookup index.
		db.set(("player", unicode(name.lower())), self)
		
	def addRealm(self, name):
		realm = DBRealm()
		realm.create(self, name)
		realm.addRoom("entrypoint", "Featureless void",
			"Unshaped nothingness stretches as far as you can see, " +
			"tempting you to start shaping it."
		)

		self.realms = self.realms | {realm}		
		return realm
	
	# Return the player's current connection, or None if the player is
	# disconnected.
	
	def connection():
		return self.__dict__["connection"]
		
	# The player has just logged in.
	
	def onLogIn(self, connection):
		self.__dict__["connection"] = connection
		
	# The player has just logged out.
	
	def onLogOut(self):
		self.__dict__["connection"] = connection
		