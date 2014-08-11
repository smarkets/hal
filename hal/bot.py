# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from os import environ
from threading import RLock, Thread
from time import sleep
from traceback import format_exc

from flask import Blueprint, Flask
from flask_injector import FlaskModule, InjectorView
from injector import inject, Injector

from hal.listeners import TextListener
from hal.outgoing_content import OutgoingContent
from hal.plugin import PluginModuleCollector
from hal.response import Envelope


class Bot(object):

    def __init__(self, name):
        self.name = name
        self.web = Blueprint(__name__, __name__)
        self.lock = RLock()

    def run(self):
        threads = self._start_threads()
        self._reload_plugins()
        self._block_until_any_thread_dies(threads)

    def _start_threads(self):
        tasks = dict(adapter=self.adapter.run, web=self._web_task)
        threads = dict((key, Thread(target=value)) for (key, value) in tasks.items())
        return threads

    def _block_until_any_thread_dies(self, threads):
        for t in threads.values():
            t.daemon = True
            t.start()

        def all_alive():
            return all(t.is_alive() for t in threads.values())

        try:
            while all_alive():
                sleep(0.1)
        except KeyboardInterrupt:
            print('Exiting')

    @inject(injector=Injector)
    def _web_task(self, injector):
        app = Flask(__name__)
        app.register_blueprint(self.web)

        injector.binder.install(FlaskModule(app, [], []))

        for endpoint, view in app.view_functions.iteritems():
            injector_aware_view = InjectorView.as_view(endpoint,
                                                       handler=view, injector=injector)
            app.view_functions[endpoint] = injector_aware_view

        app.run(host=environ.get('HAL_HTTP_HOST') or '127.0.0.1',
                port=int(environ.get('HAL_HTTP_PORT') or 8888))

    @inject(plugin_module_collector=PluginModuleCollector)
    def _reload_plugins(self, plugin_module_collector):
        self._listeners = []
        self._commands_help = []
        modules = plugin_module_collector.collect()
        for m in modules:
            m.plugin(self)
            try:
                commands = [c.strip() for c in m.__commands__.splitlines() if c.strip()]
                self._commands_help.extend(commands)
            except AttributeError:
                pass

        self._commands_help.sort()

    def hear(self, regexp, callback=None):
        if callback is None:
            def decorator(function):
                self.hear(regexp, function)
                return function
            return decorator
        else:
            self._listeners.append(TextListener(self, self._regexp_object(regexp), callback))

    def respond(self, regexp, callback=None):
        if callback is None:
            def decorator(function):
                self.respond(regexp, function)
                return function
            return decorator
        else:
            pattern, flags = self._regexp_pattern_and_flags(regexp)
            assert not pattern.startswith('^')

            new_regexp = re.compile(r'^%s[:,]?\s*(?:%s)' % (self.name, pattern,), flags)
            self._listeners.append(TextListener(self, new_regexp, callback))

    def _regexp_object(self, regexp):
        if not hasattr(regexp, 'match'):
            regexp = re.compile(regexp, re.IGNORECASE)

        return regexp

    def _regexp_pattern_and_flags(self, regexp):
        if hasattr(regexp, 'match'):
            pattern, flags = regexp.pattern, regexp.flags
        else:
            pattern, flags = regexp, re.IGNORECASE

        return pattern, flags

    def receive(self, message):
        for listener in self._listeners:
            self._try_message_on_listener(message, listener)

    def _try_message_on_listener(self, message, listener):
        try:
            listener(message)
        except Exception:
            tb = format_exc()
            response = 'Error processing %r:\n\n' % (message,) + tb
            self.send(Envelope(message.user, message.room), response)

    def send(self, envelope, content):
        """
        :type content: :class:`hal.outgoing_content.OutgoingContent` or unicode string
        """
        content = self._wrap_content_if_needed(content)
        with self.lock:
            self.adapter.send(envelope, content)

    def reply(self, envelope, content):
        """
        :type content: :class:`hal.outgoing_content.OutgoingContent` or unicode string
        """
        content = self._wrap_content_if_needed(content)
        with self.lock:
            self.adapter.reply(envelope, content)

    def _wrap_content_if_needed(self, content):
        if not isinstance(content, OutgoingContent):
            content = OutgoingContent.create_from_raw(content)
        return content

    @property
    def commands_help(self):
        return self._commands_help
