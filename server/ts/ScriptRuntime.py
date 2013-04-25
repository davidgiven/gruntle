# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

from numbers import *

from ts.exceptions import *

def both_numeric(x, y):
	return isinstance(x, Number) and isinstance(y, Number)

def type_mismatch():
	raise ScriptError("type mismatch")

class ScriptRuntime:
	def __init__(self):
		self.globals = {}

	def SetGlobal(self, k, v): self.globals[k] = v
	def GetGlobal(self, k): return self.globals[k]

	def Neg(self, x): return -x

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
