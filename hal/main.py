from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

from argparse import ArgumentParser
from imp import load_source
from os.path import join

from injector import AssistedBuilder, Injector

from hal import PROJECT_ROOT
from hal.bot import Bot
from hal.modules import ApplicationModule


def main():
    root_logger = logging.getLogger()
    root_logger.addHandler(logging.StreamHandler())
    root_logger.level = logging.DEBUG

    parser = ArgumentParser(description='HAL bot')
    parser.add_argument('--adapter', dest='adapter', default='shell')
    parser.add_argument('--name', dest='name', default='HAL')
    arguments = parser.parse_args()

    injector = Injector([ApplicationModule])
    bot_builder = injector.get(AssistedBuilder(Bot))
    bot = bot_builder.build(name=arguments.name)

    _attach_adapter(bot, arguments.adapter)
    bot.run()


def _attach_adapter(bot, adapter_name):
    directories = _get_adapter_directories()
    candidates = [join(d, '%s.py' % (adapter_name,)) for d in directories]
    existing_files = [f for f in candidates if os.path.isfile(f)]
    if not existing_files:
        raise RuntimeError(
            'No adapter %s found in %s' % (adapter_name, ':'.join(directories)),
        )
    the_best_choice = existing_files[0]
    adapter_module = load_source('adapter', the_best_choice)
    bot.adapter = adapter_module.Adapter(bot)


def _get_adapter_directories():
    return (
        os.environ.get('HAL_ADAPTER_DIRECTORIES', '').split(':') +
        [join(PROJECT_ROOT, 'adapters')]
    )
