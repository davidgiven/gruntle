# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.exceptions import *

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

def type_mismatch():
	raise ScriptError("type mismatch")

# This is a load of foul hackery. We have to fake our own methods on system
# types (int, float, bool, unicode, etc.) The following 'classes' are
# bundles of methods for each type. When a run-time operation is performed
# on a value, the type of the left parameter is looked up and the appropriate
# 'class' found.

class NumberMethods:
	def Add(x, y): return x + t_number(y)
	def Sub(x, y): return x - t_number(y)
	def Mult(x, y): return x * t_number(y)
	def Div(x, y): return x / t_number(y)
	def Mod(x, y): return x % t_number(y)

	def Neg(x, y): return -x

	def Eq(x, y): return x == y
	def NotEq(x, y): return x != y
	def Lt(x, y): return x < t_number(y)
	def LtE(x, y): return x <= t_number(y)
	def Gt(x, y): return x > t_number(y)
	def GtE(x, y): return x >= t_number(y)

class BooleanMethods:
	def Not(x, y): return not x

	def Eq(x, y): return x == y
	def Ne(x, y): return x != y

class StringMethods:
	def Add(x, y): return x + t_string(y)

	def Eq(x, y): return x == y
	def Ne(x, y): return x != y
	def Lt(x, y): return x < t_string(y)
	def LtE(x, y): return x <= t_string(y)
	def Gt(x, y): return x > t_string(y)
	def GtE(x, y): return x >= t_string(y)

method_table = {
	float: NumberMethods,
	int: NumberMethods,
	long: NumberMethods,
	bool: BooleanMethods,
	unicode: StringMethods
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

	# Any other method call gets routed through the lookup tables above.

	attrcache = {}
	def __getattr__(self, name):
		if (name in self.attrcache):
			return self.attrcache[name]

		def attr(x, y=None):
			tx = type(x)
			ty = type(y)
			mt = method_table[tx]
			try:
				return mt.__dict__[name](x, y)
			except KeyError:
				raise ScriptError("type %s does not support %s", tx, name)

		self.attrcache[name] = attr
		return attr

