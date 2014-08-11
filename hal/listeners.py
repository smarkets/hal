# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from hal.events import TextEvent
from hal.response import Response


class Listener(object):

    def __init__(self, bot, matcher, callback):
        self.bot = bot
        self.matcher = matcher
        if hasattr(callback, '__call__'):
            self.callback = callback
        else:
            self.callback = lambda *args, **kwargs: callback

    def __call__(self, message):
        match = self.matcher(message)

        if match:
            response = Response(self.bot, message, match)
            result = self.callback(response)
            if result:
                response.send(result)


class TextListener(Listener):

    def __init__(self, bot, regexp, callback):
        def match(message):
            if isinstance(message, TextEvent):
                return regexp.match(message.text)

        super(TextListener, self).__init__(bot, match, callback)
