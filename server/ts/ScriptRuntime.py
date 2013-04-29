# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.exceptions import *
from ts.Markup import Markup
import math

def t_number(x):
	if (type(x) is int) or (type(x) is float) or (type(x) is long):
		return x
	type_mismatch()

def t_string(x):
	if (type(x) is unicode):
		return x
	if (type(x) is str):
		return unicode(x, "UTF-8")
	type_mismatch()

def t_boolean(x):
	if (type(x) != bool):
		type_mismatch()
	return x

def t_list(x):
	if (type(x) is tuple):
		return x
	if (type(x) is list):
		return tuple(x)
	type_mismatch()

def t_markup(x):
	if (type(x) is Markup):
		return x
	type_mismatch()

def type_mismatch():
	raise ScriptError("type mismatch")

def unknown_property(n):
	raise ScriptError("no such property '%s'" % (n,))

# This is a load of foul hackery. We have to fake our own methods on system
# types (int, float, bool, unicode, etc.) The following classes are
# bundles of methods for each type. When a run-time operation is performed
# on a value, the type of the left parameter is looked up and the appropriate
# class found.

class GenericMethods(object):
	def Eq(self, x, y): return x == y
	def NotEq(self, x, y): return x != y

	def Property(self, x, name):
		m = getattr(self, "property_"+name)
		if not m:
			unknown_property(name)
		def f(rt, *args):
			return m(rt, x, *args)
		return f

	def property_markup(self, rt, x): return self.Markup(x)

class NumberMethods(GenericMethods):
	def Add(self, x, y): return x + t_number(y)
	def Sub(self, x, y): return x - t_number(y)
	def Mult(self, x, y): return x * t_number(y)
	def Div(self, x, y): return x / t_number(y)
	def Mod(self, x, y): return x % t_number(y)

	def Neg(self, x): return -x

	def Lt(self, x, y): return x < t_number(y)
	def LtE(self, x, y): return x <= t_number(y)
	def Gt(self, x, y): return x > t_number(y)
	def GtE(self, x, y): return x >= t_number(y)

	def Markup(self, x): return u"%g" % (x,)

	def property_toString(self, rt, x): return self.Markup(x)
	def property_toInt(self, rt, x): return float(int(x))

class BooleanMethods(GenericMethods):
	def Not(self, x): return not x

	def Markup(self, x): return u"true" if x else u"false"

	def property_toString(self, rt, x): return self.Markup(x)

class StringMethods(GenericMethods):
	def Add(self, x, y): return x + t_string(y)

	def Lt(self, x, y): return x < t_string(y)
	def LtE(self, x, y): return x <= t_string(y)
	def Gt(self, x, y): return x > t_string(y)
	def GtE(self, x, y): return x >= t_string(y)

	def Markup(self, x): return x

	def property_length(self, rt, x): return len(x)
	def property_toString(self, rt, x): return x

class ListMethods(GenericMethods):
	def Add(self, x, y): return x + t_list(y)

	def Index(self, x, y):
		index = int(t_number(y))
		return x[index]

	def Eq(self, x, y): return x is y
	def Ne(self, x, y): return not (x is y)

	def property_length(self, rt, x): return len(x)

class MarkupMethods(GenericMethods):
	def Add(self, x, y): return x + t_markup(y)

	def Markup(self, x): return x.markup

method_table = {
	float: NumberMethods(),
	int: NumberMethods(),
	long: NumberMethods(),
	bool: BooleanMethods(),
	unicode: StringMethods(),
	tuple: ListMethods(),
	list: ListMethods(),
	Markup: MarkupMethods(),
}

class ScriptRuntime(object):
	def __init__(self):
		self.globals = {}

	def SetGlobal(self, k, v): self.globals[k] = v
	def GetGlobal(self, k): return self.globals[k]

	def CheckBoolean(self, x): return t_boolean(x)

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
		m = [self.Markup(x) for x in elements]
		return Markup(*m)

	# Any other method call gets routed through the lookup tables above.

	attrcache = {}
	def __getattr__(self, name):
		if (name in self.attrcache):
			return self.attrcache[name]

		def attr(x, *y):
			tx = type(x)
			mt = method_table[tx]
			try:
				return getattr(mt, name)(x, *y)
			except KeyError:
				raise ScriptError("type %s does not support %s", tx, name)

		self.attrcache[name] = attr
		return attr

