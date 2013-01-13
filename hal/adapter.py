# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

class Adapter(object):
	def __init__(self, bot):
		self.bot = bot

	def send(self, envelope, text):
		'''
		'''

	def reply(self, envelope, text):
		'''
		'''
		self.send(envelope, '%s: %s' % (envelope.user.name, text))

	def run(self):
		'''
		'''

	def receive(self, message):
		self.bot.receive(message)
