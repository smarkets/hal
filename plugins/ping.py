__commands__ = '''
    [hal] ping - responds to pings
'''


def plugin(bot):
    bot.hear('ping$', 'pong')
    bot.respond('ping$', lambda response: response.reply('pong'))
    bot.respond('hi|hello$',
                lambda response: 'Oh hello there %s!' % (response.envelope.user.name))

    @bot.web.route('/ping')
    def ping():
        return 'pong'
