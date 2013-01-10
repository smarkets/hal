# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from injector import inject, Module, provides, singleton
import xmpp

from hal.interfaces import Configuration

class JabberConfiguration(object):
	def __init__(self, jid, password, conference_server, rooms):
		self.jid = jid
		self.password = password
		self.rooms = rooms
		self.conference_server = conference_server

		jid = xmpp.JID(jid)
		self.user = jid.getNode()
		self.server = jid.getDomain()

class JabberConfigurationModule(Module):
	@singleton
	@provides(JabberConfiguration)
	@inject(config = Configuration)
	def provide_configuration(self, config):
		section = dict(config.items('jabber'))
		section['rooms'] = [room.strip() for room in section['rooms'].split(',')]

		return JabberConfiguration(
			jid = section['jid'],
			password = section['password'],
			rooms = section['rooms'],
			conference_server = section['conference_server'])

class ConnectionFactory(object):
	@inject(configuration = JabberConfiguration)
	def create(self, configuration):
		jid = xmpp.JID(configuration.jid)
		user, server, password = jid.getNode(), jid.getDomain(), configuration.password
		connection = xmpp.Client(server)
		connection_result = connection.connect()
		if not connection_result:
			raise Exception('Unable to connect to %s' % (server,))
	
		if connection_result != 'tls':
			raise Exception('No TLS support when connecting to %s' % (server,))

		auth_result = connection.auth(user = user, password = password, resource = user)
		if not auth_result:
			raise Exception('Unable to authenticate %s@%s with %s' % (user, server, '*' * len(password)))

		for room in configuration.rooms:
			p = xmpp.Presence(to = '%s@%s/%s' % (room, configuration.conference_server, user,))
			p.setTag('x', namespace = xmpp.NS_MUC).setTagData('password', '')
			p.getTag('x').addChild('history', {'maxchars': '0', 'maxstanzas': '0'})
			connection.send(p)

		return connection
