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

There's also a builtin HTTP server which can be used by plugins to offer some functions, it's configuration consists of the following variables:

* ``HAL_HTTP_HOST`` - what address to bind listening socket to (``0.0.0.0`` listens on all interfaces, ``127.0.0.1`` allows access only from local machine), default: ``127.0.0.1``
* ``HAL_HTTP_PORT`` - port to listen on, default: ``8888``

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

* ``HAL_JABBER_CONFERENCE_SERVER`` - Specify if conference server is different than ``conference.JABBERIDSERVER``
* ``HAL_PLUGIN_DIRECTORIES`` - Directory to load other plugins from 
