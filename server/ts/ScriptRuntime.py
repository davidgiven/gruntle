# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from ts.exceptions import *

def is_number(x):
	return (type(x) is int) or (type(x) is float) or (type(x) is long)

def both_numeric(x, y):
	return is_number(x) and is_number(y)

def t_boolean(x):
	if (type(x) != bool):
		type_mismatch()
	return x

def type_mismatch():
	raise ScriptError("type mismatch")

class ScriptObject(object):
	def __eq__(self, x): type_mismatch()
	def __ne__(self, x): type_mismatch()
	def __lt__(self, x): type_mismatch()
	def __le__(self, x): type_mismatch()
	def __gt__(self, x): type_mismatch()
	def __ge__(self, x): type_mismatch()
	def __zero__(self, x): type_mismatch()
	def __str__(self): return self.__repr__()
	def __unicode__(self): return unicode(self.__repr__())

class List(ScriptObject):
	def __init__(self, *values):
		self.values = values

	def __eq__(self, x): return self.values == x
	def __ne__(self, x): return self.values != x

	def __repr__(self):
		return "List(" + \
			(", ".join([x.__repr__() for x in self.values])) + \
			")"

class ScriptRuntime(object):
	def __init__(self):
		self.globals = {}

	def SetGlobal(self, k, v): self.globals[k] = v
	def GetGlobal(self, k): return self.globals[k]

	def CheckBoolean(self, x): return t_boolean(x)

	def Neg(self, x): return -x
	def Not(self, x): return not t_boolean(x)

	def Add(self, x, y): return x + y
	def Sub(self, x, y): return x - y
	def Mult(self, x, y): return x * y
	def Div(self, x, y): return x / y
	def Mod(self, x, y): return x % y

	def Lt(self, x, y):
		if both_numeric(x, y):
			return x < y
		type_mismatch()

	def LtE(self, x, y):
		if both_numeric(x, y):
			return x <= y
		type_mismatch()

	def Gt(self, x, y):
		if both_numeric(x, y):
			return x > y
		type_mismatch()

	def GtE(self, x, y):
		if both_numeric(x, y):
			return x >= y
		type_mismatch()

	def Eq(self, x, y):
		return x == y

	def NotEq(self, x, y):
		return x != y

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

	def MakeList(self, *values):
		return List(*values)

