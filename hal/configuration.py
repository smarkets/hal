# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from ConfigParser import ConfigParser
from os import environ
from os.path import abspath, dirname, join

from injector import Module, provides, singleton

from hal.interfaces import Configuration

class ConfigurationModule(Module):
	@singleton
	@provides(Configuration)
	def provide_configuration(self):
		root = abspath(join(dirname(__file__), '..'))
		directories = [
			join(root, 'etc'),
			'/etc',
		]

		additional = environ.get('HAL_CONFIGURATION_DIRECTORY')
		if additional:
			directories.append(additional)

		config = ConfigParser()
		config.read([join(directory, 'hal.cfg') for directory in directories])
		return config
