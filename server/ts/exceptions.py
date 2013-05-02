# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

class ServerUserError(RuntimeError):
	def __eq__(self, other):
		print type(other), self.__class__
		return (type(other) == self.__class__) and (self.args == other.args)

	def __ne__(self, other):
		return not self.__eq__(other)

class InvalidObjectReference(ServerUserError):
	def __init__(self, arg=None):
		self.args = (arg,)
		
class PermissionDenied(ServerUserError):
	def __init__(self, arg=None):
		self.args = (arg,)
		
class AppError(ServerUserError):
	def __init__(self, message, *args):
		self.args = (message % args,)

class ScriptError(AppError):
	def __init__(self, message, *args):
		self.args = (message % args,)

class ScriptCompilationError(AppError):
	def __init__(self, message, *args):
		self.args = (message % args,)

