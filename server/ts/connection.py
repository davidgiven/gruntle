# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ws4py.websocket import WebSocket
import anyjson as json

import logging
import sys
import traceback

import ts.commands as commands
import ts.login_commands as login_commands
import ts.db as db
from ts.exceptions import *

class Connection(WebSocket):
	player = None

	# Changes the player currently associated with this connection.
	
	def setPlayer(self, player):
		self.player = player
	
	# A new connection has been opened.
		
	def opened(self):
		logging.info("connection %s opened", self)
		
	# The websocket has closed.
	
	def closed(self, code, reason=None):
		logging.info("connection %s closed", self)
		if self.player:
			self.player.onConnectionClosed()
		
	# A raw message has arrived on the websocket.
	
	def received_message(self, message):
		# The entire message processing code gets executed inside a
		# transaction: commands which throw an exception don't change the
		# database.
		
		try:
			oldplayer = self.player
			try:
				with db.sql:
					try:
						p = "(none)"
						if self.player:
							p = self.player.name
						logging.debug("%s< %s", p, message.data)
					
						packet = json.deserialize(message.data)
					except TypeError:
						self.onInvalidInput()
						return
			
					self.onRecvMsg(packet)
			except:
				# If an exception occurred while a player was logging in,
				# roll back the state of the connection so the player is no
				# longer logged in. (Required because self.player may not longer
				# be valid if, for example, the player was being created.)
				self.player = oldplayer
				raise
		except ServerUserError as e:
			logging.exception("user error: %s", e)
			self.sendMsg(
				{
					"event": "error",
					"message": "Error in realm (please contact the realm author):",
					"details": [unicode(e)]
				}
			)
		except Exception as e:
			logging.exception("server error: %s", e)
			(type, value, tb) = sys.exc_info()
			self.sendMsg(
				{
					"event": "error",
					"message": "Server error (please contact the server administrator):",
					"details": [e.__class__.__name__ + " " + unicode(e)] +
						traceback.format_tb(tb)
				}
			)

	# Sends a JSON reply to the client.
	
	def sendMsg(self, packet):
		j = json.serialize(packet)
		p = "(none)"
		if self.player:
			p = self.player.name
		logging.debug("%s> %s", p, j)
		self.send(j, False)

	# A processed message has arrived.
	
	def onRecvMsg(self, packet):
		commandmap = login_commands
		if self.player:
			commandmap = commands

		try:
			cmdmethodname = "cmd_" + packet["command"]
			cmdmethod = commandmap.__dict__[cmdmethodname]
		except (KeyError, AttributeError):
			print("unknown client command:",packet)
			self.onInvalidInput()
			return
		
		cmdmethod(self, packet)

	# Reports invalid input.
	
	def onInvalidInput(self):
		self.sendMsg(
			{
				"event": "malformed"
			}
		)

