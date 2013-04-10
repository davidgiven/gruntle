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
from ts.DBAction import *
        
linkToTable(DBPlayer, "players")
simpleSettersGetters(DBPlayer, ("name", "email", "password"))
simpleSettersGetters(DBPlayer, ("connected", "guest"))
objrefSettersGetters(DBPlayer, DBRoom, ("room",))
databaseSetSetter(DBPlayer, "realms", "realms_in_player", "player",
    "realm", DBRealm)

linkToTable(DBRealm, "realms")
simpleSettersGetters(DBRealm, ("name",))
databaseSetSetter(DBRealm, "rooms", "rooms_in_realm", "realm", "room", DBRoom)
databaseSetSetter(DBRealm, "instances", "instances", "realm", "id", DBInstance)

linkToTable(DBRoom, "rooms")
simpleSettersGetters(DBRoom, ("name", "title", "description", "immutable"))
databaseSetSetter(DBRoom, "actions", "actions_in_room", "room",
    "action", DBAction)

linkToTable(DBInstance, "instances")
objrefSettersGetters(DBInstance, DBRealm, ("realm",))
databaseSetSetter(DBInstance, "players", "players_in_instance", "instance",
    "player", DBPlayer) 

linkToTable(DBAction, "actions")
simpleSettersGetters(DBAction, ("description", "type", "target"))
