# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging
import hashlib

import ts.db as db
from ts.DBGuest import *

# Functions of the form cmd_FNORD are executed when a *non-authenticated*
# player tries to execute command 'FNORD'.

# Player is connecting.

def cmd_connect(connection, message):
	try:
		username = message["username"]
		password = message["password"]
	except KeyError:
		connection.onInvalidInput()
		return

	# Look to see wheth the player is logged in.
		
	r = db.sql.cursor().execute(
		"SELECT id FROM players WHERE name=? AND password=?",
		(username, hashlib.sha256(password).hexdigest())
	)
	if not r:
		connection.sendMsg(
			{
				"event": "authfailed"
			}
		)
		return

	(id,) = r.next()
	player = DBPlayer(id)

	connection.setPlayer(player)
	player.onConnectionOpened(connection)

# Someone is logging in as a guest.

def cmd_guest(connection, message):
	player = findGuest()
	connection.setPlayer(player)
	player.onConnectionOpened(connection)
	
# Someone is trying to create a new player. 

def cmd_createplayer(connection, message):
	try:
		username = message["username"]
		password = message["password"]
		email = message["email"]
	except KeyError:
		connection.onInvalidInput()
		return

	# Is there someone else with this username?
	
	(exists,) = db.sql.cursor().execute(
			"SELECT EXISTS (SELECT * FROM players WHERE name=?)",
			(username,)
		).next()
	if exists:
		connection.sendMsg(
			{
				"event": "creationfailed",
				"reason": "That username is already taken."
			}
		)
		return
	
	# Create the player and log it in.
	
	player = DBPlayer()
	player.create(username, email, hashlib.sha256(password).hexdigest())

	instance = getDefaultInstance()
	realm = instance.realm
	room = realm.findRoom("entrypoint")
	
	player.instance = instance
	player.room = room

	connection.setPlayer(player)
	player.onConnectionOpened(connection)
	