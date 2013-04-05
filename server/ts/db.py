# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging
import dbhash as dbm
import cPickle as pickle

__database = None

def __makekey(k):
	return str(k)
	
def open(filename):
	logging.info("using "+filename+" as database")
	global __database
	__database = dbm.open(filename, "c")
	
def get(k):
	mk = __makekey(k)
	return pickle.loads(__database[mk])

def set(k, v):
	mk = __makekey(k)
	__database[mk] = pickle.dumps(v)

def isset(k):
	mk = __makekey(k)
	return mk in __database

# Allocates a new unused object ID.

def createObject():
	nextobj = get(("root", "nextobj"))
	
	# Ensure that this object really does not exist.
	
	while isset(("object", nextobj)):
		nextobj = nextobj + 1
		
	set(("root", "nextobj"), nextobj+1)
	return nextobj
		