# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from hal.adapter import Adapter as HalAdapter
from hal.events import TextEvent
from hal.user import User


class Adapter(HalAdapter):

    def send(self, envelope, text):
        print(text)

    def run(self):
        user = User(id=1, name='shell', room='shell')
        done = False
        while not done:
            try:
                line = raw_input('%s >>> ' % (self.bot.name,))
                self.receive(TextEvent(user, line))
            except EOFError:
                done = True
