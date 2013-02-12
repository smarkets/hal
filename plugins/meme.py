from pprint import pformat
from random import choice

__commands__ = '''
	hal memes - displays all configured memes
'''

memes = {
	'if you know what I mean':
		'http://dc472.4shared.com/img/BNqKbMOh/s7/if_you_know_what_i_mean_mr_bea.jpg',
	'how about no': 'http://sfcitizen.com/blog/wp-content/uploads/2010/04/how-about-no-bear.jpg',
	'deal with it': (
		'http://www.roflcat.com/images/cats/Deal_With_It.jpg',
		'http://www.evilmilk.com/pictures/Deal_With_It91.jpg',
		'http://www.the-online-book.com/wp-content/uploads/2012/06/deal-with-it-cat.jpg',
		'http://www.drinkalot.com/pics/Deal_With_It.jpg',
		'http://cl.jroo.me/z3/n/D/X/d/a.aaa-Deal-with-it-D.jpg',
		'http://static.fjcdn.com/gifs/Deal+with+it_12e775_4191317.gif',
		'http://assets0.ordienetworks.com/images/GifGuide/DealWithIt/tumblr_lh6sayYpIJ1qzaxefo1_400.gif',
		'http://assets0.ordienetworks.com/images/GifGuide/DealWithIt/bettywhitedealwithit.gif',
		'http://assets0.ordienetworks.com/images/GifGuide/DealWithIt/dealwithit.gif',
		'http://assets0.ordienetworks.com/images/GifGuide/DealWithIt/dealwithitcat.gif',
		'http://assets0.ordienetworks.com/images/GifGuide/DealWithIt/norrisdeal.gif',
		'http://assets0.ordienetworks.com/images/GifGuide/DealWithIt/pan-with-it.gif',
		'http://assets0.ordienetworks.com/images/GifGuide/DealWithIt/startrekwithit.gif',
		'http://assets0.ordienetworks.com/images/GifGuide/DealWithIt/Terminator-deal-with-it.gif',
		'http://static.fjcdn.com/gifs/Deal_614cb5_2356571.gif',
	),

}

def plugin(bot):
	def get_meme(name):
		meme = memes[name.strip().lower()]
		if not isinstance(meme, basestring):
			meme = choice(meme)
		return meme

	@bot.hear('(.+)$')
	def show_meme(response):
		name = response.match.group(1)
		try:
			meme = get_meme(name)
			response.send(meme)
		except KeyError:
			pass

	@bot.respond('memes$')
	def show_memes_list(response):
		response.send('Current meme mapping:\n\n' + pformat(memes))
