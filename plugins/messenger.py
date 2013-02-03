from hal.response import Envelope

def plugin(bot):
	@bot.web.route('/echo')
	def echo():
		envelope = Envelope(user = None, room = 'staff')
		bot.send(envelope, 'echo!')
		return 'ok'
