# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.DBObject import *
from ts.DBRealm import *
from ts.DBAction import *
from ts.ScriptRuntime import *

# Represents a room template.

class DBRoom(DBObject):
	def __init__(self, id=None):
		super(DBRoom, self).__init__(id)
		
	# Return the realm this room is in.
	
	@property
	def realm(self):
		(realm,) = db.sql.cursor().execute(
				"SELECT realm FROM rooms_in_realm WHERE room = ?",
				(self.id,)
			).next()
			
		# avoid circular dependency
		from ts.DBRealm import DBRealm
		return DBRealm(realm)
	
	def create(self, realm, name, title, script):
		super(DBRoom, self).create()
		(self.realm, self.name, self.title, self.script) = \
			realm, name, title, script
		self.immutable = 0
		
	# Return markup which describes the room.
	
	def markup(self):
		return {
			"type": "room",
			"name": self.name,
			"title": self.title,
			"oid": self.id
		}
		
	# Verifies that this object is owned by the specified player.
	
	def checkOwner(self, player):
		if (self.realm.owner != player):
			raise PermissionDenied

	# Something in this room has changed.
	
	def fireChangeNotification(self):
		realm = self.realm
		for instance in realm.instances:
			for player in instance.players:
				if (player.room == self):
					player.onLook()

	# Scripting interface.

	def property_markup(self):
		return Markup(
			type=u"room",
			title=self.title,
			name=self.name,
			id=self.id
		)

	def property_toString(self, rt):
		return self.title

	def property_tell(self, rt, markup):
		rt.instance.tell(self, rt.player,
			{
				"event": "activity",
				"markup": checkMarkup(markup).markup
			}
		)

	def property_broadcast(self, rt, markup):
		rt.instance.tell(self, None,
			{
				"event": "activity",
				"markup": checkMarkup(markup).markup
			}
		)

