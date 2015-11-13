"""
This plugin requires the following environment variable to be set:

* YOUTUBE_API_KEY - YouTube V3 API application key
"""

import os
import random

import requests


__commands__ = '''
    hal (youtube|yt) [me] <query> - shows link to random top video matching query on YouTube
'''


def plugin(bot):
    @bot.respond(r'(youtube|yt)( me)? (.+)')
    def youtube(response):
        query = response.match.group(3)
        try:
            api_key = os.environ['YOUTUBE_API_KEY']
        except KeyError:
            response.send('YOUTUBE_API_KEY not provided')
            return

        result = requests.get(
            'https://www.googleapis.com/youtube/v3/search',
            params={
                'order': 'relevance',
                'q': query,
                'part': 'id',
                'key': api_key,
            },
        )
        if result.status_code != 200:
            response.send('Query failed with HTTP %s' % (result.status_code,))
            return

        video_urls = get_urls_from_youtube_response(result.json())

        if video_urls:
            response.send(random.choice(video_urls))
        else:
            response.send('Sorry, %s not found you YouTube' % (query,))


def get_urls_from_youtube_response(response):
    items = response['items']
    item_ids = [i['id'] for i in items]
    video_item_ids = [i for i in item_ids if i['kind'] == 'youtube#video']
    video_ids = [i['videoId'] for i in video_item_ids]
    return ['https://youtube.com/watch?v=%s' % vid for vid in video_ids]
