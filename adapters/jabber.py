# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from os import environ
from time import sleep

from xmpp import Client, Iq, JID, Message, NS_MUC, Presence

from hal.adapter import Adapter as HalAdapter
from hal.messages import TextMessage
from hal.user import User

log = logging.getLogger()


class JabberConfiguration(object):

    def __init__(self, jid, password, conference_server, rooms, server=None):
        self.jid = jid
        self.password = password
        self.rooms = rooms

        jid = JID(jid)
        self.user = jid.getNode()
        self.server = server or jid.getDomain()

        self.conference_server = conference_server or 'conference.%s' % (self.server,)


class Adapter(HalAdapter):

    def run(self):
        while True:
            try:
                self._run()
            except Exception as e:
                log.exception('%s, reconnecting...' % (e,))
            sleep(5)

    def _run(self):
        configuration = JabberConfiguration(
            jid=environ['HAL_JABBER_JID'],
            password=environ['HAL_JABBER_PASSWORD'],
            rooms=environ['HAL_JABBER_ROOMS'].split(','),
            conference_server=environ.get('HAL_JABBER_CONFERENCE_SERVER'),
            server=environ.get('HAL_JABBER_SERVER'),
        )
        self.configuration = configuration

        self.connection = connection = self.create_connection(configuration)
        self.connect_to_rooms(connection, configuration)

        for type, handler in (('message', self.handle_message), ('iq', self.handle_iq)):
            connection.RegisterHandler(type, handler)

        connection.sendInitPresence()

        while True:
            connection.Process(1)

            # to keep the connection alive
            connection.send(' ')

    def create_connection(self, configuration):
        jid = JID(configuration.jid)
        user, server, password = jid.getNode(), jid.getDomain(), configuration.password

        connection = Client(server)
        connection_result = connection.connect()
        if not connection_result:
            raise Exception('Unable to connect to %s' % (server,))

        if connection_result != 'tls':
            raise Exception('No TLS support when connecting to %s' % (server,))

        auth_result = connection.auth(user=user, password=password, resource=user)
        if not auth_result:
            raise Exception('Unable to authenticate %s@%s with %s' % (user, server, '*' * len(password)))

        return connection

    def connect_to_rooms(self, connection, configuration):
        for room in configuration.rooms:
            p = Presence(to='%s@%s/%s' % (room, configuration.conference_server,
                                          self.bot.name,))
            p.setTag('x', namespace=NS_MUC).setTagData('password', '')
            p.getTag('x').addChild('history', {'maxchars': '0', 'maxstanzas': '0'})
            connection.send(p)

    def handle_message(self, session, message):
        sender, text = message.getFrom(), message.getBody()
        room, name = sender.getNode(), sender.getResource()

        if text and name != self.bot.name:
            user = User(id=name, name=name, room=room)
            self.receive(TextMessage(user, text))

    def handle_iq(self, session, iq):
        children = iq.getChildren()

        # Respond to pings so server doesn't kick us
        if iq.getType() == 'get' and children and children[0].getName() == 'ping':
            response = Iq(to=iq.getFrom(), frm=iq.getTo(), typ='result')
            response.setId(iq.getId())
            session.send(response)

    def send(self, envelope, text):
        message = Message(to=JID('%s@%s' % (envelope.room, self.configuration.conference_server)),
                          body=text, typ='groupchat')
        self.connection.send(message)
