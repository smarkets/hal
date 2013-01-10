# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from imp import load_source
from os import environ, listdir
from os.path import isfile, join

from injector import inject, Key, Module, provides, singleton

from hal import PROJECT_ROOT

PluginDirectories = Key('PluginDirectories')
Plugins = Key('Plugins')

class PluginCollector(object):
	@inject(directories = PluginDirectories)
	def collect(self, directories):
		plugins = []
		for directory in directories:
			for name in listdir(directory):
				full_name = join(directory, name)
				if full_name.endswith('.py') and isfile(full_name):
					module = load_source('irrelevant', full_name)
					if hasattr(module, 'plugin'):
						plugins.append(module.plugin)

		return plugins

class PluginModule(Module):
	@singleton
	@provides(PluginDirectories)
	def provide_plugin_directories(self):
		directories = [
			join(PROJECT_ROOT, 'plugins'),
		]

		additional = environ.get('HAL_PLUGIN_DIRECTORIES')
		if additional:
			directories.extend(additional.split(','))

		return directories
