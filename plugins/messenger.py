import socket
import sys
from os import environ
from threading import Thread

import simplejson as json

from hal.outgoing_content import OutgoingContent
from hal.response import Envelope
from hal.user import User


def exit_after_finished(fun, exit_code_fun=lambda error: 1 if error else 0):
    def wrapper(*args, **kwargs):
        try:
            fun(*args, **kwargs)
            error = None
        except Exception as e:
            error = e
        finally:
            exit_code = exit_code_fun(error)
            sys.exit(exit_code)
    return wrapper


def plugin(bot):

    def decode(encoded_message):
        """
        :return: room, user and content
        """
        message = json.loads(encoded_message)
        room = message['room']
        try:
            user_name = message['user']
        except KeyError:
            user = None
        else:
            user = User(name=user_name, room=room)

        raw_content = message.get('raw_message') or message.get('message')
        html_content = message.get('html_message')
        content = OutgoingContent.guess_from_maybe_raw_and_html(raw_content, html_content)
        return room, user, content

    def forward(room, message, user):
        envelope = Envelope(user=user, room=room)

        if user:
            method = bot.reply
        else:
            method = bot.send

        method(envelope, message)

    try:
        address = environ['HAL_MESSENGER_UDP_ADDRESS']
    except KeyError:
        pass
    else:
        address = address.split(':')
        address = (address[0], int(address[1]))
        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receive_socket.bind(address)

        def loop():
            while True:
                encoded_message, address = receive_socket.recvfrom(60000)
                try:
                    room, user, content = decode(encoded_message)
                except Exception:
                    pass
                else:
                    forward(room, content, user)

        thread = Thread(target=exit_after_finished(fun=loop))
        thread.daemon = True
        thread.start()
