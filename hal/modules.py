# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from injector import Module

from hal.plugin import PluginModule


class ApplicationModule(Module):

    def configure(self, binder):
        for module in (PluginModule,):
            binder.install(module())
