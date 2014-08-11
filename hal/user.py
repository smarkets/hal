# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class User(object):

    def __init__(self, name, room=None):
        self.name = name
        self.room = room
