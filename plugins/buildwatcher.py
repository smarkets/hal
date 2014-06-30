def plugin(bot):
    bot.hear(r'project .* build .* (failure|failed)', ':(')
    bot.hear(r'Yippie, build fixed!', ':)')
