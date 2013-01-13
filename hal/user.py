# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

class User(object):
	def __init__(self, id, name, room, **kwargs):
		self.id = id
		self.name = name
		self.room = room
		self.other = kwargs
