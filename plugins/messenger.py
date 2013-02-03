from injector import inject
from flask import Request

from hal.response import Envelope
from hal.user import User

def plugin(bot):
	@bot.web.route('/talk', methods = ['POST'])
	@inject(request = Request)
	def talk(request):
		room = request.form['room']
		name = request.form.get('user') or None
		if name:
			user = User(id = name, name = name, room = room)
		else:
			user = None

		message = request.form['message']
		envelope = Envelope(user = user, room = room)

		if user:
			method = bot.reply
		else:
			method = bot.send

		method(envelope, message)
		return 'ok'
