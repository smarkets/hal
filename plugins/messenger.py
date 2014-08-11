import socket
import sys
from os import environ
from threading import Thread

import simplejson as json
from flask import Request
from injector import inject

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
    @bot.web.route('/talk', methods=['POST'])
    @inject(request=Request)
    def talk(request):
        room = request.form['room']
        name = request.form.get('user') or None
        if name:
            user = User(name=name, room=room)
        else:
            user = None

        message = request.form['message']
        forward(room, message, user)
        return 'ok'

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
                    message = json.loads(encoded_message)
                    room = message['room']
                    message_text = message['message']
                except Exception:
                    pass
                else:
                    forward(room, message_text, None)

        thread = Thread(target=exit_after_finished(fun=loop))
        thread.daemon = True
        thread.start()
