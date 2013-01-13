# HAL

Our Jabber chat bot. It's modelled after GitHub's [Hubot](http://hubot.github.com) but written in Python instead of CoffeeScript.

## Requirements

* unix-compatible operating system
* make
* Python 2.x >= 2.7
 * virtualenv

## Running

1. Clone the repository:

		git clone git://github.com/smarkets/hal.git

1. Build the virtualenv (in projects directory):

		make virtualenv
	
1. Run HAL

		./env/bin/python main.py [--name HAL] [--adapter shell]
	
As you can see, there are 2 command line parameters (both optional):

* ``name`` - the name under which bot appears in chatrooms
* ``adapter`` - chat adapter to use

### Adapters

Adapter takes care of bot's communication with event source and destination (in general - some chat room).

#### Shell

Allows use of HAL using operating system terminal. You simply run HAL and are presented with application's command prompt. To use some adapter you may need to specify additional environment variables.

#### Jabber

Provides bot support for Jabber/XMPP chat rooms.

Required environment variables:

* ``HAL_JABBER_JID`` - jabber id
* ``HAL_JABBER_PASSWORD`` - password
* ``HAL_JABBER_ROOMS`` - comma separated list of rooms (currently no password-protected rooms supported)

Optional environment variables:

* ``HAL_JABBER_CONFERENCE_SERVER`` - please specify if conference server is different than ``conference.JABBERIDSERVER``
