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
from ts.Markup import Markup
import dis
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def run_test(test):
	(script, desiredresult) = test
	print "-----"
	print script
	module = scriptcompiler.compile(script)
	rt = ScriptRuntime()
	result = module["var_test"](rt)
	print "result: ", result
	if (result != desiredresult):
		print "TEST FAILED: should be ", desiredresult
		exit(1)
	else:
		print "PASSED"

scripts = [
	(u'''
		sub test
			return true
		endsub
	''',
	True),

	(u'''
		sub test
			return false
		endsub
	''',
	False),

	(u'''
		sub test
			return 1+1
		endsub
	''',
	2),

	(u'''
		sub test
			x = 1: y = 1
			return x+y
		endsub
	''',
	2),

	(u'''
		sub test
			return 1+2*3
		endsub
	''',
	7),

	(u'''
		sub test
			return 1*2+3
		endsub
	''',
	5),

	(u'''
		sub test
			return 1/2
		endsub
	''',
	0.5),

	(u'''
		sub test
			return -1
		endsub
	''',
	-1),

	(u'''
		sub test
			x = 1
			return -x
		endsub
	''',
	-1),

	(u'''
		sub test
			return 1+ -2 * 3
		endsub
	''',
	-5),

	(u'''
		sub test
			if true then
				return 1
			else
				return 0
			endif
		endsub
	''',
	1),

	(u'''
		sub test
			if false then
				return 1
			else
				return 0
			endif
		endsub
	''',
	0),

	(u'''
		sub test
			if false then
				return 1
			elseif false then
				return 2
			elseif false then
				return 3
			else
				return 0
			endif
		endsub
	''',
	0),

	(u'''
		sub test
			if true then
				return 1
			endif
			return 0
		endsub
	''',
	1),

	(u'''
		sub test
			if false then
				return 1
			endif
			return 0
		endsub
	''',
	0),

	(u'''
		sub test
			if true then return 1 else return 0
		endsub
	''',
	1),

	(u'''
		sub test
			if false then return 1 else return 0
		endsub
	''',
	0),

	(u'''
		sub test
			if true then return 1
			return 0
		endsub
	''',
	1),

	(u'''
		sub test
			if false then return 1
			return 0
		endsub
	''',
	0),

	(u'''
		sub test
			if false then if false then if false then return 1 else return 2
			return 0
		endsub
	''',
	0),

	(u'''
		sub test
			if true then if true then if true then return 1 else return 2
			return 0
		endsub
	''',
	1),

	(u'''
		sub test
			$x = 1: return $x
		endsub
	''',
	1),

	(u'''
		sub test
			$x = 1: y = 2
			$x = $x + y
			return $x
		endsub
	''',
	3),

	(u'''
		sub test
			return not true
		endsub
	''',
	False),

	(u'''
		sub test
			x = 1: y = 2
			return not (x = y)
		endsub
	''',
	True),

	(u'''
		sub test
			y = 0
			for x = 1 to 10
				 y = y + x
			next
			return y
		endsub
	''',
	55),

	(u'''
		sub test
			y = 0
			for x = 10 to 1
				 y = y + x
			next
			return y
		endsub
	''',
	10),

	(u'''
		sub test
			y = 0
			for x = 1 to 10 step -1
				 y = y + x
			next
			return y
		endsub
	''',
	1),

	(u'''
		sub test
			y = 0
			for x = 10 to 1 step -1
				 y = y + x
			next
			return y
		endsub
	''',
	55),

	(u'''
		sub test
			y = 0
			for x = 1 to 10: y = y + x: next
			return y
		endsub
	''',
	55),

	(u'''
		sub test
			y = 0: x = 0
			while (x < 10)
				y = y + x
				x = x + 1
			endwhile
			return y
		endsub
	''',
	45),

	(u'''
		sub test
			y = 0: x = 0
			while (x < 10): y=y+x: x=x+1: endwhile
			return y
		endsub
	''',
	45),

	(u'''
		sub test
			x=1: y=2: return x < y
		endsub
	''',
	True),

	(u'''
		sub test
			x=1: y=2: return x <= y
		endsub
	''',
	True),

	(u'''
		sub test
			x=1: y=2: return x > y
		endsub
	''',
	False),

	(u'''
		sub test
			x=1: y=2: return x >= y
		endsub
	''',
	False),

	(u'''
		sub test
			x=1: y=2: return x == y
		endsub
	''',
	False),

	(u'''
		sub test
			x=1: y=2: return x = y
		endsub
	''',
	False),

	(u'''
		sub test
			x=1: y=2: return x != y
		endsub
	''',
	True),

	(u'''
		sub test
			x=1: y=2: return x <> y
		endsub
	''',
	True),

	(u'''
		sub test
			x=1: y=2: return x<y and y==2
		endsub
	''',
	True),

	(u'''
		sub test
			x=1: y=2: return x>y or y==2
		endsub
	''',
	True),

	(u'''
		sub test
			return true and true or false
		endsub
	''',
	True),

	(u'''
		sub test
			return true or true and false
		endsub
	''',
	True),

	(u'''
		sub zero
		endsub

		sub zerop()
		endsub

		sub one(p1)
			return p1
		endsub

		sub two(p1, p2)
			return p1+p2
		endsub

		sub test
			zero(): zerop()
			return one(1) + two(1, 2)
		endsub
	''',
	4),

	(u'''
		sub test
			x = 1
			return [1, x+x, x+x+x*x, 4]
		endsub
	''',
	(1.0, 2.0, 3.0, 4.0)),

	(u'''
		sub test
			for x=1 to 10
				break
			next
			return x
		endsub
	''',
	1),

	(u'''
		sub test
			for x=1 to 10
				continue
				break
			next
			return x
		endsub
	''',
	10),

	(ur'''
		sub test
			return 'Fnö\'rd'
		endsub
	''',
	u"Fnö\'rd"),

	(ur'''
		sub test
			return '123' + '456'
		endsub
	''',
	u"123456"),

	(ur'''
		sub test
			return ['1', '2', '3'][1]
		endsub
	''',
	u"2"),

	(ur'''
		sub test
			return [1, 2] + [3, 4]
		endsub
	''',
	(1.0, 2.0, 3.0, 4.0)),

	(ur'''
		sub test
			x = 1
			return "foo" + "foo{x}bar" + "foo{x}bar{x}baz"
		endsub
	''',
	Markup('foo', 'foo', '1', 'bar', 'foo', '1', 'bar', '1', 'baz')),

	(ur'''
		sub test
			x = 'cow'
			return "How now, brown {x}"
		endsub
	''',
	Markup('How now, brown ', 'cow')),

	(ur'''
		sub test
			x = 'cow'
			x = "{x}"
			return "How now, brown {x}"
		endsub
	''',
	Markup('How now, brown ', Markup('cow'))),

	(ur'''
		sub test
			a = 1.6
			return [a.toInt(), 2, 3, 4].length()
		endsub
	''',
	4),

	(ur'''
		sub test
			a = [1, 2, 3, 4]
			a.length()
			[1, 2].length()
			4
			return 0
		endsub
	''',
	0),

#	(u'''
#		return 1 < false
#	''',
#	True),
]

for test in scripts:
	run_test(test)

