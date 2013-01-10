# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from injector import inject
import xmpp

from hal.jabber import ConnectionFactory, JabberConfiguration
from hal.listener import TextListener
from hal.plugin import PluginCollector

class Bot(object):
	@inject(connection_factory = ConnectionFactory, configuration = JabberConfiguration)
	def __init__(self, connection_factory, configuration):
		self._connection_factory = connection_factory
		self.name = configuration.user

	def run(self):
		self._reload_plugins()

		connection = self._connection_factory.create()
		connection.RegisterHandler('message', self.handle_message)
		connection.sendInitPresence()

		while True:
			connection.Process(1)

	@inject(plugin_collector = PluginCollector)
	def _reload_plugins(self, plugin_collector):
		self._listeners = []
		plugins = plugin_collector.collect()
		for plugin in plugins:
			plugin(self)

	def hear(self, regexp, callback = None):
		if callback is None:
			def decorator(function):
				self.hear(regexp, function)
				return function
			return decorator
		else:
			self._listeners.append(TextListener(self, self._regexp_object(regexp), callback))

	def respond(self, regexp, callback = None):
		if callback is None:
			def decorator(function):
				self.respond(regexp, function)
				return function
			return decorator
		else:
			pattern, flags = self._regexp_pattern_and_flags(regexp)
			assert not pattern.startswith('^')

			new_regexp = re.compile(r'^%s[:,]?\s*(?:%s)' % (self.name, pattern,), flags)
			self._listeners.append(TextListener(self, new_regexp, callback))

	def _regexp_object(self, regexp):
		if not hasattr(regexp, 'match'):
			regexp = re.compile(regexp, re.IGNORECASE)

		return regexp

	def _regexp_pattern_and_flags(self, regexp):
		if hasattr(regexp, 'match'):
			pattern, flags = regexp.pattern, regexp.flags
		else:
			pattern, flags = regexp, re.IGNORECASE

		return pattern, flags

	def handle_message(self, connection, message):
		text = message.getBody()
		if text:
			sender = message.getFrom()
			sender.setResource('')

			for listener in self._listeners:
				response = listener(text)
				if response:
					connection.send(response)
					connection.send(xmpp.Message(sender, response, typ = 'groupchat'))
