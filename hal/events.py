# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class Event(object):

    def __init__(self, user):
        self.user = user

    @property
    def room(self):
        return self.user.room


class TextEvent(Event):

    def __init__(self, user, text):
        super(TextEvent, self).__init__(user)
        self.text = text

    def __repr__(self):
        return ('%s(user=%r, text=%r)' % (self.__class__.__name__, self.user, self.text)).encode('utf-8')
