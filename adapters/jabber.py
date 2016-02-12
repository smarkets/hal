# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from os import environ

from sleekxmpp import ClientXMPP

from hal.adapter import Adapter as HalAdapter
from hal.events import TextEvent
from hal.user import User

log = logging.getLogger()


class JabberConfiguration(object):

    def __init__(self, jid, password, conference_server, rooms, server):
        self.jid = jid
        self.password = password
        self.rooms = rooms
        self.server = server
        self.conference_server = conference_server


class Adapter(HalAdapter):

    def run(self):
        self.configuration = self._gather_configuration()
        self._run(self.configuration)

    def _gather_configuration(self):
        jid = environ['HAL_JABBER_JID']

        _, domain = jid.split('@')

        port = 5222

        try:
            parts = environ['HAL_JABBER_SERVER']
        except KeyError:
            host = domain
        else:
            parts = parts.split(':')
            try:
                host, port = parts
            except ValueError:
                (host,) = parts
            else:
                port = int(port)

        server = (host, int(port))

        return JabberConfiguration(
            jid=jid,
            password=environ['HAL_JABBER_PASSWORD'],
            rooms=environ['HAL_JABBER_ROOMS'].split(','),
            conference_server=environ.get('HAL_JABBER_CONFERENCE_SERVER') or 'conference.%s' % (domain,),
            server=server,
        )

    def _run(self, configuration):
        self.connection = connection = self.setup_connection(configuration)

        connection.process(block=True)

    def setup_connection(self, configuration):
        connection = ClientXMPP(configuration.jid, configuration.password)

        # xep_0045 MUC
        # xep_0199 XMPP Ping
        for plugin in ['xep_0045', 'xep_0199']:
            connection.register_plugin(plugin)

        for type_, handler in (
            ('session_start', self.handle_start),
            ('groupchat_message', self.handle_message),
        ):
            connection.add_event_handler(type_, handler)

        connection_result = connection.connect(configuration.server)
        server = configuration.server

        if not connection_result:
            raise Exception('Unable to connect to %s' % (server,))

        return connection

    def connect_to_rooms(self, connection, configuration):
        for room in configuration.rooms:
            self.connection.plugin['xep_0045'].joinMUC(
                '%s@%s' % (room, configuration.conference_server),
                self.bot.name,
                wait=True,
            )

    def handle_start(self, event):
        self.connection.send_presence()
        self.connect_to_rooms(self.connection, self.configuration)

    def handle_message(self, message):
        text = message['body']
        name = message['mucnick']
        room = message['mucroom']

        if text and name != self.bot.name:
            user = User(name=name, room=room)
            self.receive(TextEvent(user, text))

    def send(self, envelope, content):
        try:
            _, _ = envelope.room.split('@')
        except ValueError:
            message_to = '%s@%s' % (envelope.room, self.configuration.conference_server)
        else:
            message_to = envelope.room

        self.connection.send_message(
            mto=message_to,
            mbody=content.raw,
            mtype='groupchat',
        )
