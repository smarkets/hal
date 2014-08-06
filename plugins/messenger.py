import socket
from os import environ
from threading import Thread

import simplejson as json
from injector import inject
from flask import Request

from hal.response import Envelope
from hal.user import User


def plugin(bot):
    @bot.web.route('/talk', methods=['POST'])
    @inject(request=Request)
    def talk(request):
        room = request.form['room']
        name = request.form.get('user') or None
        if name:
            user = User(id=name, name=name, room=room)
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

        thread = Thread(target=loop)
        thread.daemon = True
        thread.start()
