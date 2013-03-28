from gevent import monkey; monkey.patch_all()
import gevent

from ws4py.server.geventserver import WebSocketServer
from ws4py.websocket import EchoWebSocket

import argparse

# Internal modules

import db
from connection import Connection

parser = argparse.ArgumentParser(
	description = "thickishstring prototype Python server"
)

parser.add_argument(
	'--db', '-d',
	default = 'test.db',
	dest = 'filename',
	help = 'specifies the database file to use'
)
parser.add_argument(
	'--port', '-p',
	default = 8086,
	dest = 'port',
	help = 'which port to listen on'
)

args = parser.parse_args()

# Open and initialise the database.

db.open(args.filename)
if not db.isset("root"):
	db.set("root", True)

# Create and start the server.

server = WebSocketServer(
	('0.0.0.0', args.port),
	websocket_class=Connection
)
server.serve_forever()

