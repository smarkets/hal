# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class Adapter(object):

    def __init__(self, bot):
        self.bot = bot

    def send(self, envelope, content):
        """
        :type content: :class:`hal.outgoing_content.OutgoingContent`
        """

    def reply(self, envelope, content):
        """
        :type content: :class:`hal.outgoing_content.OutgoingContent`
        """
        self.send(envelope, content.prepended('%s: ' % (envelope.user.name,)))

    def run(self):
        '''
        '''

    def receive(self, event):
        self.bot.receive(event)
