__commands__ = '''
    ?wv [name] - congratulates people on their public sprited gesture
'''


def plugin(bot):
    bot.hear(r'^\?wv$', "Well volunteered!")
    bot.hear(r'^\?wv\s(.+)$', lambda response: "Well volunteered %s!" % response.match.group(1).strip())
