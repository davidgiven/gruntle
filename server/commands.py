# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

# Functions of the form cmd_FNORD are executed when an *authenticated*
# player tries to execute command 'FNORD'.

def cmd_action(connection, message):
	try:
		actionid = message["actionid"]
	except KeyError:
		connection.onMalformed()
		return
		
	connection.player.onAction(actionid)
	