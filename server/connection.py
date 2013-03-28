from ws4py.websocket import WebSocket
import anyjson as json

import commands
import login_commands

class Connection(WebSocket):
	player = None

	def received_message(self, message):
		try:
			packet = json.deserialize(message.data)
		except TypeError:
			self.on_invalid_input()
			return

		self.on_recv_packet(packet)

	def on_recv_packet(self, packet):
		commandmap = login_commands
		if self.player:
			commandmap = commands

		try:
			cmdmethodname = "cmd_" + packet.command
			cmdmethod = commandmap.__dict__[cmdmethodname]
		except (KeyError, AttributeError):
			print("unknown client command:",packet)
			self.on_invalid_input()
			return

		cmdmethod(self, packet)

	def on_invalid_input(self):
		self.send_packet(
			{
				"event": "malformed"
			}
		)

	def send_packet(self, packet):
		self.send(json.serialize(packet), False)

