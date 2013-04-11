# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging

from ts.DBPlayer import DBPlayer
from ts.DBRealm import DBRealm
from ts.DBInstance import *
from ts.exceptions import *
import ts.db as db

# Represents a guest.

class DBGuest(DBPlayer):
	def __init__(self, id=None):
		super(DBGuest, self).__init__(id)
		
	def create(self):
		super(DBGuest, self).create("Guest", "", "")
		self.name = "Guest " + str(self.id)
		self.guest = 1
				
	# The player has just logged in. Move the guest to the entrypoint of the
	# default instance.
	
	def onLogin(self):
		instance = getDefaultInstance()
		self.instance = instance
		realm = instance.realm
		room = realm.findRoom("entrypoint")
		
		self.room = room
		
		super(DBGuest, self).onLogin()
				
# Finds an unused guest object, or creates a new one.

def findGuest():
	# Find a guest player who is currently disconnected.

	try:
		(id,) = db.cursor.execute(
			"SELECT id FROM players WHERE guest=1 AND connected=0 LIMIT 1"
			).next()

		# Found one.

		logging.info("recycling old guest player %d", id)
		return DBGuest(id)
	except StopIteration:
		# No unused guest objects, so create one.
		
		logging.info("creating new guest player")
		g = DBGuest()
		g.create()
		instance = getDefaultInstance()
		g.instance = instance
		g.room = instance.realm.findRoom("entrypoint")
		return g
		
