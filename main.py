# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from injector import Injector

from hal.bot import Bot
from hal.modules import ApplicationModule

if __name__ == '__main__':
	injector = Injector([ApplicationModule])
	bot = injector.get(Bot)
	bot.run()
