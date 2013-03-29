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

# Represents a play.

class DBPlayer(DBObject):
	def __init__(self, oid=None):
		super(DBPlayer, self).__init__("player", oid)
		
	def create(self, name, email, password):
		super(DBPlayer, self).create()
		self.set("name", name)                   # player's username
		self.set("email", email)                 # player's email
		self.set("password", password)           # player's password
		self.set("realms", frozenset())          # realms the player owns
		self.set("instance", None)               # current instance the player is in
		self.set("room", None)                   # current room oid player is in
		
	def getRealms(self):
		realms = self.get("realms")
		return [DBRealm(r) for r in realms]
		
	def addRealm(self, name):
		realm = DBRealm()
		realm.create(self, name)
		realm.addRoom("entrypoint", "Featureless void",
			"Unshaped nothingness stretches as far as you can see, " +
			"tempting you to start shaping it."
		)
		
		s = self.get("realms") | {realm.oid}
		self.set("realms", s)
		return realm
		
	def getInstance(self):
		return DBInstance(self.get("instance"))
		
	def getRoom(self):
		return DBRoom(self.get("room"))
		
	def setLocation(self, instance, room):
		self.set("instance", instance.oid)
		self.set("room", room.oid)
		