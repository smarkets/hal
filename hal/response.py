# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class Envelope(object):

    def __init__(self, user, room):
        self.user = user
        self.room = room


class Response(object):

    def __init__(self, bot, message, match):
        self.bot = bot
        self.message = message
        self.match = match

        self.envelope = Envelope(message.user, message.room)

    def send(self, *messages):
        self.bot.send(self.envelope, *messages)

    def reply(self, *messages):
        self.bot.reply(self.envelope, *messages)
