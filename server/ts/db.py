# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging
import apsw

sql = None
cursor = None

def connect(filename, initscript):
	logging.info("using "+filename+" as database")
	global sql
	global cursor
	sql = apsw.Connection(filename, statementcachesize=1000)
	cursor = sql.cursor()
	(count,) = cursor.execute(
			"SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='variables'"
		).next()
	return (count != 0)
	
def getvar(name):
	(value,) = cursor.execute(
			"SELECT value FROM variables WHERE key = ?",
			(name,)
		).next()
	return value

def setvar(name, value):
	cursor.execute(
			"INSERT OR REPLACE INTO variables VALUES (?, ?)",
			(name, value)
		)
