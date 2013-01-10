# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from hal.response import Response

class Listener(object):
	def __init__(self, bot, callback):
		self.bot = bot

		if hasattr(callback, '__call__'):
			self.callback = callback
		else:
			self.callback = lambda response: callback

	def match(self, message):
		raise NotImplementedError

	def __call__(self, message):
		result = None

		match = self.match(message)

		if match:
			result = self.handle(Response(self.bot, message, match))

		return result

	def handle(self, response):
		return self.callback(response)

class TextListener(Listener):
	def __init__(self, bot, regexp, callback):
		super(TextListener, self).__init__(bot, callback)
		if not hasattr(regexp, 'match'):
			regexp = re.compile(regexp, re.IGNORECASE)
		self.regexp = regexp

	def match(self, message):
		return self.regexp.match(message)
