# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from injector import Module

from hal.configuration import ConfigurationModule
from hal.jabber import JabberConfigurationModule
from hal.plugin import PluginModule

class ApplicationModule(Module):
	def configure(self, binder):
		for module in (ConfigurationModule, JabberConfigurationModule, PluginModule):
			binder.install(module())
