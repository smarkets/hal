from __future__ import absolute_import, division, print_function, unicode_literals

import cgi


class OutgoingContent(object):

    def __init__(self, raw, html):
        """
        :type raw: unicode string
        :type html: unicode string
        """
        self.raw = raw
        self.html = html

    def prepended(self, prefix):
        return type(self)(prefix + self.raw, prefix + self.html)

    @classmethod
    def create_from_raw(cls, raw):
        """
        :type raw: unicode string
        """
        escaped = cgi.escape(raw)
        return cls(raw, escaped)

    @classmethod
    def create_from_html(cls, html):
        """
        :type raw: unicode string
        :type html: unicode string
        """
        return cls(html, html)

    @classmethod
    def create_from_raw_and_html(cls, raw, html):
        """
        :type raw: unicode string
        :type html: unicode string
        """
        return cls(raw, html)
