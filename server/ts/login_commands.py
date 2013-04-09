# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging

import ts.db as db
from ts.DBGuest import *

# Functions of the form cmd_FNORD are executed when a *non-authenticated*
# player tries to execute command 'FNORD'.

def cmd_connect(connection, message):
	try:
		username = message["username"]
		password = message["password"]
	except KeyError:
		connection.onInvalidInput()
		return
	
	r = db.sql.cursor().execute(
		"SELECT id FROM players WHERE name=? AND password=?",
		(username, password)
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
	

