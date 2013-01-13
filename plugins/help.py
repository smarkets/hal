__commands__ = '''
	hal help - displays help for all available commands
	hal help <pattern> - displays help for all commands matching pattern
'''

import re

def plugin(bot):
	@bot.respond('help\s*(.+)?$')
	def help(response):
		commands = bot.commands_help

		regexp = response.match.group(1)
		if regexp:
			commands = [c for c in commands if regexp.match(c)]

		commands_text = '\n'.join(commands)
		commands_text = re.sub(r'\bhal\b', bot.name, commands_text,
			flags = re.IGNORECASE)
		response.send(commands_text)
