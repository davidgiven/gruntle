# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import hashlib

from ts.DBInstance import *
from ts.DBRoom import *
from ts.DBRealm import *
from ts.exceptions import *
import ts.scriptcompiler as scriptcompiler

def tounicode(s):
	if (type(s) == unicode):
		return s
	return unicode(s, "UTF-8")

# Functions of the form cmd_FNORD are executed when an *authenticated*
# player tries to execute command 'FNORD'.

# The player wants to change their password.

def cmd_changepassword(connection, message):
	try:
		oldpassword = tounicode(message["oldpassword"])
		newpassword = tounicode(message["newpassword"])
	except KeyError:
		connection.onInvalidInput()
		return

	oldhash = hashlib.sha256(oldpassword).hexdigest()
	newhash = hashlib.sha256(newpassword).hexdigest()

	connection.player.onChangePassword(oldhash, newhash)

# The player wants to perform an action on the current room.

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
		text = tounicode(message["text"])
	except KeyError:
		connection.onInvalidInput()
		return
			
	connection.player.onSay(text)
		
# The player wants to create a room.

def cmd_createroom(connection, message):
	try:
		instance = DBInstance(int(message["instance"]))
		name = tounicode(message["name"])
		title = tounicode(message["title"])
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
		name = tounicode(message["name"])
	except KeyError:
		connection.onInvalidInput()
		return

	connection.player.onCreateRealm(name)
		
# The player wants to rename a realm.

def cmd_renamerealm(connection, message):
	try:
		realm = DBRealm(int(message["realmid"]))
		newname = tounicode(message["newname"])
	except (KeyError, InvalidObjectReference):
		connection.onInvalidInput()
		return

	realm.checkOwner(connection.player)			
	connection.player.onRenameRealm(realm, newname)

# The player wants information on a particular room.

def cmd_getroomdata(connection, message):
	try:
		room = DBRoom(int(message["room"]))
	except (KeyError, InvalidObjectReference):
		connection.onInvalidInput()
		return

	room.checkOwner(connection.player)
	connection.player.onGetRoomData(room)

# The player wants to change a room.

def cmd_setroomdata(connection, message):
	try:
		room = DBRoom(int(message["room"]))
		name = tounicode(message["name"])
		title = tounicode(message["title"])
		script = tounicode(message["script"])
	except (KeyError, InvalidObjectReference):
		connection.onInvalidInput()
		return

	room.checkOwner(connection.player)
	connection.player.onSetRoomData(room, name, title, script)

# Syntax check a script.

def cmd_syntaxcheck(connection, message):
	try:
		script = tounicode(message["script"])
	except (KeyError):
		connection.onInvalidInput()
		return

	errorlog = []
	try:
		scriptcompiler.compile(script)
	except ScriptCompilationError, e:
		errorlog = e.errorlog

	connection.player.tell(
		{
			"event": "scriptcompilationfailure",
			"id": None,
			"errorlog": errorlog
		}
	)
