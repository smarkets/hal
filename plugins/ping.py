def plugin(bot):
	bot.hear('ping$', 'pong')
	bot.respond('ping$', lambda response: response.reply('pong'))
	bot.hear(r'project .* failure', ':(')
	bot.hear(r'Yippie, build fixed!', ':)')
	bot.respond('hi|hello$',
		lambda response: 'Oh hello there %s!' % (response.user.name))
