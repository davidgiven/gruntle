# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.DBObject import *	
from ts.DBPlayer import *
from ts.DBGuest import *
from ts.DBRealm import *
from ts.DBRoom import *
from ts.DBInstance import *

linkToTable(DBPlayer, "players")
simpleSettersGetters(DBPlayer, ("name", "email", "password"))
simpleSettersGetters(DBPlayer, ("connected", "guest"))
objrefSettersGetters(DBPlayer, DBRoom, ("room",))
objrefSettersGetters(DBPlayer, DBInstance, ("instance",))

linkToTable(DBRealm, "realms")
simpleSettersGetters(DBRealm, ("name",))
objrefSettersGetters(DBRealm, DBPlayer, ("owner",))

linkToTable(DBRoom, "rooms")
simpleSettersGetters(DBRoom, ("name", "title", "script", "immutable"))
objrefSettersGetters(DBRoom, DBRealm, ("realm",))

linkToTable(DBInstance, "instances")
objrefSettersGetters(DBInstance, DBRealm, ("realm",))

