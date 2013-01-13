# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

class Message(object):
	def __init__(self, user):
		self.user = user
		self.room = user.room

class TextMessage(Message):
	def __init__(self, user, text):
		super(TextMessage, self).__init__(user)
		self.text = text

class EnterMessage(Message): pass

class LeaveMessage(Message): pass
