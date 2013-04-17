# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

class ServerUserError(RuntimeError):
	pass
	
class InvalidObjectReference(ServerUserError):
	def __init__(self, arg=None):
		self.args = (arg,)
		
class PermissionDenied(ServerUserError):
	def __init__(self, arg=None):
		self.args = (arg,)
		
class AppError(ServerUserError):
	def __init__(self, message, *args):
		self.args = (message % args,)
		