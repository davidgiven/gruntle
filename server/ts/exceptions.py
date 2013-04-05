# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

class InvalidObjectReference(RuntimeError):
	def __init__(self, arg=None):
		self.arg = arg
		
class PermissionDenied(RuntimeError):
	def __init__(self, arg=None):
		self.arg = arg
		
class AppError(RuntimeError):
	def __init__(self, message, *args):
		self.arg = message % args
		