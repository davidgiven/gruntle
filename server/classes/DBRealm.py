# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from DBObject import DBObject
from DBRoom import DBRoom
from DBInstance import DBInstance

# Base class for a realm.

class DBRealm(DBObject):
	def __init__(self, oid=None):
		super(DBRealm, self).__init__("realm", oid)
		
	def create(self, owner, name):
		super(DBRealm, self).create()
		self.set("name", name)
		self.set("owner", owner.oid)
		self.set("rooms", frozenset())
		self.set("instances", frozenset())
		
	# Room management
	
	def getRooms(self):
		s = self.get("rooms")
		return [DBRoom(r) for r in s]
		
	def addRoom(self, name, title, description):
		room = DBRoom()
		room.create(self, name, title, description)
		
		s = self.get("rooms") | {room.oid}
		self.set("rooms", s)

	def findRoom(self, name):
		for r in self.getRooms():
			if (r.getName() == name):
				return r
		return None
		
	# Instance management
	
	def getInstances(self):
		s = self.get("instances")
		return [DBInstance(i) for i in instances]
		
	def addInstance(self):
		instance = DBInstance()
		instance.create(self)
		
		s = self.get("instances") | {instance.oid}
		self.set("instances", s)
		return instance
		