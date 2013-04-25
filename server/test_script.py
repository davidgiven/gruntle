# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import ts.scriptcompiler as scriptcompiler
from ts.ScriptRuntime import ScriptRuntime
import dis

def run_test(test):
	(script, desiredresult) = test
	func = scriptcompiler.compile_action(script)
	rt = ScriptRuntime()
	result = func(rt)
	if (result != desiredresult):
		print "TEST FAILED: ", result, " != ", desiredresult
		exit(1)

scripts = [
	('''
		return true
	''',
	True),

	('''
		return false
	''',
	False),

	('''
		return 1+1
	''',
	2),

	('''
		x = 1: y = 1
		return x+y
	''',
	2),

	('''
		return 1+2*3
	''',
	7),

	('''
		return 1*2+3
	''',
	5),

	('''
		return 1/2
	''',
	0.5),

	('''
		if true then
			return 1
		else
			return 0
		endif
	''',
	1),

	('''
		if false then
			return 1
		else
			return 0
		endif
	''',
	0),

	('''
		if false then
			return 1
		elseif false then
			return 2
		elseif false then
			return 3
		else
			return 0
		endif
	''',
	0),

	('''
		if true then
			return 1
		endif
		return 0
	''',
	1),

	('''
		if false then
			return 1
		endif
		return 0
	''',
	0),

	('''
		if true then return 1 else return 0
	''',
	1),

	('''
		if false then return 1 else return 0
	''',
	0),

	('''
		if true then return 1
		return 0
	''',
	1),

	('''
		if false then return 1
		return 0
	''',
	0),

	('''
		if false then if false then if false then return 1 else return 2
		return 0
	''',
	0),

	('''
		if true then if true then if true then return 1 else return 2
		return 0
	''',
	1),

	('''
		$x = 1: return $x
	''',
	1),

	('''
		$x = 1: y = 2
		$x = $x + y
		return $x
	''',
	3),

	('''
		y = 0
		for x = 1 to 10
		     y = y + x
		next
		return y
	''',
	55),

	('''
		y = 0
		for x = 10 to 1
		     y = y + x
		next
		return y
	''',
	10),

	('''
		y = 0
		for x = 1 to 10 step -1
		     y = y + x
		next
		return y
	''',
	1),

	('''
		y = 0
		for x = 10 to 1 step -1
		     y = y + x
		next
		return y
	''',
	55),
]

for test in scripts:
	run_test(test)

