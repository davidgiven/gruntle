# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging

# This represents a structured markup tree that's going to be passed to the
# client for rendering.
#
# It has two main forms:
#
#   Markup('foo', 'bar', 'baz')
#
# ...creates a simple group.
#
#   Markup(type=u'player', name=u'Bob', uid=42)
#
# ...creates a more complex node with key/value pairs.
#
# The first form will allow its arguments to be strings (both unicode and
# UTF-8) or Markup objects. If the latter, it'll do some basic attempts
# to collapse the tree. The latter form doesn't do any of this. What you
# get is what you say. Remember that strings must be unicode!

class Markup(object):
	def __init__(self, *items, **keywords):
		assert not (items and keywords)
		if items:
			v = []
			for i in items:
				if (type(i) == unicode):
					v += [i]
				elif (type(i) == str):
					v += [unicode(i, "UTF-8")]
				elif (type(i) == dict):
					v += [i]
				elif (type(i) == Markup):
					v += [i.markup]
				else:
					raise TypeError()

				self.markup = {
					u"type": u"group",
					u"values": tuple(v)
				}
		else:
			assert keywords["type"]
			self.markup = {unicode(k): v for (k, v) in keywords.items()}

	def __add__(self, other):
		if (self.type() == u"group") and (other.type() == u"group"):
			return Markup(*(self.markup["values"] + other.markup["values"]))
		else:
			return Markup(type=u"group", values=(self.markup, other.markup))

	def __repr__(self):
		s = ["Markup(type="+self.type().__repr__()]
		for k in self.markup:
			if (k != "type"):
				v = self.markup[k]
				s += ", %s=%s" % (k.__repr__(), v.__repr__())
		s += "]"

		return "".join(s)

	def __eq__(self, other): return self.markup == other.markup
	def __ne__(self, other): return self.markup != other.markup
	def __lt__(self, other): raise TypeError()
	def __le__(self, other): raise TypeError()
	def __gt__(self, other): raise TypeError()
	def __ge__(self, other): raise TypeError()

	def type(self):
		return self.markup["type"]

