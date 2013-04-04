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

		# Add the guest to the lookup index.
		
		guests = db.get(("root", "guests")) | {self}
		db.set(("root", "guests"), guests)
				
	# The player has just logged in. Move the guest to the entrypoint of the
	# default instance.
	
	def onLogin(self):
		instance = getDefaultInstance()
		realm = instance.realm
		room = realm.findRoom("entrypoint")
		
		self.instance = instance
		self.room = room
		
		super(DBGuest, self).onLogin()
				
# Finds an unused guest object, or creates a new one.

def findGuest():
	guests = db.get(("root", "guests"))
	for g in guests:
		if not g.connection:
			return g
		
	# No unused guest objects, so create one.
	
	g = DBGuest()
	g.create()
	return g
