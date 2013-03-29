# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ws4py.client.threadedclient import WebSocketClient
import anyjson as json

socket = WebSocketClient("ws://localhost:8086")
print("connecting")
socket.connect()

def sendMsg(msg):
	j = json.serialize(msg)
	socket.send(j)

def recvMsg():
	j = socket.receive()
	return json.deserialize(j)

print("authenticating")
sendMsg(
	{
		"command": "connect",
		"username": "thoth",
		"password": "testpassword"
	}
)

