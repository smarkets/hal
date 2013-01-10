# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

class Listener(object):
	def __init__(self, bot):
		self.bot = bot

	def match(self, message):
		raise NotImplementedError

	def __call__(self, message):
		result = None

		match = self.match(message)

		if match:
			result = self.handle(message, match)

		return result

	def handle(self, message, match):
		pass

class TextListener(Listener):
	regexp = None

	def match(self, message):
		if hasattr(self.regexp, 'match'):
			pattern, flags = self.regexp.pattern, self.regexp.flags
		else:
			pattern, flags = self.regexp, 0

		new_regexp = re.compile(pattern, flags)
		return new_regexp.match(message)
