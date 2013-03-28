from ws4py.websocket import WebSocket
import anyjson as json

class Connection(WebSocket):
	def received_message(self, message):
		try:
			packet = json.deserialize(message.data)
		except TypeError:
			print("invalid input from client")
			self.close_connection()
			return

		self.on_recv_packet(packet)

	def on_recv_packet(self, packet):
		print(packet)

	def send_packet(self, packet):
		self.send(json.serialize(packet), False)

