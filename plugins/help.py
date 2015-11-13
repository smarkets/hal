import re

__commands__ = '''
    hal help - displays help for all available commands
    hal help <pattern> - displays help for all commands matching pattern
'''


def plugin(bot):
    @bot.respond('help\s*(.+)?$')
    def help(response):
        commands = bot.commands_help

        regexp = response.match.group(1)
        if regexp:
            regexp = re.compile(regexp)
            commands = [c for c in commands if regexp.search(c)]

        commands_text = '\n'.join(commands)
        commands_text = re.sub(r'\bhal\b', bot.name, commands_text,
                               flags=re.IGNORECASE)
        response.send(commands_text)
