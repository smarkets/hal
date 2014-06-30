__commands__ = '''
    hal (youtube|yt) [me] <query> - shows link to random top video matching query on YouTube
'''

import random

import requests


def plugin(bot):
    @bot.respond(r'(youtube|yt)( me)? (.+)')
    def youtube(response):
        query = response.match.group(3)
        result = requests.get('http://gdata.youtube.com/feeds/api/videos', params={
            'orderBy': 'relevance',
            'max-results': 10,
            'alt': 'json',
            'q': query,
        })
        videos = result.json()['feed']['entry']
        video = random.choice(videos)
        links = [link['href'] for link in video['link']
                 if link['rel'] == 'alternate' and link['type'] == 'text/html']

        if links:
            response.send(links[0])
        else:
            response.send('Sorry, %s not found you YouTube' % (query,))
