__commands__ = '''
    hal (calc|calculate) [me] <expression> - calculates the expression
    hal (calc|calculate|convert) [me] <expression> (to|in) <units> - converts expression to specified units
'''

import execjs
import requests


def plugin(bot):
    @bot.respond('(calc|calculate|convert)( me)? (.+)')
    def calc(response):
        query = response.match.group(3)

        params = dict(hl='en', q=query)
        response = requests.get('https://www.google.com/ig/calculator', params=params)
        mapping = execjs.eval(response.content)
        rhs, error = mapping['rhs'], mapping['error']
        return rhs or error
