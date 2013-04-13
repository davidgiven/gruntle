# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.DBInstance import *
from ts.DBRoom import *
from ts.DBRealm import *
from ts.exceptions import InvalidObjectReference

# Functions of the form cmd_FNORD are executed when an *authenticated*
# player tries to execute command 'FNORD'.

def cmd_action(connection, message):
	try:
		actionid = int(message["actionid"])
	except KeyError:
		connection.onInvalidInput()
		return
		
	connection.player.onAction(actionid)
	
# The player has asked to be warped to another room and instance.

def cmd_warp(connection, message):
	try:
		instance = DBInstance(int(message["instance"]))
		if ("room" in message):
			room = DBRoom(int(message["room"]))
		else:
			room = "entrypoint"
	except (KeyError, InvalidObjectReference):
		connection.onInvalidInput()
		return
			
	connection.player.onWarp(instance, room)
	
# The player is saying something.

def cmd_say(connection, message):
	try:
		text = unicode(message["text"])
	except KeyError:
		connection.onInvalidInput()
		return
			
	connection.player.onSay(text)
		
# The player wants to create a room.

def cmd_createroom(connection, message):
	try:
		instance = DBInstance(int(message["instance"]))
		name = unicode(message["name"])
		title = unicode(message["title"])
	except (KeyError, InvalidObjectReference):
		connection.onInvalidInput()
		return

	instance.checkOwner(connection.player)			
	connection.player.onCreateRoom(instance, name, title)
		
# The player wants to delete a room.

def cmd_delroom(connection, message):
	try:
		room = DBRoom(int(message["room"]))
	except (KeyError, InvalidObjectReference):
		connection.onInvalidInput()
		return

	room.checkOwner(connection.player)			
	connection.player.onDestroyRoom(room)

# The player wants to create a realm.

def cmd_createrealm(connection, message):
	try:
		name = unicode(message["name"])
	except KeyError:
		connection.onInvalidInput()
		return

	connection.player.onCreateRealm(name)
		
# The player wants to rename a realm.

def cmd_renamerealm(connection, message):
	try:
		realm = DBRealm(int(message["realmid"]))
		newname = unicode(message["newname"])
	except (KeyError, InvalidObjectReference):
		connection.onInvalidInput()
		return

	realm.checkOwner(connection.player)			
	connection.player.onRenameRealm(realm, newname)
	
# The player wants to edit a room.

def cmd_editroom(connection, message):
	try:
		room = DBRoom(int(message["room"]))
		name = unicode(message["name"])
		title = unicode(message["title"])
		description = unicode(message["description"])
		actions = {}
		
		# Sanity check the list of actions.
		
		for k, v in message["actions"].iteritems():
			actions[int(k)] = {
				"type": unicode(v["type"]),
				"description": unicode(v["description"]),
				"target": unicode(v["target"])
			}	
	except (KeyError, InvalidObjectReference):
		connection.onInvalidInput()
		return

	room.checkOwner(connection.player)			
	connection.player.onEditRoom(room, name, title, description, actions)
