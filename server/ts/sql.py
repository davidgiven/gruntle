# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging
import sqlite3 as sql

db = None

def open(filename):
	logging.info("using "+filename+" as database")
	global db
	db = sql.connect(filename)
	
