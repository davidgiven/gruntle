# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import math
import signal
import re
import anyjson as json

from ts.exceptions import *
from ts.Markup import *
import ts.db as db

def checkNumber(x):
	if (type(x) is int) or (type(x) is float) or (type(x) is long):
		return x
	type_mismatch()

def checkString(x):
	if (type(x) is unicode):
		return x
	if (type(x) is str):
		return unicode(x, "UTF-8")
	type_mismatch()

def checkBoolean(x):
	if (type(x) != bool):
		type_mismatch()
	return x

def checkList(x):
	if (type(x) is tuple):
		return x
	if (type(x) is list):
		return tuple(x)
	type_mismatch()

def checkMarkup(x):
	if (isinstance(x, Markup)):
		return x
	type_mismatch()

def checkAction(x):
	if (isinstance(x, Action)):
		return x
	type_mismatch()

def type_mismatch():
	raise ScriptError("type mismatch")

def unknown_property(n):
	raise ScriptError("no such property/method '%s'" % (n,))

# This is a load of foul hackery. We have to fake our own methods on system
# types (int, float, bool, unicode, etc.) The following classes are
# bundles of methods for each type. When a run-time operation is performed
# on a value, the type of the left parameter is looked up and the appropriate
# class found.

class GenericMethods(object):
	def Eq(self, rt, x, y): return x == y
	def NotEq(self, rt, x, y): return x != y

	def Property(self, rt, x, name):
		try:
			m = getattr(self, "property_"+name)
			def f(rt, *args):
				return m(rt, x, *args)
			return f
		except AttributeError:
			pass

		try:
			m = getattr(x, "property_"+name)
			def f(rt, *args):
				return m(rt, *args)
			return f
		except AttributeError:
			unknown_property(name)

	def markup(self, rt, x):
		return self.property_markup(rt, x)

class NilMethods(GenericMethods):
	def property_markup(self, rt, x): return u"nil"
	def property_toString(self, rt, x): return self.markup(x)

class NumberMethods(GenericMethods):
	def Add(self, rt, x, y): return x + checkNumber(y)
	def Sub(self, rt, x, y): return x - checkNumber(y)
	def Mult(self, rt, x, y): return x * checkNumber(y)
	def Div(self, rt, x, y): return x / checkNumber(y)
	def Mod(self, rt, x, y): return x % checkNumber(y)

	def Neg(self, rt, x): return -x

	def Lt(self, rt, x, y): return x < checkNumber(y)
	def LtE(self, rt, x, y): return x <= checkNumber(y)
	def Gt(self, rt, x, y): return x > checkNumber(y)
	def GtE(self, rt, x, y): return x >= checkNumber(y)

	def property_markup(self, rt, x): return u"%g" % (x,)
	def property_toString(self, rt, x): return self.markup(x)
	def property_toInt(self, rt, x): return float(int(x))

class BooleanMethods(GenericMethods):
	def Not(self, rt, x): return not x

	def property_markup(self, rt, x): return u"true" if x else u"false"
	def property_toString(self, rt, x): return self.markup(x)

class StringMethods(GenericMethods):
	def Add(self, rt, x, y): return x + checkString(y)

	def Lt(self, rt, x, y): return x < checkString(y)
	def LtE(self, rt, x, y): return x <= checkString(y)
	def Gt(self, rt, x, y): return x > checkString(y)
	def GtE(self, rt, x, y): return x >= checkString(y)

	def property_markup(self, rt, x): return x
	def property_length(self, rt, x): return len(x)
	def property_toString(self, rt, x): return x

class ListMethods(GenericMethods):
	def Add(self, rt, x, y): return x + checkList(y)

	def Index(self, x, y):
		index = int(checkNumber(y))
		return x[index]

	def Eq(self, rt, x, y): return x is y
	def Ne(self, rt, x, y): return not (x is y)

	def property_length(self, rt, x): return len(x)

class MarkupMethods(GenericMethods):
	def Add(self, rt, x, y): return x + checkMarkup(y)

	def property_markup(self, rt, x): return x.markup

class ObjectMethods(GenericMethods):
	def property_markup(self, rt, x): return x.property_markup(rt)

method_table = {
    type(None): NilMethods(),
	float: NumberMethods(),
	int: NumberMethods(),
	long: NumberMethods(),
	bool: BooleanMethods(),
	unicode: StringMethods(),
	tuple: ListMethods(),
	list: ListMethods(),
	Markup: MarkupMethods(),
	"object": ObjectMethods(),
}

def makeAction(rt, markup, consequence):
	return Action(checkMarkup(markup).markup, checkString(consequence))

def findRoom(rt, name):
	return None

def findPlayer(rt, name):
	return None

class ScriptRuntime(object):
	def __init__(self, player, realm, instance, room):
		self.player = player
		self.realm = realm
		self.instance = instance
		self.room = room

	def SetGlobal(self, k, v):
		try:
			j = json.serialize(v)
		except ValueError:
			raise ScriptError("attempt to store value in a global which cannot be stored in a global")

		db.sql.cursor().execute("INSERT OR REPLACE INTO variables "
			"(name, realm, instance, data) VALUES (?, ?, ?, ?)",
			(k, self.realm.id, self.instance.id, j))

	def GetGlobal(self, k):
		c = db.sql.cursor().execute("SELECT data FROM variables WHERE "
			"name=? AND realm=? AND instance=?",
			(k, self.realm.id, self.instance.id))
		try:
			j = c.next()[0]
			return json.deserialize(j)
		except StopIteration:
			return None

	def CheckBoolean(self, x): return checkBoolean(x)

	def ForIterator(self, start, stop, step):
		if (step == 0):
			raise ScriptError("FOR loop cannot have a STEP of 0")

		if (step > 0):
			# Counting up

			i = start
			while True:
				yield i
				if (i >= stop):
					break
				i = i + step
		else:
			# Counting down

			i = start
			while True:
				yield i
				if (i <= stop):
					break
				i = i + step

	def MakeMarkup(self, *elements):
		m = [self.markup(x) for x in elements]
		return Markup(*m)

	# Any other method call gets routed through the lookup tables above.

	attrcache = {}
	def __getattr__(self, name):
		if (name in self.attrcache):
			return self.attrcache[name]

		def attr(x, *y):
			tx = type(x)
			try:
				mt = method_table[tx]
			except KeyError:
				mt = method_table["object"]

			return getattr(mt, name)(self, x, *y)

		self.attrcache[name] = attr
		return attr

def signalHandler(signum, frame):
	raise ScriptError("CPU quota expired")

def executeScript(rt, module, name, *args):
	signal.signal(signal.SIGALRM, signalHandler)

	module["var_player"] = rt.player
	module["var_room"] = rt.room

	signal.setitimer(signal.ITIMER_REAL, 0.5)
	try:
		result = module["var_"+name](rt)
	except NameError, e:
		r = re.compile(ur"'var_(\w+)' is not defined", re.U)
		m = re.search(r, unicode(str(e), "UTF-8"))
		if not m:
			logging.exception(e)
			raise e
		raise ScriptError(u"variable '%s' is not defined", m.group(1))
	except TypeError, e:
		r = re.compile(ur"var_(\w+)\(\) takes exactly (\d+) argument \((\d+) given\)", re.U)
		m = re.search(r, unicode(str(e), "UTF-8"))
		if not m:
			logging.exception(e)
			raise e
		raise ScriptError(u"subroutine '%s' called with %d argument(s) when it wants %d",
			m.group(1), int(m.group(3))-1, int(m.group(2))-1)
	finally:
		signal.alarm(0)

	return result
