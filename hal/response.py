# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

class Response(object):
	def __init__(self, bot, message, match):
		self.bot = bot
		self.message = message
		self.match = match
