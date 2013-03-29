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

import cPickle as pickle

import commands
import login_commands

class Connection(WebSocket):
	player = None

	def __getstate__(self):
		raise pickle.PicklingError()
		
	def received_message(self, message):
		try:
			packet = json.deserialize(message.data)
		except TypeError:
			self.onInvalidInput()
			return

		self.onRecvMsg(packet)

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

	def onInvalidInput(self):
		self.sendMsg(
			{
				"event": "malformed"
			}
		)

	def sendMsg(self, packet):
		print("> ", packet)
		self.send(json.serialize(packet), False)

	def setPlayer(self, player):
		self.player = player
		print("successfully logged in ", player.name)
		