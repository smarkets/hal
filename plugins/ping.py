def plugin(bot):
	bot.hear('ping$', 'pong')
	bot.respond('ping$', 'pong')
	bot.hear(r'project .* failure', ':(')
	bot.hear(r'Yippie, build fixed!', ':)')
	bot.respond('hi|hello$', 'Oh hello there!')
