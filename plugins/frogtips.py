import requests


__commands__ = '''
    hal (frog) [me] - shows a random frog tip
'''


def plugin(bot):
    def get_tips():
        result = requests.get('http://frog.tips/api/1/tips/')

        if result.status_code != 200:
            result.raise_for_status()

        return result.json()['tips']

    tips = []

    def get_tip():
        if len(tips) == 0:
            tips.extend(get_tips())

        return tips.pop()

    @bot.respond(r'frog(?: me)?')
    def frogs(response):
        try:
            tip = get_tip()
            response.send('TIP #%d: %s' % (tip['number'], tip['tip'],))
        except requests.exceptions.RequestException as e:
            response.send('ERROR: %s' % (e,))
