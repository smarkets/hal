# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging
import time
from os import environ

from slackclient import SlackClient

from hal.adapter import Adapter as HalAdapter
from hal.events import TextEvent
from hal.user import User

log = logging.getLogger(__name__)


class Adapter(HalAdapter):

    def send(self, envelope, content):
        """ Send a message to the channel specified in envelope with content."""

        self._slack_client.rtm_send_message(envelope.room, content.raw)

    def run(self):
        self._slack_client = SlackClient(environ['HAL_SLACK_TOKEN'])
        self._get_users()
        self._get_channels()

        if self._slack_client.rtm_connect():
            for channel in self._slack_client.server.channels:
                response = json.loads(self._slack_client.api_call("channels.info", channel=channel.id))
                if 'channel' in response and response['channel']['is_member']:
                    log.info("%s is a member of %s", self.bot.name, response['channel']['name'])
            self._run()

    def _run(self):
        """ Internal messaging loop for the slack adapter."""

        while True:
            for message in self._slack_client.rtm_read():
                if 'type' not in message:
                    continue
                message_type = message['type']
                if message_type in ('team_join', 'user_change'):
                    log.info("User change %s %s", message['user']['id'], message['user']['name'])
                    self._users[message['user']['id']] = message['user']['name']

                elif message_type in ('channel_created', 'channel_rename'):
                    log.info("Channel change %s %s", message['channel']['id'], message['channel']['name'])
                    self._channels[message['channel']['id']] = message['channel']['name']

                elif message_type == 'channel_deleted':
                    log.info("Channel deleted %s", message['channel'])
                    del self._channels[message['channel']]

                elif message_type == 'message' and 'user' in message:
                    log.info("Recieved %s from %s in %s",
                             message['text'], message['user'], message['channel'])
                    user = User(name=self._users.get(message['user'], message['user']),
                                room=self._channels.get(message['channel'], message['channel']))
                    self.receive(TextEvent(user, message['text']))

            time.sleep(1)

    def _get_users(self):
        """ Creates a dictionary of user ID to user name in self._users."""

        users = json.loads(self._slack_client.api_call("users.list"))
        self._users = {}
        for user in users['members']:
            self._users[user['id']] = user['name']

    def _get_channels(self):
        """ Creates a dictionary of channel ID to user name in self._channels."""

        channels = json.loads(self._slack_client.api_call("channels.list"))
        self._channels = {}
        for channel in channels['channels']:
            self._channels[channel['id']] = channel['name']
