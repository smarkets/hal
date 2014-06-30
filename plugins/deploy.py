__commands__ = '''
    deploy - listens to 'deploy' on a friday
'''

import datetime

DEPLOY_LINK = 'https://pbs.twimg.com/media/BkHwlGBIgAEsSP7.jpg'


def plugin(bot):
    @bot.hear('deploy$')
    def deploy(response):
        today = datetime.datetime.today().weekday()
        if today == 4:  # Friday
            return DEPLOY_LINK
